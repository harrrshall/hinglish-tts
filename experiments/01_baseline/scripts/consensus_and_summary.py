"""Compute 3-ASR consensus + summary statistics for the human GT set.

- Majority vote on intelligibility, code_switch_handling, silence_or_skip,
  roman_treated_as_english, end_of_clip_pop. Mean+round on naturalness and
  speaker_quality.
- Ceiling means per column.
- Drift comparison vs the 120-clip baseline (audit/auto_scores.csv).
"""
from __future__ import annotations

import csv
import json
import statistics
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
GT_DIR = REPO / "audit" / "human_groundtruth"
BASELINE_CSV = REPO / "audit" / "auto_scores.csv"
BASELINE_SIGNALS = REPO / "audit" / "signal_vectors.json"

BACKENDS = ["aai", "deepgram", "groq"]
INT_COLS = ["intelligibility_1to5", "naturalness_1to5",
            "code_switch_handling_1to5", "speaker_quality_1to5"]
BOOL_COLS = ["roman_treated_as_english", "silence_or_skip", "end_of_clip_pop"]


def load_scores(backend: str) -> list[dict]:
    path = GT_DIR / f"auto_scores_{backend}.csv"
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def majority_vote_int(values: list[int]) -> int:
    c = Counter(values)
    most_common = c.most_common()
    if len(most_common) >= 2 and most_common[0][1] == most_common[1][1]:
        return round(statistics.mean(values))
    return most_common[0][0]


def majority_vote_bool(values: list[str]) -> str:
    nonempty = [v for v in values if v in ("TRUE", "FALSE")]
    if not nonempty:
        return ""
    c = Counter(nonempty)
    if len(c) == 1:
        return next(iter(c))
    return c.most_common(1)[0][0]


def build_consensus():
    scores = {b: load_scores(b) for b in BACKENDS}
    n = len(scores["aai"])
    consensus_rows = []
    for i in range(n):
        row_aai = scores["aai"][i]
        consensus = {
            "model": row_aai["model"], "id": row_aai["id"],
            "category": row_aai["category"], "text": row_aai["text"],
        }
        for col in INT_COLS:
            vals = [int(scores[b][i][col]) for b in BACKENDS]
            if col in ("intelligibility_1to5", "code_switch_handling_1to5"):
                consensus[col] = majority_vote_int(vals)
            else:
                consensus[col] = round(statistics.mean(vals))
        for col in BOOL_COLS:
            consensus[col] = majority_vote_bool([scores[b][i][col] for b in BACKENDS])
        consensus["notes"] = (f"3-ASR consensus: "
            f"intel=[{','.join(scores[b][i]['intelligibility_1to5'] for b in BACKENDS)}]; "
            f"nat=[{','.join(scores[b][i]['naturalness_1to5'] for b in BACKENDS)}]; "
            f"silence=[{','.join(scores[b][i]['silence_or_skip'] for b in BACKENDS)}]")
        consensus_rows.append(consensus)

    out_path = GT_DIR / "auto_scores_consensus.csv"
    fieldnames = ["model","id","category","text",
        "intelligibility_1to5","naturalness_1to5",
        "code_switch_handling_1to5","speaker_quality_1to5",
        "roman_treated_as_english","silence_or_skip","end_of_clip_pop","notes"]
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(consensus_rows)
    print(f"Wrote {out_path.relative_to(REPO)} ({len(consensus_rows)} rows)\n")
    return consensus_rows, scores


def per_backend_means(scores):
    print("=== Per-backend per-column means (n=8 each) ===")
    for backend in BACKENDS:
        rows = scores[backend]
        m = {col: statistics.mean(int(r[col]) for r in rows) for col in INT_COLS}
        print(f"  {backend:9s}  intel={m['intelligibility_1to5']:.2f}  "
              f"nat={m['naturalness_1to5']:.2f}  "
              f"cs={m['code_switch_handling_1to5']:.2f}  "
              f"spk={m['speaker_quality_1to5']:.2f}")


def consensus_means(consensus_rows):
    print("\n=== Consensus column means (the ceiling numbers) ===")
    for col in INT_COLS:
        vals = [r[col] for r in consensus_rows]
        print(f"  {col:30s}  mean={statistics.mean(vals):.2f}  range=[{min(vals)}, {max(vals)}]")
    print("\nFlag totals:")
    for col in BOOL_COLS:
        vals = [r[col] for r in consensus_rows]
        n_true = sum(1 for v in vals if v == "TRUE")
        n_false = sum(1 for v in vals if v == "FALSE")
        n_blank = sum(1 for v in vals if v == "")
        print(f"  {col:30s}  TRUE={n_true}  FALSE={n_false}  blank={n_blank}")


def predictor_drift():
    print("\n=== Predictor drift: human GT vs 120-clip baseline ===")
    gt_signals = json.loads((GT_DIR / "signal_vectors_aai.json").read_text())
    base_signals = json.loads(BASELINE_SIGNALS.read_text())

    gt_means = {
        "utmos": statistics.mean(s["utmos"] for s in gt_signals),
        "squim_mos": statistics.mean(s["squim_mos"] for s in gt_signals),
        "squim_pesq": statistics.mean(s["squim_pesq"] for s in gt_signals),
        "squim_stoi": statistics.mean(s["squim_stoi"] for s in gt_signals),
        "squim_sisdr": statistics.mean(s["squim_sisdr"] for s in gt_signals),
    }

    print(f"{'predictor':<14} {'human_GT(n=8)':>14} {'baseline(n=120)':>16} "
          f"{'kokoro(n=30)':>14} {'parler(n=30)':>14} "
          f"{'indicf5(n=30)':>15} {'springlab(n=30)':>16} {'TTS-vs-human':>13}")
    for k in ("utmos", "squim_mos", "squim_pesq", "squim_stoi", "squim_sisdr"):
        gt_v = gt_means[k]
        base_v = statistics.mean(s[k] for s in base_signals)
        koko = statistics.mean(s[k] for s in base_signals if s["model"] == "kokoro")
        parler = statistics.mean(s[k] for s in base_signals if s["model"] == "indic_parler")
        f5 = statistics.mean(s[k] for s in base_signals if s["model"] == "indicf5")
        sl = statistics.mean(s[k] for s in base_signals if s["model"] == "springlab_f5")
        print(f"{k:<14} {gt_v:>14.3f} {base_v:>16.3f} {koko:>14.3f} {parler:>14.3f} "
              f"{f5:>15.3f} {sl:>16.3f} {base_v-gt_v:>+12.3f}")


def auto_score_drift(consensus_rows):
    print("\n=== Auto-score drift: human GT consensus vs 120-clip baseline ===")
    base_rows = []
    with BASELINE_CSV.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                base_rows.append({c: int(r[c]) for c in INT_COLS} | {"model": r["model"], "category": r["category"]})
            except ValueError:
                continue

    print(f"{'col':<28} {'human_GT':>10} {'baseline':>10} "
          f"{'kokoro':>10} {'parler':>10} {'indicf5':>10} {'springlab':>10}")
    for col in INT_COLS:
        gt_v = statistics.mean(r[col] for r in consensus_rows)
        base_v = statistics.mean(r[col] for r in base_rows)
        models = ("kokoro", "indic_parler", "indicf5", "springlab_f5")
        per_model = [statistics.mean(r[col] for r in base_rows if r["model"]==m) for m in models]
        print(f"{col:<28} {gt_v:>10.2f} {base_v:>10.2f} " +
              " ".join(f"{v:>10.2f}" for v in per_model))


def main() -> int:
    consensus_rows, scores = build_consensus()
    per_backend_means(scores)
    consensus_means(consensus_rows)
    predictor_drift()
    auto_score_drift(consensus_rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
