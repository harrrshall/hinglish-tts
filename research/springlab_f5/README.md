# SPRINGLab F5-Hindi-24kHz — Research

A Hindi-finetuned F5-TTS checkpoint from SPRING Lab, IIT Madras. Drop-in
compatible with the upstream `SWivid/F5-TTS` runtime, but ships its own
checkpoint, vocab, and "small" model config.

## Identity & links

- **HF repo**: [`SPRINGLab/F5-Hindi-24KHz`](https://huggingface.co/SPRINGLab/F5-Hindi-24KHz)
- **Checkpoint**: `model_2500000.safetensors` (also `.pt` available)
- **Vocab**: `vocab.txt`
- **Upstream runtime**: https://github.com/SWivid/F5-TTS
- **SPRINGLab fork**: https://github.com/rumourscape/F5-TTS
- **F5-TTS paper**: https://arxiv.org/abs/2410.06885
- **Training data**: `SPRINGLab/IndicTTS-Hindi`, `SPRINGLab/IndicVoices-R_Hindi`
- **Compute**: CDAC, 8× A100 40GB, ~1 week
- **Upstream registry entry**: https://github.com/SWivid/F5-TTS/blob/main/src/f5_tts/infer/SHARED.md
- **License**: **CC-BY-4.0** (model card; datasets are open).

## Architecture

- F5-TTS family — flow-matching DiT + ConvNeXt text encoder + mel-spectrogram target + **Vocos** vocoder.
- F5 "small" config: `dim=768, depth=18, heads=12, ff_mult=2, text_dim=512, conv_layers=4, pe_attn_head=1`.
- ~151 M params.
- **Output: 24 000 Hz, 16-bit PCM WAV**.
- Conditioning: zero-shot voice clone via reference audio + reference transcript.

## Installation

Tested matrix: Python 3.10–3.11, PyTorch 2.4–2.8, CUDA 12.1/12.4/12.8.

```bash
conda create -n tts-springlab-f5 python=3.11 -y
conda activate tts-springlab-f5
conda install -c conda-forge ffmpeg -y

# CUDA 12.4 (adjust)
pip install torch==2.4.1+cu124 torchaudio==2.4.1+cu124 \
  --extra-index-url https://download.pytorch.org/whl/cu124

pip install f5-tts

huggingface-cli download SPRINGLab/F5-Hindi-24KHz \
  model_2500000.safetensors vocab.txt samples/output1.wav samples/output2.wav samples/output3.wav \
  --local-dir ./ckpts/F5-Hindi-24KHz
```

## Inference

### CLI
```bash
f5-tts_infer-cli \
  --model F5TTS_Base \
  --ckpt_file ./ckpts/F5-Hindi-24KHz/model_2500000.safetensors \
  --vocab_file ./ckpts/F5-Hindi-24KHz/vocab.txt \
  --ref_audio ./ckpts/F5-Hindi-24KHz/samples/output1.wav \
  --ref_text "शिवगढ़ी गाँव, एक बड़ा गाँव था" \
  --gen_text "नमस्ते, यह एक परीक्षण वाक्य है।" \
  --output_dir ./out --output_file hindi.wav \
  --nfe_step 32 --cfg_strength 2.0 --speed 1.0
```

### Python API
```python
from f5_tts.api import F5TTS
from huggingface_hub import hf_hub_download

REPO = "SPRINGLab/F5-Hindi-24KHz"
ckpt  = hf_hub_download(REPO, "model_2500000.safetensors")
vocab = hf_hub_download(REPO, "vocab.txt")
ref   = hf_hub_download(REPO, "samples/output1.wav")

tts = F5TTS(
    model="F5TTS_Base",
    ckpt_file=ckpt, vocab_file=vocab,
    use_ema=True, device="cuda",
)

wav, sr, _ = tts.infer(
    ref_file=ref,
    ref_text="शिवगढ़ी गाँव, एक बड़ा गाँव था",
    gen_text="नमस्ते, यह F5 हिंदी मॉडल का परीक्षण है।",
    nfe_step=32, cfg_strength=2.0, sway_sampling_coef=-1.0,
    speed=1.0, cross_fade_duration=0.15,
    remove_silence=True, seed=42,
    file_wave="hindi_out.wav",
)
assert sr == 24000
```

## Reference audio requirements

- **Duration: ≤12 s** — anything longer is hard-clipped (mid-word truncation harms voice).
- Mono preferred (stereo downmixed). Any rate that ffmpeg can read (auto-resampled to 24 kHz).
- **Reference transcript** must match audio verbatim in **Devanagari**. Empty
  ref_text triggers Whisper ASR fallback, which is unreliable for Hindi —
  always supply transcripts.
- Bundled samples in repo: `samples/output1.wav`, `output2.wav`, `output3.wav`.
  Their transcripts are not published — we will transcribe them once and cache
  them in `research/springlab_f5/reference_audio/`.

## Language support

- **Primary: Hindi (Devanagari).** Vocab is Devanagari + punctuation.
- **English / Hinglish: degraded.** Latin tokens fall back to character-by-character spelling.
  For Hinglish eval, we will deliberately submit Devanagari-transliterated
  English (`मॉडल` not `model`) and also raw Latin to expose the failure mode.
- **Numerals**: Arabic digits read as English letters; pre-normalize Hindi-numeric
  prompts to words (e.g. `२०२६` → `दो हज़ार छब्बीस`).

## Sampling controls

| Param                | Default | Notes                                           |
|----------------------|--------:|-------------------------------------------------|
| `nfe_step`           | 32      | 16 fastest; 32 sweet spot; 64 marginal gains    |
| `cfg_strength`       | 2.0     | 1.5–3.0 useful; higher = more faithful, less natural |
| `sway_sampling_coef` | -1.0    | keep at -1 unless ablating                      |
| `speed`              | 1.0     | 0.7–1.3 stable                                  |
| `cross_fade_duration`| 0.15    | for chunked long-form                           |
| `seed`               | none    | int for determinism                             |
| `remove_silence`     | False   | trims leading/trailing silence post-vocoder     |

## Hardware

- **VRAM**: ~2.5–3 GB fp32 inference; ~1.6 GB fp16. Fits 6 GB GPU.
- **CPU**: feasible but slow.
- **GPU RTF**: ~0.04 on L20 at NFE=16; ~0.08 at NFE=32 on A10/RTX 4090.

## Known issues

- **30-s generation cap** per call (prompt + output). Long-form requires sentence chunking + cross-fade.
- **Code-switching**: English-script tokens spelled letter-by-letter.
- **No text normalizer** for Hindi — expand numerics/dates/currency manually.
- **Reference quality dominates output prosody**; noisy refs → unstable voice.
- **Long refs (>12 s) silently truncated** mid-word.
- **No emotion/style tags** — emotion inherited entirely from reference clip.
- **Single-speaker drift** across long generations (HF discussion #5).

## Sampling sweep for the harness

Reference clip: `output1.wav` from the HF repo (one canonical female reference).
Hinglish runs use the same reference but with prompts in Devanagari
transliteration and (for failure-mode eval) raw Latin.

| Config name        | Args                                                                  |
|--------------------|----------------------------------------------------------------------|
| `default`          | nfe=32, cfg=2.0, speed=1.0, sway=-1.0, seed=42                       |
| `fast`             | nfe=16, cfg=2.0, speed=1.0, sway=-1.0, seed=42                       |
| `high_cfg`         | nfe=32, cfg=2.8, speed=1.0, sway=-1.0, seed=42                       |
| `slow`             | nfe=32, cfg=2.0, speed=0.85, sway=-1.0, seed=42                      |
| `stochastic`       | nfe=32, cfg=2.0, speed=1.0, sway=-1.0, seed=None (3 reruns for stability) |
