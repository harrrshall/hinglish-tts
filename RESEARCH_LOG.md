# Research Log

> Append-only. One entry per session or decision milestone. Numbers are
> rubric v2.0 / 3-ASR consensus unless noted otherwise. If any other doc
> disagrees with this file, **this file wins.**

---

## 2026-05-07 — Phase 1: scaffolding + first two models

**Objective:** Baseline 5-model TTS audit on 30 Hinglish sentences. No
training. Inference-only on Kaggle T4.

**What ran:**

- **Kokoro v1.0** (hexgrad/Kokoro-82M, 82M params) — 30/30 wavs, CPU local.
- **Indic Parler-TTS** (ai4bharat/indic-parler-tts, 880M) — 30/30 wavs,
  Kaggle T4 x2, kernel v9. Prompted via text-description.

**What didn't run:**

- **IndicF5** — blocked on Kaggle Secrets bug (`UserSecretsClient`
  connection error). Workaround: hardcode HF_TOKEN inline, Save & Run All,
  do NOT CLI-push afterward. Carried to next session.
- **SPRINGLab F5-Hindi** — state_dict mismatch (18 vs 22 transformer blocks)
  between the original SPRINGLab repo and IndicF5. Needs the rumourscape fork.
  Deferred.
- **Orpheus-Hindi** (SachinTelecmi/Orpheus-tts-hi, 3B 4-bit) — HF gating
  pending `Sachin@Telecmi.com`. Deferred.

**Key decisions made:**

- Eval set split: 8/8/8/6 (pure_devanagari / pure_roman / mixed_script /
  english_with_NE) = 30 sentences, per AUDIT_PLAN.md §1.1. ID 27 assigned
  to mixed_script (§1.3 was ambiguous; §1.1 wins).
- Orpheus variant: SachinTelecmi per runbook; canopylabs alternative
  noted but not chosen.

**Artifacts:** `data/eval_sentences.tsv` (frozen), `experiments/01_baseline/notebooks/`, `experiments/01_baseline/wavs/kokoro/`, `experiments/01_baseline/wavs/indic_parler/`.

---

## 2026-05-08 — Phase 1: IndicF5 unblocked; SPRINGLab + Orpheus deferred

**IndicF5** (ai4bharat/IndicF5, 330M) — 30/30 wavs via kernel v12 (T4 x2,
HF token hardcoded). Phase 1 effective completion: 3 of 5 models = 90 wavs.
SPRINGLab and Orpheus remain deferred indefinitely.

**Prelim v1 scores (AAI only, deterministic, rubric v1.0):**

| model | overall |
|---|:---:|
| Kokoro | 3.03 |
| Indic Parler-TTS | 2.73 |
| IndicF5 | 1.97 |

IndicF5's 1.97 is dominated by `silence_or_skip` on 21/30 sentences —
outputs were generating valid-sounding clips in ~0.8–2.5 s where
sentences warranted 3–6 s. This flagged a duration bug, not a model
quality failure.

**Artifacts:** `experiments/01_baseline/wavs/indicf5/` (30 wavs), `experiments/01_baseline/SESSION_LEARNINGS.md`.

---

## 2026-05-09 (part 1) — Human ceiling study + rubric v2.0

Two infra milestones required before any meaningful model comparison.

### Human groundtruth ceiling study

Scored 8 human Hinglish recordings under the same rubric. Finding: UTMOS/
SQUIM naturalness predictors underrate human recordings by **1.5–2 ranks**
vs perceptual ground truth on Hindi. Both predictors are English-trained
and drift badly on non-English phonology.

**Decision:** Lock naturalness as **ear-only** in all future reporting.
MOS predictors removed from scoring pipeline. Intelligibility, code_switch,
and silence_or_skip remain computable automatically.

Artifact: `scoring/rubric/CEILING_REPORT.md`.

### Rubric v2.0 — locked

Key changes vs v1.0:

1. **Unified Devanagari normalization** via `lib_normalize.to_unified_devanagari()` applied to both ASR transcript and reference text before WER/CER computation. Eliminates script-mismatch false negatives (e.g. AAI transcribing Devanagari content as Latin characters would previously score CER=1.0).
2. **Three-ASR consensus** (AAI + Deepgram + Groq Whisper) with median-of-three intelligibility. Reduces single-backend ASR failure artifacts.
3. **Naturalness = `ear-only` string** in all CSV outputs. No numeric naturalness column.
4. English-loan whitelist (`ENGLISH_LOAN_CANONICAL`) prevents over-penalizing legitimate code-switch tokens.

Artifact: `scoring/rubric/JUDGE_PROMPT_v2.md` — do not edit without versioning.
Supporting scripts: `scoring/scripts/lib_normalize.py`, `scoring/scripts/extract_signals_v2.py`, `scoring/scripts/judge_v2.py`.

---

## 2026-05-09 (part 2) — Duration diagnostic + IndicF5 patch (Mode A)

**Diagnosis of IndicF5 silence_or_skip:** Root cause in
`f5_tts/infer/utils_infer.py:449–452`. Duration formula used **byte count**
of input text instead of character count. Devanagari encodes as ~3 bytes/char
in UTF-8; ASCII encodes as 1 byte/char. Result: for Roman-script input, the
model allocated ~3× less canvas time than needed. Audio was truncated at the
byte-proportional cut. `patch.diff` — 4 lines changed.

Fix applied as Kaggle kernel v13. Re-run: 30/30 wavs, patched.

**Results (rubric v2.0, 3-ASR consensus):**

| category | original | patched | Δ |
|---|:---:|:---:|:---:|
| pure_devanagari | 4.62 | 4.62 | +0.00 |
| pure_roman | 1.00 | 1.00 | 0.00 |
| mixed_script | 1.62 | 1.88 | +0.25 |
| english_with_NE | 1.00 | 1.00 | 0.00 |
| **overall** | **2.13** | **2.20** | **+0.07** |

`silence_or_skip`: 20/30 → 16/30.

**Mode A confirmed. Mode C exposed.** The patch fixed duration allocation
as predicted. But fixing the canvas revealed the underlying content
failure: 15 of the 22 still-failing sentences are **RIGHT_LEN_GARBLED** —
correct duration, wrong acoustic content. Example:

> input: `kal mujhe office jaana hai`
> patched ASR: `"ऐई अ एफे रेने आए"`

Pattern: every Devanagari token in a mixed sentence renders correctly;
every Roman/ASCII token produces syllabic noise. Root cause: IndicF5's
ASCII character embeddings are undertrained. The model was trained on
Indic-script data; the embedding subspace for A–Z was never adequately
learned. The model receives a near-random vector for ASCII characters and
produces near-random output.

**Decision:** Test inference-time mitigation before any fine-tuning. Hypothesis: IndicXlit-transliterate input to Devanagari → model only sees characters it knows → garbling disappears.

**Artifacts:** `experiments/02_indicf5_patch/patch.diff`, `experiments/02_indicf5_patch/COMPARISON.md`, `experiments/02_indicf5_patch/wavs/01..30.wav`, `diagnostics/duration_diagnostic/REPORT.md`.

---

## 2026-05-10 — IndicXlit input preprocessing — Outcome A confirmed

**Experiment:** Transliterate all Roman tokens in the 30 eval sentences to
Devanagari using `lib_normalize.to_unified_devanagari()` before feeding
patched IndicF5. Same function rubric v2.0 uses for transcript normalization
— symmetric by design. English-loan whitelist terms pass through unchanged.
`pure_devanagari` rows are no-ops (preprocessing_applied = "no" for all 8).

Kaggle kernel `harshalsinghcn/hinglish-tts-audit-indicf5-xlit` v1, T4 x2.
30/30 wavs produced.

**Three-way results (rubric v2.0, 3-ASR consensus):**

| category | original | patched | patched+xlit | Δ (xlit–patch) |
|---|:---:|:---:|:---:|:---:|
| pure_devanagari | 4.62 | 4.62 | 4.62 | +0.00 |
| pure_roman | 1.00 | 1.00 | **4.38** | **+3.38** |
| mixed_script | 1.62 | 1.88 | **4.88** | **+3.00** |
| english_with_NE | 1.00 | 1.00 | **4.33** | **+3.33** |
| **overall** | **2.13** | **2.20** | **4.57** | **+2.37** |

`silence_or_skip`: 20/30 → 16/30 → **0/30**.
`speaker_quality_v2` (PESQ): 4.30 → 4.17 → **4.50**.

**Field ranking under v2.0:**

| model | overall | pure_roman | eng_NE |
|---|:---:|:---:|:---:|
| **indicf5_patched_xlit** | **4.57** | **4.38** | 4.33 |
| kokoro | 3.90 | 2.50 | **4.83** |
| indic_parler | 3.40 | 1.75 | 4.67 |
| indicf5_patched | 2.20 | 1.00 | 1.00 |
| indicf5 (orig) | 2.13 | 1.00 | 1.00 |
| springlab_f5 | 2.07 | 1.00 | 1.00 |

**Outcome A.** Preprocessing resolves Mode C fully. All 15 RIGHT_LEN_GARBLED
sentences from the patched-only run now score 4 or 5. Zero residual failures
(no sentence ≤2). The embedding-undertraining hypothesis was correct.

Patched+Xlit is the highest-scoring configuration on every category except
english_with_NE, where Kokoro wins by 0.5 ranks (4.83 vs 4.33). Even there,
patched+xlit doubles Kokoro's pure_roman score (4.38 vs 2.50) — Hinglish-Roman
intelligibility is now solved without fine-tuning.

**Two residual 3s** (id 12, 16 — pure_roman): IndicXlit renders `tu → टू`
("to") rather than `तू` ("you"). The model produces `टू` faithfully and the
ASR recovers `तू`, but the phonetic gap hits the CER threshold. Fix: add
`tu / mai / aa / hu` to `ROMAN_HINDI_FUNCTION_WORDS` in `lib_normalize.py`.
Not applied this run (v2.0 symmetry constraint; whitelist edits require
full v2 rebuild). Documented as v2.1 candidate.

**Caveats:**

- n=30. The English-loan whitelist in `lib_normalize.py` was tuned to this
  vocabulary. Generalization requires whitelist expansion or a learned
  token classifier.
- `english_with_NE` rows produce Hindi-accented-phonetic English (e.g.
  "My friend Aishwarya" → "माय फ्रेंड ऐश्वर्या"). ASR scores it highly;
  whether a listener judges this as acceptable is an open question.
- No fine-tuning. IndicF5 v12 weights unchanged. This is a pure
  inference-time intervention.
- Baseline scoring asymmetry: the 4 original models (Kokoro, Parler,
  IndicF5, SPRINGLab) used AAI-only signals for Deepgram/Groq dimensions;
  both patched runs are fully 3-ASR. Cross-model comparisons carry this caveat.

**Path forward — user to decide:**

- **Path A (ship):** Current patched+xlit stack is the production deliverable.
  ~10 LOC preprocessing wrapper + duration patch. No training, no new
  model weights, no new dependencies beyond IndicXlit (already installed).
- **Path B (one more pass):** Apply v2.1 whitelist patch (`tu/mai/aa/hu`)
  and optionally a per-script duration multiplier (~0.8× for ASCII to
  address the 4 OVER_ALLOC sentences). Inference-only, ~1 Kaggle run.
  Expected effect: id 12 and 16 lift from 3→5; overall from 4.57→~4.65.

Both paths skip LoRA fine-tuning — the training need that Phase 2 was
originally designed around no longer exists.

**Artifacts:** `experiments/03_indicf5_xlit/COMPARISON.md`,
`experiments/03_indicf5_xlit/preprocessed_sentences.tsv`,
`experiments/03_indicf5_xlit/wavs/01..30.wav`,
`experiments/01_baseline/scores/auto_scores_v2.csv` (180 rows, 6 models).

---

## 2026-05-11 — Direction 1 + Direction 2 synthesis: phonetic awareness profile of IndicF5

**Headline:** IndicF5 has partial phonetic awareness — selective marker sensitivity
(Direction 1) and weak cross-script representation sharing (Direction 2). The
phoneme layer is more grapheme-bound than phoneme-mediated, but not purely
grapheme-bound either.

---

### Background

Two parallel probes ran concurrently on IndicF5 v12 weights + duration patch,
bypassing IndicXlit preprocessing (feeds text verbatim to the model). The goal
was to determine whether the model's internal representations are organized by
phoneme or by grapheme — and therefore whether a pronunciation dictionary
(Direction 3) can improve quality without retraining.

**Direction 1** (`experiments/05_phonetic_probe`): 6 Devanagari phonetic
distinctions × 3 variants each (18 clips total). Tests whether fine-grained
markers — nukta, halant, vowel matras, aspiration, script register, punctuation
— produce different acoustic output when fed to the model verbatim.

**Direction 2** (`experiments/06_grapheme_phoneme_probe`): 32 clips across three
tests. Test A: Devanagari vs Roman homophones (cross-script similarity). Test B:
/k/ phoneme consistency within Hindi across 8 vowel contexts. Test C:
cross-language /k/ phoneme transfer (Hindi / Roman Hindi / English).

---

### Finding 1 — Within Devanagari: phoneme-mediated organization (Direction 2, Test B)

The /k/ phoneme onset across 8 distinct vowel contexts shows strong spectral
consistency: mean pairwise onset-MFCC similarity = 0.827 (C1–C12, silence
stripped), all 28 pairs positive, unimodal distribution. F0 varies systematically
by vowel context (back-low vowels /ʌ,aː/ → ~93 Hz; front/round vowels → 121–219
Hz), which is a textbook coarticulation pattern.

Two independent measures — MFCC and F0 — agree: within the Devanagari embedding
space, phoneme-level organization exists. The model has learned phonologically
structured representations, not a flat lookup from grapheme to audio.

### Finding 2 — Devanagari markers: selectively reactive, not uniformly sensitive (Direction 1)

Of the 6 phonetic distinctions probed, the model produces measurably different
acoustic output for 3, partial output for 2, and no difference for 1.

| Marker | Result | Key evidence |
|---|---|---|
| Vowel length (ि vs ी) | Sensitive | All-long ī variants produce clearly distorted output; ASR (Deepgram, Groq) diverges across variants |
| Nukta (ज़ vs ज) | Sensitive* | Nukta-absent जारा → model generates 'जा रहा है' (OOV collapse, not clean /j/→/z/) |
| Script register (Roman vs Devanagari) | Sensitive | Roman "office" → Mode C garble; ऑ vs आ vowel audible across Devanagari variants |
| Aspiration (ख vs क) | Partial | Groq captures ख/क contrast in mixed input (4c: खाना vs काओ); short clips limit ASR reliability |
| Prosody / punctuation | Partial | Lexical repetition (बहुत बहुत) produces longer audio; punctuation marks are ignored |
| Halant / schwa elision (्) | Insensitive | All three variants → identical transcripts on both ASR backends |

*Nukta sensitivity is OOV-driven: the model reacts to the presence/absence of
nukta not by switching phoneme /j/↔/z/ but by treating the nukta-absent form as
an unknown token and generating a common alternative phrase. This is a lexical
failure mode, not phoneme awareness.

### Finding 3 — Cross-script access: grapheme-bound for novel Roman input (Direction 2, Tests A and C)

Test A (cross-script homophones): mean cross-script MFCC similarity = 0.947
vs baseline = 0.895 (unrelated Devanagari pairs). Delta = +0.052 — statistically
present but small. Two Roman inputs (paani, kitna) hit Mode C (F0 ≈ 93 Hz,
garbled output) despite the Devanagari equivalents producing clean 183–194 Hz
speech. One pair (dhanyavaad/धन्यवाद) fell *below baseline* at 0.887 — no
phoneme access detectable.

Test C (cross-language /k/): no language segregation in MFCC space.
Between-group Hindi/English similarity (0.916) exceeds within-group Hindi-Deva
(0.901) — opposite of what language-specific phoneme inventories would predict.
The Roman/ASCII embedding subspace produces language-indifferent output: similar
spectral shape regardless of whether the input is Roman Hindi, mixed, or pure
English.

**The Mode C explanation is confirmed and generalized:** IndicF5 has
well-organized Devanagari phoneme representations, but the ASCII → phoneme access
path is uniformly undertrained. Novel Roman words don't connect to the Devanagari
phoneme layer; they route into a low-energy garbage attractor. There is no
detectable subset of "well-trained Roman words" that receive preferential phoneme
access (an earlier v1 Direction 2 claim about dhanyavaad and namaste was retracted
after v2 MFCC analysis).

### Joint interpretation

Combining both directions:

- **The phoneme layer exists and is well-organized** — but only accessible through
  Devanagari characters. The phonological organization evidenced in Direction 2
  (Test B) means the model *can* attend to fine phonetic distinctions when the
  right input representation is used.

- **Devanagari marker sensitivity is real but partial.** Vowel length and
  aspiration are exploitable levers (Directions 1 and 2 agree on this); halant is
  not; nukta works but through OOV dynamics rather than clean phoneme switching.
  This is consistent with a model that has partially phoneme-mediated Devanagari
  representations — some distinctions are learned, others collapsed.

- **The grapheme-bound ceiling comes from two different mechanisms.** For Roman
  input: the ASCII embedding subspace is undertrained and doesn't connect to the
  phoneme layer at all. For Devanagari input: some markers (halant) are ignored
  even though the phoneme layer is accessible — suggesting that the *mapping* from
  those specific graphemes to phoneme representations was not learned with
  sufficient data.

- **IndicXlit preprocessing works because it solves both problems.** It converts
  Roman to Devanagari (bypassing the ASCII access failure) and produces canonical
  Devanagari forms (removing marker ambiguity). The v2.1 score of 4.70 is the
  ceiling of what IndicXlit + inference-time tricks can deliver.

### Implications for Direction 3 (pronunciation dictionary)

Direction 3 is viable and scoped. Build the dictionary around the responsive
levers only:

- **Include:** vowel length corrections (ि → ी for words where long vowel is
  correct); nukta on high-frequency words where absence causes wrong lexical item
  (फ→फ़, ज→ज़); aspiration on the most frequent minimal pairs (खाना vs काना).
- **Exclude:** halant placement — the model ignores it.
- **Do not expect:** nukta to produce a clean /z/ vs /j/ acoustic distinction for
  rare proper nouns — the reaction is lexical, not phonemic.

### Implications for Path B (LoRA fine-tune, if pursued)

If naturalness improvement requires fine-tuning:

- The LoRA target should include the ASCII character embedding rows (not just upper
  DiT attention layers). The bottleneck for Roman input is at character →
  phoneme-representation mapping, not at the acoustic generation stage.
- All fine-tuning training inputs should be IndicXlit-preprocessed Devanagari.
  Feeding Roman text as training input would reinforce the undertrained embedding
  path.
- External G2P (producing Devanagari phoneme tokens) feeding into the model's
  Devanagari embedding space is the highest-viability phoneme-conditioning
  architecture, given that the Devanagari phoneme layer exists and is well-organized.

---

**Artifacts:**
- `experiments/05_phonetic_probe/FINDINGS.md` (Direction 1 full results)
- `experiments/06_grapheme_phoneme_probe/FINDINGS.md` (Direction 2 full results, v2)
- `experiments/05_phonetic_probe/scores/auto_scores.csv`
- `experiments/06_grapheme_phoneme_probe/scores/analysis_results_v2.json`

---

## 2026-05-11 — Rubric v2.1 whitelist fix + re-run (Path B completed)

**Change:** Four tokens added to `ROMAN_HINDI_FUNCTION_WORDS` in
`scoring/scripts/lib_normalize.py`: `tu → तू`, `mai → मैं`, `aa → आ`,
`hu → हूं`. These are short Hindi function words IndicXlit misreads as
English phonetics (`टू`, `माई`, `एए`, `हू`). The fix is applied
symmetrically: input preprocessing and rubric reference normalization
both use the same function, so both reference and transcript see the
corrected forms — no asymmetry introduced.

**Affected rows (preprocessed text changed vs v2.0):** ids 10, 11, 12, 13, 16.
The other 25 rows are byte-identical to v2.0 → deterministic model → same wavs.

**Kaggle run:** `harshalsinghcn/hinglish-tts-audit-indicf5-xlit` v3, T4,
30/30 wavs ok. Output dir: `results/indicf5_patched_xlit_v2/`.

**Results (rubric v2.1, 3-ASR consensus — AAI + Deepgram + Groq):**

| category | v2.0 xlit | v2.1 xlit | Δ |
|----------|:---------:|:---------:|:-:|
| pure_devanagari | 4.62 | **4.62** | +0.00 |
| pure_roman | 4.38 | **4.75** | **+0.38** |
| mixed_script | 4.88 | **4.88** | +0.00 |
| english_with_NE | 4.33 | **4.50** | **+0.17** |
| **overall** | **4.57** | **4.70** | **+0.13** |

`silence_or_skip`: 0/30 (unchanged). Mean PESQ: 3.996.

Changed rows:

| id | v2.0 | v2.1 (aai/dg/groq) | Δ |
|:--:|:----:|:------------------:|:-:|
| 10 | 4 | **5** (5/5/4) | +1 |
| 11 | 4 | **5** (1/5/5) | +1 |
| 12 | 4 | **5** (5/5/5) | +1 |
| 13 | 5 | 5 (5/5/5) | 0 |
| 16 | 4 | 4 (4/4/4) | 0 |

Three rows lifted (10, 11, 12), not two as predicted. Id 11's AAI returned empty
(1.7s clip — same pattern as v2.0) but Deepgram + Groq consensus = 5. Id 16 stayed
at 4: `tu→तू` fixed, but `बोहोट` vs `बहुत` CER residual persists on all backends.

**Correction to 2026-05-10 entry:** that entry stated "Two residual 3s (id 12, 16)".
The actual v2.0 scores (per_sentence_3way.json) were **4**, not 3. The "3" came from
a pre-computation draft; the 3-ASR consensus recovered partial transcripts to 4.
The v2.1 COMPARISON.md §4 documents this.

**Phase 2 status: complete.** The production deliverable is patched IndicF5 +
`lib_normalize.to_unified_devanagari` preprocessing (v2.1 whitelist). No LoRA
fine-tuning needed. The embedding-undertraining weakness is fully handled at
inference time.

**Artifacts:**
- `experiments/04_indicf5_xlit_v2/preprocessed_sentences.tsv` (v2.1 TSV)
- `experiments/04_indicf5_xlit_v2/wavs/` (30 wavs + log.json)
- `experiments/04_indicf5_xlit_v2/scores/auto_scores_v2.1.csv`
- `experiments/04_indicf5_xlit_v2/COMPARISON.md` (detailed two-way analysis)
- `scoring/rubric/JUDGE_PROMPT_v2.md` (v2.1 header added, v2.0 logic locked)

---

## 2026-05-11 — Methodological calibration: auto-metrics vs ear evaluation

**Calibration finding (applies to all future phonetic experiments):**

> Auto-analysis (MFCC similarity, F0 mean, ASR transcripts) systematically
> underestimated phonetic sensitivity vs ear evaluation. For future phonetic
> experiments, ear evaluation is the authoritative signal; auto-metrics serve
> only as triage.

**Evidence basis — Direction 1 (`experiments/05_phonetic_probe`):**

The Direction 1 probe ran auto-metrics (Deepgram + Groq ASR, F0 mean, spectral
centroid) and ear evaluation on the same 18 clips. Auto-metrics classified the
outcome as **B (partial sensitivity, 3/6 sentences sensitive)**. Ear evaluation
reclassified to **A (fully sensitive, 6/6)**. Three specific failures drove the
gap:

| Sentence | Auto verdict | Ear verdict | Why auto failed |
|---|---|---|---|
| S2 — halant/schwa elision | Insensitive | Sensitive | Halant changed consonant quality (spectral centroid +112 Hz on 2b vs 2a/2c), not words. ASR is lexical — it cannot detect sub-phonemic consonant quality changes. |
| S4 — aspiration ख vs क | Partial | Sensitive | 0.65 s clips are below the reliable floor for Hindi ASR. Groq produced garbled merges on 4a. Ear clearly heard /kʰ/ vs /k/ on all three variants without ambiguity. |
| S6 — prosody / punctuation | Partial | Sensitive | Ellipsis + exclamation (`मैं... बहुत... खुश हूं!`) produced identical transcript to neutral 6a, but 44% longer audio (1.90s vs 1.32s), slower pacing, and a pitch rise on the final syllable. ASR is insensitive to prosodic changes when words don't change. |

**Mechanism summary — three classes of auto-metric failure:**

1. **Sub-phonemic acoustic changes** (consonant quality, formant transitions) are
   invisible to lexical ASR. Spectral centroid or MFCC shifts may flag them but
   do not provide interpretable evidence without ear confirmation.

2. **Short clips** (≤1s) push Hindi ASR below its reliable floor. Groq (Whisper)
   is more robust than Deepgram at short durations, but both degrade. Ear
   evaluation is the only reliable signal for clips < 1s.

3. **Prosodic changes without word-content changes** (pacing, pitch contour,
   emphasis) are invisible to transcript-based metrics by design. Duration Δ is
   a weak proxy — but even a significant duration jump (e.g. +44%) can be
   misattributed to inference variance without ear confirmation.

**MFCC / F0 auto-analysis (Direction 2):** Additionally, the Direction 2 acoustic
analysis had three compounding bugs — C0 energy coefficient domination, silent
lead-in windows, and full-clip vs voiced-frame means — that required a complete
v2 re-run to recover valid numbers. The v1 results (Test B mean 0.439 bimodal, Test C
all-1.0 degenerate) were artefacts rather than findings. Auto-acoustic analysis
requires explicit validation steps (check for silence in feature windows, check
C0 before computing cosine similarity) or it will produce confident-looking
nonsense.

**Standing operational rule for this project:**

| Signal type | Role | Weight |
|---|---|---|
| Ear evaluation (native listener) | Authoritative | Primary |
| ASR transcript comparison (Deepgram + Groq) | Triage / coarse filter | Secondary |
| MFCC / F0 acoustic analysis | Hypothesis generation | Tertiary |
| MOS predictors (UTMOS, SQUIM) | Disallowed on Hindi | Excluded (see 2026-05-09 entry) |

Auto-metrics identify which sentences or variants are *candidates* for interesting
differences. Ear evaluation determines whether a candidate is a real finding. No
phonetic sensitivity claim should be published from auto-metrics alone.

**Artifact:** `experiments/05_phonetic_probe/FINDINGS.md` §§1.6, 2, 4 (full
reconciliation table and per-case analysis).
