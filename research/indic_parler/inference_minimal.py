"""Smallest possible Indic Parler-TTS synthesis example.

Run inside `tts-indic-parler`:
    conda activate tts-indic-parler
    python research/indic_parler/inference_minimal.py
"""
from __future__ import annotations

import torch
import soundfile as sf
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer


MODEL_ID = "ai4bharat/indic-parler-tts"


def load():
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device.startswith("cuda") else torch.float32
    model = ParlerTTSForConditionalGeneration.from_pretrained(
        MODEL_ID, torch_dtype=dtype
    ).to(device)
    prompt_tok = AutoTokenizer.from_pretrained(MODEL_ID)
    desc_tok = AutoTokenizer.from_pretrained(model.config.text_encoder._name_or_path)
    return model, prompt_tok, desc_tok, device


def synthesize(model, prompt_tok, desc_tok, device, transcript, description, out_path, seed=None):
    if seed is not None:
        torch.manual_seed(seed)
    d = desc_tok(description, return_tensors="pt").to(device)
    t = prompt_tok(transcript, return_tensors="pt").to(device)
    with torch.inference_mode():
        gen = model.generate(
            input_ids=d.input_ids,
            attention_mask=d.attention_mask,
            prompt_input_ids=t.input_ids,
            prompt_attention_mask=t.attention_mask,
            do_sample=True,
            temperature=1.0,
            repetition_penalty=1.1,
        )
    audio = gen.cpu().to(torch.float32).numpy().squeeze()
    sf.write(out_path, audio, model.config.sampling_rate)
    return out_path, model.config.sampling_rate


if __name__ == "__main__":
    m, ptok, dtok, dev = load()
    synthesize(
        m, ptok, dtok, dev,
        "The quick brown fox jumps over the lazy dog.",
        "Rohit speaks at a moderate pace with a clear neutral Indian English accent. The recording is very clear and close up.",
        "indic_parler_minimal_en.wav",
    )
    synthesize(
        m, ptok, dtok, dev,
        "नमस्ते, यह एक परीक्षण है।",
        "A female speaker delivers Hindi speech at a moderate pace with a clear voice. The recording is very clear and close up.",
        "indic_parler_minimal_hi.wav",
    )
    print("Wrote indic_parler_minimal_en.wav, indic_parler_minimal_hi.wav")
