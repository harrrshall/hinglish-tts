"""Smallest possible SPRINGLab F5-Hindi-24kHz synthesis example.

Run inside `tts-springlab-f5`:
    conda activate tts-springlab-f5
    python research/springlab_f5/inference_minimal.py
"""
from __future__ import annotations

from f5_tts.api import F5TTS
from huggingface_hub import hf_hub_download


REPO = "SPRINGLab/F5-Hindi-24KHz"


def load(device: str = "cuda") -> F5TTS:
    ckpt = hf_hub_download(REPO, "model_2500000.safetensors")
    vocab = hf_hub_download(REPO, "vocab.txt")
    return F5TTS(model="F5TTS_Base", ckpt_file=ckpt, vocab_file=vocab,
                 use_ema=True, device=device)


def synthesize(tts: F5TTS, ref_audio: str, ref_text: str, gen_text: str,
               out_path: str, nfe_step: int = 32, cfg_strength: float = 2.0,
               speed: float = 1.0, seed: int | None = 42):
    wav, sr, _ = tts.infer(
        ref_file=ref_audio, ref_text=ref_text, gen_text=gen_text,
        nfe_step=nfe_step, cfg_strength=cfg_strength,
        sway_sampling_coef=-1.0, speed=speed,
        cross_fade_duration=0.15, remove_silence=True,
        seed=seed, file_wave=out_path,
    )
    return out_path, sr


if __name__ == "__main__":
    tts = load()
    ref = hf_hub_download(REPO, "samples/output1.wav")
    synthesize(
        tts, ref,
        "शिवगढ़ी गाँव, एक बड़ा गाँव था",
        "नमस्ते, यह F5 हिंदी मॉडल का परीक्षण है। अनुप्रयोग ठीक काम कर रहा है।",
        "springlab_f5_minimal.wav",
    )
    print("Wrote springlab_f5_minimal.wav")
