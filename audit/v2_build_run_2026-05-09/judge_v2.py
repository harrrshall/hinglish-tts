"""Stage-2 v2.0: deterministic judge with three-ASR consensus, ear-only naturalness.

Reads (read-only):
  audit/signal_vectors_v2_aai.json
  audit/signal_vectors_v2_deepgram.json
  audit/signal_vectors_v2_groq.json

Writes:
  audit/auto_scores_v2.csv (120 rows: 4 models × 30 sentences)

Per-column rules (rubric v2.0):

  intelligibility_v2          : MEDIAN across the 3 backends of
                                 cer_to_intel_rank(cer_unified). v1.0 anchors.
  naturalness_v2              : literal string "ear-only" (lowercase, NOT numeric).
                                 The CEILING_REPORT showed UTMOS/SQUIM_MOS/PESQ
                                 invert direction on Hindi audio; we refuse to
                                 emit a numeric score from those predictors.
  code_switch_v2              : v1.0 mapping. For pure_* categories: equals
                                 intelligibility_v2. For mixed_script /
                                 english_with_NE: rank by gap from the model's
                                 own pure-category mean intel.
  speaker_quality_v2          : SQUIM_PESQ → 1–5 (v1.0 thresholds). −1 rank if
                                 terminal_sample_abs > 0.05 (DC-tail penalty,
                                 v1.0 rule). Marked synthetic-relative-only in
                                 notes; do NOT compare across genuinely
                                 different audio sources (TTS vs human).
  roman_treated_as_english_v2 : Unchanged from v1.0
                                 (wer_en_forced + 0.15 < wer_roman AND
                                  wer_en_forced < 0.30; "" on pure_devanagari).
  silence_or_skip_v2          : TRUE iff 2+/3 backends report silence
                                 (per-backend: silence_mid > 0.5 OR transcript
                                  covering <80% of expected character count).
  end_of_clip_pop_v2          : Unchanged from v1.0
                                 (end_pop_db > 6 AND terminal_sample > 0.005).
  auto_score_confidence_v2    : HIGH if intel rank spread across backends ≤ 1,
                                 MEDIUM if = 2, LOW if ≥ 3.
"""
from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
AUDIT = REPO / "audit"

CSV_HEADER = [
    "model", "id", "category", "text",
    "intelligibility_v2", "naturalness_v2",
    "code_switch_v2", "speaker_quality_v2",
    "roman_treated_as_english_v2", "silence_or_skip_v2", "end_of_clip_pop_v2",
    "auto_score_confidence_v2",
    "notes_v2",
]

PURE_CATS = {"pure_devanagari", "pure_roman"}


def cer_to_intel_rank(cer: float) -> int:
    """v1.0 CER anchors, applied to unified-Devanagari CER."""
    if cer <= 0.05: return 5
    if cer <= 0.15: return 4
    if cer <= 0.30: return 3
    if cer <= 0.50: return 2
    return 1


def speaker_rank(pesq: float, terminal_abs: float) -> int:
    """v1.0 PESQ anchors + DC-tail −1 penalty if terminal_abs > 0.05."""
    if pesq >= 4.0: s = 5
    elif pesq >= 3.5: s = 4
    elif pesq >= 3.0: s = 3
    elif pesq >= 2.5: s = 2
    else: s = 1
    if terminal_abs > 0.05:
        s -= 1
    return max(1, s)


def is_silent_per_backend(entry: dict) -> bool:
    """Per-backend silent/skip check.

    Two triggers (either sufficient):
      1. silence_mid_clip_s > 0.5  (DSP, identical across backends)
      2. unified transcript covers <80% of unified reference character length
         (proxy for ">20% words missing"; computed on the normalized strings
         so script mismatch doesn't false-trigger).
    """
    if float(entry.get("silence_mid_clip_s", 0.0)) > 0.5:
        return True
    ref = (entry.get("ref_unified") or "").strip()
    hyp = (entry.get("transcript_unified") or "").strip()
    if not hyp:
        return True
    if not ref:
        return False
    return len(hyp) < 0.80 * len(ref)


def codeswitch_v2(intel: int, category: str, model_pure_intel_mean: float) -> int:
    """v1.0 code_switch_handling rule.

    For pure rows: equals intelligibility (caller already does this).
    For mixed rows: rank by the gap from model's pure-category baseline.
    """
    if category in PURE_CATS:
        return intel
    gap = model_pure_intel_mean - intel
    if gap <= 0.05: return 5
    if gap <= 0.15: return 4
    if gap <= 0.30: return 3
    if gap <= 0.50: return 2
    return 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-aai", default=str(AUDIT / "signal_vectors_v2_aai.json"))
    ap.add_argument("--in-deepgram", default=str(AUDIT / "signal_vectors_v2_deepgram.json"))
    ap.add_argument("--in-groq", default=str(AUDIT / "signal_vectors_v2_groq.json"))
    ap.add_argument("--out-csv", default=str(AUDIT / "auto_scores_v2.csv"))
    args = ap.parse_args()

    sv_aai  = {(e["model"], e["id"]): e for e in json.loads(Path(args.in_aai).read_text())}
    sv_dg   = {(e["model"], e["id"]): e for e in json.loads(Path(args.in_deepgram).read_text())}
    sv_groq = {(e["model"], e["id"]): e for e in json.loads(Path(args.in_groq).read_text())}

    keys = set(sv_aai)
    if not (keys == set(sv_dg) == set(sv_groq)):
        print("[fatal] backend signal-vector key sets diverge", file=sys.stderr)
        return 1

    # Pass 1: derive per-(model, id) intelligibility (median of 3 backends).
    # We need this for both the rows themselves and for the per-model
    # pure-category mean used by code_switch on mixed/NE rows.
    interim: dict[tuple[str, str], dict] = {}
    for key in keys:
        e_aai, e_dg, e_groq = sv_aai[key], sv_dg[key], sv_groq[key]
        intel_per = [
            cer_to_intel_rank(e_aai["cer_unified"]),
            cer_to_intel_rank(e_dg["cer_unified"]),
            cer_to_intel_rank(e_groq["cer_unified"]),
        ]
        intel_v2 = int(statistics.median(intel_per))
        silent_per = [is_silent_per_backend(e_aai),
                      is_silent_per_backend(e_dg),
                      is_silent_per_backend(e_groq)]
        interim[key] = {
            "e_aai": e_aai, "e_dg": e_dg, "e_groq": e_groq,
            "intel_per": intel_per, "intel_v2": intel_v2,
            "silent_per": silent_per,
        }

    by_model: dict[str, list[int]] = defaultdict(list)
    for (model, sid), v in interim.items():
        if v["e_aai"]["category"] in PURE_CATS:
            by_model[model].append(v["intel_v2"])
    model_pure_means = {m: (statistics.mean(vals) if vals else 3.0)
                        for m, vals in by_model.items()}

    # Pass 2: emit CSV rows.
    model_order = {"kokoro": 0, "indic_parler": 1, "indicf5": 2, "springlab_f5": 3}
    rows = []
    for key in sorted(keys, key=lambda k: (k[1], model_order.get(k[0], 99))):
        v = interim[key]
        e_aai, e_dg, e_groq = v["e_aai"], v["e_dg"], v["e_groq"]
        model, sid = key
        cat = e_aai["category"]
        intel_v2 = v["intel_v2"]
        intel_per = v["intel_per"]
        silent_per = v["silent_per"]

        cs_v2 = codeswitch_v2(intel_v2, cat, model_pure_means.get(model, 3.0))

        pesq = float(e_aai.get("squim_pesq", 0.0))
        terminal = float(e_aai.get("terminal_sample_abs", 0.0))
        end_pop = float(e_aai.get("end_pop_db", 0.0))
        speaker_v2 = speaker_rank(pesq, terminal)

        pop_v2 = "TRUE" if (end_pop > 6.0 and terminal > 0.005) else "FALSE"

        if cat == "pure_devanagari":
            anglic_v2 = ""
        else:
            wer_rom = float(e_aai.get("wer_roman", 1.0))
            wer_en = float(e_aai.get("wer_en_forced", 1.0))
            anglic_v2 = "TRUE" if (wer_en + 0.15 < wer_rom and wer_en < 0.30) else "FALSE"

        silence_or_skip_v2 = "TRUE" if sum(silent_per) >= 2 else "FALSE"

        spread = max(intel_per) - min(intel_per)
        if spread <= 1: confidence = "HIGH"
        elif spread == 2: confidence = "MEDIUM"
        else: confidence = "LOW"

        notes = (
            f"unified_CER aai={e_aai['cer_unified']:.3f} dg={e_dg['cer_unified']:.3f} "
            f"groq={e_groq['cer_unified']:.3f} → intel_per [aai={intel_per[0]} "
            f"dg={intel_per[1]} groq={intel_per[2]}] median={intel_v2}; "
            f"silent_per [aai={int(silent_per[0])} dg={int(silent_per[1])} "
            f"groq={int(silent_per[2])}] (rule: TRUE iff ≥2/3); "
            f"PESQ={pesq:.2f} (synthetic-relative only)"
            + (f"; terminal={terminal:.3f}>0.05 → spk -1" if terminal > 0.05 else "")
            + (f"; code_switch via pure-cat gap "
               f"({model_pure_means.get(model,3.0):.2f}-{intel_v2}={model_pure_means.get(model,3.0)-intel_v2:.2f})"
               if cat not in PURE_CATS else "")
            + "; naturalness=ear-only per CEILING_REPORT.md."
        )

        rows.append({
            "model": model,
            "id": sid,
            "category": cat,
            "text": e_aai.get("text", ""),
            "intelligibility_v2": intel_v2,
            "naturalness_v2": "ear-only",
            "code_switch_v2": cs_v2,
            "speaker_quality_v2": speaker_v2,
            "roman_treated_as_english_v2": anglic_v2,
            "silence_or_skip_v2": silence_or_skip_v2,
            "end_of_clip_pop_v2": pop_v2,
            "auto_score_confidence_v2": confidence,
            "notes_v2": notes,
        })

    out_path = Path(args.out_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_HEADER)
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {out_path.relative_to(REPO)} ({len(rows)} rows)\n")

    by_model_rows: dict[str, list] = defaultdict(list)
    for r in rows:
        by_model_rows[r["model"]].append(r)
    print("=== Per-model v2.0 summary ===")
    print(f"{'model':<14} {'intel':>6} {'cs':>6} {'spk':>6} {'silent':>9} {'pop':>6} {'anglic':>7} confidence")
    for m in sorted(by_model_rows, key=lambda k: model_order.get(k, 99)):
        rs = by_model_rows[m]
        mi = sum(r["intelligibility_v2"] for r in rs) / len(rs)
        mc = sum(r["code_switch_v2"] for r in rs) / len(rs)
        ms = sum(r["speaker_quality_v2"] for r in rs) / len(rs)
        ns = sum(1 for r in rs if r["silence_or_skip_v2"] == "TRUE")
        np_ = sum(1 for r in rs if r["end_of_clip_pop_v2"] == "TRUE")
        na = sum(1 for r in rs if r["roman_treated_as_english_v2"] == "TRUE")
        ch = sum(1 for r in rs if r["auto_score_confidence_v2"] == "HIGH")
        cm = sum(1 for r in rs if r["auto_score_confidence_v2"] == "MEDIUM")
        cl = sum(1 for r in rs if r["auto_score_confidence_v2"] == "LOW")
        print(f"  {m:<12} {mi:>6.2f} {mc:>6.2f} {ms:>6.2f} {ns:>4d}/{len(rs):<3d} "
              f"{np_:>3d}/{len(rs):<3d} {na:>3d}/{len(rs):<3d} "
              f"H={ch:<2d} M={cm:<2d} L={cl}")

    cats = ["pure_devanagari", "pure_roman", "mixed_script", "english_with_NE"]
    print(f"\n=== Per-model × per-category mean intel_v2 ===")
    print(f"{'model':<14}  " + "  ".join(f"{c[:14]:<14}" for c in cats) + "  overall")
    for m in sorted(by_model_rows, key=lambda k: model_order.get(k, 99)):
        rs = by_model_rows[m]
        cells = []
        for c in cats:
            vals = [r["intelligibility_v2"] for r in rs if r["category"] == c]
            cells.append(statistics.mean(vals) if vals else 0.0)
        overall = statistics.mean([r["intelligibility_v2"] for r in rs])
        print(f"  {m:<12}  " + "  ".join(f"{x:<14.2f}" for x in cells) + f"  {overall:.2f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
