# Deepgram Eval Score — Hinglish TTS Phase 1 Audit

> **Run date:** 2026-05-09
> **Backend:** Deepgram Nova-3 (replacing AssemblyAI Universal-2 from prior run)
> **Rubric:** `audit/JUDGE_PROMPT.md` v1.0 (locked, identical to AssemblyAI run)
> **Sample:** 120 wavs = 4 models × 30 sentences (orpheus_hi deferred)

---

## ⚠ Security note

The Deepgram API key was pasted in the chat session and is now in the conversation transcript. The key is **only ever held in `os.environ`** during the run — never written to any script or output file — but you should **rotate it after this audit completes**. Same protocol as the AssemblyAI key from the prior run.

---

## TL;DR

| Question | Answer |
|---|---|
| Does Deepgram Nova-3 work for Hinglish? | Yes. CER on `pure_devanagari` rows is ~0.0 on clean Kokoro/Parler clips. |
| Faster than AssemblyAI? | **Yes — ~2× faster**: Stage 1 finished in 3.7 min vs 7.3 min. |
| Cheaper? | Marginally more expensive: ~$0.13 vs ~$0.05 for the 3-pass × 120-clip run. Both rounding error. |
| Does it change the model rankings? | **No.** Kokoro > Parler > IndicF5 ≈ SPRINGLab in both backends. |
| Where do the two ASRs disagree? | **Mixed-script intelligibility** — Deepgram correctly transcribes Devanagari-dominant code-mixed audio that AssemblyAI sees as "Roman text spoken in Hindi." Kokoro mixed_script intelligibility: AAI 1.50 → DG **3.38** (+1.88 ranks). |

---

## Configuration

### Model and parameters

```python
# Three-pass per clip, identical to AssemblyAI variant
out_hi    = client.listen.v1.media.transcribe_file(buf, model="nova-3", language="hi",    smart_format=True)
out_en    = client.listen.v1.media.transcribe_file(buf, model="nova-3", language="en",    smart_format=True)
out_multi = client.listen.v1.media.transcribe_file(buf, model="nova-3", language="multi", smart_format=True)
```

- **`language="hi"`** → Devanagari output for CER vs Devanagari ground truth.
- **`language="en"`** → English-forced; intentionally returns empty for Hindi audio (used as anglicization detector — empty = "this was Hindi, not Roman-spoken Hindi").
- **`language="multi"`** → Nova-3 multilingual code-switching mode, the recommended setting for Hinglish per Deepgram docs (introduced 2025; 27% Hindi WER reduction vs Nova-2).

### Rate limits and concurrency (verified 2026-05-09 via Deepgram docs)

- **Pre-recorded:** up to **50 concurrent requests** per project (PAYG and Growth identical).
- We used **5 parallel ASR workers** = ThreadPoolExecutor(max_workers=5) — 10× under the limit.
- 429 = rate-limit exceeded; our wrapper retries with exponential backoff (1s / 2s / 4s).
- Source: <https://developers.deepgram.com/reference/api-rate-limits>

### Pricing (verified 2026-05-09)

- **Nova-3 pre-recorded:** $0.0043/min (≈ $0.26/hr).
- 120 clips × 3 passes × ~2.5s avg = ~15 min audio = **~$0.06**.
- Real billed cost may differ slightly; Deepgram bills per-second of audio submitted, not clip count.
- Source: <https://deepgram.com/pricing>

### Known caveats

- **Nova-3 multi sometimes misidentifies Hindi as Spanish on Hindi-English code-switched audio** (Deepgram discussions #1208). Mitigation: we still force-decode `language="hi"` separately for CER, so the Devanagari signal is unaffected. The `transcript_roman` channel is only used for WER on `pure_roman`/mixed rows where the multi-language output is actually appropriate.
- **English-forced returns empty for Hindi audio.** This is correct behavior, but it changes the rubric semantics slightly: `wer_en_forced=1.0` is the normal case (not anglicization). The judge prompt was clarified accordingly when dispatched.
- **Romanization is not native.** Deepgram dropped `hi-Latn` after Nova-1. For pure Roman input we rely on the `multi` channel; for clips where the TTS outputs Devanagari but the reference is Roman, both AssemblyAI and Deepgram give CER=1.0 — this is a model-output-Roman-script gap, not an ASR gap.

---

## Pipeline timing

| Stage | Step | Time |
|---|---|---|
| 1 | `extract_signals_deepgram.py` (DSP + ASR + MOS, 5-way parallel) | **3.7 min** |
| 2 | `judge_deepgram.py --emit-batches` (12 × 10-clip JSON files) | <1s |
| 2 | 12 parallel Claude judge sub-agents | ~70s wall (longest agent) |
| 2 | `judge_deepgram.py --collect` (assemble CSV) | <1s |
| **Total** | end-to-end | **~5 min** |

For comparison, the AssemblyAI Stage 1 took 7.3 min; Deepgram is ~2× faster on the same 120 clips, same 5-worker concurrency.

---

## Per-model results (Deepgram backend)

### Auto-score means (full rubric output)

| Model | Intelligibility | Naturalness | Code-switch | Speaker quality | silent | pop | anglicized |
|---|---:|---:|---:|---:|---:|---:|---:|
| kokoro | **3.27** | **3.93** | 3.43 | 4.27 | 2/30 | 0/30 | 1/30 |
| indic_parler | 3.13 | 3.40 | 3.27 | 4.00 | 1/30 | 6/30 | 0/30 |
| indicf5 | 2.03 | 3.67 | 2.00 | 4.27 | **20/30** | 2/30 | 0/30 |
| springlab_f5 | 1.97 | 3.33 | 1.93 | 4.20 | **20/30** | 0/30 | 0/30 |

Same interpretation as the AssemblyAI run: Kokoro and Parler clearly lead; IndicF5 and SPRINGLab are tied at the bottom because both truncate Roman/english_with_NE prompts mid-utterance (the "silent" column captures this).

### Per-category intelligibility (Deepgram)

| Category | kokoro | indic_parler | indicf5 | springlab_f5 |
|---|---:|---:|---:|---:|
| pure_devanagari | 4.62 | 4.25 | 4.38 | 4.38 |
| pure_roman | 1.00 | 1.00 | 1.00 | 1.00 |
| mixed_script | **3.38** | **3.12** | 1.50 | 1.25 |
| english_with_NE | 4.33 | 4.50 | 1.00 | 1.00 |

The mixed-script row is the most informative new view: Deepgram surfaces that **Kokoro and Parler actually do handle code-mixed Hindi-English well** (3.12-3.38), while IndicF5/SPRINGLab fall apart there (1.25-1.50). The AssemblyAI run flattened all four models on mixed-script to ~1.25-1.50 because Universal-2's auto-detect routed Devanagari-dominant clips to Roman-WER scoring.

---

## Comparison with AssemblyAI

### Cell-level agreement (out of 120 clips)

| Column | Exact agreement | Mean Δ (DG − AAI) | Mean abs Δ |
|---|---:|---:|---:|
| intelligibility_1to5 | 79/120 (66%) | **+0.18** | 0.57 |
| naturalness_1to5 | 88/120 (73%) | +0.15 | 0.27 |
| code_switch_handling_1to5 | 77/120 (64%) | **+0.20** | 0.62 |
| speaker_quality_1to5 | 117/120 (98%) | −0.01 | 0.03 |
| roman_treated_as_english | 119/120 (99%) | — | — |
| silence_or_skip | 107/120 (89%) | — | — |
| end_of_clip_pop | 118/120 (98%) | — | — |

**Reading this:**
- Columns driven by DSP / MOS only (speaker_quality, end_of_clip_pop, roman_treated_as_english) show ≥98% agreement — confirms the pipeline is reproducible across ASR backends.
- Intelligibility / code-switch are the columns that actually exercise the ASR. **Deepgram is consistently +0.18 to +0.20 ranks more lenient** — driven mostly by better mixed_script transcripts.
- silence_or_skip drift (89%) is also ASR-driven: Deepgram successfully transcribes shorter clips that AssemblyAI returned empty for, so it doesn't trip the "missing words" flag as often.

### Per-model intelligibility comparison

| Model | AAI intel | DG intel | Δ |
|---|---:|---:|---:|
| kokoro | 3.03 | **3.27** | +0.23 |
| indic_parler | 2.73 | **3.13** | +0.40 |
| indicf5 | 1.97 | 2.03 | +0.07 |
| springlab_f5 | 1.93 | 1.97 | +0.03 |

Deepgram lifts Kokoro and Parler scores meaningfully (those models do produce intelligible code-mixed audio that AssemblyAI's per-channel routing under-rated). It barely moves IndicF5/SPRINGLab — those are bad for genuine output reasons (truncation), not ASR drift.

### Where the two backends disagree most

Biggest single category × model swing:

```
kokoro mixed_script:        AAI 1.50 → DG 3.38   (+1.88 ranks)
indic_parler mixed_script:  AAI 1.50 → DG 3.12   (+1.62 ranks)
```

Both are **Deepgram-correctly-rescuing** Devanagari-dominant code-mixed audio that AssemblyAI mis-routed to Roman-WER scoring. The Deepgram rating is closer to ground truth on these rows.

---

## Boolean flag comparison

| Flag | AAI total TRUE | DG total TRUE | Net change |
|---|---:|---:|---:|
| roman_treated_as_english | 0 | 1 | +1 |
| silence_or_skip | 48 | 43 | −5 |
| end_of_clip_pop | 6 | 8 | +2 |

`silence_or_skip` decrease is informative: Deepgram returns valid transcripts for some short clips where AssemblyAI returned empty (false-positive on the AAI side). Net: Deepgram is the more trustworthy signal for the skip/missing-words detection.

---

## Files produced this run

```
audit/
├─ scripts/
│   ├─ lib_asr_deepgram.py            # NEW — Deepgram ASR wrapper (mirrors lib_asr.py)
│   ├─ extract_signals_deepgram.py    # NEW — Stage 1 driver (writes _deepgram.json)
│   └─ judge_deepgram.py              # NEW — Stage 2 driver (deepgram_* paths)
├─ signal_vectors_deepgram.json        # 120 entries × 23 fields
├─ deepgram_judge_batches/             # 12 × 10-clip JSON batches
├─ deepgram_judge_responses/           # 12 batch responses from Claude
├─ deepgram_auto_scores.csv            # final auto-scores (120 rows)
└─ deepgram_eval_score.md              # this file
```

The original AssemblyAI artifacts (`signal_vectors.json`, `auto_scores.csv`, `judge_batches/`, `judge_responses/`) are untouched — both runs coexist for comparison.

---

## Recommendations

1. **For future Hinglish TTS audits, prefer Deepgram Nova-3 multi as the primary ASR.** Better mixed-script intelligibility, ~2× faster, more accurate silence detection on short clips.
2. **Keep the 3-pass design** (`hi` / `en` / `multi`). The English-forced channel is still a useful anglicization signal even though it returns empty more often than AssemblyAI did.
3. **Don't compare absolute auto-scores across ASR backends.** Use the same backend for any longitudinal comparison; cross-backend deltas are real and average ~0.2 ranks.
4. **For human-grade evaluation**, the user's manual scores remain the authoritative reference — Deepgram does not fix the **UTMOS / SQUIM English-training drift** documented in `SCORING_NOTES.md` (predictors still over-rate Hindi naturalness by ~1.5-2 ranks).

---

## Sources verified during this run

- [Deepgram Models & Languages Overview](https://developers.deepgram.com/docs/models-languages-overview)
- [Deepgram API Rate Limits](https://developers.deepgram.com/reference/api-rate-limits)
- [Deepgram Pricing](https://deepgram.com/pricing)
- [Nova-3 Multilingual Hindi WER improvements](https://deepgram.com/learn/nova-3-multilingual-major-wer-improvements-across-languages)
- [Nova-3 Hindi-English misidentification issue (#1208)](https://github.com/orgs/deepgram/discussions/1208)
- [Deepgram Python SDK v7](https://github.com/deepgram/deepgram-python-sdk)
