"""Smallest possible Kokoro v1.0 synthesis example.

Run inside the `tts-kokoro` env:
    conda activate tts-kokoro
    python research/kokoro/inference_minimal.py
"""
from __future__ import annotations

import numpy as np
import soundfile as sf
from kokoro import KPipeline


def synthesize(text: str, out_path: str,
               voice: str = "af_heart",
               lang_code: str = "a",
               speed: float = 1.0) -> str:
    pipe = KPipeline(lang_code=lang_code)
    audio = np.concatenate([
        chunk for _, _, chunk in pipe(text, voice=voice, speed=speed)
    ])
    sf.write(out_path, audio, 24000)
    return out_path


if __name__ == "__main__":
    synthesize(
        "The quick brown fox jumps over the lazy dog.",
        "kokoro_minimal_en.wav",
    )
    synthesize(
        "नमस्ते, यह एक परीक्षण है।",
        "kokoro_minimal_hi.wav",
        voice="hf_alpha",
        lang_code="h",
    )
    print("Wrote kokoro_minimal_en.wav, kokoro_minimal_hi.wav")
