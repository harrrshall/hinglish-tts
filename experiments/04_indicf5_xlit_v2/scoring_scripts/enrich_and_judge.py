"""Stage-2: v2.1 enrichment + judge for indicf5_patched_xlit_v2.

Reads:
  experiments/04_indicf5_xlit_v2/scores/signal_vectors_aai.json  (from run_all.py)

Writes:
  experiments/04_indicf5_xlit_v2/scores/signal_vectors_v2.json   (enriched)
  experiments/04_indicf5_xlit_v2/scores/auto_scores_v2.1.csv     (final scores)

Run with py311 venv (needs fairseq for IndicXlit):
  cd ~/Desktop/hienglish
  ./venv-scoring-py311/bin/python experiments/04_indicf5_xlit_v2/scoring_scripts/enrich_and_judge.py
"""
from __future__ import annotations

import csv
import json
import re
import string
import sys
from pathlib import Path

import jiwer

REPO = Path(__file__).resolve().parents[3]
SCRIPTS = REPO / "scoring" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from lib_normalize import to_unified_devanagari

SCORES = REPO / "experiments" / "04_indicf5_xlit_v2" / "scores"
AAI_VECTORS = SCORES / "signal_vectors_aai.json"
V2_VECTORS  = SCORES / "signal_vectors_v2.json"
CSV_OUT     = SCORES / "auto_scores_v2.1.csv"

MODEL = "indicf5_patched_xlit_v2"
_PUNCT = string.punctuation + "।॥,।'\"‍‌"


def _strip_punct(text: str) -> str:
    out = "".join(" " if ch in _PUNCT else ch for ch in text)
    return re.sub(r"\s+", " ", out).strip()


def _cer(ref: str, hyp: str) -> float:
    ref = _strip_punct(ref)
    hyp = _strip_punct(hyp)
    if not ref:
        return 1.0
    return float(jiwer.cer(ref, hyp))


def _wer(ref: str, hyp: str) -> float:
    ref = _strip_punct(ref)
    hyp = _strip_punct(hyp)
    if not ref:
        return 1.0
    return float(jiwer.wer(ref, hyp))


def _token_overlap(ref_norm: str, hyp_norm: str) -> float:
    ref_toks = {t for t in _strip_punct(ref_norm).split() if len(t) > 1}
    hyp_toks = {t for t in _strip_punct(hyp_norm).split() if len(t) > 1}
    if not ref_toks:
        return 1.0
    return len(ref_toks & hyp_toks) / len(ref_toks)


def enrich(entry: dict, asr_backend: str) -> dict:
    text = entry.get("text", "") or ""
    th = entry.get("transcript_hi", "") or ""
    tr = entry.get("transcript_roman", "") or ""

    print(f"  normalizing id={entry['id']} ...", end=" ", flush=True)
    text_norm = to_unified_devanagari(text)
    th_norm   = to_unified_devanagari(th)
    tr_norm   = to_unified_devanagari(tr)
    print("done")

    silence_mid = float(entry.get("silence_mid_clip_s", 0.0))
    overlap = _token_overlap(text_norm, th_norm)
    skip_norm = silence_mid > 0.5

    out = dict(entry)
    out.update({
        "text_normalized": text_norm,
        "transcript_hi_normalized": th_norm,
        "transcript_roman_normalized": tr_norm,
        "cer_devanagari_norm": round(_cer(text_norm, th_norm), 4),
        "wer_roman_norm": round(_wer(text_norm, tr_norm), 4),
        "asr_backend": asr_backend,
        "silence_or_skip_norm": skip_norm,
        "_token_overlap_norm": round(overlap, 4),
    })
    return out


def score_intel(cer_norm: float) -> int:
    if cer_norm <= 0.05:  return 5
    if cer_norm <= 0.15:  return 4
    if cer_norm <= 0.30:  return 3
    if cer_norm <= 0.50:  return 2
    return 1


def score_speaker(pesq: float, terminal_abs: float) -> int:
    if pesq >= 4.0:  s = 5
    elif pesq >= 3.5: s = 4
    elif pesq >= 3.0: s = 3
    elif pesq >= 2.5: s = 2
    else:             s = 1
    if terminal_abs > 0.05:
        s = max(1, s - 1)
    return s


def score_end_pop(end_pop_db: float, terminal_abs: float) -> str:
    return "TRUE" if (end_pop_db > 6.0 and terminal_abs > 0.005) else "FALSE"


def score_silence(entry: dict) -> str:
    return "TRUE" if entry["silence_or_skip_norm"] else "FALSE"


def code_switch_score(intel: int, cat: str, pure_mean: float) -> int:
    if cat in ("pure_devanagari", "pure_roman"):
        return intel
    gap = pure_mean - intel
    if gap <= 0.05:  return 5
    if gap <= 0.15:  return 4
    if gap <= 0.30:  return 3
    if gap <= 0.50:  return 2
    return 1


def judge(enriched: list[dict]) -> list[dict]:
    # Compute pure-category mean intel
    pure_rows = [e for e in enriched
                 if e["category"] in ("pure_devanagari", "pure_roman")]
    pure_mean = sum(score_intel(e["cer_devanagari_norm"]) for e in pure_rows) / len(pure_rows)
    print(f"\npure-category mean intel: {pure_mean:.3f} (n={len(pure_rows)})")

    rows = []
    for e in enriched:
        intel = score_intel(e["cer_devanagari_norm"])
        pesq  = float(e.get("squim_pesq", 0.0) or 0.0)
        term  = float(e.get("terminal_sample_abs", 0.0) or 0.0)
        rows.append({
            "model": MODEL,
            "id": e["id"],
            "category": e["category"],
            "text": e["text"],
            "text_normalized": e["text_normalized"],
            "intelligibility_1to5": intel,
            "naturalness_1to5": "EAR_ONLY",
            "code_switch_handling_1to5": code_switch_score(intel, e["category"], pure_mean),
            "speaker_quality_1to5": score_speaker(pesq, term),
            "silence_or_skip": score_silence(e),
            "end_of_clip_pop": score_end_pop(
                float(e.get("end_pop_db", 0.0) or 0.0), term),
            "rubric_version": "2.1",
            "asr_backend": e["asr_backend"],
            "cer_devanagari_norm": e["cer_devanagari_norm"],
            "squim_pesq": round(pesq, 3),
            "notes": (
                f"cer_norm={e['cer_devanagari_norm']:.3f}; "
                f"squim_pesq={pesq:.3f}; "
                f"silence_mid={e.get('silence_mid_clip_s',0.0):.2f}s"
            ),
        })
    return rows


def main() -> int:
    print(f"Loading {AAI_VECTORS} ...")
    aai = json.loads(AAI_VECTORS.read_text())
    print(f"  {len(aai)} entries")

    print("\n=== v2.1 enrichment (IndicXlit + normalized CER/WER) ===")
    enriched = [enrich(e, "aai") for e in aai]
    enriched.sort(key=lambda r: int(r["id"]) if r["id"].isdigit() else 99)

    V2_VECTORS.write_text(json.dumps(enriched, ensure_ascii=False, indent=1))
    print(f"\nWrote {V2_VECTORS}")

    # CER_norm summary
    print("\n=== CER_norm by category ===")
    import numpy as np
    for cat in ("pure_devanagari", "pure_roman", "mixed_script", "english_with_NE"):
        rows = [e for e in enriched if e["category"] == cat]
        if rows:
            mean_cer = np.mean([r["cer_devanagari_norm"] for r in rows])
            print(f"  {cat:20s}: mean_cer_norm={mean_cer:.3f}  n={len(rows)}")

    print("\n=== Judging ===")
    scored = judge(enriched)

    # Write CSV
    fieldnames = [
        "model", "id", "category", "text", "text_normalized",
        "intelligibility_1to5", "naturalness_1to5", "code_switch_handling_1to5",
        "speaker_quality_1to5", "silence_or_skip", "end_of_clip_pop",
        "rubric_version", "asr_backend", "cer_devanagari_norm", "squim_pesq", "notes",
    ]
    with CSV_OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(scored)
    print(f"Wrote {CSV_OUT} — {len(scored)} rows")

    # Summary table
    print("\n=== Score summary by category ===")
    for cat in ("pure_devanagari", "pure_roman", "mixed_script", "english_with_NE", None):
        if cat is None:
            rows = scored
            label = "overall"
        else:
            rows = [r for r in scored if r["category"] == cat]
            label = cat
        if rows:
            mean_intel = sum(r["intelligibility_1to5"] for r in rows) / len(rows)
            print(f"  {label:20s}: {mean_intel:.2f}  (n={len(rows)})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
