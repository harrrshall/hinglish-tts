# v2.0 Correlation Report

**Date:** 2026-05-09  
**Inputs:** `audit/human_scores.md` (manual ratings, n=86), `audit/auto_scores.csv` (v1.0), `audit/auto_scores_v2.csv` (v2.0).  
**Comparison axis:** intelligibility (the column with both manual and auto values).  
**n paired clips:** 85 after dropping rows with missing manual intel (1 skipped) or missing auto scores (0 skipped).

## Headline

| metric | v1.0 → human | v2.0 → human | Δ (v2 − v1) |
|---|:---:|:---:|:---:|
| **Pearson r** | 0.619 (p=0.0000) | **0.643** (p=0.0000) | **+0.024** |
| Spearman ρ | 0.625 (p=0.0000) | 0.693 (p=0.0000) | +0.068 |

**Decision:** **SHIP v2.0** — v2.0 correlation with user manual ratings is at least as high as v1.0.

## Per-model correlation (intel)

| model | n | v1 Pearson r | v2 Pearson r | Δ |
|---|---:|:---:|:---:|:---:|
| indic_parler | 28 | 0.316 (p=0.1016) | 0.339 (p=0.0775) | +0.023 |
| indicf5 | 27 | 0.957 (p=0.0000) | 0.931 (p=0.0000) | -0.026 |
| kokoro | 30 | 0.507 (p=0.0042) | 0.581 (p=0.0008) | +0.073 |

## Cases where v2 disagrees with v1 by ≥2 ranks

Sorted by gap size. `closer` shows whether v1 or v2 is closer to the human rating (distance |auto − human|; tie if equal).

| model | id | human | v1 | v2 | |v1−h| | |v2−h| | closer | confidence |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| kokoro | 18 | 2 | 1 | 5 | 1 | 3 | **v1** | MEDIUM |
| indic_parler | 02 | 3 | 1 | 5 | 2 | 2 | **tie** | LOW |
| kokoro | 09 | 2 | 1 | 4 | 1 | 2 | **v1** | MEDIUM |
| kokoro | 21 | 2 | 2 | 5 | 0 | 3 | **v1** | HIGH |
| kokoro | 23 | 4 | 1 | 4 | 3 | 0 | **v2** | HIGH |
| kokoro | 10 | 2 | 1 | 3 | 1 | 1 | **tie** | HIGH |
| kokoro | 17 | 1 | 1 | 3 | 0 | 2 | **v1** | HIGH |
| kokoro | 20 | 2 | 1 | 3 | 1 | 1 | **tie** | MEDIUM |
| kokoro | 22 | 4 | 2 | 4 | 2 | 0 | **v2** | HIGH |
| kokoro | 27 | 4 | 2 | 4 | 2 | 0 | **v2** | HIGH |
| indic_parler | 11 | 1 | 1 | 3 | 0 | 2 | **v1** | MEDIUM |
| indic_parler | 18 | 1 | 2 | 4 | 1 | 3 | **v1** | LOW |
| indic_parler | 21 | 1 | 2 | 4 | 1 | 3 | **v1** | HIGH |
| indic_parler | 22 | 1 | 2 | 4 | 1 | 3 | **v1** | HIGH |
| indic_parler | 23 | 1 | 1 | 3 | 0 | 2 | **v1** | MEDIUM |
| indic_parler | 27 | 2 | 1 | 3 | 1 | 1 | **tie** | MEDIUM |
| indicf5 | 22 | 2 | 1 | 3 | 1 | 1 | **tie** | HIGH |

**Disagreement totals:** v2 closer to human in **3** cases, v1 closer in **9**, tied in **5**. (17 total clips with ≥2-rank v1↔v2 disagreement.)

## What changed and why

v2.0 made four structural changes relative to v1.0 (full justifications in `JUDGE_PROMPT_v2.md` Changelog):

1. **3-ASR consensus** (median of AAI / Deepgram / Groq intel ranks) replaces the v1.0 single-ASR (AAI) score. Effect: more robust on threshold-boundary clips.
2. **IndicXlit script normalization** on both reference and ASR transcript before CER computation. Effect: `pure_roman` and `mixed_script` rows where the ASR returned Devanagari for Roman-spoken Hindi are no longer pegged at intel=1. On the 8 human ground-truth clips this dropped mean CER from 0.45 to 0.11.
3. **Naturalness column emits the literal string `"ear-only"`** (not numeric). Per the CEILING_REPORT, UTMOS / SQUIM_MOS / SQUIM_PESQ structurally invert direction on Hindi audio (rate human Hindi lower than synthetic Hindi). v2.0 refuses to emit a numeric naturalness score from those predictors.
4. **Speaker_quality stays auto-scored from PESQ** but is annotated synthetic-relative-only in `notes_v2`. Within-TTS rankings are still informative; absolute numbers are not.

## Caveats

- Manual ratings come from a handwritten notebook transcribed via OCR + visual review. 93 cells across all 7 columns are flagged `[?]` (low confidence). They're included in the correlation analysis above, but excluding them is a sensitivity check that hasn't been run here — flag this if the gate margin is small.
- SPRINGLab F5-Hindi was not manually rated, so v2's improvement on that model (if any) cannot be cross-checked against ear truth.
- Spearman ρ (rank correlation) and Pearson r usually move together; if they diverge substantially, the linear-fit assumption of Pearson is suspect. Cross-check both.
- The correlation gate measures intelligibility only because that's the column where v2.0's IndicXlit normalization most directly applies. Naturalness wasn't compared because v2.0 doesn't emit a numeric naturalness; speaker_quality wasn't compared because the human notebook conflates speaker_quality with intelligibility on many rows.
