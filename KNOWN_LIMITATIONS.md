# Known Limitations

This document expands the [README limitations summary](README.md#known-limitations)
with detail, examples, and architectural notes where relevant.

The 4.70 / 5.0 score is real, but it measures intelligibility and code-switch
handling only. The limitations below are the honest accounting of what the score
does not capture.

---

## 1. Synthetic texture

Every output clip is identifiably synthetic to a trained ear, regardless of
intelligibility score. The model's delivery is fluent and the words are clear,
but the micro-variation in pitch, breathiness, and timing that distinguishes
natural conversational Hindi from TTS is absent. Clips that score 5/5 on
intelligibility sound robotic when compared to the human ground-truth recordings
in `data/human_recordings/`.

**Cause:** Flow-matching TTS conditioned on a reference audio clip inherits the
reference's mean spectral character but not its moment-to-moment variation.
The DiT fills the synthesis canvas with spectrally consistent frames, producing
a "smoother" output than natural speech.

**What would fix it:** A naturalness fine-tune on a curated single-speaker
Hindi dataset (Path B in `PROJECT_INSTRUCTIONS.md`). Not included in this
package.

---

## 2. Prosodic flatness

Long sentences, questions, exclamations, and imperatives receive similar
flat intonation contours. The model does not distinguish `कल मुझे दिल्ली
जाना है।` (declarative) from `क्या आप मुझे पानी दे सकते हैं?` (polite question)
in prosodic delivery — both receive a falling-then-flat contour.

Measured in the phonetic probe experiment (`experiments/05_phonetic_probe/`):
ellipsis and exclamation marks do produce subtle effects — 6c (`मैं... बहुत...
खुश हूं!`) was 44% longer than 6a (1.90s vs 1.32s) and had a higher terminal
pitch — but the effect is below the threshold of dramatic expressive delivery.

**What would fix it:** Prosody conditioning via a text-level F0 predictor or
duration predictor (e.g. PL-BERT) trained on Hindi data. This requires model
modification, not just inference-time tricks.

**What does NOT fix it:** Punctuation. The model attends to punctuation in a
limited way. Inserting `!` or `...` does not reliably produce emphasis or
dramatic pacing.

---

## 3. No naturalness number

The 4.70 score is intelligibility and code-switch handling only. There is no
naturalness number in this package, for a documented reason:

UTMOS and SQUIM_MOS — the two standard automatic naturalness predictors — rate
Hindi human recordings **1.7–2.4 ranks lower** than IndicF5 TTS outputs on the
same content. This directional inversion makes these predictors unusable as
naturalness estimates on Hindi audio. The full ceiling study is at
`scoring/rubric/CEILING_REPORT.md`.

A naturalness score would require a listening test with native Hindi speakers
and a perceptual rating scale. This was conducted informally (see
[README — Naturalness](README.md#naturalness)) but not on a statistically
adequate sample.

---

## 4. Whitelist generalisation (n=30)

The `ENGLISH_LOAN_CANONICAL` (36 entries) and `INDIAN_NE_CANONICAL` (19 entries)
tables in `scoring/scripts/lib_normalize.py` were assembled from the 30-sentence
eval set. Any English loanword or Indian proper noun not in these tables falls
through to IndicXlit transliteration.

For tokens not in the whitelist:

- **Common loanwords** (e.g. `phone`, `school`, `car`): IndicXlit usually
  produces a reasonable Devanagari rendering. Occasional short-token
  misreadings (e.g. `ok → ओके` instead of `ओके`) are possible.
- **Indian proper nouns** (city names, people names): common pan-Indian names
  and cities typically work. Less common names, brand names, and regional
  place names may be phonetically inaccurate.
- **Short ambiguous tokens** (2–3 characters): the highest risk category.
  `mai` (I), `tu` (you), `aa` (come), `hu` (am) are handled by the v2.1
  function-word whitelist, but similar short tokens outside this list
  (e.g. `se`, `ko`, `ne`) rely on IndicXlit.

**How to extend the whitelist:** add entries directly to the `ENGLISH_LOAN_CANONICAL`
or `INDIAN_NE_CANONICAL` dicts in `scoring/scripts/lib_normalize.py`. The
`ROMAN_HINDI_FUNCTION_WORDS` dict is for function words IndicXlit specifically
misreads. Changes take effect immediately — no retraining.

---

## 5. Kokoro leads on `english_with_NE`

Kokoro v1.0 (Hindi) scores **4.83** on `english_with_NE` vs this package's
**4.50**. The gap exists because:

This package transliterates full English sentences to Devanagari phonetics:
> "My friend Aishwarya from Chennai" → माय फ्रेंड ऐश्वर्या फ्रॉम चेन्नई

Kokoro, having broader English training, generates English-mode phonetics for
the English words and Indian-mode phonetics for the proper nouns.

Both approaches score 4–5 on intelligibility because the ASR rubric evaluates
after Devanagari normalisation — Hindi-accented English and native-English
phonetics both normalise to the same Devanagari reference. But a listener who
expects English words to sound English may find Kokoro's rendering more
natural for this category.

**If your use case is English-dominant content:** evaluate Kokoro for
`english_with_NE` sentences. For all Hinglish categories (pure Roman, mixed,
pure Devanagari), this package outperforms Kokoro by 0–2.25 ranks.

---

## 6. Gated model weights

IndicF5 weights are hosted at `ai4bharat/IndicF5` on HuggingFace behind a
gating form. You must create a HuggingFace account and click "Agree and access
repository" before the weights can be downloaded. This is a one-time step.

The license terms for the weights are set by AI4Bharat and are separate from
the license of the evaluation code in this repository. Attribution is required;
commercial use requires explicit permission from AI4Bharat. Check the model
card at [huggingface.co/ai4bharat/IndicF5](https://huggingface.co/ai4bharat/IndicF5)
for the current terms.

---

## 7. Python version constraint for preprocessing

IndicXlit depends on `fairseq`, which uses Python dataclasses in a way that is
incompatible with Python 3.12's stricter dataclass handling. Full IndicXlit
functionality requires Python 3.10 or 3.11.

On Python 3.12:
- Whitelist-only paths (the eval-set vocabulary) work correctly without
  IndicXlit being called.
- Unknown tokens that fall through the whitelist will fail with an import
  error when IndicXlit is called.

If you are on Python 3.12 and need full Roman-script support, create a Python
3.11 virtualenv and use `venv-scoring-py311/` (already set up if you cloned
this repository on the development machine).

---

## 8. Non-deterministic inference

IndicF5's diffusion sampler does not fix a random seed by default. Identical
input text and reference audio produce different waveforms across runs. Duration
is consistent (within ~50ms) but raw audio samples differ. This was confirmed in
the phonetic probe: two runs of identical input `मेरा नाम ज़ारा है।` produced
waveforms with max sample difference of 0.798 (on a [−1, 1] scale).

**Practical effect:** if you are building a system that requires byte-identical
reproducible outputs (e.g. for caching, A/B testing of text variants, or
deterministic evaluation), you need to set `torch.manual_seed(N)` before each
inference call and confirm that the specific IndicF5 version you are using
seeds the diffusion process from PyTorch's RNG. This is not currently handled
in `inference.py`.

---

## 9. Voice cloning fidelity not evaluated

The 4.70 score does not measure how faithfully outputs match the reference
speaker's voice. Timbre accuracy, pitch range match, and speaking rate match
were not part of the eval rubric. Informal listening suggests the model captures
broad speaker characteristics (voice weight, approximate register) from a 5–10s
reference clip, but no quantitative claim is made here.

Users who require verified speaker-identity fidelity — for dubbing, persona
consistency, or speaker authentication applications — should conduct their own
evaluation on their target voice.
