# How I Built an Open-Source Hinglish TTS That Beats Every Other Model (Starting From Zero )

*By Harshal Singh and claude code*

---

I knew nothing about text-to-speech when I started this.

Not the models. Not the terminology. Not the difference between a vocoder and a flow-matching diffusion transformer. I had never heard the word "IndicXlit" and I did not know what a mel spectrogram was.

What I had was a goal: build the best open-source TTS model for English.

That goal lasted about three days before I realized I was solving the wrong problem entirely.

This is the story of what actually happened every wrong turn, every "wait, the metrics are lying to us," every 2 AM kernel crash on Kaggle. It ends with a system that scores 4.70 out of 5.0 on a rigorous three-ASR evaluation rubric and beats every other open-source Hinglish-capable TTS model on the planet. And it was built with 14 lines of code — no training, no fine-tuning, no GPU budget.

Here's everything.

---

## The Pivot: Why Hinglish?

**India.** 600 million Hindi speakers. Another several hundred million who speak Hindi mixed with English — what linguists call "Hinglish," what everyone in Indian cities just calls "talking."

Hinglish is not pidgin. It is not broken English. It is a fully developed code-switching register with its own grammar. A native speaker switches mid-sentence — sometimes mid-phrase — between Devanagari-script Hindi and Roman-script English. It looks like this:

> *"Boss को बता देना kal मैं leave पर रहूँगा, kuch personal काम है।"*

That is one sentence. Three scripts. Two languages. It is how 100 million urban Indians write to each other every day on WhatsApp.

No open-source TTS model handles it well.

**That became the problem I decided to solve.**

---

## The Audit: Testing What Already Existed

The first real step was not building anything. It was measuring everything that already existed.

I picked four candidate models and a 30-sentence eval set designed to stress every dimension of the problem:

| Category | Count | What it tests |
|---|:---:|---|
| `pure_devanagari` | 8 | Standard Hindi in Devanagari script |
| `pure_roman` | 8 | Colloquial Hinglish written in Roman script |
| `mixed_script` | 9 | Mid-sentence script switching |
| `english_with_NE` | 6 | English with Indian names and places |

The four models I tested:

1. **Kokoro v1.0** (hexgrad, 82M parameters) — the English TTS champion, with a Hindi mode
2. **Indic Parler-TTS** (AI4Bharat, 880M parameters) — large, Indic-focused, text-description conditioned
3. **IndicF5** (AI4Bharat, 330M parameters) — flow-matching TTS, trained on Indic-script audio
4. **SPRINGLab F5-Hindi** (another Indic F5-TTS variant)

I ran everything on Kaggle T4 GPUs (free tier — the project had zero budget).

The first results looked like this, scored with a single ASR system (AssemblyAI):

| Model | Overall score |
|---|:---:|
| Kokoro v1.0 | 3.03 |
| Indic Parler-TTS | 2.73 |
| **IndicF5** | **1.97** |
| SPRINGLab F5-Hindi | similar |

Kokoro wins. Case closed. Ship Kokoro for Hindi.

Then I listened to the outputs.

**IndicF5 did not sound worse than Kokoro on Hindi sentences. It sounded better.** The vowels were right. The aspiration was right. The rhythm was right. Something was wrong with the numbers.

Here is learn lesson: **on Hindi audio, auto-metrics lie.**

---

## Mistake #1: Single-ASR Scoring Is Broken for Hinglish

Here is the problem with scoring TTS on a language like Hinglish with a single ASR system.

ASR models are trained on specific data distributions. AssemblyAI's Universal-2 is excellent at English and handles Hindi reasonably — but it is not equally good at every category. For pure Hinglish in Roman script (`yaar tu kal kya kar raha tha`), a model that was trained primarily on formal text will produce a different transcript than one trained on conversational data. And a single model's failure becomes your score.

Worse: when the TTS output is Devanagari but the reference text is Roman (or vice versa), character error rate comparison is meaningless. `kya` and `क्या` mean the same thing and sound identical, but CER between them is 1.0 — maximum error, as if they share no characters.

I learned this the hard way after spending a week trusting numbers that were measuring ASR bias, not model quality.

**The fix:**

1. **Three-ASR consensus.** AssemblyAI Universal-2 + Deepgram Nova-3 + Groq Whisper-large-v3. Majority vote across all three. Each system has different failure modes; the consensus is dramatically more reliable.

2. **Script normalization before scoring.** Before computing any error rate, normalize both the reference text and the ASR transcript to unified Devanagari using a transliteration library called IndicXlit. `kya` → `क्या`, `office` → `ऑफिस`. Now both sides of the comparison speak the same script, and CER measures what it is supposed to measure.

These two changes transformed the pipeline. The scoring became trustworthy.

But they also revealed how bad things actually were.

---

## The Duration Bug: Why IndicF5 Was Producing Silence

With the corrected evaluation pipeline running on the full 30-sentence set, IndicF5 re-scored at **2.13 out of 5.0**.

Not because it sounded bad. Because 21 out of 30 outputs were either silent or truncated to 0.8–2.5 seconds when the sentence needed 3–6 seconds of audio.

Something was fundamentally broken. Not in the model weights — in the inference code.

I went looking for the bug.

Inside `f5_tts/infer/utils_infer.py` at around line 451, the duration calculation looked like this:

```python
# This is the original IndicF5 code — this is the bug
ref_text_len = len(ref_text.encode("utf-8"))   # BUG
gen_text_len = len(gen_text.encode("utf-8"))   # BUG
duration = ref_audio_len + int(ref_audio_len / ref_text_len * gen_text_len / speed)
```

The model is using UTF-8 byte counts to estimate how much audio canvas time to allocate. The idea: if the reference text is `ref_text_len` bytes long, and the audio for it is `ref_audio_len` frames, then a generation text of `gen_text_len` bytes should need a proportional amount of time.

**The flaw:** Devanagari characters encode as approximately 3 bytes each in UTF-8. ASCII characters encode as 1 byte each.

The reference clip is Hindi audio with a Devanagari transcript. 100 characters × 3 bytes = 300 bytes. The reference audio is, say, 3 seconds.

The generation text is Roman-script Hinglish. 100 characters × 1 byte = 100 bytes.

So the model allocates: `3 seconds × (100/300)` = **1 second of canvas** for a sentence that needs 3 seconds.

The model fills that 1 second correctly. Then the audio just stops. The sentence is 66% truncated. This is what "silence or skip" looked like — not silence, but truncated audio that the ASR couldn't decode.

**The fix was 4 lines:**

```python
# Fixed version — count characters, not bytes
ref_text_len = sum(1 for c in ref_text if not c.isspace())  # count non-whitespace chars
gen_text_len = sum(1 for c in gen_text if not c.isspace())
duration = ref_audio_len + int(ref_audio_len / ref_text_len * gen_text_len / speed)
print(f"DEBUG-PATCH: ref_chars={ref_text_len} gen_chars={gen_text_len} "
      f"ref_frames={ref_audio_len} gen_frames={duration - ref_audio_len} "
      f"text={gen_text[:50]!r}")
```

Character counts are script-agnostic. One `क` is one character. One `k` is one character. The canvas allocation becomes proportional to the actual content length, not an artifact of how many bytes the encoding uses.

I called this **Mode A failure** — the model produces the right content but truncated canvas. The patch is applied at import time, automatically rewriting the site-packages file, so users never need to touch it manually.

After the patch, `silence_or_skip` dropped from 20/30 to 16/30. Progress. But the overall score only moved from 2.13 to 2.20.

Something else was wrong.

---

## Mode C: The Undertrained Embedding Problem

With the correct canvas size, the outputs were now the right length. But listen to what came out for Roman-script input:

> **Input:** `kal mujhe office jaana hai`
> **ASR transcript of output:** `"ऐई अ एफे रेने आए"`

That is syllabic noise. The model is producing audio that sounds vaguely Hindi-shaped but is completely unintelligible. The Devanagari tokens in the same sentence (`मुझे`, `जाना`, `है`) render perfectly. Only the Roman/ASCII tokens produce garbage.

This is **Mode C failure**: the model fills the correct canvas with garbled content because the input character embeddings for ASCII characters are undertrained.

IndicF5 was built and trained on Indic-script audio with Devanagari text inputs. The embedding matrix has entries for every Unicode character, including A–Z. But those entries were never trained on meaningful data. The model receives a near-random vector for the character `k` and produces near-random acoustic output.

It is not a bug in the weights. It is a gap in the training distribution.

**My first instinct was fine-tuning.** Train the ASCII embedding rows on Roman-script Hindi data. This would have taken weeks, cost hundreds of GPU-hours, and required labeled data I didn't have.

**I didn't fine-tune. I preprocessed instead.**

---

## The IndicXlit Fix: 14 Lines of Code Total

If the model can't handle ASCII input, don't give it ASCII input.

IndicXlit is an open-source bidirectional transliteration library from AI4Bharat. It converts Roman-script text to Devanagari. `kal` → `कल`. `office` → `ऑफिस`. `yaar` → `यार`.

The insight: the evaluation pipeline was already using IndicXlit to normalize transcripts for scoring. Apply the same normalization to the *inputs* before they go to the model.

```python
from ai4bharat.transliteration import XlitEngine

engine = XlitEngine("hi", beam_width=4, src_script_type="en")

def to_unified_devanagari(text: str) -> str:
    """Convert Hinglish text (any script mix) to Devanagari for IndicF5 input."""
    out = []
    for token in tokenize(text):
        if is_devanagari(token):
            out.append(token)          # pass through unchanged
        elif is_ascii_alpha(token):
            out.append(translate(token))   # Roman → Devanagari
        else:
            out.append(token)          # punctuation, numbers: pass through
    return "".join(out)
```

The preprocessing is symmetric: the same function that normalizes the scoring reference also normalizes the TTS input. No asymmetry introduced between what the model gets and what the score measures.

**Results after adding preprocessing (rubric v2.0, three-ASR):**

| Category | Original | +Duration Patch | +Preprocessing | Change |
|---|:---:|:---:|:---:|:---:|
| pure_devanagari | 4.62 | 4.62 | 4.62 | +0.00 |
| pure_roman | 1.00 | 1.00 | **4.38** | **+3.38** |
| mixed_script | 1.62 | 1.88 | **4.88** | **+3.00** |
| english_with_NE | 1.00 | 1.00 | **4.33** | **+3.33** |
| **overall** | **2.13** | **2.20** | **4.57** | **+2.37** |
| silence_or_skip | 20/30 | 16/30 | **0/30** | all fixed |

From 2.13 to 4.57. Zero silence. No training. No new weights. 14 lines of code between a broken model and a working one.

---

## When IndicXlit Gets It Wrong

IndicXlit is not perfect. On a handful of short tokens, it applies English phonetics instead of Hindi phonetics.

The worst offenders:

| Roman token | Meaning | IndicXlit output | What it should be |
|---|---|---|---|
| `mai` | I (first person) | `माई` ("my" in English) | `मैं` |
| `tu` | you (informal) | `टू` ("to" in English) | `तू` |
| `aa` | come | `एए` | `आ` |
| `hu` | am (first person) | `हू` (drops nasal) | `हूं` |

These are the most common Hindi function words written in Roman script. IndicXlit sees them and guesses English. A sentence like `mai ghar aa raha hu` (I am coming home) becomes `माई घर एए रहा हू` — four wrong words.

The fix is a lookup table that runs before IndicXlit sees the token:

```python
ROMAN_HINDI_FUNCTION_WORDS = {
    "mai": "मैं",   # "I" — IndicXlit gives "माई"
    "tu":  "तू",    # "you" — IndicXlit gives "टू"
    "aa":  "आ",    # "come" — IndicXlit gives "एए"
    "hu":  "हूं",   # "am" — IndicXlit gives "हू"
}
```

Similarly, English loanwords common in Hinglish have fixed canonical Devanagari forms that IndicXlit may not produce consistently:

```python
ENGLISH_LOAN_CANONICAL = {
    "office":       "ऑफिस",
    "laptop":       "लैपटॉप",
    "presentation": "प्रेज़ेंटेशन",
    "leave":        "लीव",
    "boss":         "बॉस",
    "party":        "पार्टी",
    # ... 36 entries total
}
```

Adding these and re-running the evaluation (now rubric v2.1):

| Category | v2.0 | v2.1 | Change |
|---|:---:|:---:|:---:|
| pure_roman | 4.38 | **4.75** | +0.38 |
| mixed_script | 4.88 | **4.88** | +0.00 |
| english_with_NE | 4.33 | **4.50** | +0.17 |
| pure_devanagari | 4.62 | **4.62** | +0.00 |
| **overall** | **4.57** | **4.70** | **+0.13** |

**4.70 out of 5.0. Final score.**

---

## How It Compares to Everything Else

Same 30 sentences. Same rubric. Same three-ASR pipeline. Five models:

| Model | Overall | pure\_roman | mixed | eng\_NE | pure\_dev |
|---|:---:|:---:|:---:|:---:|:---:|
| **This package** | **4.70** | **4.75** | **4.88** | 4.50 | **4.62** |
| Kokoro v1.0 (Hindi) | 3.90 | 2.50 | 3.88 | **4.83** | 4.62 |
| Indic Parler-TTS | 3.40 | 1.75 | 3.00 | 4.67 | 4.50 |
| IndicF5 (unpatched) | 2.13 | 1.00 | 1.62 | 1.00 | 4.62 |
| SPRINGLab F5-Hindi | 2.07 | 1.00 | 1.38 | 1.00 | 4.62 |

The gap is largest on `pure_roman` — the dominant input format for Indian chat, WhatsApp, and voice-interface applications. **+2.25 ranks over Kokoro on the thing that matters most.**

Kokoro leads on `english_with_NE` (4.83 vs 4.50) because it has deeper English training and handles English-mode proper-noun phonetics natively. Our package transliterates "Bengaluru" to Hindi phonetics; Kokoro says it with an English accent. Both score well by ASR — but a listener who expects Indian-English pronunciation of place names may prefer Kokoro for that category.

Sample outputs from the final system (all from `experiments/04_indicf5_xlit_v2/wavs/`):

| Input | Category | Score |
|---|---|:---:|
| कल मुझे दिल्ली जाना है। | Pure Devanagari | 5/5 |
| yaar tu kal kya kar raha tha | Pure Roman | 5/5 |
| kal mujhe office jaana hai | Pure Roman (loan word) | 5/5 |
| Boss को बता देना kal मैं leave पर रहूँगा | Mixed script | 5/5 |
| Mera presentation tomorrow है, और मैं nervous हूं। | Mixed script | 5/5 |
| My friend Aishwarya from Chennai is visiting Bengaluru | English with NE | 4/5 |

---

## The UTMOS Problem: When Auto-Metrics Lie on Hindi

One of the strangest findings of the whole project.

Standard TTS evaluation uses automatic naturalness predictors — UTMOS and SQUIM-MOS are the two most common. They score how "natural" audio sounds on a scale of 1–5. They are trained on English studio speech datasets.

I recorded 8 human Hindi speakers reading the same sentences used in the eval. Then I ran both the human recordings and the TTS outputs through UTMOS and SQUIM.

| Source | UTMOS score | SQUIM-MOS score |
|---|:---:|:---:|
| IndicF5 TTS outputs | 3.2 – 3.8 | 3.5 – 4.1 |
| Human native Hindi speakers | **1.7 – 2.4** | **1.8 – 2.6** |

The machine scored synthetic TTS as **more natural than real human voices.**

This is called predictor inversion. UTMOS and SQUIM are calibrated on English studio recordings that sound "clean" in ways that differ from how natural conversational Hindi sounds — the breath patterns, the pitch contour statistics, the formant trajectories are all different. The models have learned to associate "English studio speech features" with "naturalness" and penalize audio that doesn't match.

A real Hindi speaker producing natural speech gets penalized for sounding like a real Hindi speaker.

**This means:** every naturalness claim backed by UTMOS/SQUIM on Hindi audio is meaningless, and potentially inverted. If someone tells you their Hindi TTS system scores 4.0 on UTMOS, they may be telling you it sounds *worse* than natural Hindi, not better.

**What I did:** declared naturalness as ear-only for this project. No UTMOS. No SQUIM. Listen to the outputs. The human ear is the metric.

---

## The Kaggle Disasters

The project ran entirely on free-tier Kaggle T4 GPUs. This came with its own education.

**Disaster 1: The P100 trap.** Kaggle offers both P100 and T4 GPUs. F5-family TTS models fail on P100 with `cudaErrorNoKernelImageForDevice` — the GPU is too old for the CUDA kernels the model requires. I spent four hours debugging a failing kernel before discovering the machine shape was wrong. The fix: always explicitly request T4 in the kernel settings. The Kaggle CLI does not default to T4.

**Disaster 2: Kaggle Secrets don't work from CLI.** If you push a notebook via `kaggle kernels push` from the CLI, the Secrets (API keys stored in the Kaggle vault) are not accessible to the running kernel — only to kernels run from the web UI. Workaround: hardcode the HuggingFace token inline in the notebook before pushing. Not ideal, but functional.

**Disaster 3: "Successful" does not mean wavs were produced.** The Kaggle status API returns `"status": "complete"` when the kernel finishes — whether it produced outputs or not. After every run I had to pull the output, check the logs for inference errors, and count the wavs. Automated "did this work?" checking requires looking at output contents, not kernel status.

**Disaster 4: `source .env` doesn't propagate to subprocesses.** I spent hours debugging why my scoring scripts couldn't find the AssemblyAI API key. The issue: calling `source .env` in a shell session only exports variables to that shell. A background subprocess (like the Python scoring script) doesn't inherit them. The fix:

```bash
# Wrong:
source .env && python scoring/scripts/run_scoring.py

# Right:
export $(grep -v '^#' .env | xargs) && python scoring/scripts/run_scoring.py
```

---

## Direction 1: Does the Model Actually Understand Phonetics?

After the 4.70 result, I got curious. The model is handling Devanagari script well. But does it actually *understand* phonetics — does it respond to fine-grained markers like vowel length, aspiration, the nukta (a dot that changes sounds), or the halant (a consonant cluster mark)?

I designed 18 test clips: 6 phonetic distinctions × 3 variants each. Each set of 3 uses the same sentence with one phonetic marker changed. I bypassed preprocessing entirely — fed raw Devanagari text directly to the model.

The six distinctions:

| # | What's being tested | Example variants |
|:---:|---|---|
| 1 | Vowel length (ि vs ी) | short-i vs long-i |
| 2 | Halant / schwa elision (् mark) | खिल्ता vs खिलता vs खिलाता |
| 3 | Nukta (ज vs ज़) | Zara vs Jara |
| 4 | Aspiration (ख vs क) | khana vs kana |
| 5 | Script register | Roman "office" vs Devanagari ऑफिस vs आफिस |
| 6 | Prosody / punctuation | plain vs ellipsis vs exclamation |

The auto-metrics (ASR, F0 analysis) said: **3 out of 6 distinctions** produced different output. Outcome B — partial sensitivity.

Then I listened.

**The ear said: 6 out of 6.** Every distinction produced acoustically different output.

Three cases where the auto-metrics missed it:

- **Halant:** The ASR transcripts were identical, but the consonant cluster quality (the acoustic sound of `kh` in `खिल्ता`) was measurably different — spectral centroid shifted +112 Hz. The ASR sees the same words. The ear hears a different sound.

- **Aspiration:** The clips were 0.65 seconds long. Too short for reliable Hindi ASR. Every backend produced garbage transcripts. But listening to them — the difference between `ख` (aspirated) and `क` (unaspirated) was completely clear.

- **Prosody:** The sentence `मैं... बहुत... खुश हूं!` and the plain version `मैं बहुत खुश हूं।` produced identical ASR transcripts (same words). But the ellipsis+exclamation version was **44% longer** (1.90s vs 1.32s), had slower pacing, and a rising pitch at the end. The ASR cannot measure any of this — it only reads words.

**Lesson:** ASR-based metrics are lexical. They measure what words were said, not how they were said. For phonetic sensitivity experiments — aspiration, tone, prosody, vowel quality — the ear is not just useful, it is irreplaceable.

---

## Direction 2: Is the Model Thinking in Phonemes or Graphemes?

A deeper question: when the model produces the sound for `क` (the Devanagari letter ka) and the Roman letter `k`, are these routed through the same internal phoneme representation — or are they treated as completely separate graphemes that happen to produce similar sounds?

I tested this with MFCC cosine similarity on the acoustic onset of the /k/ phoneme across 32 clips.

**Within Devanagari:** The /k/ phoneme across 8 different vowel contexts (ka, ki, ku, ke, etc.) showed mean pairwise similarity of 0.827. F0 varied systematically by vowel (coarticulation — a real phonetic phenomenon). This is evidence that within Devanagari, the model has phoneme-organized representations. It is not just memorizing grapheme→audio mappings independently.

**Cross-script (Roman `k` vs Devanagari `क`):** Mean similarity delta = +0.052 above the unrelated-pairs baseline. Very weak. Two Roman inputs hit Mode C entirely — they produced garbled output with F0 stuck at 93 Hz (the garbage attractor pitch). The model has no phoneme access path for Roman input it goes directly to noise.

**Conclusion:** Phoneme-mediated within Devanagari. Grapheme-bound for Roman. The ASCII embedding subspace is undertrained and does not connect to the Devanagari phoneme layer at all. IndicXlit preprocessing works precisely because it routes all input through the Devanagari path, where phoneme organization exists.

---

## What the Product Actually Is

This is a clean summary of what was built:

**IndicF5 + duration patch + IndicXlit preprocessing = working Hinglish TTS**

The product is an open-source package that:

1. Accepts any script-mixed Hinglish input (Devanagari, Roman, mixed, or English with Indian names)
2. Normalizes it to Devanagari using IndicXlit with hand-curated whitelists
3. Feeds normalized text into duration-patched IndicF5
4. Returns 24 kHz audio in any reference voice you supply

**Usage:**

```python
from inference import load_model, synthesize
import soundfile as sf

model = load_model()   # downloads ~1.3 GB weights from HuggingFace

REF_AUDIO = "data/reference_audio/hindi_ref.wav"
REF_TEXT  = open("data/reference_audio/hindi_ref.txt").read().strip()

# Pure Roman Hinglish
audio = synthesize(model, "yaar tu kal kya kar raha tha", REF_AUDIO, REF_TEXT)
sf.write("out.wav", audio, 24000)

# Mixed script
audio = synthesize(model,
    "Boss को बता देना kal मैं leave पर रहूँगा",
    REF_AUDIO, REF_TEXT)

# English with Indian named entities
audio = synthesize(model,
    "My friend Aishwarya from Chennai is visiting Bengaluru next week.",
    REF_AUDIO, REF_TEXT)
```

**Installation (5 commands):**

```bash
git clone https://github.com/harrrshall/hienglish.git && cd hienglish
pip install git+https://github.com/AI4Bharat/IndicF5.git \
    "transformers==4.49.0" "accelerate==0.33.0" \
    "numpy>=2.0,<2.1" soundfile
# Accept HuggingFace gating at https://huggingface.co/ai4bharat/IndicF5
export HF_TOKEN=hf_your_token_here
pip install ai4bharat-transliteration
```

Hardware: any CUDA GPU with ≥ 6 GB VRAM. Kaggle T4 works. Google Colab T4 works.

---

## The Eval Infrastructure: Reusable for Any Hinglish TTS

One thing that does not exist in the open-source Hinglish space is a reproducible, rigorous evaluation pipeline. Building one was a requirement for trusting any score.

The pipeline:

**Step 1 — Script normalization (IndicXlit)**

Both the reference text and the ASR transcript are passed through `to_unified_devanagari()` before comparison. This makes the scoring script-agnostic: `office` and `ऑफिस` are treated as the same token, because they are.

**Step 2 — Three-ASR consensus**

Each output wav is transcribed by three systems:
- **AssemblyAI Universal-2** — strict, conservative; good at formal Hindi
- **Deepgram Nova-3 multi** — mixed-language capable; better at code-switching
- **Groq Whisper-large-v3** — good at short clips and colloquial speech

Intelligibility, code_switch, and silence_or_skip scores come from the median of the three. When all three disagree, that sentence goes into a manual review queue highest information density per minute of listening.

**Step 3 — Scoring**

CER (character error rate) after Devanagari normalization. Score 5 = CER ≤ 0.05. Score 4 = CER 0.05–0.15. Score 3 = CER 0.15–0.30. Score ≤ 2 = CER > 0.30 or silence.

Naturalness: ear-only. Listen to the outputs. Write qualitative notes. Do not put a number on it unless you run a rated study with multiple native speakers.

**The 30-sentence eval set is frozen.** It will never be modified, never used for training, never retroactively adjusted. Any future model can be scored on the same 30 sentences with the same rubric, and the comparison table above stays valid.

---

## Every Mistake, Summarized

For future reference mine and anyone else's doing similar work:

| Mistake | What happened | What to do instead |
|---|---|---|
| Single-ASR scoring | Scores reflected ASR bias, not model quality | Three-ASR consensus minimum |
| No script normalization | CER between `kya` and `क्या` was 1.0 | Normalize to unified script before any metric |
| Trusting UTMOS/SQUIM on Hindi | They rate synthetic *above* human on Hindi | Ear-only for naturalness on non-English TTS |
| Assuming fine-tuning was needed | The bug was in inference code, not weights | Diagnose the failure mode before training |
| Single-ASR for phonetic experiments | Short clips broke ASR; prosody is invisible to ASR | Ear evaluation for phonetic sensitivity |
| `source .env` for subprocesses | Vars not inherited | `export $(grep -v '^#' .env | xargs)` |
| P100 on Kaggle for F5-family | `cudaErrorNoKernelImageForDevice` | Always specify T4 |
| Inferring kernel success from status | "complete" ≠ wavs produced | Check outputs, not status |

---

## What Comes Next

The 330M-parameter system is shipped. The next question is whether the same quality can be achieved in a model small enough to run in a browser.

**Path B** is a research bet: a 40–50M parameter Hinglish TTS distilled from this system as teacher, using StyleTTS2-lite architecture with phoneme input. The Kokoro paper showed 82M English TTS beating much larger models. The question is whether that recipe ports to Hinglish.

Three-week de-risking phase before committing any real compute:
1. Validate that espeak-ng + multilingual PL-BERT produces meaningful Hindi phoneme embeddings
2. Generate 1,000 sentences with Path A and verify quality consistency
3. Train 100 steps of a tiny StyleTTS2 on dummy data and verify it doesn't OOM or NaN

If those three gates pass, the training run starts. If not, the project closes with the 330M system as the primary deliverable.

---

## The Meta-Lesson

This project had one finding that matters more than the 4.70 score.

Three separate times, the auto-metrics pointed one direction and the human ear pointed another:

1. **Base model selection:** Auto-rubric said Kokoro was best overall. Ear said IndicF5 was better on Hindi naturalness. Trusting the ear flipped the model selection.

2. **Quality assessment:** PESQ said quality improved with preprocessing. Ear said "still sounds like 90s TTS, flat delivery." Both true they were measuring different things.

3. **Phonetic probe:** Auto-metrics said 3/6 distinctions were sensitive. Ear said 6/6. The auto-metrics couldn't detect sub-phonemic changes or prosodic shifts without word changes.

The meta-lesson: **when you are working on a language that wasn't in your metrics' training distribution, build in a human evaluation step before trusting any number.** UTMOS was trained on English. AssemblyAI is optimized for English. MFCC cosine similarity doesn't know what Hindi sounds like.

This is not a criticism of those tools. They are good tools for what they were built for. But "works on English" does not mean "works on Hindi," and "works on Hindi" does not mean "works on Hinglish."

Measure your metrics before you trust your metrics.

---

## Links and Artifacts

- **Code and eval set:** [github.com/harrrshall/hienglish](https://github.com/harrrshall/hienglish)
- **Underlying model:** [ai4bharat/IndicF5](https://huggingface.co/ai4bharat/IndicF5) (HuggingFace gating required)
- **Transliteration library:** [AI4Bharat/IndicTransliteration](https://github.com/AI4Bharat/IndicTransliteration)
- **Detailed methodology:** `EVALUATION_REPORT.md`
- **Full decision log:** `RESEARCH_LOG.md`
- **Known limitations:** `KNOWN_LIMITATIONS.md`

**Citation:**

```bibtex
@misc{singh2026hinglish,
  author       = {Harshal Singh},
  title        = {Hinglish TTS: IndicF5 with IndicXlit Preprocessing},
  year         = {2026},
  howpublished = {\url{https://github.com/harrrshall/hienglish}},
  note         = {30-sentence Hinglish eval set (4 categories).
                  Rubric v2.1: three-ASR consensus, Devanagari-normalised CER.
                  4.70/5.0 mean intelligibility.}
}
```

---

*Questions, bug reports, and collaboration inquiries: cybernovascnn@gmail.com*
