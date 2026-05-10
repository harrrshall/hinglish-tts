# Phase 1 Audit — Progress Tracker

> Single source of truth for the Hinglish-TTS Phase-1 baseline audit.
> Spec: [`AUDIT_PLAN.md`](./AUDIT_PLAN.md). Project context: [`AGENT.md`](./AGENT.md).
> Compute notes: [`RESOURCE.md`](./RESOURCE.md). Decisions log: [`RESEARCH_LOG.md`](./RESEARCH_LOG.md).

---

## Status snapshot

| Step | What | Where | Status |
|------|------|-------|:------:|
| 0    | Read `AGENT.md` + `AUDIT_PLAN.md` end-to-end | — | ☑ |
| 1    | Generate `audit/eval_sentences.tsv` (12 anchors + 18 generated) | `audit/scripts/build_eval_set.py` | ☑ |
| 1.5  | Self-check: 31 lines, IDs 01–30, 8/8/8/6, all 18 phenomena covered | inline in §1 script | ☑ |
| 1.7  | Manual native-speaker spot-check of generated Hindi/Hinglish lines | you | ☐ |
| 2.1  | Download Hindi reference clip + transcript | `audit/scripts/prep_reference_audio.py` | ☐ |
| 2.2  | Verify reference is 24 kHz mono, 3–8 s, transcript non-empty | same script (verifies before exit) | ☐ |
| 3.1  | Run notebook 1 — Kokoro v1.0 | `audit/notebooks/01_kokoro.ipynb` | ☐ |
| 3.2  | Run notebook 2 — IndicF5 | `audit/notebooks/02_indicf5.ipynb` | ☐ |
| 3.3  | Run notebook 3 — Indic Parler-TTS | `audit/notebooks/03_indic_parler.ipynb` | ☐ |
| 3.4  | Run notebook 4 — SPRINGLab F5-Hindi | `audit/notebooks/04_springlab_f5.ipynb` | ☐ |
| 3.5  | Run notebook 5 — Orpheus-Hindi (`SachinTelecmi`) | `audit/notebooks/05_orpheus_hi.ipynb` | ☐ |
| 4    | Final folder structure matches §4 (5 model dirs × 30 wavs + log.json) | `audit/results/<model>/` | ☐ |
| 5.1  | Build `audit/scoring_template.csv` (150 rows pre-filled) | `audit/scripts/build_scoring_template.py` | ☑ |
| 5.2  | Fill `audit/METADATA.json` (success_counts, ref-clip source, description prompt) | template ready | ☐ |
| 5.3  | Append observations to `audit/RUN_NOTES.md` as you go | template ready | ◐ |
| 6    | Run `audit/scripts/verify.py` (must exit 0) | — | ☐ |
| 7    | Build `audit/HANDOFF.md` + zip `audit_phase1_YYYYMMDD.zip` | `audit/scripts/build_handoff.py` | ☐ |

Legend: ☐ todo • ◐ partial (template/skeleton in place, waiting for data) • ☑ done

---

## Files in the repo right now

```
/AGENT.md                  ← project direction (locked, May 2026)
/AUDIT_PLAN.md             ← Phase 1 runbook — sacred
/RESEARCH_LOG.md           ← append-only decisions log (new)
/RESOURCE.md               ← compute resources (pre-existing, untouched)
/README.md                 ← repo entry-point
/progress.md               ← this file
/research/<5 models>/      ← per-model README, install.sh, inference_minimal.py (background reading)
/audit/
  eval_sentences.tsv       ← 30 lines, validated
  scoring_template.csv     ← 150 rows, pre-filled
  METADATA.json            ← template, fill at run time
  RUN_NOTES.md             ← template, append as you go
  reference_audio/         ← empty; populate via prep_reference_audio.py
  notebooks/01..05_*.ipynb ← 5 Colab notebooks, independently restartable
  results/{kokoro,indicf5,indic_parler,springlab_f5,orpheus_hi}/
                           ← empty dirs; notebooks fill these
  scripts/                 ← build_eval_set.py, build_notebooks.py,
                             build_scoring_template.py, prep_reference_audio.py,
                             verify.py, build_handoff.py
```

---

## Quick-start for the executing agent

```bash
# (one-time) verify the eval set is intact
python audit/scripts/build_eval_set.py

# (one-time, on a machine with HF / network access)
python audit/scripts/prep_reference_audio.py        # writes hindi_ref.{wav,txt}

# Then on Colab T4 (one notebook at a time, fresh runtime each):
#   audit/notebooks/01_kokoro.ipynb
#   audit/notebooks/02_indicf5.ipynb
#   audit/notebooks/03_indic_parler.ipynb
#   audit/notebooks/04_springlab_f5.ipynb
#   audit/notebooks/05_orpheus_hi.ipynb
# Each writes audit/results/<model>/01.wav … 30.wav + log.json

# Final verification + handoff (locally, no GPU needed):
python audit/scripts/verify.py                      # must exit 0
python audit/scripts/build_handoff.py               # writes audit/HANDOFF.md
( cd .. && zip -r "audit_phase1_$(date -u +%Y%m%d).zip" hienglish/audit )
```

---

## What the agent must NOT do (negative scope, lifted from `AGENT.md` §5)

- Do not start training. This is inference-only.
- Do not modify the eval set retroactively after any audio is generated.
  Adding sentences = re-scoring all prior models. The 30-sentence set is sacred.
- Do not silently fall back across models. If `lang_code='h'` rejects Roman
  input on Kokoro, log the error — that's the data point.
- Do not invent the Orpheus `generate_speech` function from memory; copy it
  verbatim from the model card. The SNAC token unpacking is fiddly.
- Do not vary Indic Parler's DESCRIPTION prompt across sentences; that
  confounds the comparison.

---

## Decisions made this build (also in `RESEARCH_LOG.md`)

- **Anchor IDs from runbook §1.2 are verbatim.** None edited.
- **Runbook §1.1 vs §1.3 inconsistency:** §1.1 mandates 6 english_with_NE,
  §1.3 lists 4 (27–30). Honored §1.1 → ID 27 is mixed_script, english_with_NE
  generated IDs are 28/29/30. Logged in `audit/RUN_NOTES.md`.
- **Notebooks are generated from a single Python source-of-truth**
  (`audit/scripts/build_notebooks.py`) so re-running rebuilds all 5 .ipynb.
- **First-pass 6-phase pipeline removed (2026-05-07).** I had built a larger
  eval harness before seeing the runbook; it lived under `legacy/` for one
  build cycle and was deleted on user request. See `RESEARCH_LOG.md` for
  what it contained, in case any of it ever needs to be reconstructed.

---

## Open questions for the executing agent

1. **IndicF5 reference transcript.** The prep script's IndicF5 fallback uses
   a placeholder transcript. Replace it with the true transcript of the
   chosen clip before notebook 2 — otherwise IndicF5 prosody drifts.
2. **SPRINGLab F5 CLI vs API.** Notebook 4 uses the F5-TTS CLI. If the
   `rumourscape/F5-TTS` fork's flag names drift, swap to the Python
   `f5_tts.api.F5TTS` path (commented in-cell as the fallback).
3. **Orpheus `generate_speech`.** Stubbed; paste verbatim from the model
   card before running notebook 5.
