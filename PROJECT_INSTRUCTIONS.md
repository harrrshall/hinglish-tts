# Project Instructions — Hinglish TTS

> Forward-looking. Updated when a path is entered or completed. For the full
> decision history, see `RESEARCH_LOG.md`. For scored results, see
> `EVALUATION_REPORT.md`.

---

## Current state (2026-05-11)

Phase 2 is complete. The production inference stack is patched IndicF5 +
`lib_normalize.to_unified_devanagari` input preprocessing (rubric v2.1
whitelist). Overall intelligibility: **4.70 / 5** (3-ASR consensus, 30
Hinglish sentences). No LoRA fine-tuning was required.

---

## Path A: SHIPPED 2026-05-11

**What shipped:** Patched IndicF5 (duration patch: `experiments/02_indicf5_patch/patch.diff`)
plus IndicXlit input preprocessing (`scoring/scripts/preprocess_input.py`,
backed by `lib_normalize.to_unified_devanagari`) with the v2.1 function-word
whitelist (`tu/mai/aa/hu`). No new model weights. Inference-only.

**Close-out artifact:** `EVALUATION_REPORT.md` — full methodology, results,
and limitation accounting for an external reader.

**What Path A achieves:**

- `silence_or_skip`: 0/30 (was 21/30 on original IndicF5)
- `pure_roman` intelligibility: 4.75 (was 1.00)
- `mixed_script` intelligibility: 4.88 (was 1.62)
- `english_with_NE` intelligibility: 4.50 (was 1.00)
- Overall: 4.70 (was 2.13)

**What Path A does not achieve** (explicit, not implicit — these become
Path B requirements in the section below):

1. **Sound texture.** IndicF5 outputs are perceptually recognisable as
   synthesized speech. The DiT fills its canvas correctly and intelligibly,
   but lacks the micro-variation in pitch, timing, and breathiness that
   distinguish natural conversational Hindi from TTS. A native speaker can
   identify the output as synthetic on every clip, regardless of
   intelligibility score.

2. **Prosodic flatness.** Sentence-level prosody is monotone. The reference-
   audio conditioning contributes the speaker's voice identity but not the
   sentence's natural emphasis pattern. Questions, exclamations, and
   imperatives — all present in the eval set — receive the same flat
   delivery as declaratives. This is audible even on 5/5 intelligibility
   clips.

3. **Naturalness measurement.** No naturalness number was produced. The
   auto-scoring pipeline outputs `EAR_ONLY` for naturalness because
   available MOS predictors (UTMOS, SQUIM_MOS) are directionally inverted
   on Hindi by 1.7–2.4 ranks. A human listening session with native-speaker
   annotations is required before any naturalness claim can be made.

4. **Whitelist generalization.** The English-loan and Indian-NE whitelists
   in `lib_normalize.py` were hand-tuned to the 30-sentence eval set. Out-
   of-vocabulary tokens fall through to IndicXlit, which handles common cases
   well but degrades on ambiguous short tokens and uncommon proper nouns.

5. **Kokoro english_with_NE gap.** Kokoro scores 4.83 on english_with_NE
   vs the production stack's 4.50. The gap comes from IndicXlit's
   transliteration producing Hindi-accented phonetic English (e.g. "माय
   फ्रेंड ऐश्वर्या"), which ASR scores highly but a listener may not prefer
   over Kokoro's English-mode rendering of the same sentence.

---

## Path B: Qualitative improvement (not yet started)

Path B targets the limitations that Path A left explicit. It requires a
listening session before scope is confirmed — the five items below are
requirements, not a pre-committed plan.

**Entry criteria:** record a listening-test baseline. Score at least 20 Path
A clips from `experiments/04_indicf5_xlit_v2/wavs/` on naturalness and
prosody using a native Hindi speaker (or a calibrated Hindi-proficient rater).
This baseline is the benchmark Path B must beat.

### B.1 — Prosody conditioning (inference-time, no training)

**Requirement:** sentences with different illocutionary types (question,
imperative, exclamation) should sound perceptually distinct from declaratives.

**Candidate approach:** swap the single Devanagari reference clip for a small
bank of 3–5 reference clips covering different prosodic styles. At inference
time, select the closest-matching reference by sentence-type heuristic or
by a lightweight prosody classifier. No fine-tuning; only the reference-audio
conditioning changes.

**Cost estimate:** 1 Kaggle run + listening session. Implement only after the
baseline confirms prosodic flatness is a top-ranked listener complaint.

### B.2 — Naturalness fine-tune (LoRA, upper DiT layers)

**Requirement:** Path A output should not be immediately identifiable as
synthetic by a native Hindi speaker at a naturalness Likert score of
≥ 4/5 on a calibrated rubric.

**Candidate approach:** LoRA on IndicF5 DiT layers 6–12 (upper layers,
which shape voice texture more than canvas layout). Training data: 20–60 min
of a single Hindi speaker, clean room recording, paired with script. Expected
cost: 4–8 GPU-hours on Kaggle T4.

**Pre-condition:** naturalistic assessment of Path A output (B.1's listening
session), then a 10-step probe run to confirm VRAM + loss behaviour before
committing to a full run. Per `AGENT.md §3`, never start a training run
without a probe.

### B.3 — Whitelist expansion or learned classifier

**Requirement:** preprocessing should not degrade on Hinglish inputs whose
vocabulary is outside the 30-sentence eval set.

**Two options:**

- **(B.3a) Whitelist expansion:** extend `ENGLISH_LOAN_CANONICAL` and
  `INDIAN_NE_CANONICAL` from a representative Hinglish corpus (e.g. top-500
  tokens from a Twitter/WhatsApp Hinglish dataset). Low engineering cost;
  high curation cost.

- **(B.3b) Learned classifier:** fine-tune a token-level Hindi/English LID
  model (HingBERT-LID is the standard reference) to distinguish Roman-Hindi
  function words, English loans, Indian NEs, and non-Hindi English. Replace
  the whitelist dispatch in `_normalize_ascii_token()` with classifier
  output. Higher upfront cost; better generalization.

Implement after a production-input stress test surfaces at least 10 whitelist
misses on real Hinglish data.

### B.4 — English-with-NE phonetics decision

**Requirement:** define and measure an explicit acceptance criterion for
english_with_NE output style.

The current stack transliterates english_with_NE sentences to Devanagari,
producing Hindi-accented phonetic English. This scores 4.50 on intelligibility
but the perceptual quality is different from Kokoro's English-mode rendering
(4.83). Neither is wrong — they represent different stylistic choices:

- Patched+xlit: "माय फ्रेंड ऐश्वर्या फ्रॉम चेन्नई" — Indian-accented,
  consistent with Hindi speaker identity, intelligible.
- Kokoro: standard English pronunciation, Indian NEs rendered with mild
  accent.

A product decision is needed: which rendering is preferred for the target
use case (customer service, content, IVR)? Once decided, the scoring rubric's
english_with_NE column should be calibrated to that preference, and the
implementation adjusted accordingly.

---

## Path C: Phase 3 real fine-tune (not yet started)

Path C is the original Phase 3 from `AGENT.md §2`: curated Hinglish data +
the right text-normalization layer + LoRA or partial fine-tuning on the chosen
base. It remains the right path if Path B's naturalness fine-tune does not
close the sound-texture gap to an acceptable level.

**Entry criteria:** Path B's listening-session baseline + at least 30 minutes
of curated, labelled Hinglish speaker audio. Do not begin Path C without a
working `DATA_SOURCES.md` (all sources, licenses, sample rates) and a
successful 10-step probe run on the chosen fine-tune stack.

Path A's intelligibility gains are durable through fine-tuning — the
preprocessing wrapper and whitelist remain in effect regardless of what the
DiT weights do. Path C should target naturalness and voice texture, not
intelligibility.
