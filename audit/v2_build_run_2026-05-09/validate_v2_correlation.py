"""Phase 6 correlation gate — v2.0 vs v1.0 vs user manual ratings.

User manual ratings live in `audit/human_scores.md` as markdown tables (one
per model). Per the file's header, the columns are:
  Intel | Nat | CS | Spk | Eng | Sil | Pop      (1–5 Likert)
For Eng/Sil/Pop the higher-is-better convention applies (4–5 = "no problem").

Cells:
  • plain integer = high-confidence rating
  • integer with `[?]` suffix = low-confidence (kept; flagged in summary)
  • `—` = blank / out-of-frame (skipped)

We parse only the 3 models the user rated: Kokoro, Indic Parler-TTS, IndicF5.
SPRINGLab F5-Hindi was not manually rated.

Computes Pearson r for intel_human vs intel_v1 and vs intel_v2. Spec gate:
  v2.0 ships iff its correlation with manual intel is ≥ v1.0's.

Writes: audit/v2_validation/CORRELATION_REPORT.md
"""
from __future__ import annotations

import csv
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Optional

from scipy.stats import pearsonr, spearmanr

REPO = Path(__file__).resolve().parents[2]
HUMAN_MD = REPO / "audit" / "human_scores.md"
V1_CSV = REPO / "audit" / "auto_scores.csv"
V2_CSV = REPO / "audit" / "auto_scores_v2.csv"
OUT_DIR = REPO / "audit" / "v2_validation"
OUT_REPORT = OUT_DIR / "CORRELATION_REPORT.md"

# Map markdown header keys → internal column names.
HUMAN_COLS = ["intel", "nat", "cs", "spk", "eng", "sil", "pop"]

# Map between human_scores.md model headings and auto_scores.csv model strings.
MODEL_MAP = {
    "Kokoro": "kokoro",
    "Indic Parler-TTS": "indic_parler",
    "IndicF5": "indicf5",
}


_CELL_RE = re.compile(r"^\s*(\d+)(\s*\[\?\])?\s*$")


def parse_cell(s: str) -> tuple[Optional[int], bool]:
    """Returns (value, low_confidence). value is None if cell is — or unparseable."""
    s = s.strip()
    if not s or s == "—":
        return None, False
    m = _CELL_RE.match(s)
    if m:
        return int(m.group(1)), bool(m.group(2))
    return None, False


def parse_human_md(path: Path) -> dict[tuple[str, str], dict]:
    """Parse human_scores.md → dict[(model, id_str)] → row of ints + flags.

    id_str is zero-padded ("01" .. "30") to align with auto_scores.csv keys.
    """
    text = path.read_text()
    out: dict[tuple[str, str], dict] = {}

    # Sections are headed by `## <Model Name>` (sometimes with annotation).
    # Within each section, rows are markdown table rows starting with `| <int>`.
    current_model: Optional[str] = None

    for line in text.splitlines():
        h2 = re.match(r"##\s+([A-Za-z0-9 \-]+)", line)
        if h2:
            heading = h2.group(1).strip()
            current_model = MODEL_MAP.get(heading)
            continue

        if not current_model:
            continue

        # Match table rows like: |  1 | 2 | 2 | 3 | 2 | 3 | — | — |
        # Skip header rows (contain "Intel" or "---").
        if not line.startswith("|"):
            continue
        if "Intel" in line or "---" in line or ":" in line[:6]:
            continue

        cells = [c.strip() for c in line.strip("|").split("|")]
        # Expect 8 cells: id + 7 columns. Filter rows that don't match.
        if len(cells) != 8:
            continue
        try:
            sid_int = int(cells[0])
        except ValueError:
            continue
        if not (1 <= sid_int <= 30):
            continue

        row = {"id": f"{sid_int:02d}"}
        any_value = False
        n_uncertain = 0
        for i, col in enumerate(HUMAN_COLS):
            val, lo_conf = parse_cell(cells[1 + i])
            row[col] = val
            row[f"{col}_uncertain"] = lo_conf
            if val is not None:
                any_value = True
            if lo_conf:
                n_uncertain += 1
        row["_n_uncertain"] = n_uncertain
        if any_value:
            out[(current_model, row["id"])] = row

    return out


def load_csv(path: Path) -> dict[tuple[str, str], dict]:
    out = {}
    with path.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out[(r["model"], r["id"])] = r
    return out


def fmt_r(r: float, p: float) -> str:
    return f"{r:.3f} (p={p:.4f})"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Parsing human_scores.md ...")
    human = parse_human_md(HUMAN_MD)
    by_model = defaultdict(int)
    n_uncertain = 0
    for (m, _), r in human.items():
        by_model[m] += 1
        n_uncertain += r["_n_uncertain"]
    print(f"  parsed {len(human)} rows across {len(by_model)} models: {dict(by_model)}")
    print(f"  total uncertain cells (flagged with [?]): {n_uncertain}")

    print("Loading auto_scores.csv (v1.0) and auto_scores_v2.csv (v2.0) ...")
    v1 = load_csv(V1_CSV)
    v2 = load_csv(V2_CSV)
    print(f"  v1: {len(v1)} rows, v2: {len(v2)} rows")

    # Build per-clip joined records: (key, h_intel, v1_intel, v2_intel, ...)
    paired = []
    skipped_no_v1 = skipped_no_v2 = skipped_no_h_intel = 0
    for key, h in human.items():
        if h.get("intel") is None:
            skipped_no_h_intel += 1
            continue
        v1r = v1.get(key)
        v2r = v2.get(key)
        if v1r is None:
            skipped_no_v1 += 1
            continue
        if v2r is None:
            skipped_no_v2 += 1
            continue
        try:
            v1_intel = int(v1r["intelligibility_1to5"])
            v2_intel = int(v2r["intelligibility_v2"])
        except (KeyError, ValueError):
            continue
        paired.append({
            "model": key[0], "id": key[1],
            "h_intel": h["intel"],
            "h_uncertain": bool(h["intel_uncertain"]),
            "v1_intel": v1_intel,
            "v2_intel": v2_intel,
            "v2_confidence": v2r.get("auto_score_confidence_v2", ""),
        })
    print(f"  matched {len(paired)} rows; skipped no_h_intel={skipped_no_h_intel}, "
          f"no_v1={skipped_no_v1}, no_v2={skipped_no_v2}")

    if len(paired) < 10:
        print("[fatal] too few paired rows for meaningful correlation")
        return 1

    h_intel = [r["h_intel"] for r in paired]
    v1_intel = [r["v1_intel"] for r in paired]
    v2_intel = [r["v2_intel"] for r in paired]

    pr1, pp1 = pearsonr(h_intel, v1_intel)
    pr2, pp2 = pearsonr(h_intel, v2_intel)
    sr1, sp1 = spearmanr(h_intel, v1_intel)
    sr2, sp2 = spearmanr(h_intel, v2_intel)
    delta = pr2 - pr1

    print(f"\nIntel: human vs v1 — Pearson r={pr1:.3f} (p={pp1:.4f}), Spearman ρ={sr1:.3f} (p={sp1:.4f})")
    print(f"Intel: human vs v2 — Pearson r={pr2:.3f} (p={pp2:.4f}), Spearman ρ={sr2:.3f} (p={sp2:.4f})")
    print(f"Δr (v2 - v1) = {delta:+.3f}")

    # Per-model breakdown
    per_model_lines = []
    for m in sorted(set(r["model"] for r in paired)):
        rs = [r for r in paired if r["model"] == m]
        if len(rs) < 5:
            per_model_lines.append((m, len(rs), None, None, None, None))
            continue
        h = [r["h_intel"] for r in rs]
        a1 = [r["v1_intel"] for r in rs]
        a2 = [r["v2_intel"] for r in rs]
        try:
            r1m, p1m = pearsonr(h, a1)
            r2m, p2m = pearsonr(h, a2)
            per_model_lines.append((m, len(rs), r1m, p1m, r2m, p2m))
        except Exception:
            per_model_lines.append((m, len(rs), None, None, None, None))

    # Per-clip disagreements: |v1 - v2| >= 2; show closeness to human
    disagreements = [r for r in paired if abs(r["v1_intel"] - r["v2_intel"]) >= 2]
    disagreements.sort(key=lambda r: -abs(r["v1_intel"] - r["v2_intel"]))

    decision = "SHIP" if pr2 >= pr1 else "HOLD"
    print(f"\n{'='*60}")
    print(f"GATE DECISION: {decision}")
    print(f"  v1 Pearson r = {pr1:.3f}")
    print(f"  v2 Pearson r = {pr2:.3f}")
    print(f"  Δr           = {delta:+.3f}")
    if decision == "SHIP":
        print("  v2 correlates with user manual ratings at least as well as v1.")
    else:
        print("  v2 REGRESSED. Investigate before locking; do not ship.")
    print(f"{'='*60}\n")

    # Write CORRELATION_REPORT.md
    md_lines = []
    md_lines.append(f"# v2.0 Correlation Report")
    md_lines.append("")
    md_lines.append(f"**Date:** 2026-05-09  ")
    md_lines.append(f"**Inputs:** `audit/human_scores.md` (manual ratings, n={len(human)}), "
                    f"`audit/auto_scores.csv` (v1.0), `audit/auto_scores_v2.csv` (v2.0).  ")
    md_lines.append(f"**Comparison axis:** intelligibility (the column with both manual and auto values).  ")
    md_lines.append(f"**n paired clips:** {len(paired)} after dropping rows with missing manual intel "
                    f"({skipped_no_h_intel} skipped) or missing auto scores ({skipped_no_v1+skipped_no_v2} skipped).")
    md_lines.append("")
    md_lines.append("## Headline")
    md_lines.append("")
    md_lines.append(f"| metric | v1.0 → human | v2.0 → human | Δ (v2 − v1) |")
    md_lines.append(f"|---|:---:|:---:|:---:|")
    md_lines.append(f"| **Pearson r** | {pr1:.3f} (p={pp1:.4f}) | **{pr2:.3f}** (p={pp2:.4f}) | **{delta:+.3f}** |")
    md_lines.append(f"| Spearman ρ | {sr1:.3f} (p={sp1:.4f}) | {sr2:.3f} (p={sp2:.4f}) | {sr2-sr1:+.3f} |")
    md_lines.append("")
    md_lines.append(f"**Decision:** {'**SHIP v2.0**' if decision == 'SHIP' else '**HOLD v2.0**'} — "
                    + ("v2.0 correlation with user manual ratings is at least as high as v1.0." if decision == "SHIP"
                       else "v2.0 correlation REGRESSED versus v1.0; do not lock without investigation."))
    md_lines.append("")
    md_lines.append("## Per-model correlation (intel)")
    md_lines.append("")
    md_lines.append("| model | n | v1 Pearson r | v2 Pearson r | Δ |")
    md_lines.append("|---|---:|:---:|:---:|:---:|")
    for m, n, r1m, p1m, r2m, p2m in per_model_lines:
        if r1m is None:
            md_lines.append(f"| {m} | {n} | (n too small) | — | — |")
        else:
            md_lines.append(f"| {m} | {n} | {r1m:.3f} (p={p1m:.4f}) | {r2m:.3f} (p={p2m:.4f}) | {r2m-r1m:+.3f} |")
    md_lines.append("")
    md_lines.append("## Cases where v2 disagrees with v1 by ≥2 ranks")
    md_lines.append("")
    if not disagreements:
        md_lines.append("*None.*")
    else:
        md_lines.append("Sorted by gap size. `closer` shows whether v1 or v2 is closer to the human rating "
                        "(distance |auto − human|; tie if equal).")
        md_lines.append("")
        md_lines.append("| model | id | human | v1 | v2 | |v1−h| | |v2−h| | closer | confidence |")
        md_lines.append("|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|")
        v2_closer = v1_closer = tied = 0
        for r in disagreements:
            d1 = abs(r["v1_intel"] - r["h_intel"])
            d2 = abs(r["v2_intel"] - r["h_intel"])
            if d1 < d2: closer = "v1"; v1_closer += 1
            elif d2 < d1: closer = "v2"; v2_closer += 1
            else: closer = "tie"; tied += 1
            md_lines.append(f"| {r['model']} | {r['id']} | {r['h_intel']} | {r['v1_intel']} | {r['v2_intel']} | "
                            f"{d1} | {d2} | **{closer}** | {r['v2_confidence']} |")
        md_lines.append("")
        md_lines.append(f"**Disagreement totals:** v2 closer to human in **{v2_closer}** cases, "
                        f"v1 closer in **{v1_closer}**, tied in **{tied}**. "
                        f"({len(disagreements)} total clips with ≥2-rank v1↔v2 disagreement.)")
    md_lines.append("")
    md_lines.append("## What changed and why")
    md_lines.append("")
    md_lines.append("v2.0 made four structural changes relative to v1.0 (full justifications in `JUDGE_PROMPT_v2.md` Changelog):")
    md_lines.append("")
    md_lines.append("1. **3-ASR consensus** (median of AAI / Deepgram / Groq intel ranks) replaces the "
                    "v1.0 single-ASR (AAI) score. Effect: more robust on threshold-boundary clips.")
    md_lines.append("2. **IndicXlit script normalization** on both reference and ASR transcript before "
                    "CER computation. Effect: `pure_roman` and `mixed_script` rows where the ASR returned "
                    "Devanagari for Roman-spoken Hindi are no longer pegged at intel=1. On the 8 human "
                    "ground-truth clips this dropped mean CER from 0.45 to 0.11.")
    md_lines.append("3. **Naturalness column emits the literal string `\"ear-only\"`** (not numeric). "
                    "Per the CEILING_REPORT, UTMOS / SQUIM_MOS / SQUIM_PESQ structurally invert direction "
                    "on Hindi audio (rate human Hindi lower than synthetic Hindi). v2.0 refuses to emit "
                    "a numeric naturalness score from those predictors.")
    md_lines.append("4. **Speaker_quality stays auto-scored from PESQ** but is annotated "
                    "synthetic-relative-only in `notes_v2`. Within-TTS rankings are still informative; "
                    "absolute numbers are not.")
    md_lines.append("")
    md_lines.append("## Caveats")
    md_lines.append("")
    md_lines.append(f"- Manual ratings come from a handwritten notebook transcribed via OCR + visual review. "
                    f"{n_uncertain} cells across all 7 columns are flagged `[?]` (low confidence). "
                    f"They're included in the correlation analysis above, but excluding them is a sensitivity "
                    f"check that hasn't been run here — flag this if the gate margin is small.")
    md_lines.append("- SPRINGLab F5-Hindi was not manually rated, so v2's improvement on that model "
                    "(if any) cannot be cross-checked against ear truth.")
    md_lines.append("- Spearman ρ (rank correlation) and Pearson r usually move together; if they diverge "
                    "substantially, the linear-fit assumption of Pearson is suspect. Cross-check both.")
    md_lines.append("- The correlation gate measures intelligibility only because that's the column where "
                    "v2.0's IndicXlit normalization most directly applies. Naturalness wasn't compared "
                    "because v2.0 doesn't emit a numeric naturalness; speaker_quality wasn't compared "
                    "because the human notebook conflates speaker_quality with intelligibility on many rows.")

    OUT_REPORT.write_text("\n".join(md_lines) + "\n")
    print(f"Wrote {OUT_REPORT.relative_to(REPO)}")
    return 0 if decision == "SHIP" else 2


if __name__ == "__main__":
    raise SystemExit(main())
