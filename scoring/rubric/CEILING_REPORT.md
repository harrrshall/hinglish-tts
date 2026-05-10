# Human Ground-Truth Ceiling Report
**Date:** 2026-05-09
**Set:** 8 human-recorded Hindi/Hinglish clips, single speaker
**Pipeline:** identical to 120-clip TTS baseline — DSP + UTMOS + SQUIM + 3 ASR backends + Claude judge over `JUDGE_PROMPT.md` v1.0 (rubric NOT modified)

---

## TL;DR

The MOS predictors used in the rubric (UTMOS, SQUIM_MOS, SQUIM_PESQ) rate this human Hindi audio **lower than they rate every TTS model in the 120-clip baseline.** That is structurally impossible if the predictors were calibrated to actual perceived quality — the human recording is the upper bound by definition. The drift is large (~+1.7 to +2.2 ranks of TTS-over-human on raw MOS, ~+2.2 ranks on the rubric's `naturalness_1to5`, ~+3.2 on `speaker_quality_1to5`). Calibration of rubric v2.0 is required before the auto-naturalness scores can be cited.

The intelligibility/code-switch axis is more robust: human GT lands at 3.25 mean, vs 2.42 baseline mean (Kokoro 3.03). The rubric's intelligibility column is reliable; the naturalness/speaker-quality columns are not.

---

## Section 1 — Per-sentence breakdown (n=8)

Each row: id, category, **per-ASR intelligibility / consensus**, consensus naturalness, consensus speaker_quality, key signals, flags. Underlying CER/WER values shown to make ASR disagreement legible.

| id | category | sentence (truncated) | CER (aai/dg/gq) | WER_rom (aai/dg/gq) | intel (aai/dg/gq/**cons**) | **nat** | **spk** | UTMOS | SQUIM_MOS | PESQ | flags |
|---|---|---|---|---|---|:---:|:---:|:---:|:---:|:---:|---|
| human_01 | pure_devanagari | कल मुझे दिल्ली जाना है। | 0.00/0.00/0.14 | 0.00/0.00/0.20 | 5/5/4/**5** | 2 | 1 | 2.09 | 2.72 | 2.19 | — |
| human_02 | pure_devanagari | जल्दी आओ यार, सब तेरा इंतज़ार… | 0.15/0.13/0.28 | 0.22/0.22/0.44 | 3/4/3/**3** | 1 | 1 | 1.67 | 2.52 | 1.55 | end-of-clip pop (terminal=0.000, gated FALSE) |
| human_03 | pure_roman | kal mujhe office jaana hai | 0.85/0.62/0.85 | 1.00/0.80/1.00 | 1/1/1/**1** | 1 | 1 | 1.78 | 2.70 | 1.56 | rubric artifact: ASR returned Devanagari for Roman GT |
| human_04 | pure_roman | yaar tu kal kya kar raha tha | 0.82/0.82/0.82 | 1.00/1.00/1.00 | 1/1/1/**1** | 1 | 1 | 1.51 | 2.46 | 1.53 | rubric artifact (same as above) |
| human_05 | mixed_script | Kal mujhe ऑफिस जाना hai, but ट्राफिक… | 0.50/0.46/0.52 | 0.82/0.45/0.73 | 2/2/1/**2** | 2 | 1 | 1.89 | 2.31 | 1.43 | — |
| human_06 | mixed_script | Mera presentation tomorrow है… | 0.67/0.08/0.10 | 0.62/0.25/0.25 | 1/4/4/**4** | 3 | 1 | 2.22 | 2.80 | 1.80 | AAI disagrees with DG/Groq by 3 ranks |
| human_07 | english_with_NE | My friend Aishwarya from Chennai… | 0.34/0.25/0.00 | 0.00/0.30/0.00 | 5/4/5/**5** | 2 | 1 | 2.21 | 2.52 | 1.33 | — |
| human_08 | english_with_NE | I love butter chicken from Karim's… | 0.26/0.15/0.04 | 0.10/0.20/0.10 | 5/4/5/**5** | 2 | 1 | 2.26 | 3.60 | 1.54 | +1 NE phonetic adjust applied (Karim's→Kareem's) |

Where consensus differs from per-backend, it's a 2/3 majority vote; on tied 1.5-rank cases (none observed here) we'd round.

### Backend disagreement worth noting

- **human_06** is the only clip with ≥2-rank ASR disagreement (AAI=1 vs DG=Groq=4). AAI's transcript drops "presentation" and "tomorrow" entirely, computing CER=0.67. Deepgram and Groq retain those words and compute CER=0.08–0.10. The 2/3 majority sides with the cleaner transcripts. **This is a useful signal in its own right:** AAI's Hindi-forced model is more brittle on dense code-switched audio than Deepgram or Groq.
- **`pure_roman` rows (human_03, human_04)** all collapse to intel=1 across every backend. This is not a "human pronunciation problem" — all three ASRs returned Devanagari transcripts that phonetically match the spoken audio (e.g. `कल मुझे ऑफिस जाना है।` for `kal mujhe office jaana hai`). The rubric scores `pure_roman` against `wer_roman`, which compares Devanagari-output to Roman-input → WER_rom=1.0. **The same artifact corrupts the 120-clip baseline's `pure_roman` intelligibility (Kokoro 1.25, IndicF5 1.00). The ceiling here confirms it's a scoring-pipeline issue, not a TTS issue.**

---

## Section 2 — The ceiling numbers

Per-column means + ranges from the 3-ASR consensus table.

| column | n=8 mean | range | notes |
|---|:---:|---|---|
| `intelligibility_1to5` | **3.25** | 1 – 5 | floored on `pure_roman` rows by the script-mismatch artifact |
| `naturalness_1to5` | **1.75** | 1 – 3 | this is the rubric's MOS ceiling on this audio source |
| `code_switch_handling_1to5` | **3.25** | 1 – 5 | mirrors intel for non-mixed rows per rubric |
| `speaker_quality_1to5` | **1.00** | 1 – 1 | every clip pegged at floor; PESQ floor activated for all 8 |
| `roman_treated_as_english` | 0/8 TRUE | — | as expected on human speech |
| `silence_or_skip` | 0/8 TRUE | — | all transcripts complete; no false-skip flagging |
| `end_of_clip_pop` | 3/8 TRUE | — | informative — see Section 5 caveat |

**These are upper bounds for the auto-scoring pipeline.** Any TTS clip the rubric scores above these should be inspected — it almost certainly reflects predictor drift, not TTS audio that is genuinely better than the human reference.

---

## Section 3 — Predictor drift quantified

### Raw MOS-predictor outputs (the underlying signal)

| predictor | human GT (n=8) | baseline (n=120) | Kokoro (n=30) | Parler (n=30) | IndicF5 (n=30) | SPRINGLab (n=30) | TTS-vs-human |
|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| UTMOS | **1.954** | 3.850 | 4.395 | 3.595 | 3.795 | 3.615 | **+1.90 (Kokoro: +2.44)** |
| SQUIM_MOS | **2.703** | 4.406 | 4.449 | 4.450 | 4.345 | 4.379 | **+1.70 (Kokoro: +1.75)** |
| SQUIM_PESQ | **1.617** | 3.824 | 3.858 | 3.775 | 3.847 | 3.817 | **+2.21 (Kokoro: +2.24)** |
| SQUIM_STOI | 0.940 | 0.995 | 0.997 | 0.995 | 0.992 | 0.994 | +0.06 |
| SQUIM_SISDR (dB) | 7.5 | 26.8 | 29.2 | 25.4 | 26.9 | 25.9 | +19.3 |

**The headline finding:** the predictors give every TTS model in the baseline a higher score than they give actual human Hindi speech, on three out of three perceptual quality measures (UTMOS, SQUIM_MOS, PESQ). UTMOS is the most-cited "naturalness" predictor in TTS papers — and it rates this human recording at 1.95 while rating Kokoro Hindi synthesis at 4.40. That's a 2.4-rank inversion. PESQ and SQUIM_MOS show the same direction.

STOI and SI-SDR show smaller gaps because they're objective intelligibility/SNR predictors, not naturalness — they're penalizing the recording's ambient SNR appropriately. UTMOS and SQUIM_MOS are the perceptual estimators making the wrong call.

### After-rubric scores (auto-scoring output)

| column | human GT | baseline mean | Kokoro | Parler | IndicF5 | SPRINGLab |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `intelligibility_1to5` | **3.25** | 2.42 | 3.03 | 2.73 | 1.97 | 1.93 |
| `naturalness_1to5` | **1.75** | 3.43 | **3.97** | 3.33 | 3.37 | 3.07 |
| `code_switch_handling_1to5` | **3.25** | 2.46 | 3.10 | 2.80 | 2.00 | 1.93 |
| `speaker_quality_1to5` | **1.00** | 4.19 | **4.27** | 4.00 | 4.27 | 4.23 |

- `intelligibility_1to5`: human GT (3.25) > baseline (2.42) > best TTS Kokoro (3.03). Direction is correct. Magnitude is reasonable. **This column is trustworthy.**
- `naturalness_1to5`: human GT (1.75) << baseline (3.43) << Kokoro (3.97). Direction is **inverted by 2.22 ranks**. The rubric's naturalness scoring is unusable on its own.
- `code_switch_handling_1to5`: same shape as intelligibility, since the rubric mirrors it on pure rows.
- `speaker_quality_1to5`: human GT (1.00) << every TTS model (≥4.00). Direction inverted by 3+ ranks. Either the predictor is broken, recording conditions dominate the signal, or both — unusable alone.

---

## Section 4 — Implications for rubric v2.0 (do not implement)

Three calibration strategies, with the trade-offs you'd be picking between:

### A. Cap-at-ceiling

Clip every auto-naturalness and speaker_quality score at the human-GT consensus mean (1.75 and 1.00 respectively).

- **Effect:** every TTS model gets pushed down to 1.75 nat / 1.00 spk. Rankings between models on these axes collapse. Cross-model differentiation on naturalness is lost; ranking comes entirely from intelligibility + flags + ad-hoc human listening.
- **Pro:** intellectually honest — refuses to claim numerical superiority you cannot defend against the ceiling.
- **Con:** you lose all per-model differentiation on the perceptual axes, which is exactly the thing fine-tuning would try to improve. Capping at the ceiling makes the rubric blind to genuine naturalness gains in v2.

### B. Subtract-the-bias

Compute `bias = expected_human_score − measured_human_GT_mean`. With expected=4.5 (typical clean-recording human MOS reference) and measured=1.75: bias = +2.75 ranks. Add this to every auto-score uniformly.

- **Effect:** Kokoro naturalness jumps from 3.97 to 6.72 (over the 1-5 scale ceiling). Need to either (a) cap at 5 after shifting, which is equivalent to "everyone scores 5," or (b) re-normalize via `(score - measured_mean) / (expected_mean - measured_mean) × 4 + 1`.
- **Pro:** preserves rank ordering between TTS models.
- **Con:** assumes a fixed "expected human MOS" of 4.5 that comes from the user's outside knowledge, not the data. With phone-mic recordings as ground truth (which this is), the assumption is fragile — you'd be shifting up by an amount that bakes in the assumption that the gap is *all* predictor drift, when ~half could be recording-condition noise (see Section 5).
- **Con:** if you re-record the ceiling with studio-grade audio, the bias number changes substantially, and so does every shifted score. The calibration is brittle to the ground-truth recording setup.

### C. Reweight (drop the broken signals)

Stop using UTMOS / SQUIM_MOS / SQUIM_PESQ as primary inputs to `naturalness_1to5` and `speaker_quality_1to5`. Score those columns from observable signals only:
- `naturalness_1to5` = 5 minus rank-penalties for: silence_mid_clip > 0.5 (-1), terminal_sample > 0.005 (-1), end_pop_db > 6 (-1), audible truncation flags from human spot-check (-1 to -2).
- `speaker_quality_1to5` = function of `terminal_sample_abs`, `end_pop_db`, and SQUIM_STOI (which the data shows is well-behaved: 0.94 human, 0.99 TTS — small gap, plausible direction).
- Lean harder on `intelligibility_1to5` for overall ranking — that column survives the ceiling test.

- **Pro:** removes the predictor drift entirely by removing the predictors. Aligns with what `SCORING_NOTES.md` already says ("UTMOS / SQUIM are English-trained — absolute MOS values drift on Hindi"). Doesn't require a known-good reference recording.
- **Pro:** if you later get a better Hindi-trained MOS predictor (e.g. UTMOSv2-Hindi, Indic-MOS), you can plug it back in.
- **Con:** the rubric becomes lossier — you can't distinguish "natural-sounding TTS" from "robotic-but-correct TTS" without listening. Naturalness becomes a flag-driven proxy, not a first-class score.
- **Con:** more invasive change to rubric v2 than (A); requires re-running the 120-clip judge.

### My read (you decide)

The data favors **(C) reweight**. The drift isn't a soft calibration bias — it's directional inversion (human < TTS on the predictor) on three distinct predictors. (A) is honest but blunt. (B) is fragile because it assumes the ground truth is at the predictor's "expected human" point, which it isn't (PESQ=1.6 means the predictor genuinely thinks this is bad audio, regardless of language). (C) accepts what the audit data is telling you: stop trying to use English-trained MOS predictors as if they generalized, and let intelligibility + DSP flags + human spot-checks do the work for naturalness in v2.

That said: you have project-context I don't (training-budget timeline, willingness to recompute the 120-clip baseline, whether a Hindi MOS predictor is plausibly available before fine-tune). Make the call.

---

## Section 5 — Caveats

1. **n=8 is small.** Two outliers move the mean by ~0.3 ranks. Sentence-level MOS variance was 1.51–2.26 (UTMOS), 2.31–3.60 (SQUIM_MOS) — these are ranges, not stable means. Re-recording 8 different sentences could shift the ceiling by ±0.4.

2. **Recording conditions are confounded with predictor drift.** The 8 clips were recorded as 224 kbps stereo mp3 at 44.1 kHz, transcoded by this pipeline to 24 kHz mono PCM. Likely a phone mic in a non-treated room (SI-SDR 7.5 dB suggests ~10 dB of ambient noise present). PESQ is sensitive to ambient SNR and band-limited microphones; some of the 1.6-PESQ result is genuinely the predictor identifying microphone limitations, not "Hindi naturalness drift." We cannot fully separate the two effects with this data. **If you want a tighter ceiling, re-record on a USB condenser mic in a quiet room and re-run.** I'd expect that to lift PESQ by maybe 0.5–1.0 and UTMOS by ~0.3–0.5 — which would *narrow* the drift gap but not close it (Kokoro is ~+2.4 ranks above current; even a +1.0 lift in human ground truth still leaves a 1.4-rank inversion).

3. **The ceiling is rubric-version-specific.** Recomputed against a different scoring rubric (e.g. v2 with reweighted MOS), the ceiling numbers shift. **Re-run this script (`audit/scripts/human_gt/`) on the same 8 clips after any rubric change.** The wavs and signal vectors are immutable; only the judge step needs to be re-executed.

4. **`pure_roman` rows are diagnostically useless for the ceiling.** The rubric's intel scoring on `pure_roman` collapses across all three ASRs because every backend returns Devanagari transcripts of phonetically-correct Hindi-mode speech, and `wer_roman` compares them against Roman ground truth → WER=1.0, intel=1. This affects both human GT (intel=1 for 2/8 clips) and the 120-clip baseline (Kokoro pure_roman mean=1.25). **The pure_roman intelligibility numbers in the audit do not measure pronunciation quality — they measure script-mismatch.** This is a known issue in `SCORING_NOTES.md`; the ceiling confirms it independently.

5. **Speaker_quality is degenerate on this set.** All 8 clips peg at 1 because PESQ < 2.5 across the board. The column has zero discriminating power on this audio source. Either re-record cleaner (per caveat 2) to lift PESQ above the floor, or accept that this column is unusable in the human-GT comparison.

6. **3/8 `end_of_clip_pop` flags is high but not all are true positives.** The rubric requires `end_pop_db > 6 AND terminal_sample_abs > 0.005`. For most flagged clips here, end_pop_db>6 fired but terminal was at the threshold or below — these may be the natural fadeout of a sentence, not actual pops. Spot-check by listening if you care about this column for v2.

7. **Backend choice for the canonical ceiling.** The three ASRs give different intelligibility scores on 1/8 clips (human_06, range=3). Consensus uses majority vote, which sided with the cleaner transcripts (Deepgram and Groq) over the brittle one (AAI). If you'd like a per-backend ceiling instead of consensus, the per-backend mean intelligibility is: AAI=2.88, Deepgram=3.12, Groq=3.00 — within 0.25 of each other. Naturalness and speaker_quality are identical across backends (they don't depend on ASR).

---

## Files

```
audit/human_groundtruth/
├── wavs/                              # 24 kHz mono PCM, transcoded from mp3
│   ├── human_01.wav  …  human_08.wav
├── validation_report.csv              # native SR, peak, silence%, durations
├── wav_to_sentence.csv                # filename → sentence_id mapping (8 rows)
├── signal_vectors_aai.json            # Stage 1, AssemblyAI ASR
├── signal_vectors_deepgram.json       # Stage 1, Deepgram ASR
├── signal_vectors_groq.json           # Stage 1, Groq Whisper ASR
├── judge_batches_<aai|dg|groq>/       # Stage 2 inputs (1 batch × 8 clips each)
├── judge_responses_<aai|dg|groq>/     # Stage 2 outputs (per-backend judges)
├── auto_scores_aai.csv                # Stage 2, per-backend
├── auto_scores_deepgram.csv
├── auto_scores_groq.csv
├── auto_scores_consensus.csv          # 3-ASR majority vote
└── CEILING_REPORT.md                  # this file
```

To reproduce:

```bash
source venv-scoring/bin/activate
python audit/scripts/human_gt/validate_and_transcode.py
python audit/scripts/human_gt/build_mapping.py
python audit/scripts/human_gt/extract_signals_human.py    # 3.5 min
python audit/scripts/human_gt/judge_human.py --emit-batches
# (Claude judges each of 3 batches via Agent tool — see this report's Stage 2 prompts)
python audit/scripts/human_gt/judge_human.py --collect
python audit/scripts/human_gt/consensus_and_summary.py
```
