"""Stage 2 (human GT): emit batches and collect responses for each ASR backend.

Mirrors judge.py but operates inside audit/human_groundtruth/ with one set of
batch+response dirs per ASR backend.

Usage:
  python judge_human.py --emit-batches  → writes 3 batch JSONs (one per backend)
  python judge_human.py --collect       → reads judge_responses_<backend>/* → auto_scores_<backend>.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
GT_DIR = REPO / "audit" / "human_groundtruth"

BACKENDS = ["aai", "deepgram", "groq"]

CSV_HEADER = [
    "model", "id", "category", "text",
    "intelligibility_1to5", "naturalness_1to5",
    "code_switch_handling_1to5", "speaker_quality_1to5",
    "roman_treated_as_english", "silence_or_skip", "end_of_clip_pop",
    "notes",
]
JUDGE_FIELDS = [
    "intelligibility_1to5", "naturalness_1to5",
    "code_switch_handling_1to5", "speaker_quality_1to5",
    "roman_treated_as_english", "silence_or_skip", "end_of_clip_pop",
    "notes",
]


def emit_batches() -> None:
    for backend in BACKENDS:
        sigs_path = GT_DIR / f"signal_vectors_{backend}.json"
        if not sigs_path.exists():
            print(f"[fatal] {sigs_path} missing", file=sys.stderr); sys.exit(2)
        sigs = json.loads(sigs_path.read_text())
        bdir = GT_DIR / f"judge_batches_{backend}"
        bdir.mkdir(parents=True, exist_ok=True)
        # 8 clips → single batch
        out = bdir / "batch_00.json"
        out.write_text(json.dumps(sigs, ensure_ascii=False, indent=1))
        print(f"  wrote {out.relative_to(REPO)} ({len(sigs)} clips)")


def collect() -> int:
    rc = 0
    for backend in BACKENDS:
        sigs = {(s["model"], s["id"]): s
                for s in json.loads((GT_DIR / f"signal_vectors_{backend}.json").read_text())}
        rdir = GT_DIR / f"judge_responses_{backend}"
        if not rdir.exists():
            print(f"[skip] {rdir} missing — judge step not run for {backend}")
            rc = 1; continue
        rows = []
        for resp_file in sorted(rdir.glob("batch_*.json")):
            data = json.loads(resp_file.read_text())
            for entry in data:
                for f in ["model", "id"] + JUDGE_FIELDS:
                    if f not in entry:
                        print(f"[err] {resp_file}: missing {f!r} in {entry}")
                        rc = 1; continue
                key = (entry["model"], entry["id"])
                sig = sigs.get(key)
                if sig is None:
                    print(f"[err] no signal for {key} from {resp_file}")
                    rc = 1; continue
                row = {"model": entry["model"], "id": entry["id"],
                       "category": sig.get("category", ""), "text": sig.get("text", "")}
                for f in JUDGE_FIELDS:
                    row[f] = entry[f]
                rows.append(row)
        out_csv = GT_DIR / f"auto_scores_{backend}.csv"
        with out_csv.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=CSV_HEADER)
            w.writeheader()
            w.writerows(rows)
        print(f"  wrote {out_csv.relative_to(REPO)} ({len(rows)} rows)")
    return rc


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit-batches", action="store_true")
    ap.add_argument("--collect", action="store_true")
    args = ap.parse_args()
    if args.emit_batches:
        emit_batches(); return 0
    if args.collect:
        return collect()
    print("Usage: judge_human.py [--emit-batches | --collect]")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
