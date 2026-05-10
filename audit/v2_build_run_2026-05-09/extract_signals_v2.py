"""Stage-1 v2.0: enrich the three baseline signal vectors with unified-Devanagari
fields. NO ASR re-run.

Per the v2.0 build spec:
  - 3 separate output files (one per ASR backend)
  - baseline 4 models × 30 sentences only (do NOT include patched IndicF5;
    that's scored as a separate downstream task once v2.0 ships)
  - 4 new fields per entry: ref_unified, transcript_unified, cer_unified, wer_unified
  - all v1.0 fields preserved unchanged for backward compat / debugging

Reads:
  audit/signal_vectors.json
  audit/signal_vectors_deepgram.json
  audit/signal_vectors_groq.json

Writes:
  audit/signal_vectors_v2_aai.json        (120 entries)
  audit/signal_vectors_v2_deepgram.json   (120 entries)
  audit/signal_vectors_v2_groq.json       (120 entries)
"""
from __future__ import annotations

import json
import string
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "audit" / "scripts"))

from lib_normalize import to_unified_devanagari, compute_cer, compute_wer

AUDIT = REPO / "audit"
BACKENDS = [
    ("signal_vectors.json",          "signal_vectors_v2_aai.json",      "aai"),
    ("signal_vectors_deepgram.json", "signal_vectors_v2_deepgram.json", "deepgram"),
    ("signal_vectors_groq.json",     "signal_vectors_v2_groq.json",     "groq"),
]

# Strip punctuation before CER/WER so e.g. comma-vs-Devanagari-danda doesn't
# inflate distance. Both English and Devanagari sentence-end marks included.
_PUNCT = set(string.punctuation) | {"।", "॥", "–", "—", "…", "‘", "’", "“", "”"}


def _strip_punct(s: str) -> str:
    if not s:
        return ""
    return " ".join("".join(c if c not in _PUNCT else " " for c in s).split())


def augment(in_path: Path, out_path: Path, backend: str) -> int:
    data = json.loads(in_path.read_text())
    n = len(data)
    print(f"  loaded {n} entries from {in_path.name}")

    t0 = time.time()
    # Cache transliterations: ref text repeats across the 4 models for the same
    # sentence id, so caching reduces IndicXlit calls by ~75%.
    ref_cache: dict[str, str] = {}

    for i, entry in enumerate(data):
        ref_text = entry.get("text", "") or ""
        # Use transcript_hi as primary (matches v1.0 rubric mapping for
        # Devanagari-leaning rows); fall back to transcript_roman if hi is empty.
        transcript = entry.get("transcript_hi") or entry.get("transcript_roman") or ""

        if ref_text in ref_cache:
            ref_unified = ref_cache[ref_text]
        else:
            ref_unified = to_unified_devanagari(ref_text)
            ref_cache[ref_text] = ref_unified

        hyp_unified = to_unified_devanagari(transcript)

        ref_for_metric = _strip_punct(ref_unified)
        hyp_for_metric = _strip_punct(hyp_unified)

        entry["ref_unified"] = ref_unified
        entry["transcript_unified"] = hyp_unified
        entry["cer_unified"] = round(compute_cer(ref_for_metric, hyp_for_metric), 4)
        entry["wer_unified"] = round(compute_wer(ref_for_metric, hyp_for_metric), 4)
        entry["asr_backend"] = backend

        if (i + 1) % 30 == 0 or i + 1 == n:
            print(f"    [{i+1:3d}/{n}]  elapsed {time.time()-t0:.1f}s  "
                  f"({len(ref_cache)} unique refs cached)", flush=True)

    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=1))
    print(f"  wrote {out_path.name} ({n} entries) in {time.time()-t0:.1f}s\n")
    return n


def main() -> int:
    print("=== Augmenting v1.0 signal vectors with unified-Devanagari fields ===")
    print(f"    (caching transliterations; punctuation stripped before CER/WER)\n")
    t_total = time.time()
    for in_name, out_name, backend in BACKENDS:
        in_path = AUDIT / in_name
        out_path = AUDIT / out_name
        if not in_path.exists():
            print(f"[fatal] {in_path} missing", file=sys.stderr)
            return 1
        augment(in_path, out_path, backend)

    # Cross-backend alignment + v1→v2 CER summary
    from collections import defaultdict
    print("=== Per-(model,backend) v1→v2 CER means ===")
    print(f"{'model':<16} {'backend':<10} {'v1_CER':>7} {'v2_CER':>7} {'Δ':>7}")
    for in_name, out_name, backend in BACKENDS:
        data = json.loads((AUDIT / out_name).read_text())
        by_model: dict[str, list] = defaultdict(list)
        for r in data:
            by_model[r["model"]].append(r)
        for m in sorted(by_model.keys()):
            rs = by_model[m]
            v1 = sum(float(r["cer_devanagari"]) for r in rs) / len(rs)
            v2 = sum(float(r["cer_unified"]) for r in rs) / len(rs)
            print(f"  {m:<14} {backend:<10} {v1:>7.3f} {v2:>7.3f} {v2-v1:>+7.3f}")
    print(f"\nTotal: {time.time()-t_total:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
