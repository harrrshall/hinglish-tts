# IndicF5 patched re-run — comparison report

**Date:** 2026-05-09
**Patch:** `f5_tts/infer/utils_infer.py:449-452` byte-count → character-count proportional duration arithmetic. 4 lines changed in one file. Applied via Kaggle kernel v13 of `harshalsinghcn/hinglish-tts-audit-indicf5`.
**Inputs:** original IndicF5 v12 baseline at `audit/results/indicf5/`, patched v13 at `audit/results/indicf5_patched/`. Three-ASR consensus (AAI + Deepgram + Groq Whisper), deterministic rubric per JUDGE_PROMPT.md v1.0.

## TL;DR

The Mode A (canvas under-allocated) hypothesis from the diagnostic is **confirmed**: patched durations land at 0.86–1.29× expected across categories (vs 0.30–0.95× before), and `silence_or_skip` flags collapse from **21/30 → 0/30**. But fixing the canvas exposes a *second*, larger failure mode the diagnostic missed: **the model cannot pronounce non-Devanagari characters**. Roman tokens come out as acoustic gibberish (e.g. "kal mujhe office jaana hai" → "ऐई अ एफे रेने आए"). Per-Likert intelligibility moved only +0.17 overall (1.97 → 2.13) because most affected clips remain at score 1 (CER>0.5 / WER>0.5).

**Phase 2 verdict:** patch is necessary but not sufficient. **22 of 30 sentences still fail at intel ≤ 2**. The dominant residual mode is *right-length-garbled* (Mode C, 15/22), not still-truncating (3/22) or over-allocated (4/22). Phase 2 fine-tune should target input character embeddings + early DiT layers — *not* attention/MLP scope. Or pivot to Kokoro (3.03 overall) as the production base.

---

## Section 1 — Patch effect on duration

Per-sentence durations and scale factor (patched / original). All 30 inferences succeeded.

| id | category | text | orig (s) | patch (s) | scale | patch/expected |
|----|----------|------|---------:|----------:|------:|---------------:|
| 01 | pure_devanagari | कल मुझे दिल्ली जाना है। | 1.84 | 1.80 | 0.98× | 0.90 |
| 02 | pure_devanagari | क्या आप मुझे पानी दे सकते हैं? | 2.29 | 2.28 | 1.00× | 0.82 |
| 03 | pure_devanagari | मेरा भाई आज स्कूल नहीं गया... | 4.31 | 4.19 | 0.97× | 0.95 |
| 04 | pure_devanagari | मेरे पास सिर्फ़ तीन सौ रुपये... | 4.10 | 4.00 | 0.98× | 0.83 |
| 05 | pure_devanagari | जल्दी आओ यार, सब तेरा... | 3.18 | 3.15 | 0.99× | 0.87 |
| 06 | pure_devanagari | आज बहुत थक गया हूँ... | 3.31 | 3.24 | 0.98× | 0.81 |
| 07 | pure_devanagari | तुझे पता है कल मीटिंग... | 2.70 | 2.67 | 0.99× | 0.83 |
| 08 | pure_devanagari | अरे यार, मेरा फ़ोन कहाँ... | 2.36 | 2.48 | 1.05× | 0.88 |
| 09 | pure_roman | kal mujhe office jaana hai | 0.78 | 2.09 | **2.68×** | 1.05 |
| 10 | pure_roman | mera naam Arjun hai aur mai Bengaluru se hu | 1.29 | 3.34 | **2.59×** | 0.93 |
| 11 | pure_roman | yaar tu kal kya kar raha tha | 0.83 | 2.09 | **2.51×** | 0.75 |
| 12 | pure_roman | kya tu bhi aaj party me aa raha hai? | 1.08 | 2.67 | **2.48×** | 0.74 |
| 13 | pure_roman | abe yaar jaldi reply kar... | 1.39 | 3.52 | **2.54×** | 0.88 |
| 14 | pure_roman | kal raat ka movie tha bohot bakwaas... | 1.66 | 4.38 | **2.63×** | 1.10 |
| 15 | pure_roman | tera laptop kab tak deliver hoga bhai? | 1.14 | 3.05 | **2.67×** | 1.09 |
| 16 | pure_roman | yaar tu bohot lucky hai... | 1.45 | 3.81 | **2.62×** | 1.06 |
| 17 | mixed_script | Kal mujhe ऑफिस... will be an issue. | 2.54 | 4.19 | 1.65× | 0.98 |
| 18 | mixed_script | Mera presentation tomorrow है... | 2.18 | 4.10 | 1.88× | 1.32 |
| 19 | mixed_script | Bhai please मेरा homework... | 2.93 | 4.19 | 1.43× | 1.08 |
| 20 | mixed_script | Tumne वो new restaurant try kiya... | 2.29 | 5.25 | 2.29× | 1.13 |
| 21 | mixed_script | कल का event cancel हो गया... | 2.88 | 4.29 | 1.49× | 1.01 |
| 22 | mixed_script | Boss को बता देना kal मैं leave... | 3.49 | 4.86 | 1.39× | 0.97 |
| 23 | mixed_script | Ye file को quickly review करो... | 2.36 | 4.29 | 1.82× | 1.11 |
| 24 | english_with_NE | My friend Aishwarya from Chennai... | 1.96 | 5.34 | **2.72×** | 1.43 |
| 25 | english_with_NE | Mr. Khanna will join the meeting... | 2.06 | 5.44 | **2.64×** | 1.21 |
| 26 | english_with_NE | I love butter chicken from Karim's... | 1.45 | 3.81 | **2.62×** | 1.13 |
| 27 | mixed_script | Office में सब log lunch के लिए... | 2.96 | 4.10 | 1.38× | 0.76 |
| 28 | english_with_NE | Rohan is flying from Mumbai to Bengaluru... | 2.03 | 5.44 | **2.68×** | 1.32 |
| 29 | english_with_NE | Let's grab biryani from Paradise... | 1.78 | 4.86 | **2.73×** | 1.44 |
| 30 | english_with_NE | She just got hired at Tata... | 1.69 | 4.48 | **2.66×** | 1.19 |

### Category means

| category | orig | patch | scale | patch/expected |
|----------|-----:|------:|------:|---------------:|
| pure_devanagari | 3.01 s | 2.98 s | **0.99×** (unchanged ✓) | 0.86 |
| pure_roman | 1.20 s | 3.12 s | **2.59×** | 0.95 |
| mixed_script | 2.70 s | 4.41 s | **1.67×** | 1.04 |
| english_with_NE | 1.83 s | 4.90 s | **2.68×** | 1.29 |

This matches the diagnostic prediction almost exactly: pure_devanagari sees ~no change (the formula was already correct for Devanagari→Devanagari); pure_roman / english_with_NE roughly triple (the byte-vs-char ratio for ASCII vs Devanagari ≈ 3); mixed_script sits between.

The english_with_NE column overshoots (1.29× expected) — the patched formula is slightly too generous for ASCII-only English. This shows up as silent tail / model-padding-with-junk on 4 sentences (18, 24, 28, 29). Not a fatal issue but worth noting for any future per-script refinement.

Three-ASR debug-patch records: `audit/results/indicf5_patched/duration_log.txt`.

---

## Section 2 — Per-category intelligibility (3-ASR consensus)

| category | original IndicF5 | patched IndicF5 | Δ |
|----------|:----------------:|:---------------:|:---:|
| pure_devanagari | 4.38 | **4.75** | **+0.38** |
| pure_roman | 1.00 | 1.00 | 0.00 |
| mixed_script | 1.25 | **1.50** | **+0.25** |
| english_with_NE | 1.00 | 1.00 | 0.00 |
| **overall** | **1.97** | **2.13** | **+0.17** |

`silence_or_skip` flag count: **21/30 → 0/30** (consensus across all three ASRs).

The Likert intel barely moves on Roman/English categories because the rubric scores `1` for any CER>0.50 or WER>0.50 — and the patched outputs still score there. The functional difference is very real (audio is now full-length and contains pronounced syllables, vs the original's truncated ~0.8s clips of "Ranai." or empty transcripts) — it's just hidden under the rubric's coarse anchor structure. **The right way to read this row is: the patch eliminated truncation as a failure mode and exposed the underlying acoustic-content failure.**

Pure_devanagari `+0.38` is real but small — slight CER differences across re-runs (one sentence #04 actually regressed by 1 rank due to ASR variance on "तीन सौ" vs "300" rendering, which is a known schwa-elision / numeral issue, not a TTS regression).

---

## Section 3 — Patched IndicF5 vs the four-model field

3-ASR consensus intelligibility, original four-model figures from `audit/auto_scores.md`:

| model | pure_dev | pure_roman | mixed_script | english_NE | overall |
|-------|:--------:|:----------:|:------------:|:----------:|:-------:|
| Kokoro | 4.88 | 1.25 | 1.50 | 5.00 | **3.03** |
| Indic Parler-TTS | 4.00 | 1.12 | 1.50 | 4.83 | **2.73** |
| IndicF5 (orig) | 4.38 | 1.00 | 1.25 | 1.00 | 1.97 |
| SPRINGLab F5-Hindi | 4.25 | 1.00 | 1.25 | 1.00 | 1.93 |
| **IndicF5 (patched)** | **4.75** | 1.00 | **1.50** | 1.00 | **2.13** |

Patched IndicF5 climbs above SPRINGLab and original IndicF5 but stays well behind Kokoro and Parler. The structural gap from the field leaders is entirely on `pure_roman` and `english_with_NE` — categories where Kokoro renders clean English NE and Parler nearly so, while both F5 family models flatline at 1.00.

**This is decisive about Phase 2 strategy:** the duration patch was the cheapest possible fix (4 lines, no training, no new dependencies); it brought the working case (Devanagari) up by a fraction and surfaced the truncation→garble shift on every other category. *The remaining gap to the field leaders is an acoustic content gap, not a duration gap.*

---

## Section 4 — Residual failure modes (n = 22 at intel ≤ 2)

Each residual classified by `patch/expected` ratio + transcript inspection:

| failure mode | criterion | count | sentence ids |
|--------------|-----------|------:|--------------|
| **STILL_TRUNC** | patch_dur < 0.8 × expected | 3 | 11, 12, 27 |
| **OVER_ALLOC** | patch_dur > 1.25 × expected | 4 | 18, 24, 28, 29 |
| **RIGHT_LEN_GARBLED** | 0.8 ≤ patch/expected ≤ 1.25 but content wrong | **15** | 09, 10, 13–17, 19–23, 25, 26, 30 |

### What "RIGHT_LEN_GARBLED" looks like

The dominant residual mode (15/22). The model fills the now-correct canvas length with audio that does not correspond to the input characters. Examples:

| id | input | patched ASR transcript |
|----|-------|------------------------|
| 09 | kal mujhe office jaana hai | "ऐई अ एफे रेने आए" |
| 22 | Boss को बता देना kal मैं leave पर रहूँगा, kuch personal काम है | "पुस को बता देना आई मैं रुनी पर रहूंगा और से सरजाल काम है" |
| 24 | My friend Aishwarya from Chennai is visiting Bengaluru next week | "ई फ्रेंड एकेरी फंक्शेनाई ऐसे चें विनर ओडू निजच लिए" |
| 30 | She just got hired at Tata Consultancy Services in Pune | "सेरोज या हैन एट टैटर हैनोसन दी सरेशन उनी" |

**Pattern across all 15:** Devanagari content (where present) renders correctly. ASCII/Roman content is replaced by approximate-syllable acoustic noise that doesn't decode to either Hindi or English. This is not "the model anglicized Roman input as English"; it's "the model has no idea what to do with non-Devanagari characters". On sentence 22 you can see it cleanly: every Devanagari word survives (बता देना, मैं, पर, रहूँगा, काम है) and every Roman word is mangled (Boss→पुस, leave→रूनी, kuch personal→ऐसे सरजाल).

This is the Mode C from the diagnostic prompt's classification: *canvas correct, content garbled, tokenization/embedding issue, LoRA on input embeddings + early DiT layers can fix this.* IndicF5's training data was Indic-language text (presumably Devanagari + a small set of related scripts). The character embedding for ASCII is undertrained — the DiT receives a near-random input vector for "k", "a", "l", "m", "u", "j", "h", "e" and produces near-random output.

### What "STILL_TRUNC" looks like (3 cases)

Sentences 11, 12 (pure_roman) and 27 (mixed_script with significant Roman). Patch under-corrected because these are slightly word-dense for their character count. The duration formula is character-proportional, but the rate (chars/sec) calibrated from the Devanagari reference is slightly low for these specific Roman-Hindi inputs. Minor — would be fixed by either (a) a per-script multiplier or (b) a Roman-Hindi reference clip. Not blocking.

### What "OVER_ALLOC" looks like (4 cases)

Sentences 18, 24, 28, 29 — all longer English-with-NE inputs. The patched formula gives them more canvas than they need to speak (1.21–1.44× expected). Output contains the right syllable count's worth of audio plus silent tail or padding noise. Not strictly wrong, but evidence that ASCII chars are not perfectly 1:1 with Devanagari chars in spoken duration — English is faster per character than Hindi (more consonant clusters, shorter average syllable duration). A per-script multiplier (~0.8× for ASCII vs Devanagari) would tighten this.

---

## Section 5 — Phase 2 recommendation

Per the framework given in the original agent prompt:

> **If 10+ sentences still fail:** Phase 2 fine-tune is broader; the duration patch was necessary but not sufficient. Diagnose further before committing to a training run.

**22 sentences fail.** But the diagnosis is now done — Section 4 has it. Three options for Phase 2:

### Option A — LoRA on character embeddings + early DiT layers (focused)

Target: the 15 RIGHT_LEN_GARBLED sentences. Fine-tune scope:
- input character embeddings (esp. ASCII positions)
- DiT layers 0–4 (where char→phoneme alignment crystallizes)
- *not* attention/MLP on later layers
- training data: Roman-Hindi + English-with-Indian-NE text + paired audio. Probably needs a curated 1–2k clip dataset.

Risk: F5-TTS character embedding is small (256-dim?); LoRA may not have enough capacity to repair a never-trained subspace. Worth a 4 GPU-hour shakedown before committing.

### Option B — abandon IndicF5 base, use Kokoro

Kokoro is already at 3.03 overall (vs patched IndicF5's 2.13). Kokoro's pure_devanagari is 4.88, pure_roman 1.25, english_NE 5.00 — it loses on Roman-Hindi but wins everywhere else.

The Roman-Hindi gap on Kokoro is a different kind of problem (lang_code='h' phonemizing Roman as English, per RUN_NOTES). The fix there is a Roman→Devanagari pre-tokenization layer (IndicXlit-style), which is much cheaper than a LoRA fine-tune.

This option finishes Phase 1.5 with a different production base than originally assumed and skips Phase 2 training entirely.

### Option C — refine the patch + revisit

Two cheap inference-side improvements before training:
1. Per-script character multiplier (1.0 for Devanagari, ~0.8 for ASCII) — fixes OVER_ALLOC.
2. Try a Roman-Hindi reference audio + transcript instead of the current Devanagari one — should fix STILL_TRUNC and might partially help RIGHT_LEN_GARBLED via prosody conditioning.

Total cost: ~1 Kaggle kernel run, no training. Worth doing before either A or B.

### Recommendation

**Start with C (refinement, 1 hour), then make the A-vs-B call based on the residual.** Skipping straight to A is plausible but premature — there's still ~20% gap between the patched formula and "ideal" duration, and Roman-Hindi reference conditioning has not been tested. Skipping straight to B is also defensible if compute budget is tight; Kokoro is already a viable production base for everything except Roman-Hindi, and the Roman-Hindi fix on Kokoro doesn't require GPU training.

The user makes the final call — these three are the options.

---

## Section 6 — Caveats

- **n=30 audit set.** Generalization to wild Hinglish input is unmeasured.
- **Naturalness/speaker_quality scores were computed but are not reported above.** UTMOS/SQUIM are English-trained and drift on Hindi by 1.5–2 ranks per `audit/SCORING_NOTES.md` §2; the per-ASR consensus naturalness for patched IndicF5 came out at 3.83, but this is an artifact of the predictors, not a meaningful comparison signal. They're in the per-ASR CSVs (`auto_scores_*.csv`) for completeness.
- **Patched character-count proportionality is reference-dependent.** The current Devanagari reference clip's chars/sec calibration works well for Devanagari/mixed targets and slightly over-allocates for ASCII-only targets. Switching to a Roman-Hindi reference would re-calibrate (likely better for ASCII, worse for Devanagari). Section 5 Option C addresses this.
- **The 4 OVER_ALLOC sentences (18, 24, 28, 29) over-allocate by 21–44%.** The model fills the extra canvas with what sounds like silent / monotone trailing rather than additional content. Listen-test would distinguish "model padded with silence" (fixable by trimming) from "model produced extra phonemes" (fine-tune territory).
- **Sentence 04 regressed by 1 intel rank** (4 → 3) due to ASR transcribing "तीन सौ" as "300" — the same issue noted in original `auto_scores.md`. ASR variance, not TTS regression.
- **Three sentences (11, 12, 27) hit the rubric's 0.30 < CER ≤ 0.50 → 2 anchor on AAI but 0.50 < CER → 1 on Deepgram/Groq.** Consensus rolled them to 1. Cross-ASR variance on hard clips is a known fragility of the deterministic rubric; neither is "correct" — they reflect different ASR models' tolerance for mangled output. This is a separate issue from the patch evaluation.
- **The deterministic scorer was used in place of the original Claude-as-judge pipeline** to remove per-batch variance across the three ASR backends. The mapping matches `JUDGE_PROMPT.md v1.0` thresholds exactly; the only difference vs the original auto_scores.md is that the ±1 phonetic-not-wrong adjustment for Indian named entities (which requires audio listening) is not applied. This means proper-noun-heavy rows may underrate slightly vs the original Claude-judged scores. Not load-bearing for the comparison since both original and patched rows would get the same phantom underrating.

---

## Files

- `auto_scores_consensus.csv` — 3-ASR consensus, 30 rows (the canonical scoring output)
- `auto_scores_aai.csv`, `auto_scores_deepgram.csv`, `auto_scores_groq.csv` — per-ASR scores
- `signal_vectors_aai.json`, `signal_vectors_deepgram.json`, `signal_vectors_groq.json` — Stage 1 raw signals
- `per_sentence_compare.json` — per-sentence durations + intel deltas (Section 1 + 4 source data)
- `sanity/_sanity_09.wav` — the sentence-09 sanity wav (2.09s, vs original 0.78s)
- `KAGGLE_CELLS.md` — the Kaggle notebook cells used to produce the patched run (kernel v13)
- `patch.diff` — unified diff of the 4-line `utils_infer.py` change
- patched wavs at `audit/results/indicf5_patched/01.wav` … `30.wav` + `duration_log.txt` + `log.json`
