"""ASR + WER/CER for the auto-scoring pipeline — Groq Whisper-large-v3 backend.

Drop-in replacement for lib_asr.py / lib_asr_deepgram.py. Same `transcribe_all()`
shape so extract_signals_groq.py can swap the import without changing the schema.

Why Groq:
- Hosts OpenAI Whisper-large-v3 (the SOTA general-purpose ASR) at very high speed
- Free tier: 2,000 req/day, 7,200 audio-seconds/hour, 30 RPM
- 100% open-weight upstream model — reproducible, no proprietary tokenizer
- Whisper is the de-facto reference ASR for cross-lab comparison

Each clip gets transcribed THREE ways:
1. model=whisper-large-v3, language="hi"   → Devanagari output for CER
2. model=whisper-large-v3, language="en"   → English-forced (anglicization detector)
3. model=whisper-large-v3, language=None   → Auto-detect (Whisper picks the language)

Free-tier throughput note:
  30 RPM cap → upstream caller should use ≤3 parallel workers to avoid 429s.
  We retry on 429 with exponential backoff.

API key is read from environment variable GROQ_API_KEY ONLY. The key is
never written to any file or hardcoded in source. Set it before running:
    export GROQ_API_KEY="..."
"""
from __future__ import annotations

import functools
import os
import re
import string
import time

import jiwer
from groq import Groq


# ─────────────────────────────────────────────────────────────────────────────
# API key handling
# ─────────────────────────────────────────────────────────────────────────────

def _ensure_api_key() -> None:
    key = os.environ.get("GROQ_API_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "GROQ_API_KEY env var not set. "
            "Set it before running: export GROQ_API_KEY='...'"
        )


# ─────────────────────────────────────────────────────────────────────────────
# Text normalization for WER/CER (identical to other backends for fairness)
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
# Groq transcription with retry + 429 backoff
# ─────────────────────────────────────────────────────────────────────────────

@functools.lru_cache(maxsize=1)
def _client():
    _ensure_api_key()
    # Groq() reads GROQ_API_KEY from env automatically
    return Groq()


def _transcribe(wav_path: str, *, language: str | None = None,
                max_retries: int = 5) -> dict:
    """Submit a transcription job and wait for completion.

    Args:
        wav_path: absolute path to a wav file
        language: ISO-639-1 ("hi", "en") or None for Whisper's auto-detect
        max_retries: retry count; 429 (rate-limited) gets longer backoff

    Returns dict: {"text", "language_code", "language_confidence",
                   "status", "error"}.
    """
    client = _client()

    last_err = None
    for attempt in range(max_retries):
        try:
            with open(wav_path, "rb") as f:
                kwargs = dict(
                    file=(os.path.basename(wav_path), f.read()),
                    model="whisper-large-v3",
                    response_format="verbose_json",
                    temperature=0.0,
                )
                if language:
                    kwargs["language"] = language
                resp = client.audio.transcriptions.create(**kwargs)

            # verbose_json returns: text, language, duration, segments, words
            text = getattr(resp, "text", "") or ""
            detected = getattr(resp, "language", "") or (language or "")
            return {
                "text": text.strip(),
                "language_code": detected,
                "language_confidence": None,  # Whisper doesn't expose confidence
                "status": "completed",
                "error": None,
            }
        except Exception as e:
            last_err = e
            msg = str(e).lower()
            # 429 → longer backoff (free tier is 30 RPM → wait ~3-5s)
            if "429" in msg or "rate" in msg or "too many" in msg:
                wait = 3 * (2 ** attempt)  # 3, 6, 12, 24, 48s
            else:
                wait = 1 * (2 ** attempt)  # 1, 2, 4, 8, 16s
            time.sleep(wait)
            continue

    return {
        "text": "", "language_code": language or "",
        "language_confidence": None,
        "status": "error", "error": str(last_err),
    }


def transcribe_all(wav_path: str) -> dict:
    """Run all three transcribers (hi-forced, en-forced, auto-detect) on a wav.

    Returns the same dict shape as lib_asr.transcribe_all() / lib_asr_deepgram
    for drop-in compatibility with extract_signals.py.
    """
    out_hi    = _transcribe(wav_path, language="hi")
    out_en    = _transcribe(wav_path, language="en")
    out_auto  = _transcribe(wav_path, language=None)
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
    print(f"  CER (auto-detect vs gt):  {cer(gt, out['transcript_roman']):.3f}")
