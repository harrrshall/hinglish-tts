#!/usr/bin/env python3
"""Build audit/scoring_template.csv per AUDIT_PLAN.md §5.2.

150 rows = 30 sentences × 5 models, sorted by `id`, then by `model`. The first
four columns are pre-filled; the rest are blank for the human scorer.
"""
from __future__ import annotations

import csv
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
EVAL = REPO / "audit" / "eval_sentences.tsv"
OUT  = REPO / "audit" / "scoring_template.csv"

MODELS = ["kokoro", "indicf5", "indic_parler", "springlab_f5", "orpheus_hi"]

HEADER = [
    "model", "id", "category", "text",
    "intelligibility_1to5", "naturalness_1to5",
    "code_switch_handling_1to5", "speaker_quality_1to5",
    "roman_treated_as_english", "silence_or_skip", "end_of_clip_pop",
    "notes",
]


def main() -> int:
    with open(EVAL, encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    rows.sort(key=lambda r: r["id"])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(HEADER)
        for r in rows:
            for model in MODELS:
                w.writerow([
                    model, r["id"], r["category"], r["text"],
                    "", "", "", "", "", "", "", "",
                ])

    n = sum(1 for _ in open(OUT, encoding="utf-8")) - 1
    expected = len(rows) * len(MODELS)
    assert n == expected, f"wrote {n} rows, expected {expected}"
    print(f"Wrote {OUT} ({n} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
