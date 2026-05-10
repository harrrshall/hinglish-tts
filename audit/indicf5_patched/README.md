# IndicF5 patched re-run — work in progress

**Goal:** validate the Mode A diagnosis from `audit/duration_diagnostic/REPORT.md` by patching the byte-proportional duration formula to character-proportional and re-running the 30-sentence audit.

## Status (2026-05-09)

- ✅ Patch designed and verified locally against the F5-TTS source (`/tmp/indicf5_src/IndicF5/f5_tts/infer/utils_infer.py:449-452`).
- ✅ Kaggle deliverable prepared (`KAGGLE_CELLS.md`).
- ⏳ **Waiting on user** to run the patched cells on Kaggle T4 and return wavs.
- ⏳ Three-ASR scoring pipeline + comparison report will run locally once wavs arrive.

## What's here

- `KAGGLE_CELLS.md` — three cells to drop into the existing IndicF5 Kaggle kernel (PATCH + SANITY + INFERENCE), with insertion order, expected outputs, and failure-mode debugging.
- `patch.diff` — unified diff of the 4-line block change for reference / code review.
- `README.md` — this file.

## What's coming (to this directory) once wavs return

```
results/indicf5_patched/01.wav … 30.wav      (placed under audit/results/, not here)
signal_vectors_aai.json                       (Stage-1, AssemblyAI)
signal_vectors_deepgram.json                  (Stage-1, Deepgram)
signal_vectors_groq.json                      (Stage-1, Groq Whisper)
auto_scores_aai.csv
auto_scores_deepgram.csv
auto_scores_groq.csv
auto_scores_consensus.csv                     (3-ASR majority vote)
COMPARISON.md                                 (the headline deliverable)
```

## When user returns with the Kaggle output bundle

User extracts `indicf5_patched.tgz` to `audit/results/indicf5_patched/` (mirroring the existing `audit/results/indicf5/` layout). Then:

1. Spot-check `_sanity_09.wav` and 2-3 others by ear.
2. Run scoring pipeline (a small wrapper has to be written because `extract_signals*.py` hardcodes `MODELS = ["kokoro", "indic_parler", "indicf5", "springlab_f5"]`; the wrapper will live in `audit/scripts/patched/` per the agent prompt's "don't edit originals" rule).
3. Run judge.py per ASR.
4. Compute consensus (intelligibility, code_switch, silence_or_skip via majority; naturalness/speaker per-ASR but flagged unreliable per ground-truth ceiling caveat).
5. Write `COMPARISON.md` with sections 1-6 from the agent prompt: per-sentence durations, per-category intelligibility delta, vs four-model field, residual failure modes, Phase 2 recommendation, caveats.

Cost when scoring runs: ~$0.05 AssemblyAI + Deepgram free-tier + Groq free-tier (~22 min wall).

## Reference

- Diagnostic that justifies this work: `../duration_diagnostic/REPORT.md`
- Original IndicF5 baseline: `../auto_scores.md` (per-category intel: pure_dev 4.38, pure_roman 1.00, mixed_script 1.25, english_with_NE 1.00)
- The four-model comparison the patched run plugs into: same `auto_scores.md`
