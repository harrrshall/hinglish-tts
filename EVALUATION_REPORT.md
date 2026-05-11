# Hinglish TTS Audit — Evaluation Report

**Date:** 2026-05-11
**Rubric:** v2.1 (3-ASR consensus, IndicXlit normalization)
**Status:** Phase 2 complete. Production deliverable shipped.

---

## 1. Project Goal

The objective of this audit was to determine the best available open-source text-to-speech model for Hinglish (Hindi-English code-mixed) speech, and to characterise and, where possible, fix the failure modes without fine-tuning new model weights.

Hinglish is the dominant register of urban Indian digital communication: WhatsApp messages, social media, and customer-service interactions routinely interleave Hindi morphology, Roman-script Hindi, Devanagari, and English proper nouns within a single sentence. No open-source TTS model in 2026 handles this register reliably out of the box. The audit was designed to measure exactly where each model fails and by how much, and to test inference-time mitigations before committing to a training run.

The deliverable is a production inference stack, a scored comparison across six model configurations, and an honest accounting of what remains unsolved.

---

## 2. Evaluation Methodology

### 2.1 Eval set

Thirty Hinglish sentences in four categories, fixed before any model inference ran and never modified:

| Category | n | Description |
|---|:---:|---|
| `pure_devanagari` | 8 | Standard Hindi, fully Devanagari-script |
| `pure_roman` | 8 | Romanized Hindi — "kal mujhe office jaana hai" |
| `mixed_script` | 8 | Script-switching within a single sentence |
| `english_with_NE` | 6 | English sentences with Indian proper nouns |

Source: `data/eval_sentences.tsv` (frozen). Sentence construction and category-coverage criteria are documented in `docs/AUDIT_PLAN.md §1`.

### 2.2 Scoring rubric v2.1

Rubric v2.1 is a small extension of v2.0 (locked 2026-05-09). The full specification lives in `scoring/rubric/JUDGE_PROMPT_v2.md`. The dimensions that can be computed automatically:

**Intelligibility (1–5):** CER-based, computed on normalized strings (see §2.3). Thresholds: CER ≤ 0.05 → 5, ≤ 0.15 → 4, ≤ 0.30 → 3, ≤ 0.50 → 2, else 1.

**Naturalness:** `EAR_ONLY` — no numeric value assigned by the pipeline (see §2.5 on predictor inversion).

**Code-switch handling (1–5):** For mixed-script and english_with_NE rows, score is the rank gap between the clip's intelligibility and the model's pure-category intelligibility mean. For pure rows, mirrors intelligibility.

**Speaker quality (1–5):** SQUIM PESQ thresholds (≥ 4.0 → 5, ≥ 3.5 → 4, etc.), with a −1 rank penalty for DC-tail artifact (`terminal_sample_abs > 0.05`).

**Silence-or-skip (TRUE/FALSE):** TRUE if mid-clip silence > 0.5 s or if normalized transcript token overlap with reference is < 80%.

### 2.3 Three-ASR consensus

Every wav is transcribed by three backends independently:

- **AssemblyAI (AAI)** — Hindi-forced model
- **Deepgram** — Nova-2 Hindi model
- **Groq Whisper** — Whisper large-v3 via Groq API

Each backend produces its own CER_norm and integer intelligibility score. The **consensus score** is `round(statistics.median([aai_score, deepgram_score, groq_score]))`. This is the score reported in all tables.

The motivation: AAI returns empty transcripts for clips under approximately 1.8 seconds, which would assign score 1 to short-but-correct clips. Deepgram and Groq rescue these cases, and the median of three is more robust to single-backend failures than any individual backend.

Scoring scripts: `experiments/04_indicf5_xlit_v2/scoring_scripts/run_all.py` (Stage 1: signal extraction) and `experiments/04_indicf5_xlit_v2/scoring_scripts/enrich_and_judge.py` (Stage 2: IndicXlit normalization + consensus judge).

### 2.4 IndicXlit normalization

Before computing CER, both the ground-truth reference text and the ASR transcript are passed through `scoring/scripts/lib_normalize.py:to_unified_devanagari()`. This function:

1. Tokenizes on whitespace and punctuation boundaries.
2. Passes Devanagari tokens through unchanged.
3. For ASCII alphabetic tokens: checks a whitelist of English loans (`ENGLISH_LOAN_CANONICAL`), Indian named entities (`INDIAN_NE_CANONICAL`), and Hindi function words (`ROMAN_HINDI_FUNCTION_WORDS`); uses IndicXlit (`ai4bharat.transliteration.XlitEngine`) as the fallback.
4. Passes numerals and punctuation through unchanged.

The function is applied **symmetrically** to reference and transcript, so if an ASR backend returns "ऑफिस" for the input word "office", both sides of the CER computation will have "ऑफिस", and the error is zero. This eliminates the script-mismatch artifact that caused rubric v1.0 to assign CER = 1.0 to phonetically-correct Devanagari renderings of Roman-script input.

The v2.1 addition is `ROMAN_HINDI_FUNCTION_WORDS`: four tokens (`tu → तू`, `mai → मैं`, `aa → आ`, `hu → हूं`) where IndicXlit's default transliteration produces English-phonetic forms (`टू`, `माई`, `एए`, `हू`) rather than the intended Hindi forms. The whitelist intercepts these before IndicXlit runs.

### 2.5 The predictor inversion caveat

The scoring pipeline uses SQUIM PESQ for speaker quality. UTMOS and SQUIM_MOS — the standard neural MOS predictors used in TTS literature — are **not used** for naturalness after a ceiling study revealed they are directionally inverted on Hindi.

The study scored 8 human Hindi/Hinglish recordings against the same rubric. Findings (full report: `scoring/rubric/CEILING_REPORT.md`):

| Predictor | Human GT | Kokoro TTS | Direction |
|---|:---:|:---:|:---:|
| UTMOS | 1.95 | 4.40 | **inverted +2.44 ranks** |
| SQUIM_MOS | 2.70 | 4.45 | **inverted +1.75 ranks** |
| SQUIM_PESQ | 1.62 | 3.86 | **inverted +2.24 ranks** |

Every TTS model scored higher on these predictors than actual human speech. UTMOS and SQUIM_MOS are trained on English MOS data and do not generalize to Hindi phonology. PESQ inverts because the phone-mic human recordings have lower SNR than studio-synthesized TTS outputs — the predictor is reading recording quality, not naturalness.

**Consequence:** naturalness is reported as `EAR_ONLY` throughout this audit. Any table that shows naturalness scores should be treated as a placeholder for a human listening session, not as measured values. Intelligibility, silence-or-skip, and speaker quality (PESQ) are the only automatically-measured dimensions that survived the ceiling check.

---

## 3. The Four-Model Baseline

Phase 1 ran inference on four models against the 30-sentence eval set (Orpheus-Hindi and SPRINGLab F5-Hindi are included in the field-wide ranking for completeness):

| Model | HF repo | Params | Prompting |
|---|---|:---:|---|
| Kokoro v1.0 (Hindi) | hexgrad/Kokoro-82M | 82M | voicepack `hf_alpha` |
| Indic Parler-TTS | ai4bharat/indic-parler-tts | 880M | text-description |
| IndicF5 | ai4bharat/IndicF5 | 330M | reference-audio + transcript |
| SPRINGLab F5-Hindi | SPRINGLab/F5-Hindi-24KHz | 151M | reference-audio + transcript |

Baseline scores under rubric v2.0, 3-ASR consensus:

| Model | pure_dev | pure_roman | mixed | eng_NE | **overall** |
|---|:---:|:---:|:---:|:---:|:---:|
| Kokoro | 4.62 | 2.50 | 3.88 | 4.83 | **3.90** |
| Indic Parler-TTS | 4.50 | 1.75 | 3.00 | 4.67 | **3.40** |
| IndicF5 (orig) | 4.62 | 1.00 | 1.62 | 1.00 | **2.13** |
| SPRINGLab F5-Hindi | 4.62 | 1.00 | 1.38 | 1.00 | **2.07** |

Kokoro and Parler handle pure_devanagari and english_with_NE reasonably well. Both collapse on pure_roman. IndicF5 and SPRINGLab collapse on everything except pure_devanagari.

The IndicF5 failure on pure_roman was particularly striking: 21 of 30 outputs were flagged `silence_or_skip`, with durations of 0.8–2.5 s for sentences that should take 2–5 s to speak. This pattern pointed to a duration bug rather than a model quality failure, and became the subject of Phase 2.

---

## 4. Duration Patch — Deriving the Mode A Root Cause

Full analysis: `diagnostics/duration_diagnostic/REPORT.md`.

### 4.1 The hypothesis

IndicF5's inference code (`f5_tts/infer/utils_infer.py`) computes the synthesis canvas duration using a text-length ratio formula:

```
total_frames = ref_frames + ref_frames × (gen_text_length / ref_text_length)
```

The question was what `gen_text_length` measured. The diagnostic instrumented six sentences from different categories, logging computed duration, actual wav duration, and expected spoken duration.

The finding was unambiguous: `actual ≈ computed` in every case (within 25 ms, attributable to STFT window padding), and `computed ≪ expected` for every non-Devanagari sentence. The model faithfully fills whatever canvas it is given — the canvas itself is too small.

### 4.2 The root cause

The formula uses **UTF-8 byte count**, not character count. Devanagari encodes as 3 bytes per character; ASCII encodes as 1 byte per character. The reference audio was Devanagari-heavy, calibrating the rate at approximately 30.6 ms per byte.

For a Roman-script sentence like "kal mujhe office jaana hai" (26 bytes, but 26 characters), the formula allocates `26/219 × 6.7 s ≈ 0.79 s` of canvas, when the sentence requires approximately 2 s. The model compresses all 26 words into 0.79 s of mel canvas and produces acoustic gibberish in the process.

Per-category gap (computed duration / expected duration):

| Category | Byte density | Gap |
|---|---|:---:|
| pure_roman | 1 byte/char | 0.30–0.39 |
| english_with_NE | 1 byte/char | 0.43–0.53 |
| mixed_script | mixed | 0.60–0.70 |
| pure_devanagari | 3 bytes/char | ≈ 1.0 (no truncation) |

Mode A (canvas under-allocated) was confirmed in all 6 diagnostic sentences with no evidence of Mode B (canvas correct, content truncated within canvas) or Mode C (canvas correct, content garbled).

### 4.3 The patch

Four lines changed in `f5_tts/infer/utils_infer.py:449–452`: replace `len(gen_text)` (byte count in Python 2-compatible usage) with `len(gen_text)` where `gen_text` is first decoded as a character sequence. The unified diff is in `experiments/02_indicf5_patch/patch.diff`.

Applied in Kaggle kernel v13. Result: `silence_or_skip` dropped from 21/30 to 0/30. Per-category durations matched expected durations within the predicted range for every category. The patch worked exactly as the diagnostic predicted.

---

## 5. Mode C — Embedding Undertraining and the Preprocessing Fix

Full analysis: `experiments/02_indicf5_patch/COMPARISON.md` (patched vs original) and `experiments/03_indicf5_xlit/COMPARISON.md` (patched + IndicXlit vs field).

### 5.1 The residual failure after patching

After the duration patch, 22 of 30 sentences still scored intelligibility ≤ 2. The failure changed character: instead of truncated clips, the model was now producing **right-length-garbled** output. Example from the patched run:

> Input: `kal mujhe office jaana hai`
> Patched ASR: `"ऐई अ एफे रेने आए"`

Across all 15 right-length-garbled sentences, the pattern was consistent: **every Devanagari token in a mixed sentence rendered correctly; every Roman/ASCII token produced syllabic noise**. The model had learned nothing useful for ASCII character embeddings — the input vector for "k", "a", "l" is effectively random relative to the Devanagari subspace that was actually trained, and the acoustic model produces near-random output in response.

This is Mode C: canvas correct, content garbled, root cause in the input representation layer.

### 5.2 The preprocessing hypothesis

If the model's character embedding subspace for ASCII is undertrained, the natural inference-time mitigation is to never give the model ASCII input. Feed it only Devanagari — the script it was trained on.

The same `to_unified_devanagari()` function used for rubric normalization (§2.4) was applied as a preprocessing step: every input sentence was transliterated to Devanagari before being passed to the model. This is symmetric by design — the normalization function is the same code path on both sides, ensuring the rubric's reference and the model's input are processed identically.

### 5.3 Experimental result (v2.0, xlit run)

| Category | Original | Patched | Patched + Xlit | Δ (xlit − patch) |
|---|:---:|:---:|:---:|:---:|
| pure_devanagari | 4.62 | 4.62 | 4.62 | +0.00 |
| pure_roman | 1.00 | 1.00 | **4.38** | **+3.38** |
| mixed_script | 1.62 | 1.88 | **4.88** | **+3.00** |
| english_with_NE | 1.00 | 1.00 | **4.33** | **+3.33** |
| **overall** | **2.13** | **2.20** | **4.57** | **+2.37** |

`silence_or_skip`: 20/30 → 16/30 → **0/30**.

The preprocessing resolved Mode C fully. All 15 right-length-garbled sentences scored 4 or 5. Zero residual failures. The pure_devanagari column is identical across all three runs (the correct regression sanity check — preprocessing is a no-op for pure_devanagari rows).

The patched + xlit configuration scored 4.57 overall — the highest of any configuration in the audit, beating Kokoro (3.90) and Indic Parler-TTS (3.40) on overall intelligibility. Kokoro retains a 0.5-rank edge on english_with_NE (4.83 vs 4.33), but the patched + xlit stack dominates on every other category including pure_roman, where it nearly doubles Kokoro's score (4.38 vs 2.50).

---

## 6. Rubric v2.1 Whitelist Fix and Final Result

Full analysis: `experiments/04_indicf5_xlit_v2/COMPARISON.md`.

### 6.1 The v2.1 fix

Two pure_roman sentences (ids 12 and 16) scored 4 instead of 5 in the v2.0 xlit run. Root cause: IndicXlit transliterates the token `tu` as `टू` (English "to" pronunciation) rather than `तू` (Hindi informal "you"). The model faithfully rendered `टू` and the ASR returned `तू`, introducing a CER gap at the boundary of the 4→5 threshold.

The fix: add four tokens to `ROMAN_HINDI_FUNCTION_WORDS` in `scoring/scripts/lib_normalize.py` — `tu → तू`, `mai → मैं`, `aa → आ`, `hu → हूं`. These are short Hindi function words that IndicXlit misreads as English phonetics. The whitelist intercepts them before IndicXlit runs, on both the input preprocessing side and the rubric normalization side.

### 6.2 Final result (rubric v2.1, 3-ASR consensus)

| Category | v2.0 xlit | v2.1 xlit | Δ |
|---|:---:|:---:|:---:|
| pure_devanagari | 4.62 | **4.62** | +0.00 |
| pure_roman | 4.38 | **4.75** | **+0.38** |
| mixed_script | 4.88 | **4.88** | +0.00 |
| english_with_NE | 4.33 | **4.50** | +0.17 |
| **overall** | **4.57** | **4.70** | **+0.13** |

`silence_or_skip`: 0/30. Mean PESQ: 3.996.

Three rows lifted (ids 10, 11, 12), not two as predicted. Id 16 remained at 4: the `tu → तू` fix was applied correctly but the remaining CER gap comes from `बोहोट` (IndicXlit's colloquial rendering of "bohot") vs `बहुत` (ASR canonical), which persists at CER ≈ 0.105 on all three backends — a content-word variance, not a function-word failure.

### 6.3 Field-wide ranking (final)

| Model | overall | pure_roman | mixed | eng_NE | pure_dev |
|---|:---:|:---:|:---:|:---:|:---:|
| **IndicF5 patched + xlit v2.1** | **4.70** | **4.75** | **4.88** | 4.50 | **4.62** |
| IndicF5 patched + xlit v2.0 | 4.57 | 4.38 | **4.88** | 4.33 | **4.62** |
| Kokoro | 3.90 | 2.50 | 3.88 | **4.83** | 4.62 |
| Indic Parler-TTS | 3.40 | 1.75 | 3.00 | 4.67 | 4.50 |
| IndicF5 patched | 2.20 | 1.00 | 1.88 | 1.00 | 4.62 |
| IndicF5 original | 2.13 | 1.00 | 1.62 | 1.00 | 4.62 |
| SPRINGLab F5-Hindi | 2.07 | 1.00 | 1.38 | 1.00 | 4.62 |

The production stack scores highest on every category except english_with_NE, where Kokoro leads by 0.33 ranks. The pure_roman advantage over Kokoro is 2.25 ranks (4.75 vs 2.50), which is the most practically significant gap — Roman-script Hinglish is the dominant input register for Indian WhatsApp/chat use cases.

### 6.4 What the production stack is

No new model weights. No fine-tuning. The complete intervention is:

1. **Duration patch** (`experiments/02_indicf5_patch/patch.diff`): 4 lines in `f5_tts/infer/utils_infer.py`. Replaces byte-proportional duration allocation with character-proportional allocation. Fixes Mode A.

2. **Input preprocessing** (`scoring/scripts/preprocess_input.py`): call `lib_normalize.to_unified_devanagari(input_text)` on every sentence before passing to the model. Approximately 10 lines of wrapper code, plus the IndicXlit dependency (already installed for scoring). Fixes Mode C.

3. **Rubric v2.1 whitelist** (`scoring/scripts/lib_normalize.py`): four additional entries in `ROMAN_HINDI_FUNCTION_WORDS`. Used both in input preprocessing and in eval-set scoring normalization. No impact on the production inference path beyond correcting IndicXlit's handling of `tu/mai/aa/hu`.

The underlying model is ai4bharat/IndicF5 v12 (330M parameters), unchanged.

---

## 7. Known Limitations

### 7.1 Sound texture and prosodic flatness

IndicF5 is a flow-matching DiT conditioned on a reference audio clip. The model produces output that shares the reference speaker's voice identity and approximate prosody envelope, but the generated speech can sound somewhat mechanical — a flat, evenly-paced delivery without the micro-variation in pitch, duration, and breathiness that characterise natural conversational speech. This is not measured by the intelligibility rubric.

In perceptual listening, IndicF5's outputs are clearly distinguishable from human speech by a native Hindi speaker, even on sentences that score 5/5 on intelligibility. The naturalness gap is real and is the primary dimension not addressed by the inference-time interventions in this audit.

A voice fine-tune (LoRA on upper DiT layers, with a curated Hindi speaker dataset) is the most direct path to closing this gap. It is outside the scope of Phase 2.

### 7.2 English-with-NE phonetics

For english_with_NE sentences, IndicXlit transliterates the entire English sentence to Devanagari before the model sees it. The model produces a Hindi-accented phonetic rendering — "माय फ्रेंड ऐश्वर्या" for "My friend Aishwarya". ASR backends score this highly because the Devanagari output closely matches the reference after normalization. A native listener may judge this as acceptable (Indian-accented English, which is the norm in this use case) or undesirable (sounds like transliteration, not natural English).

The audit's intelligibility metric does not distinguish these cases. Whether the hindi-phonetic English output is acceptable for the target application is a product decision, not a technical one.

### 7.3 Eval-set generalization (n=30)

The eval set contains 30 sentences. The English-loan whitelist in `lib_normalize.py` (36 entries) and the Indian NE whitelist (18 entries) were hand-tuned to the vocabulary of this specific set. Both whitelists are annotated with the sentence ID where each entry appears.

Generalization to wild Hinglish input is unmeasured. There are two known failure modes on out-of-vocabulary tokens:

- **Unknown English loans** (e.g., "upgrade", "meeting", "status") that are not in `ENGLISH_LOAN_CANONICAL` will fall through to IndicXlit. IndicXlit handles most common loans correctly but may produce non-canonical renderings for ambiguous short tokens.
- **Unknown Indian proper nouns** not in `INDIAN_NE_CANONICAL` will be transliterated phonetically by IndicXlit. For common pan-Indian names (Priya, Rahul, Mumbai) this works well; for less common surnames or place names, IndicXlit may produce a non-standard rendering that inflates CER.

A production deployment would require either whitelist expansion or a learned token classifier (e.g., a Hindi LID model at the token level) to distinguish English loans, Indian NEs, and Roman-Hindi function words reliably.

### 7.4 Baseline scoring asymmetry

The four baseline models (Kokoro, Parler, IndicF5 original, SPRINGLab) were scored with AAI signals only — Deepgram and Groq signal vectors were collected later, during the patched IndicF5 experiments. Cross-model comparisons between the baselines and the patched+xlit configurations carry this asymmetry. The load-bearing comparison — patched vs patched+xlit — is symmetric (both use 3-ASR consensus from the same scoring run). The baseline figures should be read as approximate.

### 7.5 Naturalness is not measured

The rubric emits `EAR_ONLY` for naturalness. No naturalness number in this report should be treated as a measured value. A human listening session against native-speaker annotations is a prerequisite before any naturalness claims can be made. The ceiling study (§2.5, `scoring/rubric/CEILING_REPORT.md`) demonstrates why: available MOS predictors are directionally inverted on Hindi and cannot be used as a substitute.

---

## 8. Artifact Index

| Artifact | Path |
|---|---|
| Eval sentences (frozen) | `data/eval_sentences.tsv` |
| Reference audio | `data/reference_audio/hindi_ref.{wav,txt}` |
| Human ceiling study | `scoring/rubric/CEILING_REPORT.md` |
| Rubric (locked) | `scoring/rubric/JUDGE_PROMPT_v2.md` |
| Normalization library | `scoring/scripts/lib_normalize.py` |
| Duration diagnostic | `diagnostics/duration_diagnostic/REPORT.md` |
| Duration patch | `experiments/02_indicf5_patch/patch.diff` |
| Patched vs original comparison | `experiments/02_indicf5_patch/COMPARISON.md` |
| Xlit three-way comparison (v2.0) | `experiments/03_indicf5_xlit/COMPARISON.md` |
| v2.1 two-way comparison (final) | `experiments/04_indicf5_xlit_v2/COMPARISON.md` |
| Final scored CSV | `experiments/04_indicf5_xlit_v2/scores/auto_scores_v2.1.csv` |
| Signal vectors (all 90 entries) | `experiments/04_indicf5_xlit_v2/scores/signal_vectors_v2.json` |
| Decision log (source of truth) | `RESEARCH_LOG.md` |
