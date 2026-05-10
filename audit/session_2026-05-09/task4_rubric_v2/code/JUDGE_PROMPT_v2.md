# Judge Prompt v2 — Hindi/Hinglish TTS Auto-Scoring (LOCKED)

> **Version:** 2.0 (LOCKED 2026-05-09 — passed Phase 6 correlation gate)
> **Supersedes:** `JUDGE_PROMPT.md` v1.0 — for all evaluation conducted on or after the lock date. v1.0 is archived as `JUDGE_PROMPT_v1_archive.md`.
> **Gate evidence:** `audit/v2_validation/CORRELATION_REPORT.md` — Pearson r 0.619→0.643, Spearman ρ 0.625→0.693, n=85 paired (model, sentence) rows against `audit/human_scores.md`.
> **Inputs format:** v1.0 signal vectors enriched with 4 new fields (`ref_unified`, `transcript_unified`, `cer_unified`, `wer_unified`) plus `asr_backend`. The judge driver consumes 3 such files (one per ASR) and joins by `(model, id)`.

You are scoring synthetic Hindi/Hinglish speech against ground truth. Inputs come from a deterministic local pipeline (DSP + 3-ASR + MOS predictors). The v2.0 driver (`audit/scripts/judge_v2.py`) implements every rule in this document mechanically — there is no LLM-as-judge step. The rubric is therefore reproducible across runs given fixed inputs.

---

## Changelog from v1.0

The four structural changes, each with a one-paragraph justification citing the source data.

### 1. Three-ASR majority vote on intelligibility, code_switch, and silence_or_skip

v1.0 ran a single ASR (AssemblyAI) and the rubric was a deterministic mapping from that single backend's CER/WER to a 1–5 rank. Subsequent runs were added with Deepgram and Groq Whisper. v2.0 takes the **median of the three per-backend intel ranks** (not the mean — median is more robust to a single backend mistranscribing). On the 30 baseline sentences × 4 models = 120 (model, sentence) pairs, the three backends agree on intel rank within 1 in 100/120 (HIGH confidence), within 2 in 15/120 (MEDIUM), and ≥3 apart in 5/120 (LOW). The median equals the mode in 115/120 cases; in the 5 LOW cases it sits in the middle, the right answer for ordinal data. `silence_or_skip` and `code_switch` are derived from the same 3-ASR view, with majority rule for the binary flag and a per-model pure-category mean for the gap-based code-switch score.

**Source:** `audit/auto_scores_v2.csv` (Phase 4 output); per-(model, ASR) v1→v2 CER deltas in the Phase 3 run log show the variance pattern.

### 2. IndicXlit script normalization on both reference and transcript before WER/CER

v1.0 scored `pure_roman` rows by computing WER between the Roman ground truth and `transcript_roman` (auto-detect ASR output). When the ASR detected the audio as Hindi (which is correct for native-pronounced Roman-Hindi) and returned a Devanagari transcript, WER was 1.0 — corrupting `intelligibility = 1` for every clip in that category, including human ground-truth recordings of perfectly-spoken Roman-Hindi. The CEILING_REPORT confirmed this is a rubric artifact, not a TTS issue: human_03 (`kal mujhe office jaana hai`) scored CER=0.85 in v1.0 despite being read correctly.

v2.0 transliterates **both** reference text and ASR transcript into a unified Devanagari pivot (AI4Bharat's IndicXlit, with a hand-curated canonical-dict for English loanwords and Indian NEs to bypass IndicXlit on the eval-set's known terms). Validated on the 8 human ground-truth clips (Phase 2): mean CER drops from 0.448 (v1.0) to 0.106 (v2.0), a 76% reduction — with dramatic fixes on `pure_roman` (e.g. human_03: 0.846→0.050, human_04: 0.821→0.083). On the 120-clip TTS baseline (Phase 3), Kokoro mean CER drops 0.394→0.135 and Parler 0.389→0.321; F5-family models barely move because their transcripts are genuinely garbled, not script-mismatched.

The normalization is **symmetric** — both ref and hyp pass through the same `to_unified_devanagari` function. Asymmetric normalization would invalidate the comparison.

**Source:** `audit/v2_validation/normalization_validation.json` (Phase 2 gate output); `audit/scripts/lib_normalize.py` (canonical-dict + IndicXlit fallback implementation).

### 3. Naturalness becomes ear-only (literal string in CSV, not numeric)

v1.0's `naturalness_1to5` was derived from `mean(UTMOS, SQUIM_MOS)`. The CEILING_REPORT showed both predictors structurally invert direction on Hindi: real human Hindi recordings get UTMOS=1.95 / SQUIM_MOS=2.70, while Kokoro Hindi TTS gets UTMOS=4.40 / SQUIM_MOS=4.45 — a 1.7–2.4 rank inversion that is impossible if the predictors were calibrated to perceived naturalness. After-rubric `naturalness_1to5` inverted by 2.22 ranks (human GT 1.75 vs Kokoro TTS 3.97).

v2.0 emits the literal string `"ear-only"` for `naturalness_v2`. There is no numeric value; the column exists to make the absence of a numeric score explicit. Naturalness comparisons require human listening and are tracked in `audit/human_scores.md` (manual ratings) until a Hindi-trained MOS predictor is available.

**Source:** `audit/human_groundtruth/CEILING_REPORT.md` §3 (predictor drift table) and §4 (Reweight option C, recommended path).

### 4. Speaker_quality kept but flagged synthetic-relative only

`speaker_quality_v2` retains v1.0's PESQ→1–5 thresholds and the −1 rank penalty for `terminal_sample_abs > 0.05`. The CEILING_REPORT showed the same predictor inversion on PESQ that hits UTMOS/SQUIM_MOS (human GT 1.62 vs TTS Kokoro 3.86) — making absolute speaker_quality numbers untrustworthy for cross-source comparison.

The compromise: keep the column for *within-TTS* relative ranking (the synthesis source is consistent across the 4 baseline models, so the predictor's bias is constant and cancels out when comparing models against each other). Mark every row's `notes_v2` field with `"PESQ=X.XX (synthetic-relative only)"` so the column cannot be cited as an absolute MOS-style score. Do not compare speaker_quality across runs that mix TTS and human audio.

**Source:** Same as #3 — CEILING_REPORT.md §3.

---

## The signal vector you receive (per clip, per backend)

```
{
  "model":           one of [kokoro, indic_parler, indicf5, springlab_f5]
  "id":              "01" .. "30"
  "category":        one of [pure_devanagari, pure_roman, mixed_script, english_with_NE]
  "text":            ground-truth sentence (Devanagari, Roman, or mixed)
  "tested_phenomenon": e.g. baseline_devanagari, mixed_script_hard
  "duration_s":      wav length in seconds
  "sample_rate_hz":  wav sample rate

  ── DSP signals (ASR-independent) ──
  "silence_mid_clip_s":   longest mid-clip silence in seconds  (>0.5 = SUSPECT)
  "end_pop_db":           last-200ms peak vs prior 200ms RMS, dB  (>6 = SUSPECT pop)
  "terminal_sample_abs":  |last sample|; >0.005 (with end_pop>6) = end-of-clip pop;
                          >0.05 = DC tail / hard cutoff penalty on speaker_quality

  ── ASR transcripts (per-backend) ──
  "transcript_hi", "transcript_en_forced", "transcript_roman", "detected_lang"

  ── ASR errors vs ground truth (per-backend, raw v1.0 fields, kept for compat) ──
  "cer_devanagari", "wer_roman", "wer_en_forced"

  ── v2.0 unified-Devanagari signals (NEW, computed by extract_signals_v2.py) ──
  "ref_unified":            reference text → Devanagari pivot
  "transcript_unified":     transcript_hi (or transcript_roman fallback) → Devanagari pivot
  "cer_unified":            CER between the two unified strings (after punctuation strip)
  "wer_unified":            WER between the two unified strings
  "asr_backend":            "aai" | "deepgram" | "groq"

  ── MOS predictors (English-trained; do NOT use for naturalness in v2) ──
  "utmos", "squim_mos", "squim_pesq", "squim_stoi", "squim_sisdr"
}
```

---

## What v2 outputs (per clip, into `auto_scores_v2.csv`)

```
{
  "model": "...",                          // copy
  "id": "...",                             // copy
  "category": "...",                       // copy
  "text": "...",                           // copy
  "intelligibility_v2":         <int 1–5>, // median of 3 backends
  "naturalness_v2":             "ear-only",  // literal string
  "code_switch_v2":             <int 1–5>, // intel for pure rows; gap-from-pure for mixed/NE
  "speaker_quality_v2":         <int 1–5>, // PESQ-based, synthetic-relative-only
  "roman_treated_as_english_v2": "TRUE" | "FALSE" | "",
  "silence_or_skip_v2":         "TRUE" | "FALSE",
  "end_of_clip_pop_v2":         "TRUE" | "FALSE",
  "auto_score_confidence_v2":   "HIGH" | "MEDIUM" | "LOW",
  "notes_v2":                   "<deterministic citation of per-backend signals>"
}
```

`notes_v2` is mechanically generated and includes per-backend `cer_unified`, per-backend intel rank, per-backend silence flag (0/1), the PESQ value with the `(synthetic-relative only)` annotation, the code_switch derivation if the row is mixed/NE, and the literal `naturalness=ear-only per CEILING_REPORT.md.` footer.

---

## Signal → score mapping

| Column | Primary signal | Anchor / Rule |
|---|---|---|
| `intelligibility_v2` | median across 3 backends of `cer_to_intel_rank(cer_unified)` | v1.0 CER anchors per-backend: 5: ≤0.05, 4: ≤0.15, 3: ≤0.30, 2: ≤0.50, 1: >0.50. The median (not mean) is taken to be robust against a single-backend outlier on hard clips. |
| `naturalness_v2` | none (deliberately) | Literal string `"ear-only"`. UTMOS / SQUIM_MOS / SQUIM_PESQ are not consulted for this column. |
| `code_switch_v2` | per-row intel + per-model pure-category mean intel | For `pure_devanagari` / `pure_roman`: equals `intelligibility_v2`. For `mixed_script` / `english_with_NE`: rank by gap = `model_pure_intel_mean − intel_v2`. 5: gap ≤0.05, 4: ≤0.15, 3: ≤0.30, 2: ≤0.50, 1: >0.50. Same anchors as v1.0. |
| `speaker_quality_v2` | SQUIM_PESQ + `terminal_sample_abs` | v1.0 PESQ anchors: 5: ≥4.0, 4: ≥3.5, 3: ≥3.0, 2: ≥2.5, 1: <2.5. **−1 rank penalty if `terminal_sample_abs > 0.05`** (DC tail). Floor at 1. Marked synthetic-relative only in `notes_v2`. |
| `roman_treated_as_english_v2` | `wer_en_forced` + `wer_roman` (per-AAI; ASR-independent ratio) | Unchanged from v1.0. TRUE iff `wer_en_forced + 0.15 < wer_roman` AND `wer_en_forced < 0.30`. Empty string `""` for `pure_devanagari` (not applicable). |
| `silence_or_skip_v2` | per-backend silence test (`silence_mid > 0.5` OR unified hyp covers <80% of unified ref length) | TRUE iff at least 2 of the 3 backends report silence. The 80% length-coverage rule replaces v1.0's "missing >20% of words" because computing it on the unified Devanagari strings handles script-mismatch correctly (a Devanagari transcript of Roman input has roughly the same character-length as the Devanagari reference). |
| `end_of_clip_pop_v2` | `end_pop_db` + `terminal_sample_abs` (any one backend; DSP-only) | Unchanged from v1.0. TRUE iff `end_pop_db > 6.0` AND `terminal_sample_abs > 0.005`. |
| `auto_score_confidence_v2` | spread of intel ranks across 3 backends | HIGH if `max - min ≤ 1`. MEDIUM if `= 2`. LOW if `≥ 3`. Use this column to know when human review is most warranted (LOW rows). |

### When `notes_v2` cites disagreement

If `auto_score_confidence_v2 ∈ {MEDIUM, LOW}`, the `notes_v2` field's per-backend-intel breakdown will show the disagreement explicitly. Spot-check those rows by listening if the absolute number matters for a downstream decision.

---

## Override workflow (unchanged from v1.0)

If a human listening pass disagrees with the auto-score:

1. Append a row to `audit/human_overrides.csv` with header `model,id,column,value`. Use the v2 column names (e.g. `intelligibility_v2`, not `intelligibility_1to5`).
2. Run `python audit/scripts/judge_v2.py --merge` (mirrors v1.0's `judge.py --merge`; uses the same template).
3. Output: `audit/auto_scores_v2_filled.csv` with overrides applied; `notes_v2` gets `[human override <col>: was <auto>]` prepended on overridden rows.

---

## Caveats (read before trusting absolute numbers)

1. **`silence_or_skip` over-firing is largely solved.** v1.0 fired this on 21/30 IndicF5 clips and 21/30 SPRINGLab clips because empty AAI transcripts on short clips were interpreted as "missing >20% of words." v2.0's 2-of-3 majority rule plus length-coverage on the unified strings reduces this dramatically for any clip a single backend mishandles. Residual cases (still 20/30 for IndicF5 and 21/30 for SPRINGLab) are likely real truncation: per the duration-diagnostic report, the F5-family did genuinely under-allocate canvas on most non-Devanagari rows. The patched IndicF5 (separate task) collapses this to 0/30.

2. **UTMOS / SQUIM are not used for ranking. Column is ear-only.** A Hindi-trained MOS predictor would let us re-introduce a numeric `naturalness_v2` in v2.x. Plausible candidates: NISQA-FT, UTMOSv2-Hindi (when available), or a small Indic-MOS finetune. Until then: `audit/human_scores.md` is the source of truth for naturalness rankings.

3. **`code_switch_handling` defaults to intelligibility for non-mixed rows.** Same as v1.0. The mixed-row gap calculation uses the model's pure-category mean (computed at row-emission time over both `pure_devanagari` and `pure_roman` rows), which is a per-model calibration, not a cross-model one. A clip whose `intel_v2` matches the model's pure-category mean gets `code_switch_v2 = 5`.

4. **`roman_treated_as_english` is conservative.** Same as v1.0 (0/120 across all baseline models). The threshold `wer_en_forced < 0.30` is strict — when TTS clearly anglicizes Roman-Hindi but the audio is still Hindi-prosody enough that English-forced ASR doesn't fully decode it, the flag stays FALSE. Spot-check `pure_roman` and `mixed_script` rows manually if anglicization-vs-Hindi-prosody is the critical distinction for the downstream decision.

5. **Indian proper nouns may inflate WER on `english_with_NE` rows even after normalization.** The IndicXlit-Devanagari pivot maps "Aishwarya" → "ऐश्वर्या", "Bengaluru" → "बेंगलुरु", etc. via the canonical dict, but if the ASR transcribes a slightly different phonetic form ("ऐश्वरया", "बेंगालुरू"), CER picks up the diff. v2.0 doesn't apply v1.0's `±1 phonetic-not-wrong` adjustment automatically — it would require an LLM-judge step we removed. Note as a known residual: `english_with_NE` mean intel may be slightly underrated.

6. **Determinism.** ASR is sampling-based and re-running may produce slightly different transcripts → slightly different `cer_unified` → potentially different intel rank on threshold-boundary clips. UTMOS / SQUIM / PESQ are deterministic. The judge driver itself is fully deterministic given fixed inputs (no LLM call, no sampling). Re-running `judge_v2.py` on the same `signal_vectors_v2_*.json` files produces byte-identical CSV output.

---

## Reproducibility

```bash
cd ~/Desktop/hienglish
source venv-scoring-py311/bin/activate

# (Stage 1, v1: ASR + DSP + MOS extraction — unchanged from v1.0)
# Already done; signal_vectors{,_deepgram,_groq}.json on disk.

# (Stage 1.5, v2: enrich existing v1 signal vectors with unified-Devanagari)
python audit/scripts/extract_signals_v2.py
# → signal_vectors_v2_aai.json, _deepgram.json, _groq.json (120 entries each)

# (Stage 2: deterministic v2 judge)
python audit/scripts/judge_v2.py
# → auto_scores_v2.csv (120 rows)

# (Validation: correlation against user manual ratings)
python audit/scripts/validate_v2_correlation.py
# → audit/v2_validation/CORRELATION_REPORT.md
```

---

## File inventory (v2.0 additions)

```
audit/
├── JUDGE_PROMPT_v2.md                  # this file (locked)
├── JUDGE_PROMPT_v1_archive.md          # was JUDGE_PROMPT.md (archived after Phase 7)
├── signal_vectors_v2_aai.json          # Stage-1.5 AAI (120 entries)
├── signal_vectors_v2_deepgram.json     # Stage-1.5 Deepgram (120 entries)
├── signal_vectors_v2_groq.json         # Stage-1.5 Groq (120 entries)
├── auto_scores_v2.csv                  # Stage-2 v2 output (120 rows)
├── v2_validation/
│   ├── normalization_validation.json   # Phase 2 IndicXlit gate evidence
│   └── CORRELATION_REPORT.md           # Phase 6 correlation gate evidence
└── scripts/
    ├── lib_normalize.py                # IndicXlit normalizer + canonical dict
    ├── extract_signals_v2.py           # Stage-1.5 driver
    ├── judge_v2.py                     # Stage-2 v2 driver (no LLM)
    ├── validate_normalization.py       # Phase 2 gate runner
    └── validate_v2_correlation.py      # Phase 6 gate runner
```

The `signal_vectors_v2_*.json` files are derived purely from `signal_vectors{,_deepgram,_groq}.json` plus IndicXlit transliteration; **no new ASR calls are made**. Re-deriving from the same v1.0 inputs is byte-identical (the IndicXlit beam-search output is deterministic and the canonical dict + Levenshtein metrics are pure functions).
