"""Smallest possible Orpheus synthesis example (vLLM path).

Run inside `tts-orpheus`:
    conda activate tts-orpheus
    python research/orpheus/inference_minimal.py
"""
from __future__ import annotations

import wave
from orpheus_tts import OrpheusModel


VOICE_BY_VARIANT = {
    "en":          ("canopylabs/orpheus-tts-0.1-finetune-prod", "tara"),
    "hi_official": ("canopylabs/3b-hi-ft-research_release", "ritu"),
    "hi_snor":     ("snorbyte/snorTTS-Indic-v0", "hindi159"),
}


def synthesize(text: str, out_path: str, variant: str = "en",
               voice: str | None = None,
               temperature: float = 0.6,
               top_p: float = 0.9,
               repetition_penalty: float = 1.1):
    repo, default_voice = VOICE_BY_VARIANT[variant]
    voice = voice or default_voice
    model = OrpheusModel(model_name=repo, max_model_len=2048)
    prompt = f"{voice}: {text}"
    with wave.open(out_path, "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(24000)
        for chunk in model.generate_speech(
            prompt=prompt, voice=voice,
            temperature=temperature, top_p=top_p,
            repetition_penalty=repetition_penalty,
        ):
            wf.writeframes(chunk)
    return out_path


if __name__ == "__main__":
    synthesize(
        "Welcome to the evaluation harness <laugh>, let's see how this sounds.",
        "orpheus_minimal_en.wav",
        variant="en",
    )
    # Hindi run — comment out if you don't have access to the gated repo
    # synthesize("नमस्ते, यह एक परीक्षण है।", "orpheus_minimal_hi.wav", variant="hi_official")
    print("Wrote orpheus_minimal_en.wav")
