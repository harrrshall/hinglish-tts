"""Stage 2 (Deepgram variant): same logic as judge.py but namespaced paths.

Reads:
  audit/signal_vectors_deepgram.json (Stage 1 output from extract_signals_deepgram.py)
  audit/JUDGE_PROMPT.md              (versioned rubric — shared with AssemblyAI run)

Writes:
  audit/deepgram_judge_batches/batch_NN.json     (--emit-batches)
  audit/deepgram_auto_scores.csv                 (--collect)
  audit/deepgram_scoring_template_filled.csv    (--merge)

Reuses judge.py's helpers by importing the module and overriding its constants
at runtime. This keeps the AssemblyAI artifacts in their original locations.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import judge as _j  # original judge.py


REPO = Path(__file__).resolve().parents[2]
AUDIT = REPO / "audit"

# Override path constants on the imported module (in-process monkey patch)
_j.SIGNALS = AUDIT / "signal_vectors_deepgram.json"
_j.OUT_CSV = AUDIT / "deepgram_auto_scores.csv"
_j.BATCHES_DIR = AUDIT / "deepgram_judge_batches"
_j.RESPONSES_DIR = AUDIT / "deepgram_judge_responses"
# JUDGE_PROMPT.md remains shared (same rubric for fair comparison)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit-batches", action="store_true")
    ap.add_argument("--collect", action="store_true")
    ap.add_argument("--merge", action="store_true")
    args = ap.parse_args()
    if args.emit_batches:
        _j.emit_batches()
        return 0
    if args.collect:
        return _j.collect()
    if args.merge:
        # Override the merge output path too
        merge_out = AUDIT / "deepgram_scoring_template_filled.csv"
        # Easier: re-implement the small merge inline using overridden paths
        import csv
        overrides_path = AUDIT / "human_overrides.csv"
        if not _j.OUT_CSV.exists():
            print(f"ERROR: {_j.OUT_CSV} not found. Run --collect first.")
            return 1
        overrides = {}
        if overrides_path.exists():
            with overrides_path.open(encoding="utf-8") as f:
                for r in csv.DictReader(f):
                    overrides[(r["model"], r["id"], r["column"])] = r["value"]
        rows = []
        with _j.OUT_CSV.open(encoding="utf-8") as f:
            for r in csv.DictReader(f):
                for col in _j.JUDGE_FIELDS:
                    key = (r["model"], r["id"], col)
                    if key in overrides:
                        old = r[col]
                        r[col] = overrides[key]
                        r["notes"] = f"[human override {col}: was {old}] {r.get('notes','')}"
                rows.append(r)
        with merge_out.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=_j.CSV_HEADER)
            w.writeheader()
            w.writerows(rows)
        print(f"Wrote {merge_out} — {len(rows)} rows.")
        return 0
    print("Usage: judge_deepgram.py [--emit-batches | --collect | --merge]")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
