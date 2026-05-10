#!/usr/bin/env python3
"""Build audit/HANDOFF.md per AUDIT_PLAN.md §7.

Reads each model's log.json + RUN_NOTES.md and emits the hand-off message.
Run after `verify.py` passes and after the audit zip has been built.
"""
from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
ROOT = REPO / "audit"

MODELS = ["kokoro", "indicf5", "indic_parler", "springlab_f5", "orpheus_hi"]


def _success_counts() -> dict[str, tuple[int, int]]:
    out = {}
    for m in MODELS:
        log = ROOT / "results" / m / "log.json"
        if not log.exists():
            out[m] = (0, 30); continue
        rows = json.loads(log.read_text())
        n_ok = sum(1 for r in rows if r.get("status") == "ok")
        out[m] = (n_ok, len(rows) or 30)
    return out


def _gotchas(top_n: int = 3) -> list[str]:
    notes = ROOT / "RUN_NOTES.md"
    if not notes.exists():
        return []
    text = notes.read_text(encoding="utf-8")
    # Extract bullets under the "Install gotchas" / "Per-model deviations" sections.
    sections = re.split(r"\n## ", text)
    bullets: list[str] = []
    for s in sections:
        if s.startswith("Install gotchas") or s.startswith("Per-model deviations"):
            for line in s.splitlines():
                m = re.match(r"^- (.+)$", line.strip())
                if m and "(one bullet" not in m.group(1):
                    bullets.append(m.group(1))
    return bullets[:top_n]


def main() -> int:
    sc = _success_counts()
    total_ok = sum(v[0] for v in sc.values())
    total = sum(v[1] for v in sc.values()) or 150

    lines: list[str] = []
    lines.append(f"# Audit Phase 1 — Handoff ({dt.date.today().isoformat()})")
    lines.append("")
    lines.append(f"**Audit complete. {total_ok}/{total} audio files generated across 5 models on 30 Hinglish sentences.**")
    lines.append("")
    lines.append("## Per-model success counts")
    lines.append("")
    lines.append("| Model | Success | Total |")
    lines.append("|-------|--------:|------:|")
    for m, (ok, n) in sc.items():
        lines.append(f"| {m} | {ok} | {n} |")
    lines.append("")

    g = _gotchas()
    if g:
        lines.append("## Top gotchas (from RUN_NOTES.md)")
        lines.append("")
        for b in g:
            lines.append(f"- {b}")
        lines.append("")

    lines.append("## Agent observations (factual, not subjective)")
    lines.append("")
    for m, (ok, n) in sc.items():
        log = ROOT / "results" / m / "log.json"
        if not log.exists():
            continue
        rows = json.loads(log.read_text())
        errs = [r for r in rows if r.get("status") != "ok"]
        if errs:
            cats = {}
            for r in errs:
                cats[r.get("category", "?")] = cats.get(r.get("category", "?"), 0) + 1
            lines.append(f"- **{m}**: {len(errs)} failures by category: " +
                         ", ".join(f"{c}={k}" for c, k in sorted(cats.items())))
    lines.append("")

    lines.append("## Artifact")
    lines.append("")
    lines.append(f"- Direct path: `audit_phase1_{dt.date.today().strftime('%Y%m%d')}.zip`")
    lines.append("")
    lines.append("Next: human listens to all 150 clips, fills `scoring_template.csv`, returns it for Phase 2.")

    out = ROOT / "HANDOFF.md"
    out.write_text("\n".join(lines))
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
