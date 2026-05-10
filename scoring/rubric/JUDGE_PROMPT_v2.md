# Judge Prompt v2 — Hindi/Hinglish TTS Auto-Scoring (LOCKED)

> **Version:** 2.0 (2026-05-09)
> Pin this version in every `auto_scores_v2.csv` row's metadata so re-runs are reproducible.
> v1.0 (`JUDGE_PROMPT.md`) remains intact for reproducibility of the original 4-model audit; v2.0 is parallel, not a replacement.

## Changelog vs v1.0

1. **CER/WER computed on `to_unified_devanagari(reference)` vs `to_unified_devanagari(transcript)`.** Both reference and transcript pass through the same IndicXlit-powered normalizer (`audit/scripts/lib_normalize.py`) before edit-distance computation. Solves the script-mismatch measurement artifact: when a model produces Devanagari audio for Roman input, the v1.0 CER pegged at ~1.0 even for correct content; v2.0 measures actual content fidelity.

2. **`naturalness_1to5` becomes ear-only.** The auto-scoring path emits the literal string `"EAR_ONLY"` for every row. UTMOS and SQUIM_MOS are English-trained and drift on Hindi by 1.5–2 ranks per `SCORING_NOTES.md` §2 + the ground-truth ceiling work. Naturalness is now a separate human-listening session, not a scoring column.

3. **`speaker_quality_1to5` stays auto-scored from SQUIM_PESQ.** PESQ measures acoustic fidelity (signal-to-noise, codec quality), not perceptual quality of the speech, and generalizes acceptably to Hindi. Same thresholds as v1.0; same `terminal_sample_abs > 0.05 → -1 rank` rule.

4. **`roman_treated_as_english` is dropped.** The v1.0 column was 0/30 across all four models — non-informative. The signal it tried to capture (TTS anglicizing Roman input) is now indirectly visible: a sentence with high normalized intel but low normalized code-switch handling is anglicizing. The CSV header drops this column.

5. **`silence_or_skip` flag uses normalized text** for the "missing >20% of words" check. Token overlap is computed on `to_unified_devanagari(reference)` vs `to_unified_devanagari(transcript_hi)`. Mid-clip-silence threshold stays at >0.5 s. Expected reduction: original IndicF5's 21/30 false-positive rate should drop substantially because the empty-AAI-transcript-on-short-clips problem was fixed by the duration patch *and* the truncation-via-script-mismatch artifact is gone.

6. **`code_switch_handling_1to5` redefined** to use **normalized** intel as the comparison baseline. The model's pure-category mean (pure_devanagari + pure_roman) is computed from normalized intel; mixed_script and english_with_NE rows score by the integer rank gap to that normalized mean. Threshold structure is identical to v1.0; only the input changes.

7. **`intelligibility_1to5` thresholds are unchanged.** Same 5/4/3/2/1 anchor with CER ≤ 0.05 / 0.15 / 0.30 / 0.50 cutpoints. The phonetic ±1 NE adjustment from v1.0 is removed — redundant now that the Indian-NE whitelist gives canonical Devanagari renderings symmetrically on reference and transcript.

8. **3-ASR consensus is preserved** for patched IndicF5 only (it has 3 ASRs available); baselines stay AAI-only because they were originally scored against AAI signals and re-running 240 ASR calls just to consensus-ize the 4 baselines isn't justified by the question being asked. This asymmetry is documented in `V2_VALIDATION.md`.

---

## The signal vector you receive (per clip)

Stage-1 output (`signal_vectors_v2.json`) preserves all v1.0 fields and adds:

```
  ── v2.0 additions ──
  "text_normalized":          to_unified_devanagari(text)              -- ground-truth reference, unified
  "transcript_hi_normalized": to_unified_devanagari(transcript_hi)     -- main scoring transcript, unified
  "transcript_roman_normalized": to_unified_devanagari(transcript_roman)
  "cer_devanagari_norm":      CER on normalized strings                -- primary intel signal
  "wer_roman_norm":           WER on normalized strings (whitespace-tokenized)
  "asr_backend":              "aai" | "deepgram" | "groq"
  "silence_or_skip_norm":     bool, recomputed using normalized token overlap
```

Existing v1.0 fields stay (`cer_devanagari`, `wer_roman`, `wer_en_forced`, etc.) for backward-compat but are NOT used by v2 scoring.

## What to output (CSV row, one per (model, sentence))

```
model, id, category, text, text_normalized,
intelligibility_1to5,
naturalness_1to5,           # always "EAR_ONLY"
code_switch_handling_1to5,
speaker_quality_1to5,
silence_or_skip,
end_of_clip_pop,
notes
```

`roman_treated_as_english` column is dropped from v2.0 CSVs.

---

## Scoring anchors (use these EXACTLY)

### `intelligibility_1to5`

Use **`cer_devanagari_norm`** for ALL row categories. (v1.0 split between CER for Devanagari rows and WER for Roman rows; v2.0 unifies because both reference and transcript are now Devanagari after normalization, so CER is the natural metric.)

| Score | Anchor | Threshold |
|:---:|---|---|
| 5 | Every word crystal clear | `cer_devanagari_norm` ≤ 0.05 |
| 4 | Almost all clear, 1 minor word slurred | 0.05 < CER_norm ≤ 0.15 |
| 3 | Most clear, 2-3 muddled | 0.15 < CER_norm ≤ 0.30 |
| 2 | Half unintelligible | 0.30 < CER_norm ≤ 0.50 |
| 1 | Mostly noise / wrong words | CER_norm > 0.50 |

No phonetic ±1 adjustment. The Indian-NE whitelist (`audit/scripts/lib_normalize.py`) gives canonical Devanagari forms symmetrically on reference and transcript, so "Hyderabad" appears as "हैदराबाद" in both — no spurious CER inflation.

### `naturalness_1to5`

Output the literal string `"EAR_ONLY"`. Auto-scoring does not compute this column under v2.0. UTMOS and SQUIM_MOS are still in the signal vector for inspection but are not consulted.

### `code_switch_handling_1to5`

**For `pure_devanagari` and `pure_roman` rows:** set to the same value as `intelligibility_1to5`.

**For `mixed_script` and `english_with_NE` rows:** score by the rank gap between this clip's normalized intel and the model's *pure-category* normalized intel mean (computed from the same model's pure_devanagari + pure_roman rows in the same scoring run).

```
gap = pure_mean - this_clip_intel    # pure_mean is float; this_clip_intel is int 1-5
if gap <= 0.05:  return 5
if gap <= 0.15:  return 4
if gap <= 0.30:  return 3
if gap <= 0.50:  return 2
else:            return 1
```

### `speaker_quality_1to5`

SQUIM_PESQ thresholds, identical to v1.0:
- 5: PESQ ≥ 4.0
- 4: 3.5 ≤ PESQ < 4.0
- 3: 3.0 ≤ PESQ < 3.5
- 2: 2.5 ≤ PESQ < 3.0
- 1: PESQ < 2.5

`terminal_sample_abs > 0.05 → -1 rank` (DC tail / hard cutoff).

### `silence_or_skip` (TRUE / FALSE)

**TRUE** if either:
1. `silence_mid_clip_s > 0.5`, OR
2. `transcript_hi_normalized` token-overlap with `text_normalized` is < 80%.

The token-overlap check operates on whitespace-tokenized normalized strings. "Token overlap" = `|set(transcript_tokens) ∩ set(reference_tokens)| / |set(reference_tokens)|` after dropping single-character tokens (which are usually punctuation artifacts).

### `end_of_clip_pop` (TRUE / FALSE)

Identical to v1.0: TRUE iff `end_pop_db > 6.0` AND `terminal_sample_abs > 0.005`.

### `notes`

One sentence citing the specific signals used. At minimum cite `cer_devanagari_norm` and `squim_pesq`.

---

## Hard rules

1. One CSV row per (model, sentence). For patched IndicF5: consensus across 3 ASRs (mode of the integer / boolean) is performed in `judge_v2.py`; the CSV has one row per sentence.
2. All scoring fields present and non-null. `naturalness_1to5` is the literal string `"EAR_ONLY"` (not empty).
3. Likert scores are integers 1-5. Booleans are uppercase `"TRUE"` or `"FALSE"`.
4. `model` and `id` preserve original casing/format.
5. Signal vectors are read-only inputs — do not modify Stage-1 outputs from v1.0.

## Known v2.0 limitations (document in V2_VALIDATION.md)

- **Whitelists are eval-set-tuned (n=30).** The 36 English loans + 18 Indian NEs were extracted from `eval_sentences.tsv` and given canonical Devanagari mappings. Generalization to wild Hinglish would require whitelist expansion.
- **Baseline models have AAI-only ASR.** Patched IndicF5 has 3-ASR consensus; the 4 baselines (kokoro, indic_parler, indicf5, springlab_f5) have AssemblyAI signals only because that's what `extract_signals.py` produced. The asymmetry is documented in `V2_VALIDATION.md` §3.
- **IndicXlit has its own failure modes.** Letter-by-letter transliteration of unknown ASCII tokens (English function words like "from", "with") may produce non-canonical Devanagari that causes spurious CER on english_with_NE rows. The function-word set is small and the failure is symmetric (same on reference and transcript), so the CER inflation tends to cancel — but this is an assumption, not a guarantee.
- **Naturalness and ear-only scoring are out of scope.** The auto-scoring pipeline produces no naturalness signal; the column is a placeholder. A human listening session is a separate task.
- **Phonetic equivalence is whitelist-only.** v2.0 doesn't have a fuzzy-phonetic match (e.g. accepting "हाइदेराबाद" ≈ "हैदराबाद" via soundex). The whitelist provides canonical forms; deviations get penalized. For NEs not in the whitelist, accept ~5-10% CER as the floor.
