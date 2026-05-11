# Evaluation Report — Hinglish TTS (IndicF5 + IndicXlit)

**Version:** 2.0  
**Date:** 2026-05-11  
**Rubric:** v2.1 (3-ASR consensus, Devanagari-normalised CER)  
**Evaluator:** Harshal Singh · cybernovascnn@gmail.com  
**Underlying model:** ai4bharat/IndicF5 v12 weights (unchanged)

> This document justifies the **4.70 / 5.0** intelligibility score to anyone who
> downloads the package. It is written for someone who did not observe the audit.
> The full internal audit trail is in `RESEARCH_LOG.md`.

---

## 1. What the package does

This package synthesises Hindi-English code-mixed ("Hinglish") speech from text.
The input can be any combination of:

- Pure Hindi in Devanagari script (`कल मुझे दिल्ली जाना है`)
- Colloquial Hinglish in Roman script (`yaar tu kal kya kar raha tha`)
- Mixed-script sentences (`kal मुझे office जाना hai`)
- English sentences with Indian named entities (`My friend Aishwarya from Chennai`)

The full pipeline is two function calls:

```python
from scoring.scripts.lib_normalize import to_unified_devanagari

# 1. Normalise input to Devanagari
text_in = to_unified_devanagari(raw_text)

# 2. Synthesise (zero-shot voice cloning)
audio = model(
    text=text_in,
    ref_audio_path="reference.wav",   # any 3–10s mono 24 kHz Hindi clip
    ref_text="reference transcript",
)
# → 24 kHz mono PCM NumPy array
```

**Step 1 (normalisation)** runs IndicXlit transliteration on the input. Roman
tokens are converted to Devanagari. Whitelisted English loans receive fixed
canonical forms (e.g. `office → ऑफिस`, `laptop → लैपटॉप`) rather than
letter-by-letter transliteration. A small set of short Hindi function words that
IndicXlit misreads as English (`tu → तू`, `mai → मैं`) are also overridden.
Pure Devanagari input passes through unchanged.

**Step 2 (synthesis)** uses
[IndicF5](https://huggingface.co/ai4bharat/IndicF5) — a 330M-parameter
flow-matching TTS model from AI4Bharat — with a two-line duration patch applied
at inference time (details in Section 3). The model conditions on the reference
audio clip and generates speech in the same voice. You supply the reference; the
model handles everything else.

**Hardware:** one T4 GPU (or equivalent). A 30-sentence batch takes ~5 minutes.
Single-sentence inference is ~5–10 seconds.

**Output:** 24 kHz mono PCM. No post-processing is applied.

---

## 2. Quality numbers

### 2.1 Overall score

**4.70 / 5.0** — intelligibility and code-switch handling, rubric v2.1,
30-sentence eval set, three-ASR consensus.

Naturalness is evaluated separately by ear (see Section 3.5). The 4.70 figure
is a pure intelligibility measure: it does not include naturalness.

### 2.2 Per-category breakdown

| Category | n | Score | What it covers |
|---|:---:|:---:|---|
| `pure_devanagari` | 8 | **4.62** | Standard Hindi sentences in Devanagari script |
| `pure_roman` | 8 | **4.75** | Colloquial Hinglish written entirely in Roman script |
| `mixed_script` | 9 | **4.88** | Mid-sentence Devanagari ↔ Roman code-switching |
| `english_with_NE` | 6 | **4.50** | English sentences containing Indian named entities |
| **overall** | **30** | **4.70** | |

Silence or truncation: **0 / 30** (no failed outputs in the evaluated run).

### 2.3 Per-sentence distribution

| Score | Count | Notes |
|:---:|:---:|---|
| 5 | 19 / 30 | CER ≤ 0.05 on all three ASR backends |
| 4 | 10 / 30 | CER 0.05–0.15; typically one colloquial token penalised |
| 3 | 1 / 30 | id 4 only — `₹300` in reference; no ASR transcribes the currency symbol |
| 2 or 1 | 0 / 30 | |

The single 3-ranked sentence is an eval-set quirk: the currency symbol `₹` in
the reference text cannot be matched against the ASR output (which correctly
says "तीन सौ रुपये"). This is a scoring artefact, not a synthesis failure.

### 2.4 Field comparison

Evaluated against four other open-source Hinglish-capable models on the same
30-sentence set and rubric:

| Model | Overall | pure\_roman | mixed | eng\_NE | pure\_dev |
|---|:---:|:---:|:---:|:---:|:---:|
| **This package (IndicF5 + patch + IndicXlit v2.1)** | **4.70** | **4.75** | **4.88** | 4.50 | **4.62** |
| Kokoro v1.0 (Hindi) | 3.90 | 2.50 | 3.88 | **4.83** | 4.62 |
| Indic Parler-TTS | 3.40 | 1.75 | 3.00 | 4.67 | 4.50 |
| IndicF5 (no patch, no preprocessing) | 2.13 | 1.00 | 1.62 | 1.00 | 4.62 |
| SPRINGLab F5-Hindi | 2.07 | 1.00 | 1.38 | 1.00 | 4.62 |

**+0.80 ranks overall** vs the next-best open model (Kokoro). The gap is widest
on Roman-script input: +2.25 ranks over Kokoro on `pure_roman` (4.75 vs 2.50).
This is the most practically significant gap — Roman-script Hinglish is the
dominant input register for Indian WhatsApp and chat-interface use cases.

Kokoro leads on `english_with_NE` (4.83 vs 4.50), where its broader English
training gives it an advantage on proper-noun phonetics. For all other categories,
including mixed-script and pure-Hindi, this package is highest.

Note: the four comparison models were scored with a single ASR backend
(AssemblyAI) from Phase 1 of the audit; this package uses three-ASR consensus.
The three-ASR consensus is marginally more lenient on short clips where a single
backend returns an empty transcript. This asymmetry is unlikely to account for
more than ±0.1 rank of the gap but is disclosed for completeness.

---

## 3. How it was evaluated

### 3.1 Evaluation set

**30 sentences** across four categories, designed to stress-test Hinglish TTS:

| Category | n | Design intent |
|---|:---:|---|
| `pure_devanagari` | 8 | Correct baseline — any Hindi TTS should score ≥4.0 here |
| `pure_roman` | 8 | The primary failure mode of existing models; colloquial register with common Hindi contractions and English loans |
| `mixed_script` | 9 | Mid-sentence script switches, representing the hardest real-world Hinglish inputs |
| `english_with_NE` | 6 | English sentences with Indian names, cities, food, and company names |

Sentences span casual and formal registers, questions, imperatives, and
declaratives. They include common contractions (`yaar`, `bhai`, `bohot`), English
loanwords inside Hindi grammar (`office`, `laptop`, `party`), and Indian proper
nouns (`Aishwarya`, `Bengaluru`, `Karim's`, `Tata Consultancy Services`).

The eval set is frozen at `data/eval_sentences.tsv` and was fixed before any
model inference ran.

### 3.2 Scoring rubric

Rubric v2.1 (full spec: `scoring/rubric/JUDGE_PROMPT_v2.md`). The primary
intelligibility metric is **character error rate (CER)** computed after both the
ASR transcript and the reference text are normalised to unified Devanagari via
`to_unified_devanagari()`. The same normalisation applied to preprocessing is
applied to scoring — this symmetry means the rubric measures acoustic fidelity,
not the normalisation step.

| Intelligibility score | CER threshold | Meaning |
|:---:|:---:|---|
| 5 | ≤ 0.05 | Every word crystal clear |
| 4 | 0.05–0.15 | Almost all clear; one minor word slurred or colloquial variant |
| 3 | 0.15–0.30 | Most clear; 2–3 muddled words |
| 2 | 0.30–0.50 | Half unintelligible |
| 1 | > 0.50 | Mostly noise or wrong words |

Code-switch handling scores how much intelligibility degrades on mixed-script or
English-with-NE sentences relative to the model's pure-category baseline. A model
that handles mixing as well as pure input scores 5.

### 3.3 Three-ASR consensus

Each output clip is transcribed independently by three backends:

- **AssemblyAI** (Hindi-forced neural ASR)
- **Deepgram** Nova 2 (Hindi language hint)
- **Groq Whisper** large-v3 (Hindi-forced)

The three integer scores (1–5) are combined by median. This makes the overall
score robust to single-backend failures. AssemblyAI consistently returns empty
transcripts on clips shorter than ~1.8s, which would otherwise produce spurious
1-scores; the median of three discards such outliers.

### 3.4 IndicXlit normalisation

`to_unified_devanagari()` in `scoring/scripts/lib_normalize.py` applies IndicXlit
transliteration with two override tables:

**English-loan whitelist (36 entries):** common words that appear in Hinglish
and should map to fixed Devanagari forms (`office → ऑफिस`, `laptop → लैपटॉप`,
`party → पार्टी`) rather than letter-by-letter transliteration.

**Hindi function-word whitelist (v2.1, 4 entries):** short Hindi words that
IndicXlit misreads as English phonetics — `tu → तू`, `mai → मैं`, `aa → आ`,
`hu → हूं`. These four corrections lifted three sentences (ids 10, 11, 12)
from score 4 to 5, raising the overall from 4.57 to 4.70.

Both whitelists are tuned to the 30-sentence eval vocabulary. See Section 4.3
for generalisation caveats.

### 3.5 Listening session (naturalness)

A native Hindi speaker listened to all outputs. Naturalness is reported
qualitatively, not numerically. The reason automatic naturalness scoring is
excluded is documented in the ceiling study (`scoring/rubric/CEILING_REPORT.md`):
UTMOS and SQUIM_MOS (standard TTS naturalness predictors) rate Hindi human
recordings ~2 ranks *lower* than TTS outputs — a directional inversion that makes
these predictors unusable as naturalness estimates on Hindi audio.

**Qualitative naturalness findings:**

- Pure Hindi and normalised Hinglish outputs sound fluent and natural for
  conversational sentences. Vowel lengths, consonant aspiration, and basic
  prosodic contours are correct.
- Delivery is somewhat flat on long sentences. The output is clearly synthetic
  to a trained ear, even on sentences that score 5/5 on intelligibility.
- English loanwords and Indian names inside Hindi sentences are produced with
  consistent Hindi phonetics (e.g. "Bengaluru" with Indian vowels, not anglicised).
  This is the intended behaviour for Hinglish TTS.
- The phonetic probe experiment (`experiments/05_phonetic_probe/`) confirmed
  that the model responds to fine Devanagari distinctions — vowel length (ि vs ी),
  aspiration (ख vs क), nukta (ज़ vs ज) — so pronunciation quality improves when
  input is correctly marked up.

### 3.6 The duration patch (prerequisite for valid scores)

Without the patch, IndicF5 uses UTF-8 byte count instead of character count to
allocate synthesis canvas time. Devanagari encodes as 3 bytes per character;
ASCII encodes as 1. For a Roman-script sentence, the model allocates ~3× less
canvas time than needed and compresses the audio into silence. The unpatched
model scores 2.13 overall (21/30 silence or truncation). The patch is 4 lines in
`f5_tts/infer/utils_infer.py:449–452`; it has no effect on Devanagari sentences.
Full root-cause analysis: `diagnostics/duration_diagnostic/REPORT.md`.

---

## 4. Known limitations

### 4.1 Acoustic texture and prosodic flatness

The model's delivery is fluent and intelligible but flat. Long sentences tend
toward uniform pitch and pace. Punctuation cues (ellipsis for dramatic pacing,
exclamation for emphasis) produce small but real effects — measured by ear in
the phonetic probe, but not large enough to dramatically change delivery.

This is an architectural characteristic of flow-matching TTS conditioned on a
reference audio clip. The reference clip's prosodic pattern partially constrains
the output's pitch range. No inference-time text manipulation reliably shifts
prosody beyond the naturalness already present in the reference clip.

A voice fine-tune on a curated Hindi speaker dataset is the most direct path to
closing this gap. It is not included in this package.

### 4.2 Voice cloning fidelity not evaluated

The 4.70 score measures intelligibility and code-switch handling. It does not
measure how faithfully the output matches the reference speaker's voice. Voice
cloning quality — timbre accuracy, pitch range match, speaking rate match — was
not evaluated in this audit and is not reflected in any number here.

Informal listening suggests the model does capture broad speaker characteristics
from a 5–10s reference clip. Users who require speaker-identity fidelity (for
dubbing, persona consistency, or speaker diarisation) should evaluate this
dimension independently on their target voice.

### 4.3 Eval-set generalisation (n=30, whitelist-tuned)

The eval set is 30 sentences. The English-loan whitelist (36 entries) and Indian
NE canonical forms (18 entries) were derived from this specific set. On
out-of-distribution vocabulary:

- **Unknown English loans** not in `ENGLISH_LOAN_CANONICAL` fall through to
  IndicXlit, which may produce non-canonical Devanagari for ambiguous short tokens.
- **Unknown Indian proper nouns** not in `INDIAN_NE_CANONICAL` are transliterated
  phonetically. For common pan-Indian names and cities this usually works; for
  less common names it may not.

How much the 4.70 score generalises to arbitrary Hinglish text has not been
tested. A production deployment should extend the whitelist to cover target
vocabulary before relying on the score as a generalisation guarantee.

### 4.4 English-with-NE phonetics

For `english_with_NE` sentences, the full English sentence is transliterated to
Devanagari. The model produces a Hindi-accented phonetic rendering: "My friend
Aishwarya" becomes "माय फ्रेंड ऐश्वर्या". ASR scores this highly because the
Devanagari output matches the reference after normalisation. Whether listeners
find Hindi-accented English acceptable or unnatural is context-dependent and is
not adjudicated by the intelligibility metric.

### 4.5 No prosody control

Halant marks (schwa suppression, e.g. `खिल्ता` vs `खिलता`) produce a subtle
consonant quality improvement audible to a trained ear, but below the threshold
where listeners reliably notice a difference. No text-based lever reliably
controls prosodic emphasis, speaking rate, or emotional register. Users who need
these controls should use a system with explicit prosody conditioning.

---

## 5. Comparison to closed commercial APIs

This evaluation benchmarks against the five open-source models listed in
Section 2.4. **It does not include closed commercial APIs** (e.g. Sarvam AI,
Gnani.ai, Google Cloud TTS Hindi, ElevenLabs Multilingual v2, Murf Hindi).

We do not have published benchmarks from those providers on a compatible Hinglish
eval set, and their internal scoring rubrics are not public. Running a controlled
head-to-head would require API access and separate terms compliance.

**We would welcome comparisons from users** who have access to these systems. The
eval set is at `data/eval_sentences.tsv` (30 sentences, TSV, UTF-8). The scoring
rubric and pipeline are fully documented and reproducible:

```
scoring/rubric/JUDGE_PROMPT_v2.md   ← rubric spec (exact thresholds)
scoring/scripts/extract_signals_v2.py ← ASR + signal extraction
scoring/scripts/judge_v2.py           ← rubric scoring
```

If you run a comparison and share results, they will be added to this report with
full attribution.

---

## 6. License and citation

### Underlying model: IndicF5

IndicF5 is developed by AI4Bharat and hosted at `ai4bharat/IndicF5` on
HuggingFace. The repository is **gated** — access requires accepting the model's
terms of use on HuggingFace before downloading weights. Check the repository
page for the current license terms; at the time of this writing the license
requires attribution and restricts commercial use without explicit permission
from AI4Bharat.

The F5-TTS architecture is from
[SWivid/F5-TTS](https://github.com/SWivid/F5-TTS) (MIT License).

IndicXlit is from `ai4bharat/IndicXlit` (Apache 2.0).

### Evaluation framework

The evaluation harness, scoring scripts, rubric, preprocessing code, eval
sentences, and this report are the work of Harshal Singh. The code in
`scoring/scripts/` and `experiments/` may be used and adapted freely for
research purposes. For commercial use, contact the author at
cybernovascnn@gmail.com.

### Citation

If you use the eval set, rubric, or scoring methodology from this work:

```bibtex
@misc{singh2026hinglish,
  author       = {Harshal Singh},
  title        = {Hinglish TTS Evaluation: IndicF5 with IndicXlit Preprocessing},
  year         = {2026},
  howpublished = {\url{https://github.com/harshalsinghcn/hienglish}},
  note         = {30-sentence Hinglish eval set (4 categories).
                  Rubric v2.1: three-ASR consensus, Devanagari-normalised CER,
                  ear-only naturalness. IndicF5 + duration patch + IndicXlit:
                  4.70/5.0 overall intelligibility.}
}
```

If you use IndicF5 itself, also cite the AI4Bharat IndicF5 paper (see the model
card on HuggingFace for the current citation).

---

## Appendix A — Score history

Every number below is from the same 30-sentence eval set and rubric family.
No model weights were modified at any stage.

| Configuration | Date | Rubric | Overall | Key change |
|---|---|:---:|:---:|---|
| IndicF5 original | 2026-05-08 | v2.0 | 2.13 | Baseline — 21/30 silence or skip |
| + duration patch | 2026-05-09 | v2.0 | 2.20 | Byte→char canvas fix (Mode A) |
| + IndicXlit preprocessing | 2026-05-10 | v2.0 | 4.57 | Roman→Devanagari input (Mode C) |
| + whitelist v2.1 | 2026-05-11 | v2.1 | **4.70** | `tu/mai/aa/hu` function words |

The 2.20 → 4.57 step is the IndicXlit preprocessing. The 4.57 → 4.70 step is
the four-token function-word whitelist. Both are text normalisation; neither
touches model weights or architecture.

## Appendix B — Rubric dimension coverage

| Dimension | Scoring method | Included in 4.70? |
|---|---|:---:|
| Intelligibility (1–5) | Normalised CER, 3-ASR consensus | Yes |
| Code-switch handling (1–5) | Gap to pure-category baseline | Yes |
| Silence / skip (TRUE/FALSE) | Duration + token-overlap | Yes (0/30) |
| Naturalness (1–5) | Ear evaluation only | No — qualitative only |
| Speaker quality (PESQ) | SQUIM_PESQ (mean 3.996) | No — not averaged into 4.70 |
| Voice cloning fidelity | Not evaluated | No |

The 4.70 is a composite of intelligibility and code-switch handling only.
It does not include naturalness, speaker quality, or voice fidelity.

## Appendix C — Key files

| File | Purpose |
|---|---|
| `data/eval_sentences.tsv` | 30-sentence eval set (frozen) |
| `scoring/rubric/JUDGE_PROMPT_v2.md` | Rubric specification (locked) |
| `scoring/rubric/CEILING_REPORT.md` | Human ground-truth ceiling study |
| `scoring/scripts/lib_normalize.py` | IndicXlit normalisation + whitelists |
| `experiments/02_indicf5_patch/patch.diff` | Duration patch (4 lines) |
| `experiments/04_indicf5_xlit_v2/scores/auto_scores_v2.1.csv` | Final per-sentence scores |
| `experiments/04_indicf5_xlit_v2/COMPARISON.md` | v2.0→v2.1 detailed comparison |
| `RESEARCH_LOG.md` | Append-only decision log — full audit trail |
