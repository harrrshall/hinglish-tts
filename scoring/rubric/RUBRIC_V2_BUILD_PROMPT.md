# Agent task: Build rubric v2.0 — IndicXlit-normalized scoring + naturalness ear-only

## Read first (required)

Load these in order. Each is necessary context, not optional:

1. `/RESEARCH_LOG.md` — current project state.
2. `/audit/JUDGE_PROMPT.md` — rubric **v1.0**, the file you are *adding to* (not editing). v2.0 is a parallel rubric, not a replacement; the v1.0 file stays intact for reproducibility of the original 4-model audit.
3. `/audit/SCORING_NOTES.md` §1–§5 — the five caveats that motivate v2.0:
   - silence_or_skip over-fires on indicf5/springlab (21/30 false positives)
   - UTMOS/SQUIM are English-trained; absolute MOS values drift on Hindi
   - code_switch_handling defaults to intel for non-mixed rows (fine, keep)
   - `roman_treated_as_english` is conservative (0/30 across 4 models — non-informative)
   - Indian proper nouns inflate CER/WER artificially
4. `/audit/auto_scores.md` — the v1.0 scores you are re-baselining. Note the "21/30 silence flags" pattern on IndicF5 in particular.
5. `/audit/indicf5_patched/COMPARISON.md` — the patched-IndicF5 result that motivates the cross-script measurement problem. Section 4 ("RIGHT_LEN_GARBLED" mode) shows why scoring without normalization breaks down: when the model produces Devanagari audio for Roman input, ASR returns Devanagari, reference is Roman → CER pegs at ~1.0 even when content is correct.
6. `/audit/eval_sentences.tsv` — the 30-sentence eval set. The English-loan and Indian-NE whitelists must be tuned to *this* set; do not over-engineer for hypothetical future inputs.
7. `/audit/scripts/extract_signals.py` — the v1.0 Stage-1 driver. v2 reuses 100% of its outputs; only the scoring function changes, not the signal extraction.
8. `/audit/scripts/patched/auto_score.py` — the deterministic v1.0 scorer. v2.0's `judge_v2.py` is structurally similar — same threshold-based approach, different normalization step in front.
9. `/audit/signal_vectors.json` — Stage-1 output for the 4 baseline models (already exists, 120 entries).
10. `/audit/indicf5_patched/signal_vectors_{aai,deepgram,groq}.json` — Stage-1 outputs for the patched IndicF5 run (already exists, 30 entries each across 3 ASRs).

After loading, confirm in your reply:
- (a) You understand v2.0 is **parallel** to v1.0 — both rubrics coexist; v1.0 files are not modified.
- (b) You understand this is **scoring-only** work — no new wavs generated, no new ASR calls, no model touched. Stage-1 signal vectors stay frozen.
- (c) You understand the headline change is **symmetric IndicXlit normalization** of both reference and transcript before WER/CER, plus dropping auto-naturalness.

## What you're producing

Six artifacts:

1. `audit/scripts/lib_normalize.py` — `to_unified_devanagari(text)` function + curated whitelists. Exposed for reuse (Step 2a's input preprocessing will import this same function).
2. `audit/JUDGE_PROMPT_v2.md` — locked rubric. Header marks it `v2.0 (2026-05-09)`, frozen.
3. `audit/scripts/extract_signals_v2.py` — Stage-1 wrapper that reuses existing `signal_vectors.json` + per-ASR JSONs from indicf5_patched, but adds normalized fields (`cer_devanagari_norm`, `wer_roman_norm`, `wer_en_forced_norm`). Does **not** re-run ASR.
4. `audit/scripts/judge_v2.py` — deterministic scorer matching v2.0 anchors. Same shape as `audit/scripts/patched/auto_score.py`.
5. `audit/auto_scores_v2.csv` — 5 models × 30 sentences = 150 rows. The 5 models are: kokoro, indic_parler, indicf5, springlab_f5, indicf5_patched.
6. `audit/V2_VALIDATION.md` — sanity checks: does v1.0 vs v2.0 score the *same* model differently in expected ways? Specifically (a) does indicf5 pure_roman / english_NE lift when normalization is applied? (b) does pure_devanagari stay roughly stable across versions?

## Phase 0 — Preconditions

Before doing anything, verify:

1. `audit/signal_vectors.json` exists and has 120 entries (4 baseline models × 30).
2. `audit/indicf5_patched/signal_vectors_{aai,deepgram,groq}.json` each exist with 30 entries.
3. Local Python venv (`venv-scoring/`) has internet access for IndicXlit install. Test: `pip install --dry-run ai4bharat-transliteration` — if this hits a closed-network error, stop and ask.
4. The eval set TSV is the same one that produced both prior runs (not modified).

If any precondition fails, stop and report.

## Phase 1 — Install + smoke-test IndicXlit

The library: `ai4bharat-transliteration` (or whatever the canonical pip name is — verify before running). Search if uncertain.

```bash
source venv-scoring/bin/activate
pip install ai4bharat-transliteration  # verify package name first
```

Smoke test:

```python
from ai4bharat.transliteration import XlitEngine
xlit = XlitEngine("hi", beam_width=4, src_script_type="roman")
result = xlit.translit_word("kal", topk=1)
# Expected: {"hi": ["कल"]} or similar
```

If the install fails or the smoke test produces obviously wrong output (e.g., empty list, English passthrough), **stop and ask the user.** Don't try alternative transliteration libraries (libindic, hindi-transliteration, etc.) without explicit OK — the project committed to IndicXlit per the v2.0 design.

If install takes >15 min or the package size is >2 GB (it shouldn't be, but check), pause and confirm with the user before proceeding.

## Phase 2 — Build the curated whitelists

Two whitelists, both tuned to the 30-sentence eval set's actual vocabulary. **Do NOT over-engineer for hypothetical future Hinglish.**

Inspect `audit/eval_sentences.tsv` and extract:

### English loans whitelist (English-origin words in any sentence)

These are the English-origin words that should map to a *canonical* Devanagari form rather than IndicXlit's default transliteration. Why curated: IndicXlit may render "office" as "ओफ़िस" or "ऑफ़िस" or "ऑफिस" depending on its training-data biases; we want to lock to one form so reference and transcript match.

Build by inspection. Examples from the eval set (extract the full list yourself):

```python
ENGLISH_LOAN_CANONICAL = {
    "office":       "ऑफिस",
    "party":        "पार्टी",
    "reply":        "रिप्लाई",
    "wait":         "वेट",
    "movie":        "मूवी",
    "waste":        "वेस्ट",
    "laptop":       "लैपटॉप",
    "deliver":      "डिलीवर",
    "ticket":       "टिकट",
    "lucky":        "लकी",
    "presentation": "प्रेजेंटेशन",
    "tomorrow":     "टुमॉरो",
    "nervous":      "नर्वस",
    "homework":     "होमवर्क",
    "restaurant":   "रेस्टोरेंट",
    "try":          "ट्राई",
    "event":        "इवेंट",
    "cancel":       "कैंसल",
    "message":      "मैसेज",
    "please":       "प्लीज़",
    "file":         "फाइल",
    "quickly":      "क्विकली",
    "review":       "रिव्यू",
    "deadline":     "डेडलाइन",
    "close":        "क्लोज़",
    "log":          "लॉग",
    "lunch":        "लंच",
    "boss":         "बॉस",
    "leave":        "लीव",
    "personal":     "पर्सनल",
    # ... add the rest after grepping eval_sentences.tsv
}
```

### Indian named entities whitelist

Indian proper nouns get their conventional Devanagari rendering, not IndicXlit's letter-by-letter guess. Examples:

```python
INDIAN_NE_CANONICAL = {
    "aishwarya":    "ऐश्वर्या",
    "chennai":      "चेन्नई",
    "bengaluru":    "बेंगलुरु",
    "khanna":       "खन्ना",
    "priya":        "प्रिया",
    "karim":        "करीम",
    "delhi":        "दिल्ली",
    "rohan":        "रोहन",
    "mumbai":       "मुंबई",
    "hyderabad":    "हैदराबाद",
    "tata":         "टाटा",
    "consultancy":  "कंसल्टेंसी",
    "services":     "सर्विसेज़",
    "pune":         "पुणे",
    "paradise":     "पैराडाइज़",
    "biryani":      "बिरयानी",
    "connaught":    "कनॉट",
    "place":        "प्लेस",
    # ... add the rest
}
```

Combine both into one dict at use time. The lookup is case-insensitive on the key.

**Document each whitelist entry's source.** A single-line comment per entry citing the eval-sentence ID it appears in is enough. This isn't paranoia — it's how you justify "this whitelist is tuned to n=30, not generalized" in the v2.0 caveats.

## Phase 3 — Build `lib_normalize.py`

The function:

```python
def to_unified_devanagari(text: str) -> str:
    """Transliterate any Roman tokens in `text` to Devanagari.

    Strategy:
    - Tokenize on whitespace + punctuation boundaries (preserve punctuation in output).
    - For each token:
        - if pure Devanagari (or other non-Latin Indic): pass through unchanged
        - if pure ASCII alphabetic:
            - lowercase, look up in CANONICAL dict (English loans + Indian NEs); if found, emit canonical Devanagari
            - else IndicXlit transliterate (topk=1, deterministic)
        - if mixed (rare in eval set; e.g., "₹100"): split numerals + script and handle each
        - if pure-numeric or punctuation: pass through

    Returns: Devanagari-unified text. Idempotent: applying it twice gives the same result.
    """
```

Key implementation notes:

- **Tokenization**: split on `\s+` and around `[।,?!.]` punctuation. Re-emit punctuation in original positions. Don't be cute with regex — a word_re of `r"[A-Za-z]+|ऀ-ॿ+|\d+|."` works.
- **Lowercase before lookup** for the canonical dicts (the dicts are keyed lowercase).
- **IndicXlit invocation**: `topk=1`, deterministic. Cache the engine object globally; don't reinit per call.
- **Idempotent check** at the bottom of the file: assert `to_unified_devanagari(to_unified_devanagari(x)) == to_unified_devanagari(x)` for 5 sample sentences.

Test cases at the bottom of the file (run on `python audit/scripts/lib_normalize.py`):

```python
TESTS = [
    # (input, expected_output_substring)
    ("कल मुझे दिल्ली जाना है।", "कल मुझे दिल्ली जाना है"),  # pure Devanagari, no change
    ("kal mujhe office jaana hai", "ऑफिस"),                   # office → canonical
    ("My friend Aishwarya from Chennai", "ऐश्वर्या"),           # NE whitelist hit
    ("Mera presentation tomorrow है", "प्रेजेंटेशन"),
    ("मेरा भाई आज स्कूल नहीं गया", "स्कूल"),                  # Devanagari unchanged
    ("Boss को बता देना kal", "बॉस"),
]
for inp, expected in TESTS:
    out = to_unified_devanagari(inp)
    assert expected in out, f"FAIL: {inp!r} → {out!r} missing {expected!r}"
print("All normalization tests passed.")
```

## Phase 4 — Lock `JUDGE_PROMPT_v2.md`

This is a *policy* document, not code. Write it as a clean derivative of `JUDGE_PROMPT.md`, with the v2.0-specific changes called out in a top-of-file changelog.

### Changes from v1.0 (document at top of file)

1. **CER/WER computed on `to_unified_devanagari(reference)` vs `to_unified_devanagari(transcript)`.** The unnormalized CER/WER stays in the signal vector (for backward-compat / debugging) but does not feed scoring.

2. **`naturalness_1to5` becomes ear-only.** Auto-scoring populates this column with the literal string `"EAR_ONLY"` (or empty). The v2.0 scoring function does NOT compute naturalness from UTMOS/SQUIM. Reasoning: per `audit/SCORING_NOTES.md` §2 and the ground-truth ceiling work, English-trained predictors invert/drift on Hindi enough that the column is uninformative cross-model. Naturalness is now a separate human-listening session.

3. **`speaker_quality_1to5` stays auto-scored from SQUIM_PESQ.** Speaker quality is acoustically defined (signal-to-noise, codec quality) and SQUIM_PESQ generalizes acceptably. Document this as the one "auto" axis remaining for non-intelligibility.

4. **`roman_treated_as_english` is dropped.** Reason: 0/30 across all v1.0 models — non-informative threshold. The signal it tried to capture (TTS anglicizing Roman input) is now better captured by inspecting whether normalized intel is high but normalized code-switch handling is low. Document this explicitly.

5. **`silence_or_skip` flag uses normalized text** for the "missing >20% of words" check. Specifically: tokenize `to_unified_devanagari(reference)` and `to_unified_devanagari(transcript_hi)`, count token overlap. Mid-clip-silence threshold stays at >0.5 s. Document the 21/30→? expected reduction on IndicF5.

6. **`code_switch_handling_1to5` redefined** to use **normalized** intel as the comparison baseline. The model's pure-category mean is computed from normalized intel; mixed_script and english_with_NE rows score by the gap to that normalized mean. Otherwise structure is identical to v1.0.

7. **`intelligibility_1to5` anchors are unchanged** in numerical thresholds. Same 5/4/3/2/1 buckets, same CER/WER cutpoints. Only the input to those thresholds changes (normalized vs raw).

8. **±1 phonetic adjust for Indian NEs is removed.** It's now redundant — the Indian-NE whitelist handles the canonical rendering, so CER won't penalize "हाइदेराबाद" vs "हैदराबाद" because both reference and transcript get whitelisted to "हैदराबाद".

### Output schema (v2.0 CSV header)

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

## Phase 5 — Build `extract_signals_v2.py`

This is **a reader**, not a re-runner. It opens existing signal_vectors JSONs, applies normalization, and emits an enriched JSON.

```python
"""Add normalized CER/WER fields to existing signal vectors. Reuses Stage-1 outputs.

Inputs:
    audit/signal_vectors.json                              (4 baseline models)
    audit/indicf5_patched/signal_vectors_aai.json          (patched IndicF5 — AAI)
    audit/indicf5_patched/signal_vectors_deepgram.json     (... Deepgram)
    audit/indicf5_patched/signal_vectors_groq.json         (... Groq)

Output:
    audit/signal_vectors_v2.json                           (150 entries: 4 baseline × 30 + 1 patched × 30)
    Each entry adds:
        - text_normalized:           to_unified_devanagari(text)
        - transcript_hi_normalized:  to_unified_devanagari(transcript_hi)
        - cer_devanagari_norm:       CER on normalized strings
        - wer_roman_norm:            WER on normalized strings (transcript_roman normalized vs ref normalized)
        - asr_backend:               "aai" | "deepgram" | "groq" (only for indicf5_patched rows; "aai" for v1.0 baseline since that's what extract_signals.py used)
        - silence_or_skip_norm:      bool, recomputed using normalized token overlap
"""
```

For the indicf5_patched rows, the user's chosen consensus rule is "majority across 3 ASRs". So `signal_vectors_v2.json` should include all 3 ASR variants (3 × 30 = 90 patched rows) plus the 4 × 30 baseline = 210 total. Actually let me re-check: the COMPARISON.md uses 3-ASR consensus. So either:

- Option α: emit 3 patched-IndicF5 entries per sentence (one per ASR) and let `judge_v2.py` consensus across them
- Option β: pre-compute consensus in extract_signals_v2.py and emit one row per (model, sentence) like the baseline

Pick **Option α** — keep the per-ASR signal granularity in the JSON; do consensus in the judge step. Reason: it's more inspectable (you can see which ASR disagreed) and matches what the patched COMPARISON.md did.

For the 4 baseline models, only AAI is available (it's what v1.0 used). Don't synthesize fake Deepgram/Groq for them — just mark `asr_backend: "aai"` and accept that consensus is single-source for the baselines. Document this as a v2.0 known asymmetry (the patched IndicF5 column has 3-ASR consensus; the baselines have AAI-only).

## Phase 6 — Build `judge_v2.py`

Same structure as `audit/scripts/patched/auto_score.py`. Reads `signal_vectors_v2.json`, applies the v2.0 anchors, emits `auto_scores_v2.csv`.

For patched-IndicF5 rows that have 3 ASR variants:
- intelligibility, code_switch, silence_or_skip: majority vote across the 3 (mode of the integer or boolean)
- speaker_quality: take the AAI variant's value (the others compute the same thing — DSP signals don't depend on ASR)
- emit one row per (model, sentence), not per (model, sentence, ASR)

For baseline models (single ASR): score directly, no consensus.

Speaker_quality column: use SQUIM_PESQ thresholds from v1.0 unchanged. Same `terminal_sample_abs > 0.05 → -1 rank` rule.

Naturalness column: hardcode `"EAR_ONLY"` for every row.

## Phase 7 — Generate `auto_scores_v2.csv` and validate

Run the full pipeline:

```bash
source venv-scoring/bin/activate
python audit/scripts/extract_signals_v2.py
python audit/scripts/judge_v2.py --signals audit/signal_vectors_v2.json --out audit/auto_scores_v2.csv
```

### Validation in `audit/V2_VALIDATION.md`

Three checks, each one section:

**1. Sanity: pure_devanagari intel should not change much from v1.0 → v2.0.**

Normalization is a no-op for Devanagari rows (no Roman tokens to transliterate; reference unchanged). If intel changes by >0.3 ranks on any pure_devanagari row, that's a normalizer bug. Print v1.0 vs v2.0 per-sentence intel for all 30 pure_devanagari rows (across 4 baseline models). Flag any row with |delta| > 1.

**2. Headline: pure_roman / english_with_NE intel on patched IndicF5 should LIFT under v2.0.**

This is the partial-validation of the Mode C diagnosis. The v1.0 score pegged at 1.00 because the model produced Devanagari audio for Roman input → ASR returned Devanagari → CER vs Roman reference ≈ 1.0. With normalization, both reference and transcript are Devanagari, so CER measures actual content fidelity. Expect: pure_roman patched intel rises from 1.00 to somewhere in [1.5, 3.5]. If it stays at 1.00, the normalization isn't doing what we think — investigate.

For each of the 16 pure_roman + english_with_NE patched-IndicF5 rows: print v1.0 unnormalized CER, v2.0 normalized CER, v1.0 intel, v2.0 intel.

**3. Cross-model headline table (5 models × 4 categories, v2.0 only).**

```
| model            | pure_dev | pure_roman | mixed_script | english_NE | overall |
|------------------|:--------:|:----------:|:------------:|:----------:|:-------:|
| kokoro           |    ?     |     ?      |      ?       |     ?      |    ?    |
| indic_parler     |    ?     |     ?      |      ?       |     ?      |    ?    |
| indicf5          |    ?     |     ?      |      ?       |     ?      |    ?    |
| springlab_f5     |    ?     |     ?      |      ?       |     ?      |    ?    |
| indicf5_patched  |    ?     |     ?      |      ?       |     ?      |    ?    |
```

Compare to the v1.0 headline in `audit/auto_scores.md`. Document any rank changes and flag them. Note especially: do the F5 family models (indicf5, springlab_f5) gain on pure_roman / english_with_NE under v2.0 because the normalization stops penalizing them for script mismatch?

## What to NOT do

- **Don't modify `audit/JUDGE_PROMPT.md` (v1.0)** — it stays as-is, frozen reference.
- **Don't modify `audit/auto_scores.csv` or `auto_scores.md`** — same reasoning. v2.0 is parallel.
- **Don't modify `audit/scripts/extract_signals.py`, `extract_signals_groq.py`, `extract_signals_deepgram.py`** — they produced the signal vectors that v2.0 reuses.
- **Don't re-run any ASR API.** Stage-1 signals are frozen; only post-hoc normalization changes. If you find yourself wanting to re-call AssemblyAI/Deepgram/Groq, you've misread the design.
- **Don't generate any new wavs.** This is scoring-only.
- **Don't change MOS predictors or add new ones** (UTMOS/SQUIM stay; they just don't feed naturalness anymore).
- **Don't add the patched IndicF5 outputs to the v1.0 `auto_scores.csv`** retroactively. v1.0 stays at 4 models. v2.0 has 5.
- **Don't tune the whitelists for the patched-Xlit Step 2a experiment.** They're tuned to the eval set's vocabulary; that's it. Step 2a uses the same whitelists this task produces.
- **Don't cache the IndicXlit engine object across module reloads** in a way that hides version skew. If you upgrade ai4bharat-transliteration mid-task and it changes outputs, that's a re-run trigger.

## Stop and ask if

- IndicXlit produces obviously broken Devanagari for >5 of the eval-set's Roman tokens (e.g., empty strings, English passthrough, or transliterations that visibly miss the phoneme structure). Describe what you're seeing and ask before patching it up — IndicXlit failures may invalidate Step 2a.
- The whitelist list balloons past ~70 entries. The eval set is 30 sentences; if you're adding more than ~70 canonical mappings, you're either (a) mistakenly putting Hindi words in there (they don't need mapping) or (b) over-engineering for vocabulary not in the eval set.
- After v2.0 scoring, model rank order on `pure_devanagari` *changes* by more than one position (e.g., kokoro and indicf5 swap). That category should be normalization-invariant; a rank change there suggests a bug.
- After v2.0 scoring, `silence_or_skip` count on indicf5 stays >15/30. The whole point of the normalized check is that the false-positive-rich v1.0 flag (21/30) should drop substantially. If it doesn't, the silence check needs different logic, not a normalization patch.
- IndicXlit's pip package is unavailable / requires GPU / requires a HF gated model that needs token rotation. Stop and confirm a path before installing alternatives.

## Wall-time estimate

- Phase 0 (preconditions): 10 min
- Phase 1 (install + smoke): 20 min  (most of which is the pip install)
- Phase 2 (whitelists by inspection): 30 min  (this is the part that needs care)
- Phase 3 (lib_normalize.py): 45 min  (tokenization is fiddly)
- Phase 4 (JUDGE_PROMPT_v2.md): 30 min  (mostly writing prose)
- Phase 5 (extract_signals_v2.py): 30 min
- Phase 6 (judge_v2.py): 30 min
- Phase 7 (validation): 30 min

Total: ~3.5 hours. Mostly mechanical; the only research-y parts are the whitelist tuning (Phase 2) and verifying IndicXlit produces sane output (Phase 1 + Phase 3 testing). If you're at hour 5 and not yet at validation, something has scope-crept — stop and report.

---

## Notes on decisions baked into this prompt

**Parallel rubric, not replacement.** v1.0 stays intact. This costs ~5 KB of disk space and buys reproducibility of the original audit. The existing `auto_scores.md` is referenced in too many other docs to retroactively rewrite.

**Naturalness goes ear-only.** The ground-truth ceiling work surfaced that UTMOS/SQUIM disagree with native-speaker ear ratings on Hindi by 1.5–2 ranks consistently. Keeping auto-naturalness in v2.0 perpetuates a known-bad signal. Ear-listening is a separate session; v2.0 just doesn't pretend to score this column automatically. Speaker quality stays auto because PESQ generalizes acceptably (it measures acoustic fidelity, not perceptual quality of the *speech*).

**`roman_treated_as_english` dropped, not redefined.** It was 0/30 across all v1.0 models. Either the threshold was wrong or the underlying signal isn't measurable from the existing ASR backends. Either way, "0 across the board" is a non-informative column. Drop is cleaner than rewrite.

**Curated whitelists, not pure IndicXlit.** IndicXlit's transliterations are fine as a fallback but inconsistent across runs / vocabulary items. Curated mappings for the eval set's specific English loans + Indian NEs lock the canonical form so reference and transcript collide deterministically. This is tightly scoped — the prompt is explicit that these whitelists are tuned to n=30, not generalized.

**3-ASR consensus is preserved for patched IndicF5; baselines stay AAI-only.** Re-running AssemblyAI's free credits or paying for 4 × 30 × 2 = 240 extra ASR calls just to consensus-ize the baselines is not justified by the question being asked (which is about TTS quality, not ASR robustness). Document the asymmetry in V2_VALIDATION.md and move on.

**No phonetic ±1 adjustment in v2.0.** The Indian-NE whitelist makes it redundant, and the v1.0 implementation was instructions-to-Claude-judge-listen which didn't actually look at audio. Better to handle it deterministically via whitelist than to rely on a post-hoc judgment that wasn't auditable.

**The output of this task makes Step 2a runnable.** Once `lib_normalize.py` and `auto_scores_v2.csv` exist, the Step 2a prompt's preconditions all pass and it can run. That's the chain: v2.0 build → re-baseline 5 models on v2.0 → run patched+xlit experiment → score on v2.0 → compare three columns side-by-side. Without v2.0, step 2a's intel numbers would be measuring script-mismatch noise instead of content fidelity.
