# How it works

> Technical explainer for the IndicF5 + IndicXlit Hinglish TTS stack.
> Assumes you have read EVALUATION_REPORT.md and want to know the *why*.

---

## 1. The duration patch

The core model — AI4Bharat's IndicF5 v12 — ships with a four-line arithmetic
bug in `f5_tts/infer/utils_infer.py`. Left unpatched, the model synthesises
roughly correct-sounding audio at the wrong length: sentences get clipped to
30–70% of their natural duration, and the ASR returns noise like `"Ranai."` for
`"kal mujhe office jaana hai"`.

### What the bug is

`infer_batch_process()` sizes the output audio canvas in mel frames by computing
a byte-proportional ratio of target text length to reference text length:

```python
# Original code (IndicF5 v12, utils_infer.py ~line 451)
ref_text_len = len(ref_text.encode("utf-8"))
gen_text_len = len(gen_text.encode("utf-8"))
duration = ref_audio_len + int(ref_audio_len / ref_text_len * gen_text_len / speed)
```

UTF-8 encodes Devanagari as 3 bytes per character and ASCII as 1 byte per
character. The reference clip in the standard eval was Devanagari-heavy (219
bytes ≈ 73 characters at 3 bytes/char), calibrating the model to ~30.6 ms per
byte of target text.

Apply that calibration to Roman-script Hinglish:

```
"kal mujhe office jaana hai"  →  26 UTF-8 bytes  →  0.79 s allocated
```

The sentence needs about 2.0 seconds to say aloud. The model was handed a 0.79 s
canvas and faithfully filled it — generating the best acoustic output it could
squeeze into under one second. The canvas was the problem, not the model.

We verified this on 6 diagnostic sentences (see
`diagnostics/duration_diagnostic/REPORT.md`). In every case,
`actual_wav ≈ computed_duration` within 25 ms of STFT padding. The model
**does not stop generating early** — it always fills the canvas. The canvas
itself was specified too small.

The gap grows cleanly with ASCII density:

| Script | Bytes/char | Typical gap (computed/expected) |
|---|:---:|:---:|
| pure Devanagari | 3 | ~1.00 (no truncation) |
| mixed script | 1–3 | 0.60–0.70 |
| English with NEs | 1 | 0.43–0.53 |
| pure Roman | 1 | 0.30–0.39 |

### The fix

Count non-whitespace **characters** instead of bytes:

```python
# Patched (inference.py applies this at import time)
ref_text_len = sum(1 for c in ref_text if not c.isspace())
gen_text_len = sum(1 for c in gen_text if not c.isspace())
duration = ref_audio_len + int(ref_audio_len / ref_text_len * gen_text_len / speed)
```

This is script-agnostic: Devanagari and ASCII characters both count as one unit.
The fix is 2 lines and requires no model retraining.

`inference.py` applies the patch at module import time by rewriting
`utils_infer.py` in-situ in the installed `f5_tts` package. The patch is
idempotent (guarded by a `DEBUG-PATCH` sentinel), so re-importing is safe.
Running `python -c "import inference; print(inference._PATCH_STATUS)"` confirms
the patch is active before running any synthesis.

---

## 2. IndicXlit preprocessing (bypassing Mode C)

Fixing the duration bug revealed the second problem: 16/30 sentences still
failed after patching, with correct duration but garbled content.

The pattern was unambiguous: every Devanagari token in a sentence synthesised
correctly; every Roman/ASCII token produced syllabic noise. Example:

```
input:     "kal mujhe office jaana hai"
patched output ASR:  "ऐई अ एफे रेने आए"
```

The root cause is that IndicF5 was trained on Indic-script data. The ASCII
character embedding rows (`A`–`Z`, `a`–`z`) were never adequately learned. When
the model receives a Roman token, it looks up a near-random embedding vector and
produces near-random acoustic output. This is **Mode C failure**: correct canvas,
wrong content.

### The fix

Convert Roman input to Devanagari before it reaches the model. The model only
sees characters it knows.

`to_unified_devanagari()` in `scoring/scripts/lib_normalize.py` does this in
three passes:

1. **Whitelist lookup** (checked first). A table of ~60 English loanwords and
   Indian named entities maps to their canonical Devanagari forms:
   `office → ऑफिस`, `Mumbai → मुंबई`. Canonical forms are fixed so the model
   always sees the same Devanagari string for a given English word, regardless of
   how it was originally spelled.

2. **Function-word whitelist** (checked before IndicXlit). Short Hindi words in
   Roman script — `tu`, `mai`, `aa`, `hu` — are intercepted before the
   transliterator sees them. IndicXlit is trained on English data and misreads
   these: `tu → टू` (English "to") instead of `तू` (Hindi "you"). The four
   corrected entries are responsible for three of the four post-v2.0 score
   improvements in the v2.1 run.

3. **IndicXlit transliteration** (fallback). Any Roman token not in either
   whitelist is passed to `ai4bharat-transliteration` (`XlitEngine("hi",
   beam_width=4)`), which produces the top-1 Devanagari transliteration.

Pure Devanagari tokens pass through unchanged. Punctuation and digits pass
through unchanged. The function is idempotent: applying it twice gives the same
result.

### What this achieves

After preprocessing, the model receives the same character types it was trained
on. `silence_or_skip` dropped from 16/30 to 0/30. The per-category scores went:

| Category | Before (patch only) | After (patch + xlit) |
|---|:---:|:---:|
| pure_roman | 1.00 | 4.75 |
| mixed_script | 1.88 | 4.88 |
| english_with_NE | 1.00 | 4.50 |
| pure_devanagari | 4.62 | 4.62 |

No model weights were changed. The IndicF5 v12 parameters are identical to
the original release.

---

## 3. Three-ASR consensus scoring

The 4.70 number comes from a three-backend intelligibility score, not a single
ASR system. This matters because each backend fails differently on Hindi.

### Why single-ASR fails

AssemblyAI (AAI) returns empty transcripts on clips shorter than ~1.7 s. This
is a hard floor in their Hindi pipeline, not a model-quality signal. In the v2.1
eval, sentence id 11 produced a 1.7 s clip — AAI returned empty, which would
score as 1/5 on intelligibility. Deepgram and Groq (Whisper large-v3) both
returned the correct transcript and scored 5. A single-AAI score would have
called this sentence a failure.

The pattern is systematic: AAI penalises short-clip Hindi. Groq is more robust
at short durations but degrades differently on atypical code-switch patterns.
Deepgram handles code-switching well but is noisier on low-amplitude recordings.
No single system is uniformly reliable across all Hinglish categories.

### How consensus works

All three backends transcribe the same WAV independently. The intelligibility
score for each backend is computed via symmetric CER:

1. Apply `to_unified_devanagari()` to both the ASR transcript and the reference
   text. This normalises script — AAI sometimes returns Roman characters for
   Devanagari content; the normaliser converts both sides to the same form before
   comparing.

2. Compute CER between normalised transcript and normalised reference.

3. Map CER to a 1–5 intelligibility score (0%→5, ≤10%→4, ≤25%→3, ≤50%→2, >50%→1).

4. The sentence score is the **median** of the three backend scores.

Symmetric normalisation is the important part: the same `to_unified_devanagari`
function is used on the model input (preprocessing) and on the scoring reference
(normalisation). There is no script-mismatch false positive where the model
produces `ऑफिस` from the whitelist but the reference says `office`.

### What the numbers look like in practice

Of the 30 sentences, 26 have three-way agreement (all backends give the same
score). The remaining 4 have a 2-1 split; the median still resolves cleanly.
No sentence has a 0-2 split or a three-way disagreement. The consensus is stable.

---

## 4. What we tried that didn't work

### LoRA fine-tuning

The original Phase 2 plan was to fine-tune IndicF5 with LoRA adapters on a
curated Hinglish dataset. We measured the baseline score first and found it was
1.97/5 — but the diagnostic revealed that the failure was upstream of the
transformer entirely. The canvas-sizing formula in `utils_infer.py` runs before
the DiT receives any input. LoRA adapters in the DiT cannot enlarge the canvas;
they can only change what the DiT paints inside whatever canvas it is given. A
LoRA run would have improved acoustic quality in a 0.8 s clip while leaving the
0.8 s duration wrong. The 2-line patch saved approximately 8 GPU-hours of
Kaggle compute and the accompanying risk of confusing canvas improvements with
acoustic ones.

### Single-ASR scoring

The Phase 1 scores were computed with AssemblyAI only. The AAI-only overall
for the final configuration would have been approximately 4.40 instead of 4.70.
Four sentences where AAI returned empty (clips 1.5–1.9 s) pulled the mean down.
Those same sentences scored 5 on Groq and Deepgram consensus. The AAI-only
number was not wrong — it accurately reflected AAI's behaviour on this data —
but it understated intelligibility as a human would judge it. Moving to
three-ASR consensus added ~0.3 ranks and made the score independent of any
one backend's floor behaviour.

### Automated naturalness scoring

We ran UTMOS and SQUIM (English-trained MOS predictors) on human Hinglish
recordings as a ceiling check. UTMOS rated the human recordings at **1.95/5**
while rating the IndicF5 TTS output at **4.40/5** — a directional inversion of
+2.44 ranks. The predictors are not wrong in absolute terms; they are accurately
predicting how English-trained MOS models would rate non-English speech. But they
cannot serve as a naturalness proxy for Hindi. There is no automatic naturalness
number in this report because none of the tested predictors produce one that
tracks human perception on Hindi data. Naturalness is assessed by ear only.

---

## Summary

The package achieves 4.70/5 through two inference-time interventions, neither
of which requires model retraining:

1. **Duration patch** — fixes a byte-vs-character arithmetic error in
   `utils_infer.py` that allocated 30–70% too little audio canvas for
   non-Devanagari text.

2. **IndicXlit preprocessing** — converts Roman input to Devanagari before the
   model sees it, bypassing the undertrained ASCII embedding subspace.

The 4.70 score is a three-ASR consensus intelligibility measure on 30 Hinglish
sentences. The proof that these two fixes are sufficient is the before/after
table: 2.13 → 2.20 (duration patch alone) → 4.57 (plus preprocessing) → 4.70
(plus function-word whitelist). No steps between.
