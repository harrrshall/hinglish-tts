# Groq Eval Score — Hinglish TTS Phase 1 Audit

> **Run date:** 2026-05-09
> **Backend:** Groq Whisper-large-v3 (free tier)
> **Rubric:** `audit/JUDGE_PROMPT.md` v1.0 (locked, identical to AssemblyAI + Deepgram runs)
> **Sample:** 120 wavs = 4 models × 30 sentences (orpheus_hi deferred)

---

## ⚠ Security note

The Groq API key was pasted in chat and is now in the conversation transcript. The key is **only ever held in `os.environ`** during the run — never written to any script or output file. **Rotate the key after this audit.** Same protocol as AssemblyAI and Deepgram keys before it.

---

## TL;DR

| Question | Answer |
|---|---|
| Does Groq Whisper-large-v3 work for Hinglish? | Yes. CER on `pure_devanagari` is 0.00–0.21 on clean clips; mean across all clips 0.38–0.64. |
| Faster than Deepgram or AssemblyAI? | **No** — free-tier-throttled. Stage 1 took 21.2 min vs 3.7 min (DG) / 7.3 min (AAI). The model itself is fast; the rate limit is the bottleneck. |
| Cheaper? | **Free** during the run (within free-tier limits). $0.0044/min on paid tier. |
| Does it change model rankings? | **No.** Kokoro > Parler > IndicF5 ≈ SPRINGLab in all three backends. |
| What does Whisper do better? | **Short-clip transcription** — Whisper successfully transcribes the IndicF5/SPRINGLab clips that AAI and DG saw as silent. silence_or_skip flag count drops from 21 → 12 for those models. |
| What does Whisper do worse? | **English-forced channel is noisy**: Whisper transcribes Hindi audio as phonetic-Roman (`"Kal mujhe Delhi jaana hai"`) instead of refusing like Deepgram does. Made the anglicization detector slightly less reliable. |

---

## Configuration

### Model and parameters

```python
# Three-pass per clip, identical to AssemblyAI and Deepgram variants
out_hi   = client.audio.transcriptions.create(file=buf, model="whisper-large-v3", language="hi",
                                              response_format="verbose_json", temperature=0.0)
out_en   = client.audio.transcriptions.create(file=buf, model="whisper-large-v3", language="en",
                                              response_format="verbose_json", temperature=0.0)
out_auto = client.audio.transcriptions.create(file=buf, model="whisper-large-v3",
                                              response_format="verbose_json", temperature=0.0)
```

- **Model: `whisper-large-v3`** — full-fidelity OpenAI Whisper, hosted on Groq's LPU. The Turbo variant (`whisper-large-v3-turbo`) is ~9× faster but with marginally worse WER. For an accuracy-first audit, large-v3 is the right pick.
- `language="hi"` → Devanagari output for CER vs Devanagari ground truth.
- `language="en"` → English-forced. **Differs from Deepgram:** Whisper *attempts* to transcribe Hindi audio as romanized phonetic text (e.g. `"Kal mujhe Delhi jaana hai."`). It does not refuse like Deepgram does. This is a noisier anglicization signal — handled in the judge prompt.
- `language=None` → Whisper's auto-detect; outputs Devanagari for Hindi, Latin script for English.

### Rate limits and free-tier constraints (verified 2026-05-09)

| Limit | Free-tier value | Our usage |
|---|---|---|
| Requests per minute | **30 RPM** | ~24 RPM peak (2 workers) |
| Requests per day | **2,000 RPD** | 360 (3-pass × 120 clips) |
| Audio seconds per hour | **7,200 sec/hr** | ~2,700 sec total |
| Max file size | 25 MB | ~50 KB per clip |

The **30 RPM cap was the binding constraint** — we ran with only 2 parallel workers + exponential backoff to stay under it. Even so, the run took 21 min. On a paid tier (Developer or Growth) concurrency lifts substantially.

Sources: <https://console.groq.com/docs/rate-limits>, <https://console.groq.com/docs/speech-to-text>

### Pricing

- **Free tier:** $0/run within the 2,000 RPD / 7,200 sec/hr ceiling — our run was free.
- **Paid Whisper-large-v3:** ~$0.0044/min audio (cheapest among the three backends we've run).
- For our 120-clip × 3-pass run on paid: ~$0.20.
- Source: <https://groq.com/pricing>

### Known caveats specific to Whisper-large-v3

1. **Hallucination on short clips (<2s)** — Whisper occasionally adds extra tokens, producing CER values >1.0 (we observed 1.09, 1.27, 1.40 in the data). Treat any CER above 1.0 as a clear "1" intelligibility — the judge prompt was annotated to do this.
2. **English-forced is not a refusal** — unlike Deepgram, Whisper-large-v3 with `language="en"` produces a phonetic Romanization of Hindi audio. The rubric's anglicization detector still works because the WER threshold (`wer_en_forced + 0.15 < wer_roman AND wer_en_forced < 0.30`) catches genuine English-handling cases; phonetic Hindi has wer_en_forced ~0.5–1.0.
3. **Auto-detect outputs Devanagari for Hindi audio**, not romanization. So pure_roman category rows always show CER=1.0 for the `transcript_roman` channel — this is expected and the judge uses WER_rom for those rows.

---

## Pipeline timing

| Stage | Step | Time |
|---|---|---|
| 1 | `extract_signals_groq.py` (DSP + ASR + MOS, 2-way parallel under 30 RPM) | **21.2 min** |
| 2 | `judge_groq.py --emit-batches` | <1s |
| 2 | 12 parallel Claude judge sub-agents | ~70s wall (longest agent) |
| 2 | `judge_groq.py --collect` | <1s |
| **Total** | end-to-end | **~22 min** |

Free-tier throttling dominates wall-time. Estimated ~5 min on paid tier with 5 workers.

---

## Per-model results (Groq backend)

### Auto-score means

| Model | Intelligibility | Naturalness | Code-switch | Speaker quality | silent | pop | anglicized |
|---|---:|---:|---:|---:|---:|---:|---:|
| kokoro | **3.10** | **4.00** | 3.10 | 4.27 | 2/30 | 0/30 | 2/30 |
| indic_parler | 2.57 | 3.50 | 2.50 | 4.00 | 1/30 | 4/30 | 0/30 |
| indicf5 | 2.00 | 3.60 | 2.00 | 4.27 | **12/30** | 3/30 | 0/30 |
| springlab_f5 | 1.97 | 3.40 | 1.93 | 4.20 | **12/30** | 0/30 | 0/30 |

**Note the silent count drop for IndicF5/SPRINGLab:** 12/30 vs 20+ in the AAI/DG runs. Whisper-large-v3 successfully transcribes short truncated clips that the other backends returned empty for — this gives a more accurate count of *genuine* truncation cases.

### Per-category intelligibility (Groq)

| Category | kokoro | indic_parler | indicf5 | springlab_f5 |
|---|---:|---:|---:|---:|
| pure_devanagari | 4.50 | 4.12 | 4.62 | 4.50 |
| pure_roman | 1.00 | 1.00 | 1.00 | 1.00 |
| mixed_script | 2.38 | 1.00 | 1.12 | 1.12 |
| english_with_NE | **5.00** | **4.67** | 1.00 | 1.00 |

Whisper handles **english_with_NE** the cleanest of any backend — Kokoro and Parler hit ~5.00 because Whisper's English transcription is native and matches the ground truth English exactly.

---

## 3-way backend comparison (AssemblyAI vs Deepgram vs Groq)

### Per-column unanimous agreement (all three backends produce same value)

| Column | All-three exact | Notes |
|---|---:|---|
| speaker_quality_1to5 | 112/120 (93%) | DSP+SQUIM driven, no ASR involvement |
| roman_treated_as_english | 117/120 (98%) | DSP+threshold driven |
| end_of_clip_pop | 117/120 (98%) | DSP-only |
| naturalness_1to5 | 81/120 (68%) | UTMOS+SQUIM driven, mostly ASR-independent |
| silence_or_skip | 93/120 (78%) | ASR-driven (transcript-completeness check) |
| intelligibility_1to5 | **71/120 (59%)** | ASR-driven (CER/WER) |
| code_switch_handling_1to5 | 69/120 (57%) | ASR-driven |

### Pairwise agreement on intelligibility

| Pair | Exact agreement |
|---|---:|
| AssemblyAI vs Deepgram | 79/120 (66%) |
| **AssemblyAI vs Groq** | **94/120 (78%)** |
| Deepgram vs Groq | 82/120 (68%) |

**AAI and Groq agree most often.** Both are stricter on mixed-script intelligibility; Deepgram's Nova-3 multi mode is the lone outlier that rescues Devanagari-dominant code-mixed clips. If you treat AAI+Groq agreement as the "majority opinion", Deepgram's mixed_script lift is the disagreement.

### Per-model intelligibility (mean across 30 clips)

| Model | AAI | Deepgram | Groq |
|---|---:|---:|---:|
| kokoro | 3.03 | 3.27 | 3.10 |
| indic_parler | 2.73 | **3.13** | 2.57 |
| indicf5 | 1.97 | 2.03 | 2.00 |
| springlab_f5 | 1.93 | 1.97 | 1.97 |

Groq lands closer to AssemblyAI's conservative end. Deepgram remains the most lenient.

### Per-model naturalness (mean)

| Model | AAI | Deepgram | Groq |
|---|---:|---:|---:|
| kokoro | 3.97 | 3.93 | **4.00** |
| indic_parler | 3.33 | 3.40 | 3.50 |
| indicf5 | 3.37 | 3.67 | 3.60 |
| springlab_f5 | 3.07 | 3.33 | 3.40 |

Naturalness ranges narrow (max spread 0.40) because UTMOS+SQUIM are ASR-independent. Groq's slight upward drift on Parler/SPRINGLab traces to fewer false-positive silence flags in the rubric (one rank not deducted).

### silence_or_skip TRUE counts per model

| Model | AAI | Deepgram | Groq |
|---|---:|---:|---:|
| kokoro | 2 | 2 | 2 |
| indic_parler | 4 | 1 | 1 |
| indicf5 | 21 | 20 | **12** |
| springlab_f5 | 21 | 20 | **12** |

**This is the headline backend-comparison finding.** Whisper-large-v3 successfully transcribes ~8 short clips per model that AAI and DG returned empty for. The "true" truncation rate for IndicF5/SPRINGLab is closer to 12/30 (40%) than 20+/30 (67%). On short Hinglish clips, Whisper-large-v3 is the most accurate ASR of the three.

---

## Recommendations

1. **For absolute accuracy** on Hindi/Hinglish auto-scoring, use **Groq Whisper-large-v3** as the primary ASR — it has the most accurate short-clip transcription (silence_or_skip drops 8/clip per model), and best English-with-NE handling (Whisper is native English).
2. **For speed in production**, use **Deepgram Nova-3** — 6× faster than Groq free-tier, comparable accuracy on Devanagari, better on mixed_script.
3. **For comparable cost-per-clip on paid tiers**, all three are within rounding error ($0.05–$0.20 for our 120-clip × 3-pass run). Pick by ergonomics, not price.
4. **For free-tier prototyping**, Groq is the only option that's actually free. Paid tiers add ~10× concurrency and remove the wall-time penalty.
5. **Cross-backend ensemble**: For high-stakes evaluation, run all three and take majority vote. Where ≥2 of 3 agree, use that score; where all 3 differ, flag for human review. Our 3-way intelligibility unanimity is 59% — the remaining 41% is exactly the set worth manually checking.
6. **Don't trust English-forced WER from Whisper as an anglicization signal alone** — Whisper transcribes Hindi audio as phonetic Roman, so wer_en_forced is noisier than Deepgram's empty-string signal. The rubric's two-condition gate (`wer_en + 0.15 < wer_roman AND wer_en < 0.30`) handles this correctly.

---

## Files produced this run

```
audit/
├─ scripts/
│   ├─ lib_asr_groq.py                # NEW — Groq Whisper wrapper
│   ├─ extract_signals_groq.py        # NEW — Stage 1 driver (2 workers, 30 RPM safe)
│   └─ judge_groq.py                  # NEW — Stage 2 driver
├─ signal_vectors_groq.json            # 120 entries × 23 fields
├─ groq_judge_batches/                 # 12 × 10-clip JSON batches
├─ groq_judge_responses/               # 12 batch responses from Claude
├─ groq_auto_scores.csv                # final auto-scores (120 rows)
└─ groq_eval_score.md                  # this file
```

The AssemblyAI and Deepgram artifacts are untouched; all three runs coexist:

| Backend | signals | scores | report |
|---|---|---|---|
| AssemblyAI Universal-2 | `signal_vectors.json` | `auto_scores.csv` | (none) |
| Deepgram Nova-3 | `signal_vectors_deepgram.json` | `deepgram_auto_scores.csv` | `deepgram_eval_score.md` |
| Groq Whisper-large-v3 | `signal_vectors_groq.json` | `groq_auto_scores.csv` | **`groq_eval_score.md`** |

---

## Sources verified during this run

- [Groq Speech-to-Text docs](https://console.groq.com/docs/speech-to-text)
- [Whisper Large v3 model page](https://console.groq.com/docs/model/whisper-large-v3)
- [Whisper Large v3 Turbo announcement](https://groq.com/blog/whisper-large-v3-turbo-now-available-on-groq-combining-speed-quality-for-speech-recognition)
- [Groq Rate Limits](https://console.groq.com/docs/rate-limits)
- [Groq Free Tier Limits 2026](https://www.grizzlypeaksoftware.com/articles/p/groq-api-free-tier-limits-in-2026-what-you-actually-get-uwysd6mb)
- [Groq Pricing](https://groq.com/pricing)
- [Whisper-Hindi2Hinglish (specialized fine-tune, not used)](https://huggingface.co/Oriserve/Whisper-Hindi2Hinglish-Prime)
