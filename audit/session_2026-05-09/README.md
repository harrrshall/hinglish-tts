# Session bundle — 2026-05-09

Everything generated in the 2026-05-09 work session, copied (not moved) from in-place locations under `audit/`. The live pipeline still resolves at the original paths; this bundle is a frozen handoff snapshot.

## Layout

```
session_2026-05-09/
├── README.md                                       (this file)
├── task1_duration_diagnostic/                      Mode A diagnosis
│   ├── REPORT.md                                   6/6 sentences, byte-vs-char duration formula recovered
│   └── raw_measurements.json
│
├── task2_indicf5_patched/                          Duration patch + 30-sentence Kaggle re-run + scoring
│   ├── COMPARISON.md                               Headline 5-model comparison (under v1 rubric)
│   ├── README.md
│   ├── per_sentence_compare.json
│   ├── kaggle/
│   │   ├── KAGGLE_CELLS.md                         The 3 cells inserted into Kaggle kernel v13
│   │   └── patch.diff                              4-line utils_infer.py byte→char change
│   ├── wavs/                                       30 patched wavs from Kaggle T4 + sanity wav + logs
│   │   ├── 01.wav … 30.wav
│   │   ├── _sanity_09.wav
│   │   ├── duration_log.txt                        DEBUG-PATCH lines for all 30
│   │   └── log.json
│   ├── scores/                                     3-ASR Stage-1 + Stage-2 outputs (v1 rubric)
│   │   ├── signal_vectors_aai.json
│   │   ├── signal_vectors_deepgram.json
│   │   ├── signal_vectors_groq.json
│   │   ├── auto_scores_aai.csv
│   │   ├── auto_scores_deepgram.csv
│   │   ├── auto_scores_groq.csv
│   │   └── auto_scores_consensus.csv
│   └── scoring_wrappers/                           Tiny scripts to run extract_signals_*.py against indicf5_patched
│       ├── _common.py
│       ├── run_aai.py
│       ├── run_deepgram.py
│       ├── run_groq.py
│       └── auto_score.py                           Deterministic v1.0 rubric scorer
│
├── task3_v2_build_prompt/                          The agent prompt that drove task 4
│   └── RUBRIC_V2_BUILD_PROMPT.md
│
└── task4_rubric_v2/                                Rubric v2.0 build (4 baseline models, 3-ASR consensus)
    ├── V2_VALIDATION.md                            Validation report — sanity, headline, ASR disagreement
    ├── code/
    │   ├── lib_normalize.py                        to_unified_devanagari + 55-entry whitelist + compute_cer/wer
    │   ├── extract_signals_v2.py                   Augments 3 v1 signal_vectors files with unified-Devanagari fields
    │   ├── judge_v2.py                             3-ASR median consensus, ear-only naturalness
    │   └── JUDGE_PROMPT_v2.md                      Locked rubric (changelog from v1.0 + thresholds)
    └── outputs/
        ├── signal_vectors_v2_aai.json              120 entries each
        ├── signal_vectors_v2_deepgram.json
        ├── signal_vectors_v2_groq.json
        └── auto_scores_v2.csv                      120 rows, _v2 columns + auto_score_confidence_v2
```

## What still lives outside this bundle (unchanged in-place originals)

- All v1.0 baseline files (`audit/JUDGE_PROMPT.md`, `audit/auto_scores.csv`, `audit/auto_scores.md`, `audit/SCORING_NOTES.md`, etc.)
- `audit/eval_sentences.tsv` (the 30-sentence eval, untouched)
- `audit/scripts/{lib_audio.py, lib_asr*.py, lib_mos.py, extract_signals*.py, judge.py, ...}` (v1 pipeline, untouched)
- `audit/results/{kokoro,indic_parler,indicf5,springlab_f5}/` (4 baseline TTS wavs, untouched)
- `audit/signal_vectors{,_deepgram,_groq}.json` (v1 Stage-1 outputs for 4 baselines, used as input by extract_signals_v2.py)

## Key results

**Task 1:** Mode A canvas under-allocation confirmed on 6/6 diagnostic sentences. Formula recovered: `gen_frames = ref_frames × (gen_text_bytes / ref_text_bytes)` — byte-proportional, not char-proportional. Pure Roman: ratio 0.30–0.39× expected; pure Devanagari unchanged.

**Task 2:** Duration patch (4 lines, byte→char) eliminates Mode A. Patched IndicF5 wavs are full-length (silence_or_skip 21/30 → 0/30 under v1 rubric). But Mode C surfaced: model produces acoustically wrong content for non-Devanagari inputs (15/22 RIGHT_LEN_GARBLED). Patched intel under v1 rubric: 1.97 → 2.13 overall; pure_roman / english_NE pinned at 1.00.

**Task 4 — rubric v2.0 (4 baseline models, 3-ASR consensus):**

| model | pure_dev | pure_roman | mixed_script | english_NE | overall | v1→v2 Δ |
|-------|---------:|-----------:|-------------:|-----------:|--------:|--------:|
| **kokoro** | 4.62 | 2.50 | 3.88 | 4.83 | **3.90** | +0.87 |
| **indic_parler** | 4.50 | 1.75 | 3.00 | 4.67 | **3.40** | +0.67 |
| indicf5 | 4.62 | 1.00 | 1.62 | 1.00 | 2.13 | +0.16 |
| springlab_f5 | 4.62 | 1.00 | 1.38 | 1.00 | 2.07 | +0.14 |

Patched IndicF5 is **not yet in the v2 table** by design (separate downstream task); add it by pointing the v2 pipeline at `audit/indicf5_patched/signal_vectors_*.json`.

## Reproducibility

```bash
cd /home/cybernovas/Desktop/hienglish

# v1 baseline regen (already done, kept as inputs):
source venv-scoring/bin/activate
python audit/scripts/extract_signals.py
python audit/scripts/extract_signals_deepgram.py
python audit/scripts/extract_signals_groq.py

# v2 rubric:
source venv-scoring-py311/bin/activate
python audit/scripts/lib_normalize.py     # self-tests
python audit/scripts/extract_signals_v2.py
python audit/scripts/judge_v2.py
```

## Stale artifact (not in this bundle)

`audit/signal_vectors_v2.json` (300 KB) is left behind in the parent dir — output of the first `extract_signals_v2.py` design before the per-ASR rewrite. No longer consumed by anything; safe to delete.
