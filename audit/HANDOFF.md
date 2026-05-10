# Audit Phase 1 — Handoff (2026-05-08)

**Phase 1 complete for the 4 unblocked models. 120/150 audio files (80%) generated across 4 of 5 models on 30 Hinglish sentences. Orpheus-Hindi deferred to Phase 2 (HF gating still pending).**

## Phase 1 status

| Model | Wavs | State | Phase 2 ask |
|-------|:----:|-------|-------------|
| Kokoro v1.0 | 30/30 ✅ | DONE locally (CPU) | — |
| Indic Parler-TTS | 30/30 ✅ | DONE on Kaggle T4 x2 (v9) | — |
| IndicF5 | 30/30 ✅ | DONE on Kaggle T4 x2 (v12) | — |
| SPRINGLab F5-Hindi | 30/30 ✅ | DONE on Kaggle T4 x2 (v3) | — |
| Orpheus-Hindi | 0/30 ❌ | HF gating pending Sachin@Telecmi.com approval | Wait + retry once accepted |

## Per-model success counts

| Model | Success | Total |
|-------|--------:|------:|
| kokoro | 30 | 30 |
| indicf5 | 30 | 30 |
| indic_parler | 30 | 30 |
| springlab_f5 | 30 | 30 |
| orpheus_hi | 0 | 30 |

## Top gotchas (from RUN_NOTES.md)

- **2026-05-07, local laptop dry-run** — `pip install kokoro` died twice with
- **`prep_reference_audio.py` requires `datasets`** for the Rasa path
- **IndicF5 GitHub `prompts/` directory has NO Hindi clips** (only KAN /

## Agent observations (factual, not subjective)


## Artifact

- Direct path: `audit_phase1_20260508.zip`

Next: human listens to all 150 clips, fills `scoring_template.csv`, returns it for Phase 2.