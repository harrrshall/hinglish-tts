"""Deterministic implementation of JUDGE_PROMPT.md v1.0 thresholds.

For the patched IndicF5 re-run: scoring 30 clips × 3 ASR backends = 90 deterministic
scoring decisions. Avoids the per-batch variance of Claude-as-judge across backends
and the cost of 9 Agent calls.

Usage:
    python audit/scripts/patched/auto_score.py \\
        --signals audit/indicf5_patched/signal_vectors_aai.json \\
        --out     audit/indicf5_patched/auto_scores_aai.csv
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

CSV_HEADER = [
    "model", "id", "category", "text",
    "intelligibility_1to5", "naturalness_1to5",
    "code_switch_handling_1to5", "speaker_quality_1to5",
    "roman_treated_as_english", "silence_or_skip", "end_of_clip_pop",
    "notes",
]

DEVA_CATS = {"pure_devanagari", "mixed_script"}  # CER-primary
ROMAN_CATS = {"pure_roman", "english_with_NE"}    # WER-primary


def score_intel(cer: float, wer_rom: float, cat: str) -> int:
    """Anchor-based 1-5 from CER (Devanagari rows) or WER (Roman rows)."""
    err = cer if cat in DEVA_CATS else wer_rom
    if err <= 0.05: return 5
    if err <= 0.15: return 4
    if err <= 0.30: return 3
    if err <= 0.50: return 2
    return 1


def score_naturalness(utmos: float, squim_mos: float, silence_mid: float, skip: bool) -> int:
    """mean(UTMOS, SQUIM_MOS) rounded; -1 if predictors disagree>0.7, -1 if mid-clip skip."""
    mean_mos = (utmos + squim_mos) / 2.0
    score = max(1, min(5, int(round(mean_mos))))
    disagree = abs(utmos - squim_mos) > 0.7
    if disagree: score -= 1
    if silence_mid > 0.5 or skip: score -= 1
    return max(1, score)


def score_speaker(pesq: float, terminal_abs: float) -> int:
    """SQUIM_PESQ thresholds, -1 rank if terminal_sample_abs > 0.05."""
    if pesq >= 4.0: s = 5
    elif pesq >= 3.5: s = 4
    elif pesq >= 3.0: s = 3
    elif pesq >= 2.5: s = 2
    else: s = 1
    if terminal_abs > 0.05: s -= 1
    return max(1, s)


def flag_silence(silence_mid: float, transcript_hi: str, gt_text: str) -> bool:
    """TRUE if mid-clip silence>0.5 OR transcript missing >20% of words."""
    if silence_mid > 0.5: return True
    # crude: count tokens in gt vs transcript
    gt_tokens = [t for t in gt_text.split() if t]
    if not gt_tokens: return False
    if not transcript_hi.strip(): return True
    # word-level: how many gt tokens (or their devanagari equivalents) appear in the transcript?
    # since transcript_hi may be Devanagari and gt may be Roman or mixed, this is approximate.
    # Use the simpler proxy: empty/very-short transcript on a non-trivial sentence = TRUE
    if len(transcript_hi.replace(" ", "")) < 0.3 * len(gt_text.replace(" ", "")):
        return True
    return False


def flag_pop(end_pop_db: float, terminal_abs: float) -> bool:
    return end_pop_db > 6.0 and terminal_abs > 0.005


def flag_anglic(wer_rom: float, wer_en: float, cat: str) -> str:
    """TRUE iff Roman/mixed AND English-forced beats Roman by 0.15 AND wer_en<0.30."""
    if cat == "pure_devanagari": return "FALSE"
    if wer_en + 0.15 < wer_rom and wer_en < 0.30: return "TRUE"
    return "FALSE"


def score_codeswitch(intel: int, cat: str, model_pure_intel_mean: float) -> int:
    """For mixed_script / english_with_NE: rank gap vs the model's pure-category mean."""
    if cat in {"pure_devanagari", "pure_roman"}:
        return intel
    gap = model_pure_intel_mean - intel
    if gap <= 0.05: return 5
    if gap <= 0.15: return 4
    if gap <= 0.30: return 3
    if gap <= 0.50: return 2
    return 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--signals", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    sigs = json.loads(args.signals.read_text())

    # First pass: compute each clip's intelligibility, then per-model pure-category mean
    rows = []
    for s in sigs:
        cat = s["category"]
        cer = float(s["cer_devanagari"])
        wer_rom = float(s["wer_roman"])
        wer_en = float(s["wer_en_forced"])
        intel = score_intel(cer, wer_rom, cat)
        s["_intel"] = intel
        s["_anglic"] = flag_anglic(wer_rom, wer_en, cat)
        s["_pop"]    = flag_pop(float(s["end_pop_db"]), float(s["terminal_sample_abs"]))
        s["_skip"]   = flag_silence(float(s["silence_mid_clip_s"]), s.get("transcript_hi", ""), s.get("text", ""))
    pure_intels = [s["_intel"] for s in sigs if s["category"] in {"pure_devanagari", "pure_roman"}]
    pure_mean = sum(pure_intels) / len(pure_intels) if pure_intels else 3.0

    for s in sigs:
        cat = s["category"]
        intel = s["_intel"]
        nat = score_naturalness(float(s["utmos"]), float(s["squim_mos"]),
                                float(s["silence_mid_clip_s"]), bool(s["_skip"]))
        spk = score_speaker(float(s["squim_pesq"]), float(s["terminal_sample_abs"]))
        cs = score_codeswitch(intel, cat, pure_mean)
        rows.append({
            "model": s["model"], "id": s["id"], "category": cat, "text": s["text"],
            "intelligibility_1to5": intel,
            "naturalness_1to5": nat,
            "code_switch_handling_1to5": cs,
            "speaker_quality_1to5": spk,
            "roman_treated_as_english": s["_anglic"],
            "silence_or_skip": "TRUE" if s["_skip"] else "FALSE",
            "end_of_clip_pop": "TRUE" if s["_pop"] else "FALSE",
            "notes": (
                f"CER={s['cer_devanagari']:.2f} WER_rom={s['wer_roman']:.2f} "
                f"WER_en={s['wer_en_forced']:.2f} UTMOS={s['utmos']:.2f} "
                f"SQUIM={s['squim_mos']:.2f} PESQ={s['squim_pesq']:.2f} "
                f"silence_mid={s['silence_mid_clip_s']:.2f}"
            ),
        })

    rows.sort(key=lambda r: int(r["id"]))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_HEADER)
        w.writeheader()
        w.writerows(rows)

    # Per-category summary
    print(f"Wrote {args.out} ({len(rows)} rows)")
    print("\nPer-category mean intelligibility:")
    by_cat: dict[str, list[int]] = {}
    for r in rows:
        by_cat.setdefault(r["category"], []).append(r["intelligibility_1to5"])
    for c, vals in sorted(by_cat.items()):
        print(f"  {c:18s}: {sum(vals)/len(vals):.2f}  (n={len(vals)})")
    overall = sum(r["intelligibility_1to5"] for r in rows) / len(rows)
    n_skip = sum(1 for r in rows if r["silence_or_skip"] == "TRUE")
    n_anglic = sum(1 for r in rows if r["roman_treated_as_english"] == "TRUE")
    print(f"\nOverall mean intel: {overall:.2f}")
    print(f"silence_or_skip: {n_skip}/{len(rows)}")
    print(f"roman_treated_as_english: {n_anglic}/{len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
