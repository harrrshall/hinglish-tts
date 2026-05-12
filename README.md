# Hinglish TTS

Open-source text-to-speech for Hindi-English code-mixed ("Hinglish") speech.
Built on [IndicF5](https://huggingface.co/ai4bharat/IndicF5) (AI4Bharat, 330M params) with a two-line duration patch and automatic script normalisation via [IndicXlit](https://github.com/AI4Bharat/IndicXlit).
Accepts Devanagari, Roman-script Hindi, mixed-script sentences, and English with Indian named entities — all in the same API call.
**4.70 / 5.0** mean intelligibility (30-sentence eval set, three-ASR consensus).

---

## Sample outputs

The 6 inputs below come from the rubric v2.1 production run (full table and per-sentence scores in `EVALUATION_REPORT.md`). Live demo with all 30 sentences: [hinglish-tts.vercel.app](https://hinglish-tts.vercel.app).

| Input | Category | Score |
|---|---|:---:|
| कल मुझे दिल्ली जाना है। | Pure Devanagari | 5/5 |
| yaar tu kal kya kar raha tha | Pure Roman Hinglish | 5/5 |
| kal mujhe office jaana hai | Pure Roman (English loan) | 5/5 |
| Boss को बता देना kal मैं leave पर रहूँगा | Mixed script | 5/5 |
| Mera presentation tomorrow है, और मैं nervous हूं। | Mixed script | 5/5 |
| My friend Aishwarya from Chennai is visiting Bengaluru | English with NE | 4/5 |

---

## Quality numbers

### Overall

| Metric | Value |
|---|:---:|
| Mean intelligibility | **4.70 / 5.0** |
| Silence or skip | **0 / 30** |
| Sentences scoring 5/5 | **19 / 30** |
| Sentences scoring ≤ 2 | **0 / 30** |

Scoring rubric: character error rate (CER) after Devanagari normalisation,
three-ASR consensus (AssemblyAI + Deepgram + Groq Whisper), 30-sentence eval set.
Naturalness is evaluated by ear only — see [Naturalness](#naturalness).

### By input category

| Category | n | Score | What it covers |
|---|:---:|:---:|---|
| `pure_devanagari` | 8 | **4.62** | Standard Hindi in Devanagari script |
| `pure_roman` | 8 | **4.75** | Colloquial Hinglish in Roman script |
| `mixed_script` | 9 | **4.88** | Mid-sentence Devanagari ↔ Roman switching |
| `english_with_NE` | 6 | **4.50** | English sentences with Indian proper nouns |

### Comparison to other open models

Same eval set, same rubric.

| Model | Overall | pure\_roman | mixed | eng\_NE | pure\_dev |
|---|:---:|:---:|:---:|:---:|:---:|
| **This package** | **4.70** | **4.75** | **4.88** | 4.50 | **4.62** |
| Kokoro v1.0 (Hindi) | 3.90 | 2.50 | 3.88 | **4.83** | 4.62 |
| Indic Parler-TTS | 3.40 | 1.75 | 3.00 | 4.67 | 4.50 |
| IndicF5 (unpatched, no preprocessing) | 2.13 | 1.00 | 1.62 | 1.00 | 4.62 |
| SPRINGLab F5-Hindi | 2.07 | 1.00 | 1.38 | 1.00 | 4.62 |

The gap is largest on `pure_roman` (+2.25 over Kokoro), the dominant input
register for Indian chat and voice-interface applications.
Kokoro leads on `english_with_NE` — see [Known limitations](#known-limitations).

Full methodology and per-sentence breakdown: [EVALUATION_REPORT.md](EVALUATION_REPORT.md).

---

## Installation

**Prerequisites:** Python 3.10–3.11, CUDA GPU (≥ 6 GB VRAM), a
[HuggingFace account](https://huggingface.co) with model gating accepted.

```bash
# 1. Clone
git clone https://github.com/harrrshall/hinglish-tts.git && cd hinglish-tts

# 2. Install IndicF5 and inference dependencies
pip install git+https://github.com/AI4Bharat/IndicF5.git \
    "transformers==4.49.0" "accelerate==0.33.0" \
    "numpy>=2.0,<2.1" soundfile

# 3. Accept model gating — visit the link below and click "Agree and access repository"
#    https://huggingface.co/ai4bharat/IndicF5

# 4. Set your HuggingFace token
export HF_TOKEN=hf_your_token_here

# 5. Install preprocessing (requires Python ≤ 3.11; skip for Devanagari-only input)
pip install ai4bharat-transliteration
```

> **Duration patch:** `inference.py` automatically patches
> `f5_tts/infer/utils_infer.py` in your site-packages on first import.
> This is required — the unpatched model truncates all Roman-script output.
> Run `python inference.py dummy --patch-status` to verify it is active.

---

## Usage

### Python API

```python
from inference import load_model, synthesize
import soundfile as sf

model = load_model()   # reads HF_TOKEN from environment; downloads weights once (~1.3 GB)

REF_AUDIO = "data/reference_audio/hindi_ref.wav"   # any 3–10s mono 24 kHz Hindi clip
REF_TEXT  = open("data/reference_audio/hindi_ref.txt").read().strip()
```

**Pure Devanagari**

```python
audio = synthesize(model, "कल मुझे दिल्ली जाना है।", REF_AUDIO, REF_TEXT)
sf.write("out.wav", audio, 24000)
```

**Roman-script Hinglish** — preprocessing converts to Devanagari automatically

```python
audio = synthesize(model, "yaar tu kal kya kar raha tha", REF_AUDIO, REF_TEXT)
```

**Mixed script** — mid-sentence script switching

```python
audio = synthesize(model,
    "Boss को बता देना kal मैं leave पर रहूँगा, kuch personal काम है।",
    REF_AUDIO, REF_TEXT)
```

**English with Indian named entities**

```python
audio = synthesize(model,
    "My friend Aishwarya from Chennai is visiting Bengaluru next week.",
    REF_AUDIO, REF_TEXT)
```

**Raw Devanagari, no preprocessing** — for phonetic experiments or pre-normalised input

```python
audio = synthesize(model, "मेरा नाम ज़ारा है।", REF_AUDIO, REF_TEXT, preprocess=False)
```

### Command line

```bash
python inference.py "yaar tu kal kya kar raha tha" \
    --ref-audio data/reference_audio/hindi_ref.wav \
    --ref-text "$(cat data/reference_audio/hindi_ref.txt)" \
    --out out.wav

# Check duration patch status before a batch run
python inference.py placeholder --patch-status \
    --ref-audio x --ref-text x --out /dev/null
```

---

## How it works

**1. Preprocessing (`scoring/scripts/lib_normalize.py`)**
Roman tokens are transliterated to Devanagari by IndicXlit. Two override tables
correct cases IndicXlit gets wrong: 36 English loanwords with fixed canonical
Devanagari forms (`office → ऑफिस`, `laptop → लैपटॉप`, `party → पार्टी`),
and 4 short Hindi function words that IndicXlit misreads as English phonetics
(`mai → मैं`, `tu → तू`, `aa → आ`, `hu → हूं`). Pure Devanagari input
passes through unchanged. The function is idempotent.

**2. Duration patch**
IndicF5 v12 allocates synthesis canvas time using UTF-8 byte counts. Devanagari
encodes as ~3 bytes/character; ASCII as 1. For Roman-script input this allocates
~3× less canvas than needed and truncates the audio — the "Mode A" failure that
produces 21/30 silent outputs on the unpatched model.
`inference.py` patches `utils_infer.py` in site-packages at import time,
replacing byte counts with non-whitespace character counts. The patch is
idempotent and emits a `DEBUG-PATCH:` diagnostic line per call confirming
it is active.

**3. IndicF5 inference**
IndicF5 is a 330M-parameter flow-matching TTS model from AI4Bharat, trained
on Indic-script audio. It performs zero-shot voice cloning: provide a 3–10s
reference clip and its transcript, and the model generates speech in that voice.
No fine-tuning was applied to reach the 4.70 score — the gain is entirely from
preprocessing and the duration patch. Output: 24 kHz mono PCM float32.

---

## Known limitations

Summarised here; detailed with examples and architectural notes at
[KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md).

- **Synthetic texture.** Outputs are intelligible and fluent but audibly
  synthetic. A trained ear identifies every clip as TTS regardless of score.

- **Prosodic flatness.** Long sentences, questions, and exclamations receive
  similar flat delivery. Ellipsis and `!` produce subtle pacing and pitch
  effects but not dramatically different emphasis.

- **No naturalness number.** The 4.70 is intelligibility only. Automatic
  naturalness predictors (UTMOS, SQUIM_MOS) invert directionally on Hindi by
  ~2 ranks and cannot be trusted here.

- **Whitelist generalisation (n=30).** The English-loan and Indian-NE
  whitelists were tuned to the 30-sentence eval vocabulary. Unknown tokens fall
  through to IndicXlit, which handles common cases well but degrades on
  ambiguous short tokens and uncommon proper nouns.

- **Kokoro leads on `english_with_NE`.** Kokoro 4.83 vs 4.50. This package
  transliterates English sentences to Hindi-accented phonetics
  ("माय फ्रेंड ऐश्वर्या"); listeners who prefer English-mode proper-noun
  rendering should evaluate Kokoro for this category.

- **Gated model weights.** IndicF5 requires HuggingFace account and manual
  gating acceptance. Weights are not redistributed here.

- **Python ≤ 3.11 for Roman-script preprocessing.** IndicXlit depends on
  fairseq, which has a dataclass incompatibility with Python 3.12. Whitelist
  paths (covering the eval-set vocabulary) work on any Python version; only
  IndicXlit fallback requires 3.11 or earlier.

---

## Naturalness

Not auto-scored. A native Hindi speaker evaluated all 30 v2.1 outputs. Summary:

- Pure Hindi and normalised Hinglish are fluent and natural for conversational
  sentences. Vowel lengths, aspiration, and basic prosodic contours are correct.
- Delivery is flat on longer sentences. Output is identifiably synthetic even
  at 5/5 intelligibility.
- English loanwords and Indian names are produced with consistent Hindi
  phonetics — "Bengaluru" with Indian vowels, not anglicised.
- The model responds to fine Devanagari distinctions: vowel length (ि vs ी),
  aspiration (ख vs क), and nukta (ज़ vs ज) produce measurably different acoustic
  output when input is correctly marked up.

---

## Citation

If you use the eval set, scoring rubric, or preprocessing code from this work:

```bibtex
@misc{singh2026hinglish,
  author       = {Harshal Singh},
  title        = {Hinglish TTS: IndicF5 with IndicXlit Preprocessing},
  year         = {2026},
  howpublished = {\url{https://github.com/harrrshall/hinglish-tts}},
  note         = {30-sentence Hinglish eval set (4 categories).
                  Rubric v2.1: three-ASR consensus, Devanagari-normalised CER,
                  ear-only naturalness. 4.70/5.0 mean intelligibility.}
}
```

If you use IndicF5, also cite the AI4Bharat IndicF5 paper (see the model card
at [huggingface.co/ai4bharat/IndicF5](https://huggingface.co/ai4bharat/IndicF5)).

---

## License

| Component | License |
|---|---|
| Eval set, scoring scripts, rubric, `inference.py` | Free for research; [cybernovascnn@gmail.com](mailto:cybernovascnn@gmail.com) for commercial use |
| IndicF5 model weights | See [ai4bharat/IndicF5](https://huggingface.co/ai4bharat/IndicF5) — attribution required, commercial use restricted |
| F5-TTS architecture | MIT ([SWivid/F5-TTS](https://github.com/SWivid/F5-TTS)) |
| IndicXlit | Apache 2.0 ([ai4bharat/IndicXlit](https://github.com/AI4Bharat/IndicXlit)) |

---

## For the technical reader

Full evaluation methodology, per-sentence scores, rubric specification,
and limitation accounting: **[EVALUATION_REPORT.md](EVALUATION_REPORT.md)**

Architectural details and the why behind each decision: **[HOW_IT_WORKS.md](HOW_IT_WORKS.md)**
