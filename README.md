# Hinglish TTS Research

Evaluating open-source TTS models on Hindi-English code-mixed (Hinglish) speech.
Goal: identify the best model for Phase 2 fine-tuning.

## Project Structure

```
hienglish/
│
├── data/                        # Shared, immutable eval data
│   ├── eval_sentences.tsv       # 30 Hinglish sentences (4 categories)
│   ├── reference_audio/         # Hindi reference wav + transcript
│   └── human_recordings/        # 8 human Hinglish recordings (ground-truth ceiling)
│
├── scoring/                     # Scoring infrastructure (shared across experiments)
│   ├── rubric/
│   │   ├── JUDGE_PROMPT_v2.md   # Locked rubric (v2.0) — do not edit
│   │   ├── JUDGE_PROMPT_v1_archive.md
│   │   ├── CEILING_REPORT.md    # Human ground-truth ceiling study
│   │   ├── V2_VALIDATION.md
│   │   └── RUBRIC_V2_BUILD_PROMPT.md
│   └── scripts/
│       ├── lib_normalize.py     # IndicXlit normalization (used by rubric + preprocessing)
│       ├── lib_audio.py / lib_asr*.py / lib_mos.py
│       ├── extract_signals_v2.py  # Stage-1: 3-backend ASR + signal extraction
│       ├── judge_v2.py            # Stage-2: Claude-as-judge (rubric v2.0)
│       ├── preprocess_input.py    # IndicXlit input preprocessor
│       └── v1_archive/            # Old v1 scripts (reference only)
│
├── experiments/                 # One folder per research experiment
│   ├── 01_baseline/             # Phase 1: 5-model baseline
│   │   ├── notebooks/           # 01_kokoro.ipynb … 05_orpheus_hi.ipynb
│   │   ├── wavs/<model>/        # 30 wavs per model
│   │   ├── scores/              # auto_scores_v1/v2.csv, signal_vectors_*, judge_cache_*
│   │   └── scripts/             # Build/verify/handoff helpers
│   │
│   ├── 02_indicf5_patch/        # Phase 2a: IndicF5 duration patch (Mode A fix)
│   │   ├── patch.diff
│   │   ├── KAGGLE_CELLS.md      # Kaggle kernel cells (T4 GPU required)
│   │   ├── wavs/                # 30 patched outputs
│   │   ├── scores/
│   │   ├── scoring_scripts/
│   │   └── COMPARISON.md        # Patched vs original per category
│   │
│   └── 03_indicf5_xlit/         # Phase 2b: IndicXlit input preprocessing (Mode C)
│       ├── KAGGLE_CELLS.md
│       ├── preprocessed_sentences.tsv   # original + Devanagari side-by-side
│       ├── wavs/
│       ├── scores/
│       ├── scoring_scripts/
│       └── COMPARISON.md        # 3-way: original vs patched vs patched+xlit
│
├── diagnostics/
│   └── duration_diagnostic/     # Mode A root-cause analysis (REPORT.md)
│
├── models/                      # Per-model research: install steps + minimal inference
│   ├── kokoro/ indicf5/ indic_parler/ springlab_f5/ orpheus/
│
├── landscape/                   # Competitor / market analysis
│
├── papers/                      # Reference papers
│
├── docs/                        # Project planning docs
│
├── RESEARCH_LOG.md              # Append-only decision log — source of truth
├── AGENT.md                     # Agent instructions for this codebase
└── RESOURCE.md                  # Resource inventory (APIs, compute, HF tokens)
```

## Models Under Evaluation

| # | Model | Params | Status |
|---|---|---|---|
| 1 | Kokoro v1.0 (Hindi) | 82M | Phase 1 done |
| 2 | IndicF5 | 330M | Phase 1 + patch + xlit experiments |
| 3 | Indic Parler-TTS | 880M | Phase 1 done |
| 4 | SPRINGLab F5-Hindi-24KHz | 151M | Phase 1 done |
| 5 | Orpheus-Hindi | 3B (4-bit) | Deferred |

## Scoring Pipeline (v2.0)

```
WAVs → scoring/scripts/extract_signals_v2.py   (AAI + Deepgram + Groq, 3-ASR consensus)
     → scoring/scripts/judge_v2.py             (Claude-as-judge)
     → experiments/<N>/scores/auto_scores_consensus.csv
```

Rubric dimensions: **intelligibility** (1–5), **naturalness** (ear-only), **code_switch**, **silence_or_skip**.

## Adding a New Experiment

1. Create `experiments/NN_<name>/` with `README.md`, `wavs/`, `scores/`
2. Run scoring against `data/eval_sentences.tsv` using scripts in `scoring/scripts/`
3. Write `COMPARISON.md` vs `experiments/01_baseline/scores/auto_scores_v2.csv`
4. Append findings to `RESEARCH_LOG.md`

## Key Files

| File | Purpose |
|---|---|
| `data/eval_sentences.tsv` | The 30-sentence eval set — never modify |
| `scoring/rubric/JUDGE_PROMPT_v2.md` | Locked rubric — changes require versioning |
| `RESEARCH_LOG.md` | Every decision with reasoning — append only |
