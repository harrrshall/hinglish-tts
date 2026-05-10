"""Stage 2: Claude as judge — synthesize signal vectors into final scores.

Reads:
  audit/signal_vectors.json   (Stage 1 output)
  audit/JUDGE_PROMPT.md       (versioned rubric)

Writes:
  audit/auto_scores.csv       (120 rows, schema matches scoring_template.csv)

Run modes:
  python audit/scripts/judge.py
      → outputs audit/auto_scores.csv (assumes inside Claude Code session;
        emits one batch JSON to stdout per call so you can pipe to Claude judge)

  python audit/scripts/judge.py --merge
      → merges audit/auto_scores.csv + audit/human_overrides.csv
        → audit/scoring_template_filled.csv

The judging itself happens INSIDE the Claude Code session via the Agent tool —
this script is the orchestrator that prepares batches and assembles the CSV.
For the auto-judge step, the calling agent is expected to invoke the judge
batch-by-batch and write back JSON responses to a sidecar file.

Workflow when running inside Claude Code:
  1. python judge.py --emit-batches → writes audit/judge_batches/*.json
  2. Claude Code reads each batch, judges via Agent (general-purpose, with
     JUDGE_PROMPT.md content), writes responses to audit/judge_responses/*.json
  3. python judge.py --collect → assembles auto_scores.csv from responses
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
AUDIT = REPO / "audit"
SIGNALS = AUDIT / "signal_vectors.json"
PROMPT = AUDIT / "JUDGE_PROMPT.md"
TEMPLATE = AUDIT / "scoring_template.csv"
OUT_CSV = AUDIT / "auto_scores.csv"

BATCHES_DIR = AUDIT / "judge_batches"
RESPONSES_DIR = AUDIT / "judge_responses"

# Match scoring_template.csv schema exactly
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

BATCH_SIZE = 10  # 12 batches × 10 clips = 120


def emit_batches() -> None:
    """Split signal_vectors.json into BATCH_SIZE-sized JSON files for Claude.

    Each file at judge_batches/batch_NN.json contains a list of clip vectors.
    """
    BATCHES_DIR.mkdir(parents=True, exist_ok=True)
    sigs = json.loads(SIGNALS.read_text())
    total = len(sigs)
    n_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE
    for i in range(n_batches):
        chunk = sigs[i * BATCH_SIZE: (i + 1) * BATCH_SIZE]
        path = BATCHES_DIR / f"batch_{i:02d}.json"
        path.write_text(json.dumps(chunk, ensure_ascii=False, indent=1))
    print(f"Wrote {n_batches} batches to {BATCHES_DIR}/ ({total} clips total).")
    print(f"\nNext: have Claude judge each batch using the prompt in {PROMPT}.")
    print(f"      Write responses to {RESPONSES_DIR}/batch_NN.json (same indices).")
    print(f"      Then run:  python {Path(__file__).name} --collect")


def collect() -> int:
    """Read all batch responses, validate, and assemble auto_scores.csv."""
    sigs = {(s["model"], s["id"]): s for s in json.loads(SIGNALS.read_text())}
    rows = []
    seen = set()

    if not RESPONSES_DIR.exists():
        print(f"ERROR: {RESPONSES_DIR} doesn't exist. Run --emit-batches first, then have Claude judge.")
        return 1

    for resp_file in sorted(RESPONSES_DIR.glob("batch_*.json")):
        try:
            data = json.loads(resp_file.read_text())
        except json.JSONDecodeError as e:
            print(f"ERROR parsing {resp_file}: {e}")
            return 1
        if not isinstance(data, list):
            print(f"ERROR: {resp_file} is not a JSON list")
            return 1
        for entry in data:
            for f in ["model", "id"] + JUDGE_FIELDS:
                if f not in entry:
                    print(f"ERROR in {resp_file}: missing field {f!r} in {entry}")
                    return 1
            key = (entry["model"], entry["id"])
            if key in seen:
                print(f"WARN duplicate {key}, taking later value")
            seen.add(key)
            sig = sigs.get(key)
            if sig is None:
                print(f"ERROR: {key} from {resp_file} has no matching signal vector")
                return 1
            row = {
                "model": entry["model"],
                "id": entry["id"],
                "category": sig.get("category", ""),
                "text": sig.get("text", ""),
            }
            for f in JUDGE_FIELDS:
                row[f] = entry[f]
            rows.append(row)

    # Sort to match scoring_template.csv order: by id, then by model
    model_order = {"kokoro": 0, "indicf5": 1, "indic_parler": 2,
                   "springlab_f5": 3, "orpheus_hi": 4}
    rows.sort(key=lambda r: (r["id"], model_order.get(r["model"], 99)))

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_HEADER)
        w.writeheader()
        w.writerows(rows)

    print(f"Wrote {OUT_CSV} — {len(rows)} rows.")

    # Per-model summary
    from collections import defaultdict
    by_model = defaultdict(list)
    for r in rows:
        by_model[r["model"]].append(r)
    print("\n=== Per-model summary ===")
    for model, clips in sorted(by_model.items()):
        try:
            mi = sum(int(c["intelligibility_1to5"]) for c in clips) / len(clips)
            mn = sum(int(c["naturalness_1to5"]) for c in clips) / len(clips)
            n_silent = sum(1 for c in clips if str(c["silence_or_skip"]).upper() == "TRUE")
            n_pop = sum(1 for c in clips if str(c["end_of_clip_pop"]).upper() == "TRUE")
            n_anglic = sum(1 for c in clips if str(c["roman_treated_as_english"]).upper() == "TRUE")
            print(f"  {model:14s}  intel={mi:.2f} nat={mn:.2f}  "
                  f"silent={n_silent}/{len(clips)}  pop={n_pop}/{len(clips)}  anglic={n_anglic}/{len(clips)}")
        except Exception as e:
            print(f"  {model:14s}  summary failed: {e}")

    return 0


def merge() -> int:
    """Merge auto_scores.csv + human_overrides.csv → scoring_template_filled.csv."""
    overrides_path = AUDIT / "human_overrides.csv"
    out_path = AUDIT / "scoring_template_filled.csv"
    if not OUT_CSV.exists():
        print(f"ERROR: {OUT_CSV} not found. Run --collect first.")
        return 1
    overrides = {}
    if overrides_path.exists():
        with overrides_path.open(encoding="utf-8") as f:
            for r in csv.DictReader(f):
                overrides[(r["model"], r["id"], r["column"])] = r["value"]
        print(f"Loaded {len(overrides)} human overrides from {overrides_path}")
    else:
        print(f"No {overrides_path} found — using auto_scores as-is.")

    rows = []
    with OUT_CSV.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            for col in JUDGE_FIELDS:
                key = (r["model"], r["id"], col)
                if key in overrides:
                    old = r[col]
                    r[col] = overrides[key]
                    r["notes"] = f"[human override {col}: was {old}] {r.get('notes','')}"
            rows.append(r)

    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_HEADER)
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {out_path} — {len(rows)} rows.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit-batches", action="store_true", help="Write judge_batches/*.json from signal_vectors.json")
    ap.add_argument("--collect",      action="store_true", help="Read judge_responses/*.json → auto_scores.csv")
    ap.add_argument("--merge",        action="store_true", help="Merge auto_scores.csv + human_overrides.csv → scoring_template_filled.csv")
    args = ap.parse_args()
    if args.emit_batches:
        emit_batches()
        return 0
    if args.collect:
        return collect()
    if args.merge:
        return merge()
    print("Usage: judge.py [--emit-batches | --collect | --merge]")
    print("\nDefault flow inside Claude Code:")
    print("  1. python judge.py --emit-batches")
    print("  2. <Claude judges each batch via Agent tool, writes responses>")
    print("  3. python judge.py --collect")
    print("  4. (later, after human review) python judge.py --merge")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
