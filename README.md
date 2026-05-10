# Hinglish TTS — Phase 1 (Baseline Audit)

This repo holds the Phase-1 baseline audit for the Hinglish (Hindi-English
code-mixed) TTS project. We are testing **5 open-source TTS models** on the
**same 30 Hinglish sentences**, on Colab T4, to decide which model to fine-tune
in Phase 2. **Inference only — no training.**

For project context, direction, and watch-list, read [`AGENT.md`](./AGENT.md).
For the executable audit spec, read [`AUDIT_PLAN.md`](./AUDIT_PLAN.md). For
the live Phase-1 checklist, read [`progress.md`](./progress.md). Every
decision lives in [`RESEARCH_LOG.md`](./RESEARCH_LOG.md).

## Models under audit

| # | Model | HF repo | ~Params | Prompting |
|---|---|---|---|---|
| 1 | Kokoro v1.0 (Hindi) | `hexgrad/Kokoro-82M` | 82 M | voicepack |
| 2 | IndicF5 | `ai4bharat/IndicF5` | 330 M | reference-audio + transcript |
| 3 | Indic Parler-TTS | `ai4bharat/indic-parler-tts` | 880 M | text-description + prompt |
| 4 | SPRINGLab F5-Hindi-24KHz | `SPRINGLab/F5-Hindi-24KHz` | 151 M | reference-audio + transcript |
| 5 | Orpheus-Hindi | `SachinTelecmi/Orpheus-tts-hi` | 3 B (4-bit) | LLM-style prompt |

## Quick start

```bash
# 1. Eval set (already validated; rebuild only if you edit sentences)
python audit/scripts/build_eval_set.py

# 2. Reference audio (one-time, needs network)
python audit/scripts/prep_reference_audio.py

# 3. On Colab T4, one notebook per model, fresh runtime each time:
#    audit/notebooks/01_kokoro.ipynb
#    audit/notebooks/02_indicf5.ipynb
#    audit/notebooks/03_indic_parler.ipynb
#    audit/notebooks/04_springlab_f5.ipynb
#    audit/notebooks/05_orpheus_hi.ipynb

# 4. Verify
python audit/scripts/verify.py                      # must exit 0

# 5. Handoff
python audit/scripts/build_handoff.py
zip -r "audit_phase1_$(date -u +%Y%m%d).zip" audit
```

## Layout

```
audit/                Phase-1 active workspace
  eval_sentences.tsv     30 sentences (12 anchors + 18 generated)
  reference_audio/       hindi_ref.{wav,txt}    (populated by prep script)
  notebooks/             01..05 Colab notebooks
  results/<model>/       01.wav .. 30.wav + log.json   (filled by notebooks)
  scoring_template.csv   150 rows, pre-filled, blank score columns
  scripts/               build/verify/handoff helpers
  METADATA.json          run metadata
  RUN_NOTES.md           deviations & gotchas log

research/<model>/      Per-model research: README, install.sh, inference_minimal.py
                       (background reading; the notebooks reference this)

AGENT.md / AUDIT_PLAN.md / progress.md / RESEARCH_LOG.md / RESOURCE.md
```

## Why per-model Colab notebooks (not a single orchestrator)

Pin conflicts between F5-TTS / Parler / Orpheus / vLLM / older
`transformers` / `numpy<=1.26` make a single environment intractable. One
notebook per model = one fresh Colab kernel = no transitive headaches. Each
is independently restartable.

## What does NOT run on the local machine

Per `RESOURCE.md`: this laptop has no CUDA GPU and ~15 GB RAM. Even Kokoro
82M is borderline locally. The 5 audit notebooks **must** run on Colab T4
(or any 15+ GB CUDA GPU). Everything else (eval-set generation, scoring CSV,
verification, handoff packaging) runs locally.
