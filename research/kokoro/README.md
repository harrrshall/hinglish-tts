# Kokoro v1.0 — Research

## Identity & links

- **Hugging Face (weights)**: [hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M)
- **GitHub (Python package)**: https://github.com/hexgrad/kokoro
- **PyPI**: https://pypi.org/project/kokoro/
- **G2P engine**: [hexgrad/misaki](https://github.com/hexgrad/misaki)
- **Demo Space**: https://huggingface.co/spaces/hexgrad/Kokoro-TTS
- **ONNX port**: https://huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX
- **Voices doc**: https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md
- **Eval doc**: https://huggingface.co/hexgrad/Kokoro-82M/blob/main/EVAL.md
- **Latest v1.0 checkpoint**: `kokoro-v1_0.pth` on `main`, published **2025-01-27**, SHA256 `496dba118d1a58f5f3db2efc88dbdc216e0483fc89fe6e47ee1f2c53f18ad1e4`.
- **Paper**: No standalone paper — derives from [StyleTTS 2](https://arxiv.org/abs/2306.07691) + [ISTFTNet](https://arxiv.org/abs/2203.02395).

## Architecture

- StyleTTS 2 derivative (decoder-only release; no diffusion sampler).
- ISTFTNet vocoder.
- ~82 M parameters.
- IPA phoneme labels via `misaki` G2P + `espeak-ng` fallback.
- License: **Apache 2.0** (weights & code).

## Installation

- Python: **>=3.10, <3.13**.
- System dep: **`espeak-ng`** required (OOV phonemizer fallback).

```bash
sudo apt-get install -y espeak-ng        # Linux
pip install "kokoro>=0.9.4" soundfile numpy
```

Latest PyPI release at research time: **0.9.4** (2025-04-05).

## Languages & voices

`KPipeline(lang_code=...)` — one language per pipeline:

| `lang_code` | Language       | Notes |
|-------------|----------------|-------|
| `a` | American English  | Best grades (`af_heart` A-, `af_bella` A-) |
| `b` | British English   | Best is `bf_emma` (B-) |
| `e` | Spanish           | C/D grades |
| `f` | French            | Only `ff_siwis` (B-) |
| `h` | **Hindi**         | 4 voices (`hf_alpha`, `hf_beta`, `hm_omega`, `hm_psi`) — all **graded C** |
| `i` | Italian           | C/D grades |
| `j` | Japanese          | C grades |
| `p` | Brazilian Portuguese | C/D grades |
| `z` | Mandarin          | C/D grades |

**Hinglish: NOT officially supported.** `KPipeline` is initialised with one
`lang_code`. No code-switching mode. Workaround for our harness: chunk by
script and run each chunk through the matching pipeline, then concatenate.
Quality is best-effort.

Voice prefix encodes language + gender: `<lang_letter><f|m>_<name>`, e.g.
`af_heart` = American Female "heart"; `hm_omega` = Hindi Male "omega".

## Sampling controls

- `voice` — voice id string (or precomputed style tensor for blending).
- `speed` — float, default 1.0, range ~0.5–2.0.
- `split_pattern` — regex used to chunk long text. Default `r'\n+'`.
- **No temperature/top-k/seed knobs.** Decoder is non-AR; output is deterministic
  given (voice, phonemes, speed). For our "stochastic vs deterministic" sweep,
  we'll vary `voice` and `speed` instead of sampling temp.

## Hardware

- **VRAM**: <1 GB FP16 weights, ~2–3 GB peak; runs on a 4 GB GPU.
- **CPU**: feasible (>100× realtime reported on modern CPUs).
- **GPU RTF**: ~0.03 (≈30× realtime) on A100; ONNX path can hit ~50× on GPU.

## Known issues

- **Hallucination / truncation** when phonemizer mis-handles input.
- **G2P weakness** on non-English; Hindi voices are graded C.
- **Token sweet spot** ~100–200 per chunk (max 510). Very short utterances
  (<20 tokens) sometimes degrade.
- **Number/acronym/date/currency** edge cases mis-pronounce — pre-normalise.
- **No emotion/style control**, no zero-shot voice cloning.
- **Hinglish unsupported** — treat as a known weakness in our eval.

## Minimal inference snippet

```python
import numpy as np, soundfile as sf
from kokoro import KPipeline

_PIPES: dict[str, KPipeline] = {}

def _pipe(lang_code: str) -> KPipeline:
    if lang_code not in _PIPES:
        _PIPES[lang_code] = KPipeline(lang_code=lang_code)
    return _PIPES[lang_code]

def synthesize(text: str, out_path: str,
               voice: str = "af_heart",
               lang_code: str = "a",
               speed: float = 1.0) -> str:
    pipe = _pipe(lang_code)
    audio = np.concatenate([
        chunk for _, _, chunk in pipe(text, voice=voice, speed=speed)
    ])
    sf.write(out_path, audio, 24000)   # 24 kHz mono float32
    return out_path
```

Sample rate: **24000 Hz** mono float32.

## Sampling sweep for the harness

| Config name      | Args                                              |
|------------------|---------------------------------------------------|
| `default`        | voice=`af_heart` (en) / `hf_alpha` (hi), speed=1.0 |
| `male`           | voice=`am_michael` / `hm_omega`, speed=1.0         |
| `slow`           | speed=0.85                                         |
| `fast`           | speed=1.15                                         |

Hinglish: use the **English pipeline** for whole-text, plus a second pass with
the **Hindi pipeline** for whole-text, and let human review judge which is
less wrong. (Neither will be correct.)
