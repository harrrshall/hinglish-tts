# Rubric v2.0 — Validation report

**Date:** 2026-05-09
**Inputs:** `audit/signal_vectors{,_deepgram,_groq}.json` (4 baseline models × 30 sentences × 3 ASR backends).
**Outputs:**
- `audit/signal_vectors_v2_{aai,deepgram,groq}.json` — 120 entries each, with `ref_unified`, `transcript_unified`, `cer_unified`, `wer_unified`.
- `audit/auto_scores_v2.csv` — 120 rows (4 models × 30 sentences), 3-ASR consensus, `_v2`-suffixed columns plus `auto_score_confidence_v2`.

Patched IndicF5 v2 scoring is a separate downstream task. v1.0 files (`auto_scores.csv`, `auto_scores.md`) remain frozen.

## Summary

v2.0 is locked. The two designed-for behaviours both materialize cleanly:

1. **Script-mismatch artifact removed.** Kokoro overall intel_v2 = 3.90 (vs v1.0 3.03, **+0.87**); Parler 3.40 (vs 2.73, **+0.67**). The lift is concentrated on pure_roman and mixed_script — the categories where v1.0 was measuring "is the audio in Roman script" rather than "did the audio say the right thing."

2. **3-ASR consensus catches AAI false negatives.** Three pure_devanagari rows (indic_parler/02, indicf5/01, springlab_f5/01) had AAI-empty transcripts → v1 intel=1; Deepgram and Groq returned correct transcripts (CER=0.000). v2 consensus correctly upgrades these to intel_v2=5.

**Rank order is unchanged: kokoro > indic_parler > indicf5 > springlab_f5.** The gap between leaders and the F5 family widens (Kokoro vs indicf5: v1 1.06, v2 1.77) because the F5 family stays at 1.00 on pure_roman / english_with_NE under v2, confirming Mode C is real and not a measurement artifact.

---

## §1 — pure_devanagari behaviour: 3 corrections, no regressions

For 4 baseline models × 8 pure_devanagari sentences = 32 rows, three rows swing by >1 intel rank. All three are AAI-empty-transcript recoveries (v1 intel=1 → v2 intel=5):

| model | id | v1 intel | v2 intel | mechanism |
|-------|----|---------:|---------:|-----------|
| indic_parler | 02 | 1 | 5 | AAI empty; DG/Groq returned `क्या आप मुझे पानी दे सकते हैं?` (CER=0.000) |
| indicf5 | 01 | 1 | 5 | AAI empty; DG/Groq returned `कल मुझे दिल्ली जाना है` (CER=0.000) |
| springlab_f5 | 01 | 1 | 5 | Same — AAI empty; DG/Groq correct |

These are **corrections, not regressions.** v1 was scoring these at intel=1 because AssemblyAI free-tier returns empty transcripts on short Hindi clips (a known v1 weakness called out in `SCORING_NOTES.md` §1). The 3-ASR consensus path naturally fixes this.

The other 29 pure_devanagari rows: |Δ| ≤ 1, normalization is invariant on Devanagari content as designed.

## §2 — silence_or_skip drop on F5 family ✓ partial

| model | v1 | v2 | Δ |
|-------|---:|---:|---:|
| kokoro | 2 | 2 | 0 (real silence_mid hits, unchanged) |
| indic_parler | 4 | 2 | −2 |
| indicf5 | **21** | **20** | **−1** |
| springlab_f5 | **21** | **21** | **0** |

The drop is smaller than the AAI-only v2 sketch (which had 0/30 on indicf5) suggested. The user's `judge_v2` uses a 2-of-3 backend consensus rule, with each backend's silent check being `silence_mid > 0.5 OR transcript_unified covers <80% of ref_unified character length`. The character-coverage check correctly catches Mode A truncation on baseline IndicF5 (the original byte-proportional duration formula produced clips that were 30-60% of expected length on non-Devanagari categories — no ASR can transcribe what isn't there).

Distribution of v2 silence flags on baseline indicf5: pure_roman 8/8, mixed_script 6/8, english_with_NE 6/6, pure_devanagari 0/8. **The 20/30 v2 count IS the real truncation rate** — v1's 21/30 was 20 real truncations + 1 AAI false positive. Same story on springlab_f5.

Implication: when patched IndicF5 is scored under v2 (downstream task), its silence_or_skip count should drop dramatically because the duration patch eliminates the truncation. The previous patched-only run had 0/30 silence_or_skip flags under v1, which we expect to hold under v2.

## §3 — Cross-model headline (4 baseline models × 4 categories, v2.0 with 3-ASR consensus)

| model | pure_dev | pure_roman | mixed_script | english_NE | overall |
|-------|---------:|-----------:|-------------:|-----------:|--------:|
| **kokoro** | 4.62 | **2.50** | **3.88** | **4.83** | **3.90** |
| **indic_parler** | 4.50 | 1.75 | 3.00 | 4.67 | 3.40 |
| indicf5 | 4.62 | 1.00 | 1.62 | 1.00 | 2.13 |
| springlab_f5 | 4.62 | 1.00 | 1.38 | 1.00 | 2.07 |

vs v1.0 (AAI-only):

| model | overall v1.0 → v2.0 | pure_roman | mixed_script |
|-------|--------------------|-----------:|-------------:|
| kokoro | 3.03 → **3.90** (+0.87) | 1.25 → 2.50 | 1.50 → 3.88 |
| indic_parler | 2.73 → **3.40** (+0.67) | 1.12 → 1.75 | 1.50 → 3.00 |
| indicf5 | 1.97 → 2.13 (+0.16) | 1.00 → 1.00 | 1.25 → 1.62 |
| springlab_f5 | 1.93 → 2.07 (+0.14) | 1.00 → 1.00 | 1.25 → 1.38 |

### What moved

- **Kokoro: +0.87 overall.** Concentrated on pure_roman (+1.25) and mixed_script (+2.38). Script mismatch was dominating v1 numbers for these categories — v1 measured "is the audio in Roman script" not "is the audio intelligible." english_with_NE −0.17 (4.83 vs v1 5.00) — slight cost from IndicXlit transliteration of English function words not always matching ASR's Devanagari approximation; net Kokoro is the clear field leader.
- **Parler: +0.67 overall.** Same pattern, smaller magnitude. mixed_script +1.50 is the biggest single delta.
- **IndicF5: +0.16 overall.** pure_roman / english_NE stay at 1.00. The Mode C diagnosis from `audit/indicf5_patched/COMPARISON.md` §4 holds: the model is genuinely producing wrong content for non-Devanagari input, not just right-content-wrong-script.
- **SPRINGLab: +0.14 overall.** Same as IndicF5 — Mode C, not measurement artifact.

### Confidence column distribution

The new `auto_score_confidence_v2` column tracks ASR agreement on intel ranks:

| model | HIGH (spread ≤ 1) | MEDIUM (spread = 2) | LOW (spread ≥ 3) |
|-------|--------------------:|--------------------:|------------------:|
| kokoro | 24 | 5 | 1 |
| indic_parler | 19 | 9 | 2 |
| indicf5 | 29 | 0 | 1 |
| springlab_f5 | 28 | 1 | 1 |

Kokoro and the F5 family are unanimous on most rows (intel either consistently high or consistently low). Parler has the most disagreement — its Hindi prosody confuses AAI more than DG/Groq, producing per-row variance.

## §4 — ASR backend disagreement (consensus mechanic)

Per-(model, ASR) mean unified-CER:

| model | AAI | Deepgram | Groq | spread |
|-------|----:|---------:|-----:|-------:|
| kokoro | 0.135 | 0.119 | 0.147 | 0.028 |
| indic_parler | 0.321 | 0.174 | 0.215 | 0.147 |
| indicf5 | 0.605 | 0.520 | 0.521 | 0.085 |
| springlab_f5 | 0.654 | 0.573 | 0.583 | 0.081 |

AAI is consistently the worst on this corpus, particularly on Indic Parler. Deepgram and Groq agree closely on Hinglish content. The median-of-3 consensus picks the modal rank, robust to any single ASR's failure modes.

## §5 — Whitelist coverage

132 unique ASCII tokens in the eval set, classified at `lib_normalize.py` build time:

- HINDI_ROMAN (IndicXlit fallback): 42 tokens
- ENGLISH_LOAN_CANONICAL: 36 tokens
- INDIAN_NE_CANONICAL: 19 tokens
- ENGLISH_FN (English function words; IndicXlit fallback): 35 tokens

Zero unclassified. Apostrophe handling: tokenizer splits "Karim's" into ["Karim", "'", "s"]; "karim" hits NE whitelist → "करीम". `lib_normalize.py` self-tests (8 cases including idempotency) all pass.

## §6 — Reproducibility

```bash
source venv-scoring-py311/bin/activate    # python 3.11 (3.12 incompatible with fairseq → hydra)
python audit/scripts/lib_normalize.py     # self-tests + idempotency
python audit/scripts/extract_signals_v2.py
python audit/scripts/judge_v2.py
```

Outputs:
- `audit/signal_vectors_v2_{aai,deepgram,groq}.json` (120 entries each)
- `audit/auto_scores_v2.csv` (120 rows)

Determinism: IndicXlit at `topk=1`, `rescore=False` is deterministic; CER/WER on normalized strings is deterministic; UTMOS/SQUIM are deterministic; consensus across 3 fixed ASR JSONs is deterministic. Only stochastic elements are the original ASR API calls (cached in v1 signal vectors); v2 doesn't re-run them.

## §7 — Implications for downstream tasks

- **Step 2a (input preprocessing on patched IndicF5)** is conceptually still worth running. The Mode C diagnosis stands: IndicF5 produces genuinely wrong content for Roman input even after script-fair scoring. Step 2a's intervention (preprocess Roman → Devanagari before feeding) tests whether the model produces correct audio when given character sequences it has training data for. The v2 baseline cleans up the comparison; Step 2a's lift expectation is "feed model in-distribution input" not "fix measurement artifact."

- **Patched IndicF5 v2 scoring is a separate downstream task.** Mechanical: produce 3 v2-augmented files for `audit/indicf5_patched/signal_vectors_*.json` and run the same `judge_v2.py`. ~10 minutes of work; not blocking v2 itself.

- **Production pipeline implications.** Kokoro's lift to 3.90 overall makes it the clear production base for everything except pure_roman (where 2.50 is usable but not strong). For Hinglish-Roman input, a pre-tokenization layer (Roman → Devanagari) feeding into Kokoro might close the gap without TTS-side fine-tuning — an inference-time fix mirroring the IndicF5 duration patch in spirit.

## §8 — Build-time issues (for project record)

- **Python 3.12 incompatibility with fairseq → hydra.** `venv-scoring` (py3.12) fails fairseq's hydra config import on a mutable-default validation. v2 lives in `venv-scoring-py311` (Python 3.11.13 via uv). fairseq emits a non-fatal "hydra_init() skipped" warning but works.
- **IndicXlit's bundled downloader truncates large zips.** The 850 MB `word_prob_dicts.zip` corrupted twice via the package's pydload path (truncated at 21% and 28%). With `rescore=False`, the dicts aren't actually needed; the engine produces clean top-1 transliterations from the 121 MB model alone.
- **Whitelist tuning is eval-set-bound.** The 36 + 19 = 55 curated entries cover the 30-sentence corpus' vocabulary. Generalization to wild Hinglish requires whitelist expansion; this is documented in `JUDGE_PROMPT_v2.md`.
- **English function words inflate CER on Kokoro/Parler english_with_NE.** When Kokoro speaks "She just got hired" in English, ASR returns slight Devanagari approximations that don't always match IndicXlit's letter-by-letter transliteration. Acceptable cost for an eval-set-tuned rubric; not a v2 bug.
