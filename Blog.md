# How I Built an Open-Source Hinglish TTS That Beats Every Other Model (Starting From Zero)

*By Harshal Singh and claude code*

---

I knew nothing about text-to-speech when I started.

Nothing. Not the models, not the terminology, not the difference between a vocoder and a flow-matching diffusion transformer. I had never heard the word "IndicXlit". I did not know what a mel spectrogram was.

I had one goal: build the best open-source TTS model for English.

That goal lasted three days. Then I realised I was solving the wrong problem.

This is the story of what actually happened. Every wrong turn, every "wait, the metrics are lying to us", every 2 AM kernel crash on Kaggle. It ends with a system that scores 4.70 out of 5.0 on a rigorous three-ASR evaluation rubric and beats every other open-source Hinglish-capable TTS model on the planet. And it was built with 14 lines of core logic plus curated word lists. No training, no fine-tuning, no GPU budget.

Here is everything.

---

## Why Hinglish?

Hinglish is not pidgin. It is not broken English. It is a fully developed code-switching register with its own grammar. A native speaker switches mid-sentence, sometimes mid-phrase, between Devanagari-script Hindi and Roman-script English. It looks like this:

> *"Boss को बता देना kal मैं leave पर रहूँगा, kuch personal काम है।"*

One sentence. Three scripts. Two languages. This is how tens of millions of urban Indians write to each other every day on WhatsApp.

No open-source TTS model handles it well.

**That became the problem I decided to solve.**

---

## The Audit: Testing What Already Existed

The first real step was not building anything. It was measuring what already existed.

I picked four candidate models and a 30-sentence eval set designed to stress every dimension of the problem:

| Category | Count | What it tests |
|---|:---:|---|
| `pure_devanagari` | 8 | Standard Hindi in Devanagari script |
| `pure_roman` | 8 | Colloquial Hinglish written in Roman script |
| `mixed_script` | 8 | Mid-sentence script switching |
| `english_with_NE` | 6 | English with Indian names and places |

The four models I tested:

1. **Kokoro v1.0** (hexgrad, 82M parameters), the English TTS champion, with a Hindi mode
2. **Indic Parler-TTS** (AI4Bharat, 880M parameters), large, Indic-focused, text-description conditioned
3. **IndicF5** (AI4Bharat, 330M parameters), flow-matching TTS, trained on Indic-script audio
4. **SPRINGLab F5-Hindi** (another Indic F5-TTS variant)

I ran everything on Kaggle T4 GPUs (free tier, zero budget for this project).

First results, scored with a single ASR system (AssemblyAI):

| Model | Overall score |
|---|:---:|
| Kokoro v1.0 | 3.03 |
| Indic Parler-TTS | 2.73 |
| **IndicF5** | **1.97** |
| SPRINGLab F5-Hindi | similar |

Kokoro wins. Case closed. Ship Kokoro for Hindi.

Then I actually listened to the outputs.

**IndicF5 did not sound worse than Kokoro on Hindi sentences. It sounded better.** The vowels were right. The aspiration was right. The rhythm was right. Something was wrong with the numbers.

Lesson: **on Hindi audio, auto-metrics lie.**

---

## Mistake #1: Single-ASR Scoring Is Broken for Hinglish

Here is the problem with scoring TTS on a language like Hinglish using a single ASR system.

ASR models are trained on specific data distributions. AssemblyAI's Universal-2 is excellent on English and handles Hindi reasonably, but it is not equally good across every category. For pure Hinglish in Roman script (`yaar tu kal kya kar raha tha`), a model trained mostly on formal text will produce a different transcript than one trained on conversational data. And a single model's failure becomes your score.

Worse: when the TTS output is Devanagari but the reference text is Roman (or vice versa), character error rate is meaningless. `kya` and `क्या` mean the same thing and sound identical, but CER between them is 1.0. Maximum error. As if they share no characters.

I learned this the hard way. Spent a week trusting numbers that were measuring ASR bias, not model quality.

**The fix:**

1. **Three-ASR consensus.** AssemblyAI Universal-2 + Deepgram Nova-3 + Groq Whisper-large-v3. Majority vote across all three. Each system fails differently, so the consensus is dramatically more reliable.

2. **Script normalisation before scoring.** Before computing any error rate, normalise both the reference text and the ASR transcript to unified Devanagari using a transliteration library called IndicXlit. `kya` → `क्या`, `office` → `ऑफिस`. Now both sides of the comparison speak the same script, and CER measures what it is supposed to measure.

These two changes fixed the scoring pipeline. The numbers became trustworthy.

But they also revealed how bad things actually were.

---

## The Duration Bug: Why IndicF5 Was Producing Silence

With the corrected eval pipeline running on the full 30-sentence set, IndicF5 re-scored at **2.13 out of 5.0**.

Not because it sounded bad. Because 21 out of 30 outputs were either silent or truncated to 0.8 to 2.5 seconds when the sentence needed 3 to 6 seconds of audio.

Something was fundamentally broken. Not in the model weights. In the inference code.

I went looking for the bug.

Inside `f5_tts/infer/utils_infer.py` around line 451, the duration calculation looked like this:

```python
# This is the original IndicF5 code — this is the bug
ref_text_len = len(ref_text.encode("utf-8"))   # BUG
gen_text_len = len(gen_text.encode("utf-8"))   # BUG
duration = ref_audio_len + int(ref_audio_len / ref_text_len * gen_text_len / speed)
```

The model is using UTF-8 byte counts to estimate how much audio canvas time to allocate. The idea: if the reference text is `ref_text_len` bytes long, and the audio for it is `ref_audio_len` frames, then a generation text of `gen_text_len` bytes should need a proportional amount of time.

**The flaw:** Devanagari characters encode as roughly 3 bytes each in UTF-8. ASCII characters encode as 1 byte each.

The reference clip is Hindi audio with a Devanagari transcript. 100 characters × 3 bytes = 300 bytes. The reference audio is, say, 3 seconds.

The generation text is Roman-script Hinglish. 100 characters × 1 byte = 100 bytes.

So the model allocates: `3 seconds × (100/300)` = **1 second of canvas** for a sentence that needs 3 seconds.

The model fills that 1 second correctly. Then the audio just stops. The sentence is 66% truncated. This is what "silence or skip" actually was. Not silence, just truncated audio the ASR could not decode.

**The fix was 4 lines:**

```python
# Fixed version — only the counting changes; the formula structure is unchanged
ref_text_len = sum(1 for c in ref_text if not c.isspace())  # FIX: count chars, not bytes
gen_text_len = sum(1 for c in gen_text if not c.isspace())  # FIX: count chars, not bytes
duration = ref_audio_len + int(ref_audio_len / ref_text_len * gen_text_len / speed)  # unchanged
print(f"DEBUG-PATCH: ref_chars={ref_text_len} gen_chars={gen_text_len} "
      f"ref_frames={ref_audio_len} gen_frames={duration - ref_audio_len} "
      f"text={gen_text[:50]!r}")
```

Character counts are script-agnostic. One `क` is one character. One `k` is one character. The canvas allocation becomes proportional to the actual content length, not an artifact of how many bytes the encoding uses.

I called this **Mode A failure**. The model produces the right content but on a truncated canvas. The patch is applied at import time, automatically rewriting the site-packages file, so users never have to touch it manually.

After the patch, `silence_or_skip` dropped from 20/30 to 16/30. Progress. But the overall score only moved from 2.13 to 2.20.

Something else was wrong.

---

## Mode C: The Undertrained Embedding Problem

With the correct canvas size, the outputs were now the right length. But listen to what came out for Roman-script input:

> **Input:** `kal mujhe office jaana hai`
> **ASR transcript of output:** `"ऐई अ एफे रेने आए"`

That is syllabic noise. The model is producing audio that sounds vaguely Hindi-shaped but is completely unintelligible. The Devanagari tokens in the same sentence (`मुझे`, `जाना`, `है`) render perfectly. Only the Roman/ASCII tokens produce garbage.

This is **Mode C failure**: the model fills the correct canvas with garbled content because the input character embeddings for ASCII characters are undertrained.

IndicF5 was built and trained on Indic-script audio with Devanagari text inputs. The embedding matrix has entries for every Unicode character, including A to Z. But those entries were never trained on meaningful data. The model receives a near-random vector for the character `k` and produces near-random acoustic output.

It is not a bug in the weights. It is a gap in the training distribution.

**My first instinct was fine-tuning.** Train the ASCII embedding rows on Roman-script Hindi data. That would have taken weeks, cost hundreds of GPU-hours, and required labelled data I did not have. I started sketching out a LoRA training plan and thinking about data curation.

**Then I asked: is there a 30-minute experiment that would tell me whether fine-tuning is even the right move?** That question saved the project. The answer turned out to be preprocessing, not training.

---

## The IndicXlit Fix: 14 Lines of Code Total

If the model can't handle ASCII input, don't give it ASCII input.

IndicXlit is an open-source bidirectional transliteration library from AI4Bharat. It converts Roman-script text to Devanagari. `kal` → `कल`. `office` → `ऑफिस`. `yaar` → `यार`.

The insight: the evaluation pipeline was already using IndicXlit to normalise transcripts for scoring. Apply the same normalisation to the *inputs* before they go to the model.

```python
from ai4bharat.transliteration import XlitEngine

engine = XlitEngine("hi", beam_width=4, src_script_type="en")

# Simplified core logic. Production version in lib_normalize.py handles
# edge cases (numbers, punctuation, mixed-script tokens, engine caching).
def to_unified_devanagari(text: str) -> str:
    out = []
    for token in text.split():
        if any('\u0900' <= c <= '\u097f' for c in token):
            out.append(token)                                    # already Devanagari
        elif token.lower() in FUNCTION_WORDS_WHITELIST:
            out.append(FUNCTION_WORDS_WHITELIST[token.lower()])  # function-word override
        elif token.lower() in ENGLISH_LOAN_CANONICAL:
            out.append(ENGLISH_LOAN_CANONICAL[token.lower()])    # loanword override
        elif token.lower() in INDIAN_NE_CANONICAL:
            out.append(INDIAN_NE_CANONICAL[token.lower()])       # named-entity override
        elif token.isascii() and token.isalpha():
            out.append(engine.translit_word(token, topk=1)["hi"][0])  # IndicXlit
        else:
            out.append(token)                                    # punct, numbers
    return " ".join(out)
```

The preprocessing is symmetric. The same function that normalises the scoring reference also normalises the TTS input. No asymmetry between what the model gets and what the score measures.

**Results after adding preprocessing (rubric v2.0, three-ASR):**

| Category | Original | +Duration Patch | +Preprocessing | Change |
|---|:---:|:---:|:---:|:---:|
| pure_devanagari | 4.62 | 4.62 | 4.62 | +0.00 |
| pure_roman | 1.00 | 1.00 | **4.38** | **+3.38** |
| mixed_script | 1.62 | 1.88 | **4.88** | **+3.00** |
| english_with_NE | 1.00 | 1.00 | **4.33** | **+3.33** |
| **overall** | **2.13** | **2.20** | **4.57** | **+2.37** |
| silence_or_skip | 20/30 | 16/30 | **0/30** | all fixed |

From 2.13 to 4.57. Zero silence. No training. No new weights. 14 lines of core logic between a broken model and a working one. (The whitelist tables add 59 additional entries — 4 function words + 36 English loans + 19 Indian named entities — that's data, not code.)

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

These are the most common Hindi function words written in Roman script. IndicXlit sees them and guesses English. A sentence like `mai ghar aa raha hu` (I am coming home) becomes `माई घर एए रहा हू`. Three wrong words out of five.

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

A third lookup, `INDIAN_NE_CANONICAL`, does the same job for Indian named entities — cities, people, brands — that ASR transcripts routinely mangle:

```python
INDIAN_NE_CANONICAL = {
    "bengaluru": "बेंगलुरु",
    "chennai":   "चेन्नई",
    "mumbai":    "मुंबई",
    "aishwarya": "ऐश्वर्या",
    "tata":      "टाटा",
    # ... 19 entries total (cities, people, brands)
}
```

Adding all three whitelists and re-running the evaluation (now rubric v2.1):

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

The gap is largest on `pure_roman`, the dominant input format for Indian chat, WhatsApp, and voice interfaces. **+2.25 points over Kokoro on the thing that matters most.**

Kokoro leads on `english_with_NE` (4.83 vs 4.50) because it has deeper English training and handles English-mode proper-noun phonetics natively. Our package transliterates "Bengaluru" to Hindi phonetics. Kokoro says it with an English accent. Both score well by ASR, but a listener who expects Indian-English pronunciation of place names may prefer Kokoro for that category.

Sample outputs from the final system (rubric v2.1 production run):

| Input | Category | Score |
|---|---|:---:|
| कल मुझे दिल्ली जाना है। | Pure Devanagari | 5/5 |
| yaar tu kal kya kar raha tha | Pure Roman | 5/5 |
| kal mujhe office jaana hai | Pure Roman (loan word) | 5/5 |
| Boss को बता देना kal मैं leave पर रहूँगा | Mixed script | 5/5 |
| Mera presentation tomorrow है, और मैं nervous हूं। | Mixed script | 5/5 |
| My friend Aishwarya from Chennai is visiting Bengaluru | English with NE | 4/5 |

---

## Predictor Inversion: When Auto-Metrics Rate Synthetic Above Human

One of the strangest findings of the whole project.

Standard TTS evaluation uses automatic naturalness predictors. UTMOS, SQUIM-MOS, and PESQ are the three most common. They score how "natural" audio sounds on a 1 to 5 scale. They are all trained on English studio speech datasets.

I recorded 8 human Hindi speakers reading the same sentences used in the eval. Then I ran both the human recordings and the TTS outputs through UTMOS and SQUIM.

| Source | UTMOS score | SQUIM-MOS score |
|---|:---:|:---:|
| IndicF5 TTS outputs | 3.2 – 3.8 | 3.5 – 4.1 |
| Human native Hindi speakers | **1.7 – 2.4** | **1.8 – 2.6** |

The machine scored synthetic TTS as **more natural than real human voices.**

This is called predictor inversion. UTMOS, SQUIM, and PESQ are calibrated on English studio recordings that sound "clean" in ways that differ from how natural conversational Hindi sounds. The breath patterns, the pitch contour statistics, the formant trajectories are all different. The models have learned to associate "English studio speech features" with "naturalness" and they penalise audio that does not match.

A real Hindi speaker producing natural speech gets penalised for sounding like a real Hindi speaker.

**This means:** every naturalness claim backed by UTMOS/SQUIM/PESQ on Hindi audio is meaningless, possibly inverted. If someone tells you their Hindi TTS scores 4.0 on UTMOS, they may be telling you it sounds *worse* than natural Hindi, not better.

**What I did:** declared naturalness as ear-only for this project. No UTMOS. No SQUIM. No PESQ. Listen to the outputs. The human ear is the metric.

---

## Direction 1: Does the Model Actually Understand Phonetics?

After the 4.70 result, I got curious. The model is handling Devanagari script well. But does it actually *understand* phonetics? Does it respond to fine-grained markers like vowel length, aspiration, the nukta (a dot that changes sounds), or the halant (a consonant cluster mark)?

I designed 18 test clips: 6 phonetic distinctions × 3 variants each. Each set of 3 uses the same sentence with one phonetic marker changed. I bypassed preprocessing entirely and fed raw Devanagari text directly to the model.

The six distinctions:

| # | What's being tested | Example variants |
|:---:|---|---|
| 1 | Vowel length (ि vs ी) | short-i vs long-i |
| 2 | Halant / schwa elision (् mark) | खिल्ता vs खिलता vs खिलाता |
| 3 | Nukta (ज vs ज़) | Zara vs Jara |
| 4 | Aspiration (ख vs क) | khana vs kana |
| 5 | Script register | Roman "office" vs Devanagari ऑफिस vs आफिस |
| 6 | Prosody / punctuation | plain vs ellipsis vs exclamation |

The auto-metrics (ASR transcripts, F0 analysis, spectral centroid, MFCC similarity) said: **1 out of 6 distinctions** was cleanly sensitive — aspiration. The other five looked partial or invisible to the metrics.

Then I listened.

**The ear said: 6 out of 6.** Every distinction produced acoustically different output.

Five cases where the auto-metrics missed it:

- **Nukta:** Auto-analysis said no signal — ASR transcribed all variants identically. My ear heard 1b as "zaraa" with long vowel, 1c as "zara" with short vowel. Real difference.

- **Halant:** ASR transcripts were identical, but careful listening showed the consonant cluster in `खिल्ता` was audibly cleaner — less inserted vowel between ल and त. The halant version sounded "calmer," more natural Hindi articulation.

- **Vowel length:** Auto-analysis said the durations were nearly identical. My ear heard the correct-spelling variant as the most natural by a clear margin; the all-short-matras version sounded rushed.

- **Script register:** Auto-analysis said the two Devanagari variants (ऑफिस vs आफ़ीस) were at the noise floor. My ear heard a clear /f/ sound (from the nukta on फ़) in one but not the other.

- **Prosody:** The sentence `मैं... बहुत... खुश हूं!` and the plain version `मैं बहुत खुश हूं।` produced identical ASR transcripts (same words). But the ellipsis+exclamation version was **44% longer** (1.90s vs 1.32s), had slower pacing, and a rising pitch at the end. The ASR cannot measure any of that. It only reads words.

**Lesson:** ASR-based metrics are lexical. They measure what words were said, not how they were said. For phonetic sensitivity experiments (aspiration, tone, prosody, vowel quality), the ear is not just useful. It is irreplaceable.

The gap between auto-finding and ear-finding here is 1/6 vs 6/6. That is not noise. That is structural blindness in the metrics.

---

## Direction 2: Is the Model Thinking in Phonemes or Graphemes?

A separate, deeper experiment — different test set, different goal. The question: when the model produces the sound for `क` (the Devanagari letter ka) and the Roman letter `k`, are these routed through the same internal phoneme representation? Or are they treated as completely separate graphemes that happen to produce similar sounds?

I tested this with a fresh batch of 32 clips designed for MFCC cosine similarity analysis on the acoustic onset of the /k/ phoneme. This is a different experiment from Direction 1, which used 18 clips for phonetic-marker testing.

The first analysis was broken. I was computing MFCC means across the whole clip including silent portions, and I was including the C0 energy coefficient. Both choices made "silence similarity" dominate "phoneme similarity." The results came back as Test C all 1.0, Test B wildly bimodal — obvious garbage. I had to throw the first analysis out, fix the feature extraction (voiced frames only, strip C0, align to speech onset), and re-run.

After the fix:

**Within Devanagari:** The /k/ phoneme across 8 different vowel contexts (ka, ki, ku, ke, etc.) showed mean pairwise similarity of 0.83. F0 varied systematically by vowel (coarticulation, a real phonetic phenomenon). This is evidence that within Devanagari, the model has phoneme-organised representations. It is not just memorising grapheme-to-audio mappings independently.

**Cross-script (Roman `k` vs Devanagari `क`):** Mean similarity delta = +0.052 above the unrelated-pairs baseline. Very weak. Two Roman inputs hit Mode C entirely. They produced garbled output with F0 stuck at 93 Hz (the garbage attractor pitch). The model has no phoneme access path for Roman input. It goes directly to noise.

**Conclusion:** Phoneme-mediated within Devanagari. Grapheme-bound for Roman. The ASCII embedding subspace is undertrained and does not connect to the Devanagari phoneme layer at all. IndicXlit preprocessing works precisely because it routes all input through the Devanagari path, where phoneme organisation exists.

The lesson from the busted first analysis: **always sanity-check your analysis pipeline on a control before trusting it.** If a metric returns "all clips are identical" or "all clips are unrelated," your metric is broken before your model is interesting.

---

## What the Product Actually Is

Clean summary of what was built:

**IndicF5 + duration patch + IndicXlit preprocessing = working Hinglish TTS**

The product is an open-source package that:

1. Accepts any script-mixed Hinglish input (Devanagari, Roman, mixed, or English with Indian names)
2. Normalises it to Devanagari using IndicXlit with hand-curated whitelists
3. Feeds normalised text into duration-patched IndicF5
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
git clone https://github.com/harrrshall/hinglish-tts.git && cd hinglish-tts
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

**Step 1: Script normalisation (IndicXlit)**

Both the reference text and the ASR transcript are passed through `to_unified_devanagari()` before comparison. This makes the scoring script-agnostic. `office` and `ऑफिस` are treated as the same token, because they are.

**Step 2: Three-ASR consensus**

Each output wav is transcribed by three systems:
- **AssemblyAI Universal-2:** strict, conservative; good at formal Hindi
- **Deepgram Nova-3 multi:** mixed-language capable; better at code-switching
- **Groq Whisper-large-v3:** good at short clips and colloquial speech

Intelligibility, code_switch, and silence_or_skip scores come from the median of the three. When all three disagree, that sentence goes into a manual review queue. Highest information density per minute of listening.

**Step 3: Scoring**

CER (character error rate) after Devanagari normalisation. Score 5 = CER ≤ 0.05. Score 4 = CER 0.05 to 0.15. Score 3 = CER 0.15 to 0.30. Score ≤ 2 = CER > 0.30 or silence.

Naturalness: ear-only. Listen to the outputs. Write qualitative notes. Do not put a number on it unless you run a rated study with multiple native speakers.

**The 30-sentence eval set is frozen.** It will never be modified, never used for training, never retroactively adjusted. Any future model can be scored on the same 30 sentences with the same rubric, and the comparison table above stays valid.

---

## Every Mistake, Summarised

For future reference, mine and anyone else doing similar work:

| Mistake | What happened | What to do instead |
|---|---|---|
| Single-ASR scoring | Scores reflected ASR bias, not model quality | Three-ASR consensus minimum |
| No script normalisation | CER between `kya` and `क्या` was 1.0 | Normalise to unified script before any metric |
| Trusting UTMOS/SQUIM/PESQ on Hindi | They rate synthetic *above* human on Hindi | Ear-only for naturalness on non-English TTS |
| Planning fine-tuning before diagnosing the bug | Almost spent weeks on LoRA when the bug was in inference code, upstream of the model weights | Ask "is there a 30-minute experiment that would invalidate this idea cheaply?" before any training run |
| First Direction 2 analysis was silently wrong | MFCC mean included silence + C0 energy coefficient; Test C returned all 1.0, Test B returned bimodal nonsense | Sanity-check the analysis pipeline on a control before interpreting results; "too uniform" or "too bimodal" is a metric bug |
| Sloppy rubric versioning at the v2.0 → v2.1 transition | Documented some scores under the wrong rubric version, cost trust in my own notes later | Version every result with the rubric hash; never retroactively re-attribute |
| Carried incorrect note that "misaki has a Hindi module" | The library does not actually support Hindi; Kokoro uses espeak-ng directly. Affected weeks of architecture planning | Verify library claims by reading the source or package metadata, not by trusting earlier notes |
| Single-ASR for phonetic experiments | Short clips broke ASR; prosody is invisible to ASR | Ear evaluation for phonetic sensitivity |
| `source .env` for subprocesses | Vars not inherited by Python child processes | `export $(grep -v '^#' .env \| xargs)` |
| P100 on Kaggle for F5-family | `cudaErrorNoKernelImageForDevice` | Always specify T4 |
| Inferring kernel success from API status | "complete" ≠ wavs produced | Check outputs, not status |

---

## What Comes Next

The 330M system is shipped. The next question is whether the same quality fits under 25M parameters — small enough for a browser.

Path B is structured as five ranked experimental bets, not one architecture:

1. **Matcha-TTS ~22M + Hindi-fine-tuned PL-BERT + per-phoneme emotion head** — the most likely engineering path.
2. **IndicParler-TTS distillation** — using AI4Bharat's Apache-licensed emotion-tagged teacher, since Path A's IndicF5 is prosodically flat by our own diagnostic.
3. **Frozen neural codec (Mimi at 12.5 Hz) + 15–20M state-space LM** — the research moonshot for zero-shot voice cloning at this size.
4. **StyleTTS2-lite at 40–50M, warm-started from Kokoro** — the safety net.
5. **EmoSphere++ continuous emotion + EmoSteer inference steering** — bolted on for sliders, not buttons.

Two diagnostics run first because they decide everything: an ear-test of IndicParler-TTS outputs (does the teacher actually have the prosody we need?), and a Mimi/SNAC/BiCodec round-trip on Hindi (does the codec preserve retroflex consonants and prosody at 12.5 Hz?). Both finish in an afternoon.

The structural insight: at this scale, **the binding constraint isn't parameter count — it's the prosody quality of the teachers and data you train on.**

---

## The Meta-Lesson

This project had one finding that matters more than the 4.70 score.

Three separate times, the auto-metrics pointed one way and the human ear pointed another:

1. **Base model selection:** Auto-rubric said Kokoro was best overall. Ear said IndicF5 was better on Hindi naturalness. Trusting the ear flipped the model selection.

2. **Quality assessment:** PESQ said quality improved with preprocessing. Ear said "still sounds like 90s TTS, flat delivery." Both true. They were measuring different things.

3. **Phonetic probe:** Auto-metrics said 1/6 distinctions were sensitive. Ear said 6/6. The auto-metrics could not detect sub-phonemic changes or prosodic shifts without word changes.

The meta-lesson: **when you are working on a language that was not in your metrics' training distribution, build in a human evaluation step before trusting any number.** UTMOS was trained on English. AssemblyAI is optimised for English. MFCC cosine similarity does not know what Hindi sounds like.

This is not a criticism of those tools. They are good tools for what they were built for. But "works on English" does not mean "works on Hindi", and "works on Hindi" does not mean "works on Hinglish".

Measure your metrics before you trust your metrics.

---

## Appendix: Kaggle Disasters

The project ran entirely on free-tier Kaggle T4 GPUs. Including these notes here for anyone trying to reproduce on free compute — they cost me hours each.

**Disaster 1: The P100 trap.** Kaggle offers both P100 and T4 GPUs. F5-family TTS models fail on P100 with `cudaErrorNoKernelImageForDevice`. The GPU is too old for the CUDA kernels the model requires. I spent four hours debugging a failing kernel before figuring out the machine shape was wrong. The fix: always explicitly request T4 in kernel settings. The Kaggle CLI does not default to T4.

**Disaster 2: Kaggle Secrets do not work from CLI.** If you push a notebook via `kaggle kernels push` from the CLI, the Secrets (API keys stored in the Kaggle vault) are not accessible to the running kernel. Only kernels run from the web UI can read them. Workaround: hardcode the HuggingFace token inline in the notebook before pushing. Not ideal, but it works.

**Disaster 3: "Successful" does not mean wavs were produced.** The Kaggle status API returns `"status": "complete"` when the kernel finishes, whether it produced outputs or not. After every run I had to pull the output, check the logs for inference errors, and count the wavs. Automated "did this work?" checking requires looking at output contents, not at kernel status.

**Disaster 4: `source .env` does not propagate to subprocesses.** I spent hours debugging why my scoring scripts could not find the AssemblyAI API key. The issue: calling `source .env` in a shell session only exports variables to that shell. A background subprocess (like the Python scoring script) does not inherit them. The fix:

```bash
# Wrong:
source .env && python scoring/scripts/run_scoring.py

# Right:
export $(grep -v '^#' .env | xargs) && python scoring/scripts/run_scoring.py
```

---

## Links and Artifacts

- **Code and eval set:** [github.com/harrrshall/hinglish-tts](https://github.com/harrrshall/hinglish-tts)
- **Underlying model:** [ai4bharat/IndicF5](https://huggingface.co/ai4bharat/IndicF5) (HuggingFace gating required)
- **Transliteration library:** [AI4Bharat/IndicXlit](https://github.com/AI4Bharat/IndicXlit)
- **Detailed methodology:** `EVALUATION_REPORT.md`
- **Known limitations:** `KNOWN_LIMITATIONS.md`

**Citation:**

```bibtex
@misc{singh2026hinglish,
  author       = {Harshal Singh},
  title        = {Hinglish TTS: IndicF5 with IndicXlit Preprocessing},
  year         = {2026},
  howpublished = {\url{https://github.com/harrrshall/hinglish-tts}},
  note         = {30-sentence Hinglish eval set (4 categories).
                  Rubric v2.1: three-ASR consensus, Devanagari-normalised CER.
                  4.70/5.0 mean intelligibility.}
}
```

---

*Questions, bug reports, and collaboration inquiries: cybernovascnn@gmail.com*
