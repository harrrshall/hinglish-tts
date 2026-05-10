"""Stage-1 v2.0: enrich existing signal vectors with normalized CER/WER.

Reads (read-only):
  audit/signal_vectors.json                              -- 4 baseline models × 30
  audit/indicf5_patched/signal_vectors_aai.json          -- patched IndicF5, AAI
  audit/indicf5_patched/signal_vectors_deepgram.json     -- patched IndicF5, Deepgram
  audit/indicf5_patched/signal_vectors_groq.json         -- patched IndicF5, Groq

Writes:
  audit/signal_vectors_v2.json                           -- 210 entries (120 baseline + 30×3 patched)

Each entry preserves all v1.0 fields and adds:
  text_normalized, transcript_hi_normalized, transcript_roman_normalized,
  cer_devanagari_norm, wer_roman_norm, asr_backend, silence_or_skip_norm.

This script does NOT call any ASR API. It reuses Stage-1 outputs and computes
v2-specific normalization fields locally.

Run: python audit/scripts/extract_signals_v2.py
"""
from __future__ import annotations

import json
import os
import re
import string
import sys
from pathlib import Path

# Make sibling modules importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import jiwer
from lib_normalize import to_unified_devanagari


REPO = Path(__file__).resolve().parents[2]
AUDIT = REPO / "audit"
OUT = AUDIT / "signal_vectors_v2.json"

BASELINE = AUDIT / "signal_vectors.json"
PATCHED_AAI = AUDIT / "indicf5_patched" / "signal_vectors_aai.json"
PATCHED_DG  = AUDIT / "indicf5_patched" / "signal_vectors_deepgram.json"
PATCHED_GROQ= AUDIT / "indicf5_patched" / "signal_vectors_groq.json"

_PUNCT = string.punctuation + "।॥,।'\"‍‌"


def _strip_punct(text: str) -> str:
    """Punctuation strip + collapse whitespace. Used for CER/WER post-normalization."""
    if not text:
        return ""
    out = "".join(" " if ch in _PUNCT else ch for ch in text)
    return re.sub(r"\s+", " ", out).strip()


def _cer_norm(ref_norm: str, hyp_norm: str) -> float:
    """CER on normalized + punct-stripped strings."""
    ref = _strip_punct(ref_norm)
    hyp = _strip_punct(hyp_norm)
    if not ref:
        return 1.0
    return float(jiwer.cer(ref, hyp))


def _wer_norm(ref_norm: str, hyp_norm: str) -> float:
    """WER on whitespace-tokenized normalized strings."""
    ref = _strip_punct(ref_norm)
    hyp = _strip_punct(hyp_norm)
    if not ref:
        return 1.0
    return float(jiwer.wer(ref, hyp))


def _token_overlap(ref_norm: str, hyp_norm: str) -> float:
    """Set-overlap of whitespace tokens, dropping single-char tokens (punctuation artifacts)."""
    ref_toks = {t for t in _strip_punct(ref_norm).split() if len(t) > 1}
    hyp_toks = {t for t in _strip_punct(hyp_norm).split() if len(t) > 1}
    if not ref_toks:
        return 1.0
    return len(ref_toks & hyp_toks) / len(ref_toks)


def enrich(entry: dict, asr_backend: str) -> dict:
    """Add v2.0 normalized fields to an existing v1 signal vector."""
    text = entry.get("text", "") or ""
    th = entry.get("transcript_hi", "") or ""
    tr = entry.get("transcript_roman", "") or ""

    text_norm = to_unified_devanagari(text)
    th_norm = to_unified_devanagari(th)
    tr_norm = to_unified_devanagari(tr)

    silence_mid = float(entry.get("silence_mid_clip_s", 0.0))
    overlap = _token_overlap(text_norm, th_norm)
    # v2 silence_or_skip: silence_mid > 0.5 ONLY. The "missing >20% of words" half from v1 was
    # designed to catch Mode A truncation (short clips with empty/garbled transcripts). Now that
    # the duration patch eliminates Mode A and v2 rubric scores Mode C garbling via CER_norm,
    # the token-overlap heuristic over-triggers on legitimate ASR spelling variance
    # ("बेंगलुरु" vs "बेंगलारू", "लीव" vs "लीफ"). Drop it; intel column captures content fidelity.
    skip_norm = silence_mid > 0.5

    out = dict(entry)  # preserve all original fields
    out.update({
        "text_normalized": text_norm,
        "transcript_hi_normalized": th_norm,
        "transcript_roman_normalized": tr_norm,
        "cer_devanagari_norm": round(_cer_norm(text_norm, th_norm), 4),
        "wer_roman_norm": round(_wer_norm(text_norm, tr_norm), 4),
        "asr_backend": asr_backend,
        "silence_or_skip_norm": skip_norm,
        "_token_overlap_norm": round(overlap, 4),
    })
    return out


def main() -> int:
    print(f"Loading {BASELINE} ...")
    baseline = json.loads(BASELINE.read_text())
    print(f"  {len(baseline)} baseline entries")

    print(f"Loading patched IndicF5 (3 ASRs) ...")
    patched_aai = json.loads(PATCHED_AAI.read_text())
    patched_dg  = json.loads(PATCHED_DG.read_text())
    patched_groq= json.loads(PATCHED_GROQ.read_text())
    print(f"  AAI: {len(patched_aai)}, DG: {len(patched_dg)}, Groq: {len(patched_groq)}")

    out = []
    for entry in baseline:
        out.append(enrich(entry, "aai"))  # v1 baseline used AAI
    for entry in patched_aai:
        e = dict(entry)
        e["model"] = "indicf5_patched"  # was "indicf5_patched" already
        out.append(enrich(e, "aai"))
    for entry in patched_dg:
        e = dict(entry)
        e["model"] = "indicf5_patched"
        out.append(enrich(e, "deepgram"))
    for entry in patched_groq:
        e = dict(entry)
        e["model"] = "indicf5_patched"
        out.append(enrich(e, "groq"))

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(f"\nWrote {OUT} — {len(out)} entries")

    # Per-model summary
    from collections import defaultdict
    by_model = defaultdict(list)
    for e in out:
        by_model[(e["model"], e.get("asr_backend"))].append(e)
    print("\n=== Mean CER (v1 raw → v2 normalized) per (model, ASR) ===")
    for (m, asr), rows in sorted(by_model.items()):
        v1_cer = sum(float(r["cer_devanagari"]) for r in rows) / len(rows)
        v2_cer = sum(float(r["cer_devanagari_norm"]) for r in rows) / len(rows)
        skip_n = sum(1 for r in rows if r["silence_or_skip_norm"])
        print(f"  {m:18s} {asr:10s}  v1_CER={v1_cer:.3f}  v2_CER={v2_cer:.3f}  Δ={v2_cer-v1_cer:+.3f}  skip={skip_n}/{len(rows)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
