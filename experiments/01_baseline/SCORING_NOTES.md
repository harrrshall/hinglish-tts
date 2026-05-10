# Scoring Notes — Auto-Scoring Pipeline (2026-05-08)

## Output

`audit/auto_scores.csv` — 120 rows (4 models × 30 sentences). Same column schema as `scoring_template.csv`. Each row's `notes` field cites the raw signals Claude used to derive the scores.

## Pipeline

Two-stage. Stage 1 extracts signals locally; Stage 2 has Claude judge from those signals via Agent calls.

### Stage 1 — Signal extraction
- DSP: `audit/scripts/lib_audio.py` — silence detection, end-pop, terminal sample
- ASR: `audit/scripts/lib_asr.py` — AssemblyAI Universal-2 (Hindi, English, auto-detect)
- MOS: `audit/scripts/lib_mos.py` — UTMOS22 (tarepan/SpeechMOS) + Torchaudio SQUIM (subjective MOS, PESQ, STOI, SI-SDR)
- Driver: `audit/scripts/extract_signals.py` (parallel ASR with 5 workers; serialized MOS via lock)
- Output: `audit/signal_vectors.json` — 120 entries × 23 fields each

Wall time: 7.3 min for 120 clips with 5 parallel ASR workers (vs ~45 min sequential).

### Stage 2 — Claude as judge
- Rubric: `audit/JUDGE_PROMPT.md` v1.0 (locked)
- Driver: `audit/scripts/judge.py`
- Per-batch flow:
  ```
  judge.py --emit-batches  → audit/judge_batches/batch_NN.json (12 batches × 10 clips)
  <Claude judges each batch via Agent tool, reading JUDGE_PROMPT.md>
  judge.py --collect       → audit/auto_scores.csv
  ```
- 12 batches of 10 clips each; one Agent call per batch.

## Signal → score mapping (rubric v1.0)

See `audit/JUDGE_PROMPT.md` for the authoritative thresholds. Summary:

| Column | Primary signal | Anchor |
|---|---|---|
| `intelligibility_1to5` | CER (Devanagari rows) or WER (Roman rows) | 5: ≤0.05, 4: ≤0.15, 3: ≤0.30, 2: ≤0.50, 1: >0.50 |
| `naturalness_1to5` | mean(UTMOS, SQUIM_MOS) | bucket 1-5; -1 rank if predictors disagree >0.7 or silence_mid_clip_s>0.5 |
| `code_switch_handling_1to5` | gap on mixed_script/english_with_NE vs pure | 5: equal/better, 1: >0.5 worse |
| `speaker_quality_1to5` | SQUIM_PESQ | 5: ≥4.0, 4: ≥3.5, 3: ≥3.0, 2: ≥2.5, 1: <2.5; -1 rank if terminal>0.05 |
| `roman_treated_as_english` | wer_en_forced + 0.15 < wer_roman AND wer_en_forced < 0.30 | TRUE only when both met |
| `silence_or_skip` | silence_mid_clip_s > 0.5 OR ASR transcript missing >20% of words | TRUE if either |
| `end_of_clip_pop` | end_pop_db > 6 AND terminal_sample_abs > 0.005 | TRUE if both |

## Per-model summary (auto-scored)

| Model | mean intel | mean nat | silence | pop | anglic |
|---|:---:|:---:|:---:|:---:|:---:|
| **kokoro** | **3.03** | **3.97** ← best naturalness | 2/30 | 0/30 | 0/30 |
| indic_parler | 2.73 | 3.33 | 4/30 | 4/30 | 0/30 |
| indicf5 | 1.97 | 3.37 | 21/30 | 2/30 | 0/30 |
| springlab_f5 | 1.93 | 3.07 | 21/30 | 0/30 | 0/30 |

## Known caveats (read before trusting absolute numbers)

1. **`silence_or_skip` is over-firing for indicf5 and springlab_f5 (21/30 each).**
   AssemblyAI Universal-2 returned **empty transcripts** for short Hindi clips (~1.5–2s) on these two models — possibly under the API's confidence threshold for short audio. The rubric interprets "transcript missing >20% of words" as silence/skip, so empty transcripts auto-trigger TRUE. The clips themselves may be perfectly fine to listen to. Spot-check before trusting.

2. **UTMOS and SQUIM_MOS were trained on English speech.** Absolute MOS values drift on Hindi. Within-model rank ordering (which sentence sounds best for a given model) is reliable. Cross-model comparison on raw MOS should be treated with skepticism. Naturalness scoring is the highest-uncertainty column.

3. **`code_switch_handling_1to5` defaults to intelligibility for non-mixed rows.** For `pure_devanagari` and `pure_roman` rows, this column equals `intelligibility_1to5` per the rubric.

4. **`roman_treated_as_english` is conservative (0/30 across all models).**
   The threshold `wer_en_forced + 0.15 < wer_roman AND wer_en_forced < 0.30` is strict. Even when models clearly anglicize Roman text (e.g. Kokoro's pure_roman clips have WER_rom=1.0 / WER_en=0.6), the WER_en threshold (<0.30) prevents flagging — because AssemblyAI in English mode also struggles with TTS-anglicized Hindi. This column flags only obvious cases. Spot-check Roman/mixed_script rows manually.

5. **Indian proper nouns** ("Hyderabad", "Aishwarya", "Delhi") may inflate CER/WER artificially. The judge was instructed to discount this in `notes`, but absolute intelligibility on `english_with_NE` rows may be slightly underrated.

6. **Determinism**: AssemblyAI is sampling-based; re-running may produce slightly different transcripts → slightly different WER/CER. UTMOS/SQUIM are deterministic. Claude judge is sampling-based across Agent calls — re-running would re-prompt Claude and produce minor score variations (within ±1 on Likert scales).

## How to spot-check + override

**Recommended:** human listens to ~20 clips selected as follows:
- All clips with `intelligibility_1to5 ≤ 2` (typically failure cases)
- All clips with `silence_or_skip = TRUE` (the 48 flagged clips, but most are likely false positives — sample 10)
- Random 5% of the rest as calibration

**Override workflow:**
1. Create `audit/human_overrides.csv` with header: `model,id,column,value`
2. One row per (model, sentence, column) you want to override
3. Run: `python audit/scripts/judge.py --merge`
4. Output: `audit/scoring_template_filled.csv` with overrides applied; `notes` column gets `[human override <col>: was <auto>]` prepended.

Example `human_overrides.csv`:
```
model,id,column,value
indicf5,01,silence_or_skip,FALSE
indicf5,01,intelligibility_1to5,4
springlab_f5,03,intelligibility_1to5,3
```

## Reproducibility

Re-running the full pipeline:
```bash
cd ~/Desktop/hienglish
source venv-scoring/bin/activate
export ASSEMBLYAI_API_KEY="..."           # NEVER write to a file
python audit/scripts/extract_signals.py    # ~7 min
python audit/scripts/judge.py --emit-batches
# then have Claude Code judge each batch (12 Agent calls)
python audit/scripts/judge.py --collect    # writes auto_scores.csv
```

## File inventory

```
audit/
├── JUDGE_PROMPT.md                  # versioned scoring rubric (v1.0)
├── SCORING_NOTES.md                 # this file
├── signal_vectors.json              # Stage 1 output (120 entries)
├── auto_scores.csv                  # Stage 2 output (120 rows)
├── judge_batches/batch_*.json       # 12 batches, 10 clips each
├── judge_responses/batch_*.json     # 12 batches of judge output
└── scripts/
    ├── lib_audio.py                 # DSP helpers (silence, pop, terminal)
    ├── lib_asr.py                   # AssemblyAI wrapper + jiwer WER/CER
    ├── lib_mos.py                   # UTMOS + SQUIM
    ├── extract_signals.py           # Stage 1 driver (parallel)
    └── judge.py                     # Stage 2 orchestrator
```

## Total cost

- AssemblyAI: 120 clips × 3 transcribe calls × ~3 sec each ≈ 18 min audio = **~$0.05**
- UTMOS + SQUIM: free (one-time download ~400 MB)
- Claude as judge: ~12 batch calls × ~36K tokens each ≈ 430K tokens; covered by Claude Code session
