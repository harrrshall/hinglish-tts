"""Stage-2 v2.0: deterministic scorer matching JUDGE_PROMPT_v2.md anchors.

Reads 3 backend signal-vector files (4 baseline models × 30 sentences × 3 ASRs):
  audit/signal_vectors_v2_aai.json
  audit/signal_vectors_v2_deepgram.json
  audit/signal_vectors_v2_groq.json

Per (model, sentence): consensus across the 3 ASRs (mode of the integer score).
DSP-only fields (speaker_quality, silence_or_skip, end_of_clip_pop) are ASR-independent
and identical across backends, so they're taken from any one (here: AAI).

Writes:
  audit/auto_scores_v2.csv  -- 120 rows (4 models × 30 sentences)

Patched IndicF5 is scored as a separate downstream task and NOT included here.

Run: python audit/scripts/judge_v2.py
"""
from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path


CSV_HEADER_V2 = [
    "model", "id", "category", "text", "ref_unified",
    "intelligibility_1to5",
    "naturalness_1to5",          # always "EAR_ONLY"
    "code_switch_handling_1to5",
    "speaker_quality_1to5",
    "silence_or_skip",
    "end_of_clip_pop",
    "notes",
]

PURE_CATS = {"pure_devanagari", "pure_roman"}


def score_intel_norm(cer_unified: float) -> int:
    """v2 anchors — CER on normalized (Devanagari-unified) strings."""
    if cer_unified <= 0.05: return 5
    if cer_unified <= 0.15: return 4
    if cer_unified <= 0.30: return 3
    if cer_unified <= 0.50: return 2
    return 1


def score_speaker(pesq: float, terminal_abs: float) -> int:
    if pesq >= 4.0: s = 5
    elif pesq >= 3.5: s = 4
    elif pesq >= 3.0: s = 3
    elif pesq >= 2.5: s = 2
    else: s = 1
    if terminal_abs > 0.05:
        s -= 1
    return max(1, s)


def flag_skip(silence_mid: float) -> bool:
    """v2 silence_or_skip: silence_mid > 0.5 only.

    The 'missing >20% words' half from v1 was eliminated because (a) Mode A truncation
    is solved by the duration patch and (b) Mode C garbling is captured by intel.
    Token-overlap heuristics over-trigger on legitimate ASR spelling variance.
    """
    return silence_mid > 0.5


def flag_pop(end_pop_db: float, terminal_abs: float) -> bool:
    return end_pop_db > 6.0 and terminal_abs > 0.005


def score_codeswitch(intel: int, cat: str, pure_intel_mean: float) -> int:
    if cat in PURE_CATS:
        return intel
    gap = pure_intel_mean - intel
    if gap <= 0.05: return 5
    if gap <= 0.15: return 4
    if gap <= 0.30: return 3
    if gap <= 0.50: return 2
    return 1


def _consensus_int(vals: list[int]) -> int:
    return Counter(vals).most_common(1)[0][0]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit-dir", type=Path, default=Path("audit"))
    ap.add_argument("--out", type=Path, default=Path("audit/auto_scores_v2.csv"))
    args = ap.parse_args()

    sigs_aai = json.loads((args.audit_dir / "signal_vectors_v2_aai.json").read_text())
    sigs_dg  = json.loads((args.audit_dir / "signal_vectors_v2_deepgram.json").read_text())
    sigs_grq = json.loads((args.audit_dir / "signal_vectors_v2_groq.json").read_text())
    print(f"Loaded: aai={len(sigs_aai)}, deepgram={len(sigs_dg)}, groq={len(sigs_grq)}")

    # Index each by (model, id) for join
    by_aai = {(s["model"], s["id"]): s for s in sigs_aai}
    by_dg  = {(s["model"], s["id"]): s for s in sigs_dg}
    by_grq = {(s["model"], s["id"]): s for s in sigs_grq}

    keys = sorted(by_aai.keys(), key=lambda k: (int(k[1]) if k[1].isdigit() else 99, k[0]))

    # First pass: per-(model, id) compute consensus intel + DSP-driven flags
    rows: list[dict] = []
    for (model, sid) in keys:
        s_aai = by_aai[(model, sid)]
        s_dg  = by_dg.get((model, sid))
        s_grq = by_grq.get((model, sid))
        if s_dg is None or s_grq is None:
            print(f"  [skip] missing DG/Groq for {model}/{sid}")
            continue

        # CER from each ASR's normalized field
        cers = [float(s_aai["cer_unified"]), float(s_dg["cer_unified"]), float(s_grq["cer_unified"])]
        intels = [score_intel_norm(c) for c in cers]
        intel = _consensus_int(intels)

        # DSP signals (ASR-independent, same across backends; use AAI)
        pesq = float(s_aai["squim_pesq"])
        term = float(s_aai["terminal_sample_abs"])
        end_pop = float(s_aai["end_pop_db"])
        silence_mid = float(s_aai["silence_mid_clip_s"])
        spk = score_speaker(pesq, term)
        skip = flag_skip(silence_mid)
        pop = flag_pop(end_pop, term)

        rows.append({
            "model": model, "id": sid,
            "category": s_aai["category"], "text": s_aai["text"],
            "ref_unified": s_aai["ref_unified"],
            "intel": intel,
            "spk": spk, "skip": skip, "pop": pop,
            "_cer_mean": sum(cers) / len(cers),
            "_pesq": pesq, "_silence_mid": silence_mid,
            "_intels_per_asr": intels,
        })

    # Second pass: per-model pure-category intel mean for code_switch
    by_model: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_model[r["model"]].append(r)
    pure_means: dict[str, float] = {}
    for m, rs in by_model.items():
        pures = [r["intel"] for r in rs if r["category"] in PURE_CATS]
        pure_means[m] = statistics.mean(pures) if pures else 3.0

    # Third pass: emit CSV
    out_rows = []
    for r in rows:
        cs = score_codeswitch(r["intel"], r["category"], pure_means[r["model"]])
        out_rows.append({
            "model": r["model"], "id": r["id"],
            "category": r["category"], "text": r["text"],
            "ref_unified": r["ref_unified"],
            "intelligibility_1to5": r["intel"],
            "naturalness_1to5": "EAR_ONLY",
            "code_switch_handling_1to5": cs,
            "speaker_quality_1to5": r["spk"],
            "silence_or_skip": "TRUE" if r["skip"] else "FALSE",
            "end_of_clip_pop": "TRUE" if r["pop"] else "FALSE",
            "notes": (
                f"v2 3-ASR consensus: CER_unified mean={r['_cer_mean']:.3f} "
                f"(intels per ASR: AAI={r['_intels_per_asr'][0]}, "
                f"DG={r['_intels_per_asr'][1]}, GRQ={r['_intels_per_asr'][2]}); "
                f"PESQ={r['_pesq']:.2f}; silence_mid={r['_silence_mid']:.2f}"
            ),
        })

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_HEADER_V2)
        w.writeheader()
        w.writerows(out_rows)

    print(f"\nWrote {args.out} — {len(out_rows)} rows ({len(by_model)} models)")

    # Per-model × per-category headline
    print("\n=== Per-model × per-category mean intel (v2.0, 3-ASR consensus) ===")
    cats = ["pure_devanagari", "pure_roman", "mixed_script", "english_with_NE"]
    print(f"  {'model':<14}  " + "  ".join(f"{c[:14]:<14}" for c in cats) + "  overall")
    for m in sorted(by_model.keys()):
        rs = by_model[m]
        cells = []
        for c in cats:
            vals = [r["intel"] for r in rs if r["category"] == c]
            cells.append(statistics.mean(vals) if vals else 0.0)
        overall = statistics.mean([r["intel"] for r in rs])
        print(f"  {m:<14s}  " + "  ".join(f"{x:<14.2f}" for x in cells) + f"  {overall:.2f}")

    print("\n=== silence_or_skip flags ===")
    for m, rs in sorted(by_model.items()):
        n_skip = sum(1 for r in rs if r["skip"])
        print(f"  {m:<18s}: {n_skip}/{len(rs)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
