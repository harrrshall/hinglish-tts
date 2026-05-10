"""ASR + WER/CER for the auto-scoring pipeline — AssemblyAI Universal-2 backend.

Why AssemblyAI:
- Hindi + code-switching natively supported by Universal-2 (verified 2026-05-08)
- ~$0.02 for the full 120-clip audit (much cheaper than local-CPU GPU-time)
- No giant model downloads on flaky networks

Each clip gets transcribed THREE ways:
1. language_code="hi"  → Devanagari output for CER vs Devanagari ground truth
2. language_code="en"  → English output for the en-forced contrast (anglicization detector)
3. language_detection=True → auto-detect; we record `language_code` and
   `language_confidence` to detect when TTS anglicized Roman text

API key is read from environment variable ASSEMBLYAI_API_KEY ONLY. The key
is never written to any file or hardcoded in source. Set it before running:
    export ASSEMBLYAI_API_KEY="..."
"""
from __future__ import annotations

import functools
import os
import re
import string
import time

import assemblyai as aai
import jiwer


# ─────────────────────────────────────────────────────────────────────────────
# API key handling
# ─────────────────────────────────────────────────────────────────────────────

def _ensure_api_key() -> None:
    key = os.environ.get("ASSEMBLYAI_API_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "ASSEMBLYAI_API_KEY env var not set. "
            "Set it before running: export ASSEMBLYAI_API_KEY='...'"
        )
    aai.settings.api_key = key


# ─────────────────────────────────────────────────────────────────────────────
# Text normalization for WER/CER
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
# AssemblyAI transcription with retry
# ─────────────────────────────────────────────────────────────────────────────

@functools.lru_cache(maxsize=1)
def _transcriber():
    _ensure_api_key()
    return aai.Transcriber()


def _transcribe(wav_path: str, *, language_code: str | None = None,
                language_detection: bool = False) -> dict:
    """Submit a transcription job and wait for completion.

    Returns dict: {"text": str, "language_code": str, "language_confidence": float|None,
                   "status": "completed" or "error", "error": str | None}.
    """
    transcriber = _transcriber()
    cfg = aai.TranscriptionConfig(
        language_code=language_code,
        language_detection=language_detection,
        punctuate=True,
        format_text=True,
        speech_model=aai.SpeechModel.universal,
    )
    try:
        t = transcriber.transcribe(wav_path, config=cfg)
    except Exception as e:
        return {"text": "", "language_code": language_code or "",
                "language_confidence": None, "status": "error", "error": str(e)}
    if t.status == aai.TranscriptStatus.error:
        return {"text": "", "language_code": language_code or "",
                "language_confidence": None, "status": "error",
                "error": str(t.error)}
    return {
        "text": (t.text or "").strip(),
        "language_code": getattr(t, "language_code", None) or language_code or "",
        "language_confidence": getattr(t, "language_confidence", None),
        "status": "completed",
        "error": None,
    }


def transcribe_all(wav_path: str) -> dict:
    """Run all three transcribers (hi-forced, en-forced, auto-detect) on a wav.

    Returns:
      {transcript_hi, transcript_en_forced, transcript_roman,
       detected_lang, lang_confidence}
    where transcript_roman is the auto-detect transcript (Devanagari if model
    decided 'hi'; Latin if it decided 'en' — which is itself the anglicization
    signal).
    """
    out_hi    = _transcribe(wav_path, language_code="hi")
    out_en    = _transcribe(wav_path, language_code="en")
    out_auto  = _transcribe(wav_path, language_detection=True)
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
