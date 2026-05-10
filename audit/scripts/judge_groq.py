"""Stage 2 (Groq variant): same logic as judge.py but namespaced paths.

Reuses judge.py's helpers by overriding its constants at runtime.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import judge as _j


REPO = Path(__file__).resolve().parents[2]
AUDIT = REPO / "audit"

_j.SIGNALS = AUDIT / "signal_vectors_groq.json"
_j.OUT_CSV = AUDIT / "groq_auto_scores.csv"
_j.BATCHES_DIR = AUDIT / "groq_judge_batches"
_j.RESPONSES_DIR = AUDIT / "groq_judge_responses"


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
        import csv
        merge_out = AUDIT / "groq_scoring_template_filled.csv"
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
    print("Usage: judge_groq.py [--emit-batches | --collect | --merge]")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
