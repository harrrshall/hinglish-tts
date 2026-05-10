# IndicF5 — Research

## Identity & links

- **HF (gated)**: [`ai4bharat/IndicF5`](https://huggingface.co/ai4bharat/IndicF5) — must accept terms + `huggingface-cli login`
- **GitHub**: https://github.com/AI4Bharat/IndicF5
- **Project page**: https://ai4bharat.iitm.ac.in/areas/model/TTS/IndicF5
- **Demo Space**: https://huggingface.co/spaces/ai4bharat/IndicF5
- **Upstream**: F5-TTS https://github.com/SWivid/F5-TTS (paper https://arxiv.org/abs/2410.06885)
- **License**: **MIT**
- **Cite**: Praveen S V, Srija Anand, Soma Siddhartha, Mitesh M. Khapra (2025).
- No standalone IndicF5 paper — README references the F5-TTS upstream paper.

## Architecture

- F5-TTS family — non-autoregressive **flow-matching** transformer over mel.
- DiT backbone with ConvNeXt text branch. Reference-conditioned (zero-shot voice clone). No phoneme front-end.
- Backbone config (matches F5-TTS Base): `dim=1024, depth=22, heads=16, ff_mult=2, text_dim=512, conv_layers=4`.
- Vocoder: **Vocos** (24 kHz, 100-mel, hop 256). BigVGAN supported by code paths but released weights ship with Vocos.
- ~0.4 B params (1.4 GB safetensors).
- Training data: 1417 h from Rasa, IndicTTS (IITM), LIMMITS, IndicVoices-R.
- Output: 24 000 Hz mono.

## Languages (11)

Assamese, Bengali, Gujarati, **Hindi**, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, Telugu.

**English / Hinglish: NOT officially supported.** Training corpora are all-Indic.
English-in-Devanagari sometimes works opportunistically; quality not guaranteed.
For pure English baseline, route to upstream F5-TTS (we won't, since the
question is "how does IndicF5 fail on English/Hinglish?" — that's a real
finding for the user).

## Installation

```bash
conda create -n tts-indicf5 python=3.10 -y
conda activate tts-indicf5
sudo apt-get install -y ffmpeg     # pydub + librosa need it
pip install git+https://github.com/AI4Bharat/IndicF5.git
huggingface-cli login              # gated repo — accept terms first
```

Pinned deps (from upstream `requirements.txt`):
`torch>=2.0`, `torchaudio>=2.0`, `transformers<4.50`, `numpy<=1.26.4`,
`accelerate>=0.33`, `vocos`, `x_transformers>=1.31.14`, `torchdiffeq`,
`ema_pytorch`, `librosa`, `soundfile`, `pydub`, `safetensors`, `cached_path`.

The `transformers<4.50` and `numpy<=1.26.4` pins **will conflict** with the
master env's metric stack — must isolate in its own conda env.

## Inference

The HF repo ships a `model.py` exposing `AutoModel` with signature
`model(gen_text, ref_audio_path, ref_text)` returning a 1-D NumPy array @24 kHz.
Internally wraps F5-TTS `infer_process` with Vocos.

```python
from transformers import AutoModel
import numpy as np, soundfile as sf, torch

device = "cuda" if torch.cuda.is_available() else "cpu"
model = AutoModel.from_pretrained("ai4bharat/IndicF5", trust_remote_code=True).to(device)

audio = model(
    "नमस्ते! आज मौसम बहुत सुहाना है।",                # gen_text (target)
    ref_audio_path="prompts/PAN_F_HAPPY_00001.wav",   # 24 kHz mono WAV, ≤15 s
    ref_text="ਭਹੰਪੀ ਵਿੱਚ ਸਮਾਰਕਾਂ ਦੇ ਭਵਨ …",         # exact transcript of ref
)
if audio.dtype == np.int16:
    audio = audio.astype(np.float32) / 32768.0
sf.write("out.wav", np.asarray(audio, dtype=np.float32), 24000)
```

For NFE/CFG/speed/seed control, bypass the HF wrapper and use
`f5_tts.api.F5TTS().infer(...)` from the cloned package — same weights, all knobs.

## Reference audio requirements

- **Format**: WAV, mono. Auto-resampled, but providing 24 kHz avoids quality loss.
  `ffmpeg -i in.mp3 -ar 24000 -ac 1 -c:a pcm_s16le ref.wav`.
- **Duration**: hard cap **15 s** (`preprocess_ref_audio_text` clips to 15 000 ms).
  Sweet spot 5–10 s with ~1 s leading/trailing silence.
- **Reference text**: must transcribe the ref clip *exactly*, in its native script.
- **Bundled prompts** in `prompts/` of the GitHub repo:
  `KAN_F_HAPPY_00001.wav`, `MAR_F_HAPPY_00001.wav`, `MAR_F_WIKI_00001.wav`,
  `MAR_M_WIKI_00001.wav`, `PAN_F_HAPPY_00001.wav`, `PAN_F_HAPPY_00002.wav`,
  `TAM_F_HAPPY_00001.wav`. **Reference texts NOT in the README** — obtain from
  demo Space or transcribe with Indic ASR. We will cache these in
  `research/indicf5/reference_audio/` along with their transcripts.

## Sampling controls (defaults from `utils_infer.py`)

| Param                | Default | Notes                                        |
|----------------------|--------:|----------------------------------------------|
| `nfe_step`           | 32      | 16 fast / 32 quality / 64 marginal          |
| `cfg_strength`       | 2.0     | Classifier-free guidance scale              |
| `sway_sampling_coef` | −1.0    | F5-TTS sway sampler                         |
| `speed`              | 1.0     | linear duration scale                       |
| `target_rms`         | 0.1     | output loudness normalization               |
| `cross_fade_duration`| 0.15 s  | crossfade between chunks for long text      |
| `fix_duration`       | None    | force absolute output length (sec)          |
| `seed`               | -1      | random; set int for reproducibility         |
| `max_chars`          | 135     | per-chunk text split                        |

The HF `AutoModel(...)` call hardcodes these. For sweeps, use `F5TTS.infer`.

## Hardware

- VRAM: ~3–4 GB fp32 @ NFE=32; fits 6 GB. fp16 ~2 GB (not officially validated).
- CPU: functional but RTF 5–15× slower than realtime.
- GPU RTF: ~0.1–0.2 (5–10× faster than realtime) on A100/RTX 4090 @ NFE=32.
- First call downloads ~1.4 GB safetensors + ~50 MB Vocos.

## Known issues

- **Long-form drift**: chunks >135 chars split + crossfaded — speaker/prosody drifts.
- **Code-switching**: Latin tokens often mispronounced or skipped. Romanized Hindi weak.
- **Numbers/dates/units**: no normalizer; pre-expand ("123" → "एक सौ तेईस").
- **Repetition / cut-offs**: when ref-text is wrong or padding silence missing.
- **Gated download**: `from_pretrained` throws `GatedRepoError` until terms accepted + `HF_TOKEN` set.
- **Pinned deps conflict** with master env — isolate.
- **`trust_remote_code=True` mandatory** — `model.py` runs custom code at load.

## Sampling sweep for the harness

Reference: bundled `PAN_F_HAPPY_00001.wav` (Punjabi female-happy) is the most
robust default per upstream, but for Hindi runs we will also stash a clean
Hindi clip + transcript in `research/indicf5/reference_audio/hi_female_neutral/`.

| Config name        | Args                                                                  |
|--------------------|----------------------------------------------------------------------|
| `default`          | nfe=32, cfg=2.0, speed=1.0, seed=42                                  |
| `fast`             | nfe=16, cfg=2.0, speed=1.0, seed=42                                  |
| `high_cfg`         | nfe=32, cfg=2.8, speed=1.0, seed=42                                  |
| `slow`             | nfe=32, cfg=2.0, speed=0.85, seed=42                                 |
| `stochastic`       | nfe=32, cfg=2.0, speed=1.0, seed=None (3 reruns for stability)       |

For our **English / Hinglish** prompts, IndicF5 is being tested as a known
weakness — expect degraded results. Run them anyway; the user wanted a fair
multi-model comparison and "this model can't handle Hinglish well" is a
useful finding.
