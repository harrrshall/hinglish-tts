# Research Log

> Append-only. If any other doc disagrees with this file, **this file wins**
> (per `AGENT.md` §6).

Each entry: date, decision/observation, why, and a pointer to artifacts.

---

## 2026-05-07 — Project scaffolding & audit pipeline (Phase 1)

- **Project state:** Phase 1 (baseline audit). No training. No fine-tune yet.
  Goal of this session: produce everything an executing agent needs to run
  the audit on Colab T4 and hand back 150 .wav files + a scoring template.

- **Pre-existing files honored, not modified:** `AGENT.md`, `RESOURCE.md`.
  `AGENT.md` §6 lists `RESEARCH_LOG.md` and `AUDIT_PLAN.md` as files the repo
  should have — both created this session.

- **First-pass mistake (logged for posterity):** I initially built a much
  larger 6-phase eval pipeline (112 prompts, 5 runners, Streamlit dashboard,
  metric framework with WER/CER/UTMOS/PESQ/STOI/spectral). That work was
  superseded when the user shared the actual Phase-1 runbook
  (now `AUDIT_PLAN.md`). It briefly lived in `legacy/` but was deleted on
  the user's request later the same day. The lesson: confirm the spec
  before building.

  If the contents ever need to be reconstructed, the shape was:
  `prompts/{schema,categories,templates,generator}.py`,
  `evaluation/metrics/{wer_cer,speaker_similarity,utmos,pesq_stoi,spectral,perf,stability,aggregate,registry}.py`,
  `runners/{base_runner,kokoro_runner,indicf5_runner,indic_parler_runner,
  springlab_f5_runner,orpheus_runner,registry,run_model}.py`,
  `pipeline/{orchestrator,result_schema}.py`,
  `review/{app,storage,data}.py` (Streamlit), and `scripts/01..06_*.py`
  driver scripts. The per-model research at `research/<model>/` survived
  because the audit notebooks still reference it.

- **Per-model research (still useful):** `research/<model>/README.md` has
  install steps, sampling-knob defaults, hardware needs, known failure
  modes, and minimal inference snippets for Kokoro v1.0, IndicF5, Indic
  Parler-TTS, SPRINGLab F5-Hindi-24KHz, and Orpheus. The audit notebooks
  reference these.

- **Eval-set decision (will repeat in `audit/RUN_NOTES.md`):** Runbook §1.1
  mandates 8/8/8/6 totals (= 30) but §1.3 lists 27–30 as the english_with_NE
  generated range, which would yield 8/8/7/7. We honored §1.1: ID 27 is
  **mixed_script** (5 generated for that category) and english_with_NE has
  3 anchors + 3 generated (28/29/30). All 18 phenomenon tags from §1.4 are
  still covered ≥1×. Verified by `audit/scripts/build_eval_set.py` self-check.

- **Orpheus variant chosen:** `SachinTelecmi/Orpheus-tts-hi` (per runbook),
  4-bit nf4 quantization for T4. The earlier-research-pass agent had
  surfaced both this variant and `canopylabs/3b-hi-ft-research_release` —
  the runbook explicitly picks SachinTelecmi because it claims code-mixed
  support, which is what we care about.

- **What ships in this checkpoint** (paths relative to repo root):
  - `AUDIT_PLAN.md` — runbook, sacred
  - `audit/eval_sentences.tsv` — 30 sentences (12 anchors + 18 generated)
  - `audit/notebooks/{01..05}_*.ipynb` — 5 Colab notebooks, each restartable
  - `audit/scripts/{build_eval_set,build_notebooks,build_scoring_template,
    prep_reference_audio,verify,build_handoff}.py`
  - `audit/scoring_template.csv` — 150 rows pre-filled
  - `audit/METADATA.json`, `audit/RUN_NOTES.md` — templates
  - `progress.md` — phase tracker (rewritten)
  - `research/<model>/README.md` — reference material the notebooks rely on

- **What does NOT ship:** the audio. That's produced when the human (or a
  GPU-backed agent) runs the 5 notebooks on Colab. The local machine has no
  CUDA and ~15 GB RAM; running these models locally would swap or OOM.

- **Open questions (carried into audit execution):**
  1. The IndicF5 reference clip currently has a **placeholder** transcript
     in the prep fallback path. The transcript MUST be replaced with the
     true transcript of the chosen clip before §3.2 is run, otherwise
     IndicF5 prosody will drift and skew the comparison. Best plan: use
     Rasa's bundled `text` field; if Rasa fails, transcribe the IndicF5
     bundled clip with an Indic ASR model once and cache it.
  2. The SPRINGLab F5-Hindi notebook uses a CLI call. The Python API
     fallback (`f5_tts.api.F5TTS`) is documented in the cell but commented
     out. If the SPRINGLab fork's CLI flags drift again, swap to the API.
  3. Orpheus's `generate_speech` function is intentionally a stub. The
     executing agent must paste the verbatim version from the HF model card
     into `audit/notebooks/05_orpheus_hi.ipynb` Cell 5 before running.
