"""Smallest possible IndicF5 synthesis example.

Run inside `tts-indicf5`:
    conda activate tts-indicf5
    python research/indicf5/inference_minimal.py
"""
from __future__ import annotations

import numpy as np
import soundfile as sf
import torch
from transformers import AutoModel


def load(device: str | None = None):
    device = device or ("cuda" if torch.cuda.is_available() else "cpu")
    model = AutoModel.from_pretrained(
        "ai4bharat/IndicF5", trust_remote_code=True
    ).to(device).eval()
    return model


def synthesize(model, gen_text: str, ref_audio: str, ref_text: str, out_path: str):
    audio = model(gen_text, ref_audio_path=ref_audio, ref_text=ref_text)
    if audio.dtype == np.int16:
        audio = audio.astype(np.float32) / 32768.0
    audio = np.asarray(audio, dtype=np.float32).squeeze()
    sf.write(out_path, audio, 24000)
    return out_path


if __name__ == "__main__":
    m = load()
    synthesize(
        m,
        "नमस्ते, यह IndicF5 का परीक्षण है।",
        "research/indicf5/reference_audio/PAN_F_HAPPY_00001.wav",
        "ਭਹੰਪੀ ਵਿੱਚ ਸਮਾਰਕਾਂ ਦੇ ਭਵਨ ਅਤੇ ਮੰਦਰ ਹਨ।",
        "indicf5_minimal.wav",
    )
    print("Wrote indicf5_minimal.wav")
