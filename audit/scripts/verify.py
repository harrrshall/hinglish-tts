#!/usr/bin/env python3
"""Self-check before declaring the audit done. Implements AUDIT_PLAN.md §6.

Exits 0 only when:
  • eval_sentences.tsv has 31 lines (header + 30)
  • reference_audio/hindi_ref.{wav,txt} exist and the .txt is non-empty
  • each of the 5 model output dirs has ≥28 .wav files + a log.json
  • no zero-byte .wav files
  • scoring_template.csv, METADATA.json, RUN_NOTES.md exist
"""
from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
ROOT = REPO / "audit"

EXPECTED_MODELS = ["kokoro", "indicf5", "indic_parler", "springlab_f5", "orpheus_hi"]


def main() -> int:
    problems: list[str] = []

    # 1. Eval set
    es = ROOT / "eval_sentences.tsv"
    if not es.exists():
        problems.append("eval_sentences.tsv missing")
    else:
        n = sum(1 for _ in es.open(encoding="utf-8"))
        if n != 31:
            problems.append(f"eval_sentences.tsv has {n} lines, expected 31")

    # 2. Reference audio
    if not (ROOT / "reference_audio" / "hindi_ref.wav").exists():
        problems.append("reference_audio/hindi_ref.wav missing")
    txt = ROOT / "reference_audio" / "hindi_ref.txt"
    if not txt.exists() or not txt.read_text(encoding="utf-8").strip():
        problems.append("reference_audio/hindi_ref.txt missing or empty")

    # 3. Per-model: 30 wavs + log.json, no zero-byte files
    for m in EXPECTED_MODELS:
        d = ROOT / "results" / m
        if not d.exists():
            problems.append(f"results/{m}/ missing")
            continue
        wavs = sorted(d.glob("*.wav"))
        if len(wavs) < 28:
            problems.append(f"{m}: only {len(wavs)}/30 audio files")
        zero = [p for p in wavs if p.stat().st_size == 0]
        if zero:
            problems.append(f"{m}: {len(zero)} zero-byte files: {[p.name for p in zero]}")
        if not (d / "log.json").exists():
            problems.append(f"{m}: log.json missing")

    # 4. Auxiliary files
    for f in ("scoring_template.csv", "METADATA.json", "RUN_NOTES.md"):
        if not (ROOT / f).exists():
            problems.append(f"{f} missing")

    if problems:
        print("VERIFICATION FAILED:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1

    print("All checks passed. Audit ready for human review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
