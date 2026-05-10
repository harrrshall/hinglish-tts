# Orpheus TTS — Research

## Identity & links

- **GitHub**: https://github.com/canopyai/Orpheus-TTS (Canopy Labs)
- **HF org**: https://huggingface.co/canopylabs
- **Project page**: https://canopylabs.ai/model-releases
- **Multilingual release blog**: https://canopylabs.ai/releases/orpheus_can_speak_any_language
- **First public release**: 2025-03-18; multilingual research preview 2025-04-09/10.
- **License**: **Apache-2.0** (some HF repos behind a contact-share gate).

### Checkpoints

**English production (3B)**
- [`canopylabs/orpheus-3b-0.1-ft`](https://huggingface.co/canopylabs/orpheus-3b-0.1-ft) — production English finetune (use this)
- [`canopylabs/orpheus-3b-0.1-pretrained`](https://huggingface.co/canopylabs/orpheus-3b-0.1-pretrained) — base for downstream FT
- `canopylabs/orpheus-tts-0.1-finetune-prod` — alias used by `orpheus-speech` package

**Multilingual research preview (3B each)** — https://huggingface.co/collections/canopylabs/orpheus-multilingual-research-release

| Lang | FT repo                                          | Pretrain repo                                |
|------|--------------------------------------------------|----------------------------------------------|
| hi   | `canopylabs/3b-hi-ft-research_release`           | `canopylabs/3b-hi-pretrain-research_release` |
| fr   | `canopylabs/3b-fr-ft-research_release`           | `…`                                          |
| de   | `canopylabs/3b-de-ft-research_release`           | `…`                                          |
| ko   | `canopylabs/3b-ko-ft-research_release`           | `…`                                          |
| zh   | `canopylabs/3b-zh-ft-research_release`           | `…`                                          |
| es+it| `canopylabs/3b-es_it-ft-research_release`        | `…`                                          |

**Smaller sizes (1B/400M/150M)**: announced on roadmap, not shipped at research time.

**Community Hindi / Hinglish finetunes (great for our Hinglish runs)**
- [`snorbyte/snorTTS-Indic-v0`](https://huggingface.co/snorbyte/snorTTS-Indic-v0) — 9 Indic languages incl. Hindi; explicit code-switching support; speaker IDs `hindi159`, `hindi49`, `hindi43`.
- [`SachinTelecmi/Orpheus-tts-hi`](https://huggingface.co/SachinTelecmi/Orpheus-tts-hi) — Hindi + English + code-mix, single voice.
- [`lex-au/Orpheus-3b-Hindi-FT-Q8_0.gguf`](https://huggingface.co/lex-au/Orpheus-3b-Hindi-FT-Q8_0.gguf) — GGUF for llama.cpp.
- [`unsloth/orpheus-3b-0.1-ft`](https://huggingface.co/unsloth/orpheus-3b-0.1-ft) — faster mirror.

## Architecture

- Backbone: **Llama-3.2-3B-Instruct** (decoder-only LLM).
- Audio codec: **SNAC @ 24 kHz**, 3 codebooks → 12 288 audio tokens added to LM vocab.
- Pure AR next-token prediction over interleaved text + SNAC tokens; SNAC decodes back to 24 kHz waveform.
- ~3 B params (≈4 B effective with audio embed expansion).
- Training: 100 k+ hours English speech for the English pretrain; multilingual variants are continued-pretrains on per-language corpora.

## Installation

```bash
pip install orpheus-speech
pip install vllm==0.7.3            # pin — latest vLLM has known regressions
pip install snac
pip install transformers torch torchaudio soundfile huggingface_hub
```

Requirements: Python 3.10+, PyTorch 2.2+, CUDA 12.1+ for vLLM.

## Inference

### Recommended (vLLM-backed)
```python
import wave
from orpheus_tts import OrpheusModel

model = OrpheusModel(
    model_name="canopylabs/orpheus-tts-0.1-finetune-prod",
    max_model_len=2048,
)

prompt = "tara: Hey there <laugh>, this is Orpheus speaking — pretty natural, right?"
syn_tokens = model.generate_speech(
    prompt=prompt, voice="tara",
    temperature=0.6, top_p=0.9, repetition_penalty=1.1,
)

with wave.open("out.wav", "wb") as wf:
    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(24000)
    for chunk in syn_tokens:
        wf.writeframes(chunk)
```

### Bare HF transformers (CPU-ish / smoke)
```python
from transformers import AutoTokenizer, AutoModelForCausalLM
from snac import SNAC
import torch

tok = AutoTokenizer.from_pretrained("canopylabs/orpheus-3b-0.1-ft")
lm  = AutoModelForCausalLM.from_pretrained(
    "canopylabs/orpheus-3b-0.1-ft", torch_dtype=torch.bfloat16, device_map="auto"
)
snac = SNAC.from_pretrained("hubertsiuzdak/snac_24khz").eval().cuda()

text = "tara: Welcome to the eval harness."
ids  = tok(text, return_tensors="pt").input_ids.cuda()
out  = lm.generate(ids, max_new_tokens=1200, do_sample=True,
                   temperature=0.6, top_p=0.9, repetition_penalty=1.1)
# Strip text tokens, regroup SNAC codes (3 codebooks), call snac.decode → 24kHz waveform.
```

Prompt format: `"{voice}: {text with optional <emotion> tags}"`.

## Voices & emotion tags

**English voices (recommended order)**: `tara` (default), `leah`, `jess`, `leo`, `dan`, `mia`, `zac`, `zoe`.

**Emotion tags (inline)**: `<laugh>`, `<chuckle>`, `<sigh>`, `<cough>`, `<sniffle>`, `<groan>`, `<yawn>`, `<gasp>`.

**Multilingual ft voices**: ~3 voices per language (24 total across the 8).

**snorbyte Hindi voices**: `hindi159`, `hindi49`, `hindi43`.

## Language support

- **English** production model is English-only and tends to anglicize foreign words.
- **Hindi natively?** Not in production English ft. Use:
  - `canopylabs/3b-hi-ft-research_release` (official, beta)
  - `snorbyte/snorTTS-Indic-v0` (best for code-switched **Hinglish** + 8 other Indic langs)
  - `SachinTelecmi/Orpheus-tts-hi` (single voice; supports `<hmm..>`, `<breath>`, `<think>`)

## Hardware

- **3B FP16 + vLLM**: comfortable on a single 24 GB card (3090/4090/A10G). Fails on 12 GB unquantized.
- **FP8 / 4-bit / GGUF Q8/Q4**: fits in 8–10 GB; community GGUFs run near real-time on llama.cpp.
- **Latency**: ~200 ms first-audio with vLLM streaming on 4090; ~100 ms with input streaming.
- **RTF**: <1 (faster than realtime) on RTX 3090+ with vLLM. CPU-only is impractical for live use.

## Known issues

- **End-of-audio hallucination**: stray audio after intended utterance, esp. multilingual variants ([issue #276](https://github.com/canopyai/Orpheus-TTS/issues/276)). Trim by detecting EOS audio-token or silence-trim postproc.
- **Repetition / loops** on long inputs — `repetition_penalty=1.1–1.2` + sentence chunking.
- **vLLM word-skipping** vs HF transformers ([issue #251](https://github.com/canopyai/Orpheus-TTS/issues/251)) — pin `vllm==0.7.3`.
- **Long-form drift** past ~30 s — chunk + concat (slight discontinuities).
- **Code-switching**: English base mispronounces non-English; use Hindi FT for Hinglish.
- **HF gating**: `canopylabs/orpheus-3b-0.1-ft` requires accepting a contact-share form — needs logged-in HF token in CI.

## Sampling sweep for the harness

For our eval, run **three Orpheus sub-models** as separate logical models in
the comparison so the user can clearly see which language-specialised variant
wins on which axis:

| Logical model id            | Underlying repo                                |
|-----------------------------|-----------------------------------------------|
| `orpheus_en`                | `canopylabs/orpheus-tts-0.1-finetune-prod`     |
| `orpheus_hi_official`       | `canopylabs/3b-hi-ft-research_release`         |
| `orpheus_hinglish_snor`     | `snorbyte/snorTTS-Indic-v0`                    |

(Decision: surface as one `orpheus` family in `configs/models.yaml`,
parameterized by `variant`. The orchestrator dispatches to the right HF repo
based on the prompt language, so the user sees a single Orpheus column with
the best-effort variant chosen automatically. Tracked in `progress.md`
"Open questions / decisions log".)

| Config name     | Args                                              |
|-----------------|---------------------------------------------------|
| `default`       | T=0.6, top_p=0.9, rep=1.1                         |
| `expressive`    | T=0.85, top_p=0.95, rep=1.1                       |
| `deterministic` | T=0.0 (greedy), top_p=1.0, rep=1.05               |
| `with_emotion`  | inline `<laugh>`/`<sigh>` tags + T=0.6            |
