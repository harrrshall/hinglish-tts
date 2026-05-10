# Indic Parler-TTS — Research

## Identity & links

- **Canonical checkpoint** (use this): [`ai4bharat/indic-parler-tts`](https://huggingface.co/ai4bharat/indic-parler-tts) (~0.9 B params, SFT)
- **Pretrained variant**: [`ai4bharat/indic-parler-tts-pretrained`](https://huggingface.co/ai4bharat/indic-parler-tts-pretrained) (base, before SFT)
- **HF collection**: https://huggingface.co/collections/ai4bharat/indic-parler-tts
- **Upstream library**: https://github.com/huggingface/parler-tts (no AI4Bharat fork — use upstream)
- **Project page**: https://ai4bharat.iitm.ac.in/areas/model/TTS/Indic%20Parler%20TTS
- **Paper**: Sankar et al., *Rasmalai*, **Interspeech 2025**.
- **License**: **Apache 2.0**.

## Architecture

- AR text-to-codec transformer: Flan-T5 encoder for the *description*, separate prompt encoder for the *transcript*, codec decoder predicts DAC tokens.
- Audio codec: **Descript Audio Codec (DAC) at 44.1 kHz**, 9 codebooks RVQ.
- ~0.9 B parameters.
- Training data: 1,806 h across GLOBE (en, 535 h), IndicTTS (382 h, 12 langs), LIMMITS (568 h, 7 langs), Rasa (288 h, 9 langs).
- 69 named voices across supported languages (e.g. Rohit, Divya, Leela, Maya, Aditi, Sita).
- Output: 44 100 Hz mono.

## Installation

```bash
pip install --upgrade pip
pip install git+https://github.com/huggingface/parler-tts.git
pip install "transformers>=4.46,<4.50" "torch>=2.1" soundfile sentencepiece accelerate descript-audio-codec
```

Use a CUDA-matched torch wheel (https://pytorch.org) for GPU.

## Languages

**Officially supported (21)**: Assamese, Bengali, Bodo, Dogri, English, Gujarati, **Hindi**, Kannada, Konkani, Maithili, Malayalam, Manipuri, Marathi, Nepali, Odia, Sanskrit, Santali, Sindhi, Tamil, Telugu, Urdu.

**Unofficial (lower quality)**: Chhattisgarhi, Kashmiri, Punjabi.

**Emotion-tagged subset (10)**: Assamese, Bengali, Bodo, Dogri, Kannada, Malayalam, Marathi, Sanskrit, Nepali, Tamil. (Hindi NOT in the emotion-tagged subset.)

**Hinglish / code-switching**: not a first-class trained mode. Works informally if Hinglish is written in **Latin script** with an English-accent description. Brittle and inconsistent — this is a key thing our eval should expose.

## The "description" prompt

Style is conditioned on a free-form natural-language **caption**. Best results
mention: named speaker (recommended for reproducibility), gender, pitch,
speaking rate, expressivity, recording quality, accent/language.

**Templates that work well**:

```
"Rohit speaks at a moderate pace with a clear, neutral Indian English accent in a very high-quality, close-sounding recording with no background noise."
"A female speaker delivers Hindi speech slowly and expressively, with a slightly high pitch. The recording is very clear and close up."
"Divya's voice is monotone yet slightly fast in delivery, captured in a very clean studio recording."
"Aditi speaks Tamil with subtle emotional depth, normal pace, slightly higher pitch, recorded in high quality."
"Leela narrates Bengali calmly and slowly with low pitch, in a clear, close-up, noise-free studio recording."
```

**Tips**:
- Always include "very clear audio" / "no background noise" for cleanest output.
- Use **commas** to insert natural pauses.
- Avoid contradictory adjectives ("monotone" + "highly expressive").
- **Pin a named speaker** (Rohit, Divya, Aditi, Leela…) for reproducibility.

## Inference (minimal)

```python
import torch, soundfile as sf
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer

MODEL_ID = "ai4bharat/indic-parler-tts"
device = "cuda:0" if torch.cuda.is_available() else "cpu"
dtype  = torch.float16 if device.startswith("cuda") else torch.float32

model = ParlerTTSForConditionalGeneration.from_pretrained(MODEL_ID, torch_dtype=dtype).to(device)
prompt_tok      = AutoTokenizer.from_pretrained(MODEL_ID)                              # transcript
description_tok = AutoTokenizer.from_pretrained(model.config.text_encoder._name_or_path)  # style caption

def synthesize(transcript, description, out_path="out.wav", seed=None):
    if seed is not None:
        torch.manual_seed(seed)
    desc = description_tok(description, return_tensors="pt").to(device)
    txt  = prompt_tok(transcript,  return_tensors="pt").to(device)
    with torch.inference_mode():
        gen = model.generate(
            input_ids=desc.input_ids,
            attention_mask=desc.attention_mask,
            prompt_input_ids=txt.input_ids,
            prompt_attention_mask=txt.attention_mask,
            do_sample=True, temperature=1.0, repetition_penalty=1.1,
        )
    audio = gen.cpu().to(torch.float32).numpy().squeeze()
    sf.write(out_path, audio, model.config.sampling_rate)  # 44100 Hz mono
    return out_path
```

The **two-tokenizer pattern is mandatory**: description → Flan-T5 tokenizer,
transcript → model prompt tokenizer (Indic byte-fallback). Mixing them silently
degrades output.

## Hardware

- **VRAM**: ~3–4 GB fp16 (≤10 s utterances), ~6–8 GB fp32. Fits T4/L4/RTX 3060.
- **CPU**: feasible <10 s, but RTF >5× real time. Avoid in our run.
- **GPU RTF**: ~0.3–0.6× on A10/A100 fp16 short prompts; approaches 1× on long.
- SDPA / Flash-Attn 2 supported via `attn_implementation="sdpa"`.

## Known issues

- **Long-form**: degrades past ~20–30 s — chunk by sentence and concat.
- **Repetition / hallucination**: occasional token loops at `temperature>1.0`
  or with very short transcripts. Mitigate: `temperature=1.0`, `repetition_penalty=1.1`, fixed seed.
- **Code-switching** (Hindi/English mid-sentence): unreliable; pronunciation
  reverts to the dominant script's phonotactics. Eval target.
- **Description sensitivity**: same transcript can sound very different across
  reruns if the description doesn't pin a named speaker. Always pin.
- **No text normalization** — expand "2025" → "twenty twenty-five", "Dr." → "Doctor".
- **No streaming** API; full-utterance generation only.

## Sampling sweep for the harness

| Config name        | description hint                                     | sampling                          |
|--------------------|------------------------------------------------------|-----------------------------------|
| `default_neutral`  | "Rohit speaks at a moderate pace, very clear audio." | `do_sample=True, T=1.0, rep=1.1`  |
| `expressive_fem`   | "Divya speaks expressively, slightly high pitch…"    | same                              |
| `slow_calm`        | "Leela narrates calmly and slowly, low pitch…"       | same                              |
| `fast`             | "Maya speaks at a fast pace, clear audio…"           | same                              |
| `deterministic`    | same as default_neutral                              | `do_sample=False`                 |
