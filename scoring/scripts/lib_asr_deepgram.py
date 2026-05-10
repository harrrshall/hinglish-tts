"""ASR + WER/CER for the auto-scoring pipeline — Deepgram Nova-3 backend.

Drop-in replacement for lib_asr.py (AssemblyAI). Same `transcribe_all()` shape
so extract_signals_deepgram.py can swap the import without changing the schema.

Why Deepgram (vs AssemblyAI):
- Nova-3 has 27% WER reduction over Nova-2 on Hindi (per Deepgram blog 2026)
- `language="multi"` natively handles Hinglish code-switching at utterance level
- 50 concurrent pre-recorded requests (10x our 5-worker headroom)
- $0.0043/min pre-recorded ≈ ~$0.13 for our 120-clip × 3-pass run
- Known caveat (deepgram/discussions/1208): Nova-3 multi sometimes
  misidentifies Hindi as Spanish on Hindi-English code-switched audio.
  Mitigation: we still force-decode lang=hi separately for CER, and
  language=multi is only used for the "auto/roman" channel.

Each clip gets transcribed THREE ways:
1. model=nova-3, language=hi    → Devanagari output for CER vs Devanagari ground truth
2. model=nova-3, language=en    → English output for the en-forced contrast
3. model=nova-3, language=multi → Multilingual code-switching transcript

API key is read from environment variable DEEPGRAM_API_KEY ONLY. The key is
never written to any file or hardcoded in source. Set it before running:
    export DEEPGRAM_API_KEY="..."
"""
from __future__ import annotations

import functools
import os
import re
import string
import time

import jiwer
from deepgram import DeepgramClient


# ─────────────────────────────────────────────────────────────────────────────
# API key handling
# ─────────────────────────────────────────────────────────────────────────────

def _ensure_api_key() -> None:
    key = os.environ.get("DEEPGRAM_API_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "DEEPGRAM_API_KEY env var not set. "
            "Set it before running: export DEEPGRAM_API_KEY='...'"
        )


# ─────────────────────────────────────────────────────────────────────────────
# Text normalization for WER/CER (identical to AssemblyAI variant for fairness)
# ─────────────────────────────────────────────────────────────────────────────

_PUNCT = string.punctuation + "।॥,।'\"‍‌"  # incl. Devanagari danda + ZWJ/ZWNJ


def normalize_for_compare(text: str, *, lowercase: bool = True) -> str:
    """Strip punctuation, collapse whitespace, optionally lowercase. Preserves Devanagari."""
    if text is None:
        return ""
    text = "".join(" " if ch in _PUNCT else ch for ch in text)
    text = re.sub(r"\s+", " ", text).strip()
    if lowercase:
        text = text.lower()
    return text


def wer(reference: str, hypothesis: str) -> float:
    ref = normalize_for_compare(reference)
    hyp = normalize_for_compare(hypothesis)
    if not ref:
        return 1.0
    return float(jiwer.wer(ref, hyp))


def cer(reference: str, hypothesis: str) -> float:
    ref = normalize_for_compare(reference)
    hyp = normalize_for_compare(hypothesis)
    if not ref:
        return 1.0
    return float(jiwer.cer(ref, hyp))


# ─────────────────────────────────────────────────────────────────────────────
# Deepgram transcription with retry
# ─────────────────────────────────────────────────────────────────────────────

@functools.lru_cache(maxsize=1)
def _client():
    _ensure_api_key()
    # DeepgramClient() reads DEEPGRAM_API_KEY from env automatically
    return DeepgramClient()


def _extract_text_and_lang(response) -> tuple[str, str, float | None]:
    """Pull the top alternative transcript + detected language from a Deepgram response.

    The response object from SDK v7 exposes nested results; we navigate defensively
    and tolerate both attribute and dict access. Returns (text, detected_lang, confidence).
    """
    try:
        results = getattr(response, "results", None) or response.get("results")
    except Exception:
        results = None
    if results is None:
        return "", "", None

    channels = getattr(results, "channels", None)
    if channels is None and isinstance(results, dict):
        channels = results.get("channels")
    if not channels:
        return "", "", None

    ch0 = channels[0]
    alts = getattr(ch0, "alternatives", None)
    if alts is None and isinstance(ch0, dict):
        alts = ch0.get("alternatives")
    if not alts:
        return "", "", None

    alt0 = alts[0]
    text = getattr(alt0, "transcript", None)
    if text is None and isinstance(alt0, dict):
        text = alt0.get("transcript", "")

    # detected_language lives on the channel for multilingual responses
    lang = getattr(ch0, "detected_language", None)
    if lang is None and isinstance(ch0, dict):
        lang = ch0.get("detected_language", "")

    conf = getattr(alt0, "confidence", None)
    if conf is None and isinstance(alt0, dict):
        conf = alt0.get("confidence", None)

    return (text or "").strip(), (lang or ""), conf


def _transcribe(wav_path: str, *, language: str = "multi",
                max_retries: int = 3) -> dict:
    """Submit a transcription job and wait for completion.

    Args:
        wav_path: absolute path to a wav file
        language: Deepgram language code: "hi" | "en" | "multi"
        max_retries: retry count on transient failures (429, network)

    Returns dict: {"text", "language_code", "language_confidence",
                   "status", "error"}.
    """
    client = _client()
    payload_kwargs = {
        "model": "nova-3",
        "language": language,
        "smart_format": True,
        "punctuate": True,
    }

    last_err = None
    for attempt in range(max_retries):
        try:
            with open(wav_path, "rb") as f:
                buffer_data = f.read()
            response = client.listen.v1.media.transcribe_file(
                request=buffer_data,
                **payload_kwargs,
            )
            text, detected_lang, conf = _extract_text_and_lang(response)
            return {
                "text": text,
                "language_code": detected_lang or language,
                "language_confidence": conf,
                "status": "completed",
                "error": None,
            }
        except Exception as e:
            last_err = e
            # Linear backoff: 1s, 2s, 4s
            time.sleep(2 ** attempt)
            continue

    return {
        "text": "", "language_code": language,
        "language_confidence": None,
        "status": "error", "error": str(last_err),
    }


def transcribe_all(wav_path: str) -> dict:
    """Run all three transcribers (hi-forced, en-forced, multi) on a wav.

    Returns the same dict shape as lib_asr.transcribe_all() for drop-in
    compatibility with extract_signals.py.
    """
    out_hi    = _transcribe(wav_path, language="hi")
    out_en    = _transcribe(wav_path, language="en")
    out_auto  = _transcribe(wav_path, language="multi")
    return {
        "transcript_hi":         out_hi["text"],
        "transcript_en_forced":  out_en["text"],
        "transcript_roman":      out_auto["text"],
        "detected_lang":         out_auto.get("language_code", ""),
        "lang_confidence":       out_auto.get("language_confidence"),
        "_status_hi":            out_hi["status"],
        "_status_en":            out_en["status"],
        "_status_auto":          out_auto["status"],
    }


if __name__ == "__main__":
    # Smoke-test on kokoro/01.wav (known ground truth)
    from pathlib import Path
    wav = Path("/home/cybernovas/Desktop/hienglish/audit/results/kokoro/01.wav")
    gt  = "कल मुझे दिल्ली जाना है।"

    t0 = time.time()
    out = transcribe_all(str(wav))
    print(f"\nTranscribed in {time.time()-t0:.1f}s")
    print(f"Ground truth: {gt}")
    for k, v in out.items():
        print(f"  {k:24s} {v!r}")
    print()
    print(f"  CER (hi vs gt):           {cer(gt, out['transcript_hi']):.3f}")
    print(f"  WER (en-forced vs gt):    {wer(gt, out['transcript_en_forced']):.3f}")
    print(f"  CER (multi vs gt):        {cer(gt, out['transcript_roman']):.3f}")
