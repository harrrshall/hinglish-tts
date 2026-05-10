"""Extend the canonical v2 per-ASR signal files with patched + patched_xlit entries.

Inputs (read-only):
  audit/signal_vectors_v2_{aai,deepgram,groq}.json   -- 4 baselines × 30 (already enriched)
  audit/indicf5_patched/signal_vectors_{aai,deepgram,groq}.json   -- patched-only, raw v1
  audit/indicf5_patched_xlit/signal_vectors_{aai,deepgram,groq}.json -- patched+xlit, raw v1

Outputs:
  audit/signal_vectors_v2_{aai,deepgram,groq}.json  (overwritten with 180 entries each:
    120 baselines + 30 patched + 30 patched_xlit)

Uses the canonical v2 augmentation logic from
audit/v2_build_run_2026-05-09/extract_signals_v2.py (compute_cer/wer + IndicXlit).
"""
from __future__ import annotations

import json
import string
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "audit" / "v2_build_run_2026-05-09"))

from lib_normalize import to_unified_devanagari, compute_cer, compute_wer  # canonical v2 lib

AUDIT = REPO / "audit"

BACKENDS = [
    # (raw_baseline_filename, patched_filename, patched_xlit_filename, v2_output, backend_label)
    ("signal_vectors.json",          "signal_vectors_aai.json",      "signal_vectors_aai.json",      "signal_vectors_v2_aai.json",      "aai"),
    ("signal_vectors_deepgram.json", "signal_vectors_deepgram.json", "signal_vectors_deepgram.json", "signal_vectors_v2_deepgram.json", "deepgram"),
    ("signal_vectors_groq.json",     "signal_vectors_groq.json",     "signal_vectors_groq.json",     "signal_vectors_v2_groq.json",     "groq"),
]

_PUNCT = set(string.punctuation) | {"।", "॥", "–", "—", "…", "‘", "’", "“", "”"}


def _strip_punct(s: str) -> str:
    if not s:
        return ""
    return " ".join("".join(c if c not in _PUNCT else " " for c in s).split())


def augment_entry(entry: dict, backend: str, ref_cache: dict[str, str]) -> dict:
    ref_text   = entry.get("text", "") or ""
    transcript = entry.get("transcript_hi") or entry.get("transcript_roman") or ""
    if ref_text in ref_cache:
        ref_unified = ref_cache[ref_text]
    else:
        ref_unified = to_unified_devanagari(ref_text)
        ref_cache[ref_text] = ref_unified
    hyp_unified = to_unified_devanagari(transcript)
    rfm = _strip_punct(ref_unified)
    hfm = _strip_punct(hyp_unified)
    out = dict(entry)
    out["ref_unified"]         = ref_unified
    out["transcript_unified"]  = hyp_unified
    out["cer_unified"]         = round(compute_cer(rfm, hfm), 4)
    out["wer_unified"]         = round(compute_wer(rfm, hfm), 4)
    out["asr_backend"]         = backend
    return out


def main() -> int:
    ref_cache: dict[str, str] = {}
    t0 = time.time()
    for raw_baseline, patched_name, xlit_name, v2_out, backend in BACKENDS:
        # Load existing v2 baseline file (already enriched)
        v2_path = AUDIT / v2_out
        if not v2_path.exists():
            print(f"[fatal] {v2_path} missing — run canonical v2 build first", file=sys.stderr)
            return 1
        existing = json.loads(v2_path.read_text())
        baseline_models = sorted({e["model"] for e in existing})
        print(f"\n=== {backend} ===  existing v2 file has {len(existing)} entries from models {baseline_models}")

        # Drop any stale patched/patched_xlit entries from prior runs of this script
        existing = [e for e in existing if e["model"] not in {"indicf5_patched", "indicf5_patched_xlit"}]
        print(f"  after dropping stale patched: {len(existing)} baseline entries")

        # Load + enrich patched
        patched_path = AUDIT / "indicf5_patched" / patched_name
        patched_raw = json.loads(patched_path.read_text())
        for e in patched_raw:
            existing.append(augment_entry(e, backend, ref_cache))
        print(f"  + {len(patched_raw)} indicf5_patched entries from {patched_path.name}")

        # Load + enrich patched_xlit
        xlit_path = AUDIT / "indicf5_patched_xlit" / xlit_name
        if not xlit_path.exists():
            print(f"  [warn] {xlit_path} missing — skipping patched_xlit for {backend}")
        else:
            xlit_raw = json.loads(xlit_path.read_text())
            for e in xlit_raw:
                existing.append(augment_entry(e, backend, ref_cache))
            print(f"  + {len(xlit_raw)} indicf5_patched_xlit entries from {xlit_path.name}")

        v2_path.write_text(json.dumps(existing, ensure_ascii=False, indent=1))
        print(f"  wrote {v2_path.name}: {len(existing)} entries")

    # Per-(model, backend) v2 CER summary
    from collections import defaultdict
    print("\n=== v2 CER (per-model × per-backend) ===")
    print(f"{'model':<25} {'backend':<10} {'mean v2_CER':>12}")
    for _, _, _, v2_out, backend in BACKENDS:
        data = json.loads((AUDIT / v2_out).read_text())
        by_model: dict[str, list] = defaultdict(list)
        for r in data:
            by_model[r["model"]].append(r)
        for m in sorted(by_model.keys()):
            rs = by_model[m]
            v2 = sum(float(r["cer_unified"]) for r in rs) / len(rs)
            print(f"  {m:<23} {backend:<10} {v2:>12.3f}")

    print(f"\nTotal: {time.time()-t0:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
