"""Build wav_to_sentence.csv from the user-provided mapping + eval_sentences.tsv.

Hardcoded mapping (provided by user):
  human_01.wav  -> id 1
  human_02.wav  -> id 5
  human_03.wav  -> id 9
  human_04.wav  -> id 11
  human_05.wav  -> id 17
  human_06.wav  -> id 18
  human_07.wav  -> id 24
  human_08.wav  -> id 26
"""
from __future__ import annotations

import csv
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
EVAL_TSV = REPO / "audit" / "eval_sentences.tsv"
OUT_CSV = REPO / "audit" / "human_groundtruth" / "wav_to_sentence.csv"

MAPPING = [
    ("human_01.wav", 1),
    ("human_02.wav", 5),
    ("human_03.wav", 9),
    ("human_04.wav", 11),
    ("human_05.wav", 17),
    ("human_06.wav", 18),
    ("human_07.wav", 24),
    ("human_08.wav", 26),
]


def main() -> int:
    eval_rows = {}
    with EVAL_TSV.open(encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            eval_rows[int(r["id"])] = r

    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["filename", "sentence_id", "category", "reference_text", "tested_phenomenon"])
        for filename, sid in MAPPING:
            row = eval_rows[sid]
            w.writerow([filename, f"{sid:02d}", row["category"], row["text"], row["tested_phenomenon"]])

    print(f"Wrote {OUT_CSV.relative_to(REPO)} ({len(MAPPING)} rows)")
    with OUT_CSV.open(encoding="utf-8") as f:
        for line in f:
            print("  " + line.rstrip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
