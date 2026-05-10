# Auto-Scores — Hinglish TTS Audit (2026-05-08)

Auto-scored by Claude as judge over signal vectors extracted by `extract_signals.py`. 
Rubric: `JUDGE_PROMPT.md` v1.0. Caveats and override workflow: `SCORING_NOTES.md`.

## Per-model summary

| Model | Intel | Nat | Code-switch | Speaker | Silent flags | Pop flags | Anglic flags |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Kokoro** | 3.03 | 3.97 | 3.10 | 4.27 | 2/30 | 0/30 | 0/30 |
| **Indic Parler-TTS** | 2.73 | 3.33 | 2.80 | 4.00 | 4/30 | 4/30 | 0/30 |
| **IndicF5** | 1.97 | 3.37 | 2.00 | 4.27 | 21/30 | 2/30 | 0/30 |
| **SPRINGLab F5-Hindi** | 1.93 | 3.07 | 1.93 | 4.23 | 21/30 | 0/30 | 0/30 |

## Per-category mean intelligibility

| Model | pure devanagari | pure roman | mixed script | english with NE |
|---|:---:|:---:|:---:|:---:|
| **Kokoro** | 4.88 | 1.25 | 1.50 | 5.00 |
| **Indic Parler-TTS** | 4.00 | 1.12 | 1.50 | 4.83 |
| **IndicF5** | 4.38 | 1.00 | 1.25 | 1.00 |
| **SPRINGLab F5-Hindi** | 4.25 | 1.00 | 1.25 | 1.00 |

## Per-sentence comparison (4 models × 30 sentences)

Each section: ground-truth text, category, phenomenon tag, then 4-model side-by-side scoring. 
Flags column legend: 🚩 = TRUE, · = FALSE. Order: Silent | Pop | Anglic.

### 01 — `pure_devanagari` / baseline_devanagari

> कल मुझे दिल्ली जाना है।

_Expected: Standard Hindi declarative._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 5 | 4 | 5 | 4 | ··· | CER=0.0 (perfect Devanagari) + UTMOS=4.37, SQUIM_MOS=4.45 (mean=4.41) + PESQ=3.63 + silence_mid=0.42<0.5 + end_pop_db=-0.56 (no flags). |
| Indic Parler-TTS | 5 | 3 | 5 | 4 | 🚩·· | CER=0.0455 (≤0.05) → intel=5; UTMOS=3.96 + SQUIM_MOS=4.46 (mean=4.21→4) but silence_mid=0.52>0.5 dropped naturalness 1 rank to 3 and triggered silence_or_skip=TRUE; PESQ=3.67 → spk=4; end_pop_db=14.41 but terminal=0.0... |
| IndicF5 | 1 | 3 | 1 | 4 | 🚩·· | transcript_hi empty → CER=1.0 → intel=1 and silence_or_skip=TRUE (>20% words missing); UTMOS=3.80 + SQUIM_MOS=4.46 (mean=4.13→4) dropped 1 rank for truncation → nat=3; PESQ=3.61 → spk=4; end_pop_db=-1.49 → no pop. |
| SPRINGLab F5-Hindi | 1 | 3 | 1 | 5 | 🚩·· | transcript_hi empty → CER=1.0 → intel=1 and silence_or_skip=TRUE; UTMOS=3.83 + SQUIM_MOS=4.13 (mean=3.98→4) dropped 1 rank for truncation → nat=3; PESQ=4.09 → spk=5; end_pop_db=-67.49 → no pop. |

### 02 — `pure_devanagari` / question_devanagari

> क्या आप मुझे पानी दे सकते हैं?

_Expected: Polite Hindi question._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 5 | 4 | 5 | 4 | ··· | CER=0.0 → intel=5; UTMOS=4.42 + SQUIM_MOS=4.46 (mean=4.44→4); PESQ=3.71 → spk=4; silence_mid=0.38<0.5 + end_pop_db=-17.55 (no flags). |
| Indic Parler-TTS | 1 | 2 | 1 | 4 | 🚩·· | transcript_hi empty → CER=1.0 → intel=1 and silence_or_skip=TRUE; UTMOS=3.54 + SQUIM_MOS=4.44 disagree by 0.90>0.7 (mean=3.99→4) dropped 1 for uncertainty + 1 for truncation → nat=2; PESQ=3.93 → spk=4; end_pop_db=9.2 ... |
| IndicF5 | 5 | 4 | 5 | 5 | ··· | CER=0.0 → intel=5; UTMOS=4.26 + SQUIM_MOS=4.46 (mean=4.36→4); PESQ=4.23 → spk=5; end_pop_db=9.9 but terminal=0.0<0.005 → no pop; silence_mid=0.26<0.5. |
| SPRINGLab F5-Hindi | 5 | 3 | 5 | 5 | ··· | CER=0.0 → intel=5; UTMOS=3.40 + SQUIM_MOS=4.46 disagree by 1.06>0.7 (mean=3.93→4) dropped 1 for uncertainty → nat=3; PESQ=4.09 → spk=5; end_pop_db=-70.34 → no pop. |

### 03 — `pure_devanagari` / loanword_in_devanagari

> मेरा भाई आज स्कूल नहीं गया क्योंकि उसकी तबीयत खराब है।

_Expected: Long Hindi sentence with English loanword \"स्कूल\" written in Devanagari._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 5 | 4 | 5 | 4 | ··· | CER=0.0 (loanword स्कूल rendered cleanly) + UTMOS=4.42 + SQUIM_MOS=4.46 (mean=4.44→4); PESQ=3.97 → spk=4; silence_mid=0.44<0.5 + end_pop_db=2.3 (no flags). |
| Indic Parler-TTS | 5 | 3 | 5 | 3 | ··· | CER=0.0189 → intel=5; UTMOS=3.54 + SQUIM_MOS=4.45 disagree by 0.91>0.7 (mean=3.99→4) dropped 1 for uncertainty → nat=3; PESQ=3.39 → spk=3; end_pop_db=15.08 but terminal=0.0031<0.005 → no pop; silence_mid=0.22<0.5. |
| IndicF5 | 5 | 4 | 5 | 4 | ··· | CER=0.0 + UTMOS=4.25 + SQUIM_MOS=4.46 -> clean Devanagari rendering; PESQ=3.71 -> speaker_quality=4; end_pop_db=8.72 but terminal=0.0038<0.005 so no pop flag. |
| SPRINGLab F5-Hindi | 5 | 4 | 5 | 4 | ··· | CER=0.0189 + UTMOS=4.22 + SQUIM_MOS=4.45 -> near-perfect Devanagari; PESQ=3.99 -> speaker_quality=4; end_pop_db=-69.81 (silent tail), no pop. |

### 04 — `pure_devanagari` / numbers_devanagari

> मेरे पास सिर्फ़ तीन सौ रुपये हैं, बस इतने में चला लो।

_Expected: Numerals expressed in Devanagari words; casual register._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 4 | 4 | 4 | 4 | ··· | CER=0.1961 mostly from ASR rewriting 'तीन सौ' as '300' (phonetic-not-wrong, +1 adjust); UTMOS=4.41 + SQUIM_MOS=4.45 -> naturalness=4; PESQ=3.73 -> 4; end_pop_db=2.16 clean. |
| Indic Parler-TTS | 3 | 4 | 3 | 4 | ··· | CER=0.2941 -> 3; numeral substitution offset by 'चल लो' vs 'चला लो' real miss; UTMOS=3.95 + SQUIM_MOS=4.46 mean=4.2; PESQ=3.95 -> 4; end_pop_db=6.18 but terminal=0.0034<0.005 no pop. |
| IndicF5 | 4 | 4 | 4 | 5 | ··· | CER=0.2745 mainly from ASR rendering 'तीन सौ' as '₹300' (phonetic-not-wrong, +1 adjust); UTMOS=4.04 + SQUIM_MOS=4.46 -> 4; PESQ=4.17 -> 5; end_pop_db=2.97 clean. |
| SPRINGLab F5-Hindi | 3 | 4 | 3 | 5 | ··· | CER=0.3137 -> base 2; numeral substitution + 'लूं' vs 'लो' minor (+1 phonetic adjust) -> 3; UTMOS=3.96 + SQUIM_MOS=4.15 mean=4.05; PESQ=4.07 -> 5; end_pop_db=-73.93 silent tail. |

### 05 — `pure_devanagari` / imperative_devanagari

> जल्दी आओ यार, सब तेरा इंतज़ार कर रहे हैं।

_Expected: Casual imperative with informal pronoun \"तेरा\"._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 5 | 4 | 5 | 4 | ··· | CER=0.0256 -> crystal-clear Devanagari; UTMOS=4.38 + SQUIM_MOS=4.45 mean=4.41 -> 4; PESQ=3.81 -> 4; end_pop_db=2.41 clean. |
| Indic Parler-TTS | 5 | 3 | 5 | 4 | ··· | CER=0.0256 -> intelligibility=5; UTMOS=3.49 vs SQUIM_MOS=4.47 diff=0.98>0.7 -> drop one rank to 3; PESQ=3.77 -> 4; end_pop_db=11.4 but terminal=0.0017<0.005 no pop. |
| IndicF5 | 5 | 4 | 5 | 5 | ··· | CER=0.0256 -> 5; UTMOS=3.83 + SQUIM_MOS=4.45 diff=0.62<0.7 mean=4.14 -> 4; PESQ=4.21 -> 5; end_pop_db=-29 silent tail. |
| SPRINGLab F5-Hindi | 5 | 3 | 5 | 4 | ··· | CER=0.0256 -> 5; UTMOS=2.97 vs SQUIM_MOS=4.44 diff=1.47>0.7 -> drop one rank from mean 3.7 to 3; PESQ=3.80 -> 4; end_pop_db=-73.27 silent tail. |

### 06 — `pure_devanagari` / baseline_devanagari

> आज बहुत थक गया हूँ, बस सीधा सोना चाहता हूँ।

_Expected: Casual declarative; common contraction \"सीधा\"._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 5 | 4 | 5 | 5 | ··· | CER=0.0 (perfect Devanagari) + UTMOS=4.18, SQUIM_MOS=4.42 (mean=4.30) + PESQ=4.01; silence_mid=0.4 and end_pop=2.39 below thresholds. |
| Indic Parler-TTS | 5 | 3 | 5 | 4 | ··· | CER=0.0488 (still <=0.05 anchor, hu->ho is schwa-level) + UTMOS=3.48 vs SQUIM_MOS=4.45 disagree by 0.97>0.7 so naturalness dropped to 3; PESQ=3.90. |
| IndicF5 | 5 | 4 | 5 | 4 | ··· | CER=0.0 + UTMOS=4.14, SQUIM_MOS=4.47 (mean=4.30) + PESQ=3.79; end_pop=9.59 but terminal_sample_abs=0.0 (<0.005) so no pop flag. |
| SPRINGLab F5-Hindi | 5 | 4 | 5 | 4 | ··· | CER=0.0 + UTMOS=3.64, SQUIM_MOS=4.33 (mean=3.98, disagree=0.70 not >0.7) -> 4; PESQ=3.94; end_pop=-68.92 clean. |

### 07 — `pure_devanagari` / question_devanagari

> तुझे पता है कल मीटिंग कितने बजे है?

_Expected: Informal question; \"मीटिंग\" is an English loanword in Devanagari._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 5 | 4 | 5 | 4 | ··· | CER=0.0 (perfect rendering of Devanagari question) + UTMOS=4.33, SQUIM_MOS=4.46 (mean=4.39) + PESQ=3.82; no DSP flags. |
| Indic Parler-TTS | 5 | 4 | 5 | 5 | ··· | CER=0.0 + UTMOS=3.80, SQUIM_MOS=4.44 (mean=4.12, diff=0.64<0.7) -> 4; PESQ=4.00 -> 5; end_pop=11.79 but terminal=0.0043<0.005 so no pop flag. |
| IndicF5 | 5 | 4 | 5 | 5 | ··· | CER=0.0294 (he->hain trivial) + UTMOS=3.99, SQUIM_MOS=4.45 (mean=4.22) + PESQ=4.16; clean DSP. |
| SPRINGLab F5-Hindi | 5 | 4 | 5 | 5 | ··· | CER=0.0 + UTMOS=3.95, SQUIM_MOS=4.45 (mean=4.20, diff=0.50<0.7) + PESQ=4.21; end_pop=-68.67 very clean. |

### 08 — `pure_devanagari` / imperative_devanagari

> अरे यार, मेरा फ़ोन कहाँ रखा था?!

_Expected: Exclamative question; everyday casual reaction._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 5 | 4 | 5 | 5 | ··· | CER=0.0 + UTMOS=4.40, SQUIM_MOS=4.46 (mean=4.43) + PESQ=4.00; end_pop=-18.9 clean, no flags. |
| Indic Parler-TTS | 3 | 3 | 3 | 4 | ··· | CER=0.2069 (yaar dropped, 1 of 7 words ~14% so under 20% skip threshold) -> 3; UTMOS=3.52 vs SQUIM_MOS=4.48 disagree by 0.96>0.7 so naturalness 4->3; PESQ=3.56; end_pop=7.46 but terminal=0.0001<0.005 so no pop flag. |
| IndicF5 | 5 | 4 | 5 | 4 | ··· | CER=0.0345 (clean Devanagari) + UTMOS=4.254 + SQUIM_MOS=4.45 (mean=4.35); SQUIM_PESQ=3.884 -> rank 4; end_pop_db=13.62 but terminal=0.0007 (<0.005) so no pop flag. |
| SPRINGLab F5-Hindi | 5 | 4 | 5 | 4 | ··· | CER=0.0 (perfect Devanagari) + UTMOS=3.985 + SQUIM_MOS=4.443 (mean=4.21, disagree<0.7); SQUIM_PESQ=3.429 -> rank 4; end_pop_db=-68.22 (silent tail). |

### 09 — `pure_roman` / roman_hindi_with_english_loan

> kal mujhe office jaana hai

_Expected: Should sound Hindi, NOT English. \"office\" is the only English word._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 1 | 4 | 1 | 4 | ··· | WER_rom=1.0 and WER_en_forced=0.6 (gap=0.4 but en_forced>0.30) -> not anglicized, just garbled; UTMOS=4.401 + SQUIM_MOS=4.45 (mean=4.43) -> rank 4 naturalness; SQUIM_PESQ=3.842 -> rank 4. |
| Indic Parler-TTS | 1 | 4 | 1 | 4 | ··· | WER_rom=0.8 and WER_en_forced=0.8 (no gap) -> not clearly anglicized; UTMOS=3.965 + SQUIM_MOS=4.429 (mean=4.20, disagree<0.7) -> rank 4; SQUIM_PESQ=3.761 -> rank 4; end_pop_db=11.51 but terminal=0.0007 so no pop flag. |
| IndicF5 | 1 | 3 | 1 | 4 | 🚩·· | duration=0.779s (severely truncated, transcript='Ranai.') -> >20% words missing, silence_or_skip=TRUE; WER_rom=WER_en=1.0; UTMOS=3.293 + SQUIM_MOS=3.859 (mean=3.58) -> rank 4 minus 1 for truncation = 3; SQUIM_PESQ=3.5... |
| SPRINGLab F5-Hindi | 1 | 3 | 1 | 3 | 🚩·· | duration=0.779s (truncated, transcript='Ava.') -> silence_or_skip=TRUE; WER_rom=WER_en=1.0; UTMOS=3.59 + SQUIM_MOS=4.608 (disagree>0.7, mean=4.10 -> rank 4 minus 1 uncertainty minus 1 truncation = 3, but floor at sens... |

### 10 — `pure_roman` / homograph_hai_hi

> mera naam Arjun hai aur mai Bengaluru se hu

_Expected: \"hai\" is Hindi \"is\", NOT \"hi\" greeting. \"Bengaluru\" must be pronounced Indian, not anglicized._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 1 | 4 | 1 | 4 | ··· | WER_rom=1.0 and WER_en_forced=1.0 (no anglicization gap); UTMOS=4.398 + SQUIM_MOS=4.458 (mean=4.43) -> rank 4; SQUIM_PESQ=3.92 -> rank 4; silence_mid_clip=0.42 (under 0.5). |
| Indic Parler-TTS | 1 | 4 | 1 | 3 | ··· | WER_rom=1.0, WER_en_forced=1.0 (no gap, garbled both ways); UTMOS=3.154 + SQUIM_MOS=4.389 (disagree>0.7, mean=3.77 -> rank 4 minus 1 uncertainty = 3, but rounded mean=4 -> 3 after penalty; using mean rank 4 then -1 = ... |
| IndicF5 | 1 | 3 | 1 | 4 | 🚩·· | duration=1.291s vs expected ~4s (severe truncation, transcript='Or when a muruho.') -> silence_or_skip=TRUE; WER_rom=WER_en=1.0; UTMOS=3.27 + SQUIM_MOS=4.365 (disagree>0.7, mean=3.82 -> rank 4 minus 1 uncertainty minu... |
| SPRINGLab F5-Hindi | 1 | 3 | 1 | 4 | 🚩·· | duration=1.291s (truncated, transcript_roman empty, en_forced='Or agahava.') -> silence_or_skip=TRUE; WER_rom=WER_en=1.0; UTMOS=4.108 + SQUIM_MOS=4.445 (mean=4.28) -> rank 4 minus 1 truncation = 3; SQUIM_PESQ=3.938 ->... |

### 11 — `pure_roman` / casual_roman_hindi

> yaar tu kal kya kar raha tha

_Expected: Casual Hinglish, common words yaar/tu/kya._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 1 | 4 | 1 | 5 | ··· | WER_rom=1.0 (transcript is Devanagari garble of Roman input) -> intel=1; UTMOS=4.31 + SQUIM_MOS=4.46 -> nat=4; PESQ=4.02 -> spk=5; wer_en_forced=1.0 so not anglicized; silence=0.38<0.5, end_pop=-8.69 -> no DSP flags. |
| Indic Parler-TTS | 1 | 3 | 1 | 4 | ··· | WER_rom=0.71 -> intel=1; UTMOS=3.29 vs SQUIM_MOS=4.44 disagree by 1.15>0.7 -> mean=3.86 dropped 1 = nat=3; PESQ=3.64 -> spk=4; wer_en_forced=0.71 not <0.30 so anglicization=FALSE; end_pop=23.4 but terminal=0.0019<0.00... |
| IndicF5 | 1 | 3 | 1 | 2 | 🚩·· | duration=0.83s with empty transcript_hi -> skip flagged (>20% words missing); WER_rom=1.0 -> intel=1; UTMOS=2.93 vs SQUIM_MOS=4.57 diff 1.64>0.7 -> mean 3.75 dropped 1 = nat=3; PESQ=2.94 -> spk=2; wer_en_forced=1.0 ->... |
| SPRINGLab F5-Hindi | 1 | 3 | 1 | 4 | 🚩·· | duration=0.83s with near-empty transcripts ('Or vava.') -> skip flagged; WER_rom=1.0 -> intel=1; UTMOS=3.45 vs SQUIM_MOS=4.44 diff 0.98>0.7 -> mean 3.94 dropped 1 = nat=3; PESQ=3.67 -> spk=4; wer_en_forced=1.0 -> not ... |

### 12 — `pure_roman` / roman_question

> kya tu bhi aaj party me aa raha hai?

_Expected: Roman-script Hindi question with English loan \"party\"._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 1 | 4 | 1 | 4 | ··· | WER_rom=1.0 (Devanagari garble of Roman input) -> intel=1; UTMOS=4.24 + SQUIM_MOS=4.45 mean=4.34 -> nat=4; PESQ=3.82 -> spk=4; wer_en_forced=1.0 -> not anglicized; silence=0.4<0.5, end_pop=1.91 -> no flags. |
| Indic Parler-TTS | 1 | 3 | 1 | 5 | ··· | WER_rom=1.0 -> intel=1; UTMOS=3.60 vs SQUIM_MOS=4.46 diff 0.86>0.7 -> mean 4.03 dropped 1 = nat=3; PESQ=4.10 -> spk=5; wer_en_forced=1.0 not <0.30 -> anglicization=FALSE; end_pop=14.57 but terminal=0.0012<0.005 -> no ... |
| IndicF5 | 1 | 2 | 1 | 4 | 🚩·· | duration=1.08s with empty transcript_hi ('Heo rawai.') -> skip flagged; WER_rom=1.0 -> intel=1; UTMOS=3.08 vs SQUIM_MOS=4.39 diff 1.31>0.7 -> mean 3.73 dropped 1 + drop 1 for skip = nat=2; PESQ=3.78 -> spk=4; wer_en_f... |
| SPRINGLab F5-Hindi | 1 | 2 | 1 | 3 | 🚩·· | duration=1.08s with empty/Thai transcript ('Or.') -> skip flagged; WER_rom=1.0 -> intel=1; UTMOS=3.23 vs SQUIM_MOS=4.23 diff 1.0>0.7 -> mean 3.73 dropped 1 + drop 1 for skip = nat=2; PESQ=3.23 -> spk=3; wer_en_forced=... |

### 13 — `pure_roman` / roman_imperative

> abe yaar jaldi reply kar, mai wait kar raha hu

_Expected: Roman-Hindi imperative; \"reply\" and \"wait\" must NOT be re-anglicized in pronunciation._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 1 | 4 | 1 | 5 | ··· | WER_rom=1.0 (Devanagari rendering of Roman input with reply/wait re-anglicized) -> intel=1; UTMOS=4.49 + SQUIM_MOS=4.45 mean=4.47 -> nat=4; PESQ=4.15 -> spk=5; wer_en_forced=0.8 not <0.30 so anglicization=FALSE; silen... |
| Indic Parler-TTS | 1 | 3 | 1 | 4 | ··· | WER_rom=1.0 -> intel=1; UTMOS=2.66 vs SQUIM_MOS=4.42 diff 1.76>0.7 -> mean 3.54 dropped 1 = nat=3; PESQ=3.84 -> spk=4; wer_en_forced=1.0 -> not anglicized; end_pop=12.89 but terminal=0.0025<0.005 -> no pop. |
| IndicF5 | 1 | 3 | 1 | 4 | 🚩·· | WER_rom=1.0, transcript empty + duration 1.39s for long sentence -> skip; UTMOS=3.735, SQUIM_MOS=4.317, PESQ=3.607; end_pop_db=11.62 but terminal=0.0 so no pop. |
| SPRINGLab F5-Hindi | 1 | 2 | 1 | 4 | 🚩·· | WER_rom=1.0, transcript 'A hut of agraha' garbled + duration 1.39s skip; UTMOS=3.349 vs SQUIM_MOS=4.448 (diff=1.1>0.7 uncertainty drop) plus skip drop; PESQ=3.834. |

### 14 — `pure_roman` / casual_roman_hindi

> kal raat ka movie tha bohot bakwaas, paisa bilkul waste

_Expected: Casual film reaction; multiple English loans inside Roman-Hindi._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 2 | 4 | 2 | 4 | ··· | WER_rom=1.1 (Roman rendered as Devanagari transcript) + WER_en=0.8; +1 adjust for phonetic ASR confusion since transcript_hi covers most words; UTMOS=4.39, SQUIM_MOS=4.463, PESQ=3.817. |
| Indic Parler-TTS | 1 | 3 | 1 | 3 | ··· | WER_rom=0.9, WER_en=0.9 -> mostly wrong; UTMOS=3.0 vs SQUIM_MOS=4.476 (diff=1.48>0.7 uncertainty drop); PESQ=3.276; end_pop_db=9.77 but terminal=0.0023<0.005. |
| IndicF5 | 1 | 3 | 1 | 4 | 🚩·· | WER_rom=1.0, transcript 'Haluas hassa village' + duration 1.66s for long sentence -> skip; UTMOS=4.206, SQUIM_MOS=4.481, PESQ=3.761; end_pop_db=8.81 but terminal=0.0004. |
| SPRINGLab F5-Hindi | 1 | 3 | 1 | 4 | 🚩·· | WER_rom=1.0, transcript empty + duration 1.66s skip; UTMOS=3.842, SQUIM_MOS=4.297 (mean=4.07, diff=0.45); PESQ=3.857; end_pop_db=-68.15 -> no pop. |

### 15 — `pure_roman` / roman_hindi_with_english_loan

> tera laptop kab tak deliver hoga bhai?

_Expected: Roman-Hindi question with English nouns \"laptop\" / \"deliver\"._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 2 | 4 | 2 | 5 | ··· | WER_rom=0.5714, WER_en=0.5714; +1 adjust since transcript 'Terra laptop cab Tac deliver Hoga buy' covers all expected words phonetically; UTMOS=4.268, SQUIM_MOS=4.448, PESQ=4.153. |
| Indic Parler-TTS | 2 | 3 | 2 | 5 | ··· | WER_rom=1.0 but transcript 'Karen laptop cab dag dag deliver hook up high' has key words; UTMOS=3.724 vs SQUIM_MOS=4.448 (diff=0.72>0.7 uncertainty drop); PESQ=4.087. |
| IndicF5 | 1 | 3 | 1 | 5 | 🚩·· | WER_rom=1.0, transcript 'Chaivrahangarai' + duration 1.14s for long sentence -> severe skip; UTMOS=4.02, SQUIM_MOS=4.238, PESQ=4.079; end_pop_db=8.05 but terminal=0.0016<0.005. |
| SPRINGLab F5-Hindi | 1 | 1 | 1 | 4 | 🚩·· | WER_rom=1.0, transcript 'Oh' + duration 1.14s severe skip; UTMOS=2.527 vs SQUIM_MOS=3.746 (diff=1.22>0.7 uncertainty drop) plus skip drop; PESQ=3.671. |

### 16 — `pure_roman` / casual_roman_hindi

> yaar tu bohot lucky hai, mujhe nahi mila ticket!

_Expected: Casual exclamation; \"hai\" must read as Hindi \"is\", not \"hi\"._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 1 | 4 | 1 | 4 | ··· | WER_rom=1.0 (Roman fully misrendered to Devanagari mush) → intel=1; UTMOS=4.42 + SQUIM_MOS=4.44 mean=4.43 → nat=4; PESQ=3.96 → speaker=4; wer_en_forced=0.67 not <0.30 so anglicization=FALSE. |
| Indic Parler-TTS | 1 | 3 | 1 | 4 | ·🚩· | WER_rom=0.67 (>0.5) → intel=1; UTMOS=3.20 vs SQUIM_MOS=4.44 disagree by 1.24>0.7 → nat dropped from 4 to 3; PESQ=3.50 → speaker=4; end_pop_db=7.25 + terminal=0.0058 → pop=TRUE. |
| IndicF5 | 1 | 3 | 1 | 5 | 🚩·· | duration=1.45s with empty transcript_roman (skip) → silence_or_skip=TRUE, intel=1, WER_rom=1.0; UTMOS=4.15 + SQUIM_MOS=4.26 mean=4.20→4 minus 1 for skip=3; PESQ=4.06 → speaker=5; terminal=0.0 so no pop. |
| SPRINGLab F5-Hindi | 1 | 2 | 1 | 3 | 🚩·· | duration=1.45s with empty transcript (skip) → silence_or_skip=TRUE, WER_rom=1.0 → intel=1; UTMOS=3.73 vs SQUIM_MOS=4.47 disagree by 0.74>0.7 mean=4.10→4 minus 1 disagree minus 1 skip → nat=2; PESQ=3.40 → speaker=3. |

### 17 — `mixed_script` / mixed_script_hard

> Kal mujhe ऑफिस जाना hai, but ट्राफिक will be an issue.

_Expected: The hardest case — script switches mid-sentence._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 1 | 4 | 2 | 4 | ··· | CER=0.558 (>0.5) on Devanagari-leaning mixed → intel=1; English tokens rendered as Devanagari transliteration ('विल बी इन इशू') so code_switch=2; UTMOS=4.38 + SQUIM_MOS=4.46 mean=4.42 → nat=4; PESQ=3.56 → speaker=4; w... |
| Indic Parler-TTS | 1 | 4 | 2 | 4 | ·🚩· | CER=0.519 → intel=1; WER_rom=0.55 with detected_lang=en, English chunks rendered but Hindi 'mujhe' dropped → code_switch=2; UTMOS=3.81 + SQUIM_MOS=4.46 mean=4.14 → nat=4; PESQ=3.64 → speaker=4; end_pop_db=15.04 + term... |
| IndicF5 | 1 | 3 | 2 | 4 | 🚩·· | Transcript 'ऑफिस जाना है। आर ट्रैफिक ओइन।' missing 'Kal mujhe', 'but', 'will be an issue' (>20% missed) → skip=TRUE, CER=0.635 → intel=1; UTMOS=4.10 + SQUIM_MOS=4.44 mean=4.27→4 minus 1 for skip → nat=3; PESQ=3.90 → s... |
| SPRINGLab F5-Hindi | 1 | 3 | 1 | 4 | 🚩·· | Transcript 'जाना और ट्रैफिक और होगा।' missing >50% of source tokens → skip=TRUE, CER=0.731 → intel=1; severe content loss on mixed input → code_switch=1; UTMOS=4.14 + SQUIM_MOS=4.45 mean=4.29→4 minus 1 skip → nat=3; P... |

### 18 — `mixed_script` / mixed_script_grammar

> Mera presentation tomorrow है, और मैं nervous हूं।

_Expected: Hindi grammar around English content words._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 1 | 4 | 2 | 4 | ··· | CER=0.667 (>0.5) → intel=1, but transcript covers all source words ('मीर प्रेजेंटेशन तमारु है और मैं नर्वस हूँ') so content present → code_switch=2; UTMOS=4.45 + SQUIM_MOS=4.47 mean=4.46 → nat=4; PESQ=3.97 → speaker=4... |
| Indic Parler-TTS | 2 | 4 | 3 | 4 | ··· | CER=0.458 (0.30<CER≤0.50) → intel=2; full content present in transcript with reasonable mixed handling → code_switch=3; UTMOS=3.98 + SQUIM_MOS=4.47 mean=4.23 → nat=4; PESQ=3.78 → speaker=4; end_pop_db=8.29 but termina... |
| IndicF5 | 1 | 3 | 1 | 3 | 🚩·· | CER=0.71, WER_rom=0.625 (transcript drops 'presentation', 'tomorrow', 'nervous'); UTMOS=2.98 vs SQUIM_MOS=4.44 disagree>0.7 so naturalness mean rounded then -1; PESQ=3.04; transcript missing >20% of expected words so ... |
| SPRINGLab F5-Hindi | 1 | 3 | 1 | 4 | 🚩·· | CER=0.67, WER_rom=0.625 (English content words 'presentation/tomorrow/nervous' missing); UTMOS=3.23 vs SQUIM_MOS=4.47 disagree>0.7 → -1 penalty; PESQ=3.62; WER_en=1.0 not better than WER_rom; end_pop_db=-74 clean. |

### 19 — `mixed_script` / mixed_script_currency

> Bhai please मेरा homework कर दे, मैं तुझे ₹100 दूंगा।

_Expected: Currency symbol + Devanagari numerals/script switch._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 2 | 4 | 2 | 5 | ··· | CER=0.37, WER_rom=0.4 → ~half clear; UTMOS=4.42 + SQUIM_MOS=4.46 mean=4.44; PESQ=4.02 ≥4.0 → speaker=5; WER_en=0.8 not better than WER_rom=0.4 so FALSE; silence_mid=0.42<0.5. |
| Indic Parler-TTS | 1 | 4 | 1 | 4 | 🚩🚩· | CER=0.53, WER_rom=1.0 → mostly wrong; UTMOS=3.87 + SQUIM_MOS=4.44 mean=4.16; PESQ=3.76; WER_en=1.0 equal to WER_rom; end_pop_db=11.07 + terminal=0.0054>0.005 → pop TRUE; transcript clearly missing >20% words. |
| IndicF5 | 2 | 3 | 2 | 5 | ··· | CER=0.45, WER_rom=0.4 → half-intelligible; UTMOS=3.65 vs SQUIM_MOS=4.46 disagree>0.7 → mean 4.05 -1 = 3; PESQ=4.05 ≥4.0; WER_en=1.0 not better; end_pop=8.3 but terminal=0.0027<0.005 → no pop. |
| SPRINGLab F5-Hindi | 2 | 4 | 2 | 4 | ··· | CER=0.45, WER_rom=0.4 → half intelligible (homework→'अलग'); UTMOS=3.60 + SQUIM_MOS=4.19 mean=3.9; PESQ=3.89; end_pop_db=-71 clean; WER_en=1.0 not better. |

### 20 — `mixed_script` / mixed_script_question

> Tumne वो new restaurant try kiya jo Connaught Place में khula hai?

_Expected: Mid-sentence script switch with question intonation._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 1 | 4 | 1 | 5 | ··· | CER=0.78, WER_rom=0.83 → mostly wrong (Tumne→टमनी, hai→हाए); UTMOS=4.43 + SQUIM_MOS=4.46 mean=4.45; PESQ=4.10 ≥4.0; WER_en=0.83 equal to WER_rom; end_pop=2.34 below threshold. |
| Indic Parler-TTS | 2 | 3 | 2 | 4 | 🚩·· | CER=0.46, WER_rom=0.75 → about half-wrong (multiple words dropped: 'Tumne','new','Connaught'); UTMOS=3.50 vs SQUIM_MOS=4.46 disagree>0.7 → mean 3.98 -1 = 3; PESQ=3.94; transcript missing >20% so skip TRUE; end_pop=9.3... |
| IndicF5 | 1 | 3 | 1 | 4 | 🚩🚩· | CER=0.89, WER_rom=1.0 → mostly noise; duration=2.29s suggests truncation, transcript missing >20% words → skip TRUE and -1 naturalness from mean(UTMOS=3.87,SQUIM_MOS=4.14)=4 → 3; PESQ=4.01 ≥4.0 but terminal=0.0051>0.0... |
| SPRINGLab F5-Hindi | 1 | 2 | 1 | 5 | 🚩·· | CER=0.89, WER_rom=1.0, detected_lang=ur (transcript_roman is Urdu script) → mostly wrong; duration=2.29s shows truncation, transcript missing >20% → skip TRUE; UTMOS=3.35 vs SQUIM_MOS=4.44 disagree>0.7, mean 3.89→4, -... |

### 21 — `mixed_script` / mixed_script_grammar

> कल का event cancel हो गया, सबको message कर देना please।

_Expected: English content nouns inside Hindi grammatical frame._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 2 | 4 | 2 | 5 | ··· | CER=0.45, WER_rom=0.36; transcript_hi cleanly renders English nouns phonetically (इवेंट/कांसल/मैसेज/प्लीज); UTMOS=4.41+SQUIM_MOS=4.46 → naturalness 4; PESQ=4.20 → speaker 5; WER_en=0.64 not better than WER_rom → FALSE... |
| Indic Parler-TTS | 2 | 3 | 2 | 3 | ·🚩· | CER=0.45, WER_rom=0.64; UTMOS=2.73 vs SQUIM_MOS=4.47 disagree>0.7 → naturalness dropped to 3; end_pop_db=11.53 + terminal=0.006 → pop TRUE, PESQ=3.84 dropped 1 rank to 3; WER_en=0.64 = WER_rom → FALSE. |
| IndicF5 | 1 | 4 | 1 | 5 | 🚩·· | CER=0.49 (near threshold) but transcript_hi missing 'event cancel message please' (>20% loss) → skip TRUE, intelligibility floored to 1; UTMOS=4.05+SQUIM_MOS=4.47 → 4; PESQ=4.06 → 5; WER_en=1.0 > WER_rom=0.55 → FALSE. |
| SPRINGLab F5-Hindi | 1 | 3 | 1 | 3 | 🚩·· | CER=0.58 → intelligibility 1; transcript drops 'event/cancel/message/please' entirely → skip TRUE; UTMOS=3.42 vs SQUIM_MOS=4.48 disagree>0.7 → naturalness 3; PESQ=3.46 → speaker 3; end_pop_db=-71 → no pop. |

### 22 — `mixed_script` / mixed_script_hard

> Boss को बता देना kal मैं leave पर रहूँगा, kuch personal काम है।

_Expected: Heavy code-switching; office register; double script switches._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 2 | 4 | 2 | 5 | ··· | CER=0.43, WER_rom=0.54; transcript_hi covers all tokens phonetically (बॉस/लीफ/पर्सनल); UTMOS=4.25+SQUIM_MOS=4.46 → 4; PESQ=4.03 → 5; WER_en=0.69 > WER_rom=0.54 → FALSE anglicization. |
| Indic Parler-TTS | 2 | 4 | 2 | 4 | ··· | CER=0.46, WER_rom=0.54; UTMOS=3.94+SQUIM_MOS=4.48 → naturalness 4; end_pop_db=10.19 but terminal=0.0033 < 0.005 → pop FALSE; PESQ=3.98 → speaker 4; WER_en=0.85 > WER_rom → FALSE anglicization. |
| IndicF5 | 1 | 4 | 1 | 5 | 🚩·· | CER=0.44 but transcript drops 'Boss/kuch personal' and mangles 'leave' → skip TRUE, intelligibility 1; UTMOS=4.09+SQUIM_MOS=4.47 → 4; PESQ=4.18 → 5; terminal=0.0023 < 0.005 → pop FALSE; WER_en=1.0 > WER_rom=0.54 → FALSE. |
| SPRINGLab F5-Hindi | 1 | 3 | 1 | 5 | 🚩·· | CER=0.51, WER_rom=1.0 (transcript flagged as Urdu, lang=ur); transcript drops 'Boss/leave/kuch personal' → skip TRUE; UTMOS=3.76 vs SQUIM_MOS=4.47 disagree>0.7 → naturalness 3; PESQ=4.03 → speaker 5; end_pop_db=-71 → ... |

### 23 — `mixed_script` / mixed_script_grammar

> Ye file को quickly review करो, deadline बहुत close है।

_Expected: Imperative with English verb embedded in Hindi auxiliary structure._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 1 | 4 | 1 | 4 | ··· | CER=0.62, WER_rom=0.7 → intelligibility 1; WER_en=0.5 not <0.30 so FALSE anglicization; UTMOS=4.35+SQUIM_MOS=4.42 → naturalness 4; PESQ=3.65 → speaker 4. |
| Indic Parler-TTS | 1 | 3 | 1 | 4 | ··· | CER=0.67, WER_rom=0.6 → intelligibility 1; UTMOS=3.78 vs SQUIM_MOS=4.46 disagree>0.7 → naturalness dropped to 3; PESQ=3.65 → 4; end_pop_db=9.96 but terminal=0.005 (not >0.005) → pop FALSE; WER_en=WER_rom=0.6 → FALSE. |
| IndicF5 | 1 | 4 | 1 | 4 | 🚩🚩· | CER=0.6538 + WER_rom=0.70 → mostly wrong words; UTMOS=4.02/SQUIM_MOS=4.44 → naturalness=4; end_pop_db=6.21 with terminal=0.006 triggers pop flag. |
| SPRINGLab F5-Hindi | 1 | 3 | 1 | 4 | 🚩·· | CER=0.7692 + WER_rom=0.90 → garbled output; UTMOS=2.99 vs SQUIM_MOS=4.46 disagree>0.7 → naturalness dropped to 3; PESQ=3.74. |

### 24 — `english_with_NE` / english_with_indian_NE

> My friend Aishwarya from Chennai is visiting Bengaluru next week.

_Expected: Three Indian named entities in pure-English sentence._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 5 | 3 | 5 | 4 | 🚩·· | WER_rom=0.0 + WER_en=0.0 → perfect English+NE rendering; UTMOS=4.50/SQUIM_MOS=4.47 → 4 but silence_mid_clip_s=0.54>0.5 drops naturalness to 3; PESQ=3.80. |
| Indic Parler-TTS | 5 | 4 | 5 | 4 | ··· | WER_rom=0.0 + WER_en=0.0 → perfect English+NE; UTMOS=3.84/SQUIM_MOS=4.47 → naturalness=4; PESQ=3.92; end_pop_db=-13.66. |
| IndicF5 | 1 | 3 | 1 | 3 | 🚩·· | CER=1.0/WER_rom=1.0/WER_en=1.0 with detected_lang=ar → output is non-English gibberish; UTMOS=3.70 vs SQUIM_MOS=4.46 disagree>0.7 → naturalness=3; PESQ=3.42 → speaker=3. |
| SPRINGLab F5-Hindi | 1 | 3 | 1 | 4 | 🚩·· | CER=1.0/WER_rom=1.0 with detected_lang=ar → garbled non-English output; UTMOS=3.64 vs SQUIM_MOS=4.38 disagree>0.7 → naturalness=3; PESQ=3.61. |

### 25 — `english_with_NE` / english_with_indian_names

> Mr. Khanna will join the meeting after he finishes lunch with Priya.

_Expected: Indian surname + first name in English context._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 5 | 4 | 5 | 4 | ··· | WER_rom=0.0 + WER_en=0.0 → perfect rendering; UTMOS=4.51/SQUIM_MOS=4.45 → naturalness=4; PESQ=3.66; silence_mid=0.46<0.5. |
| Indic Parler-TTS | 5 | 4 | 5 | 4 | ··· | WER_rom=0.0 + WER_en=0.0 → perfect English+NE; UTMOS=3.97/SQUIM_MOS=4.42 → naturalness=4; PESQ=3.91; end_pop_db=11.23 but terminal=0.002<0.005 so no pop flag. |
| IndicF5 | 1 | 3 | 1 | 4 | 🚩·· | CER=1.0/WER_rom=1.0 with empty transcripts → severely truncated/wrong; UTMOS=3.46 vs SQUIM_MOS=4.41 disagree>0.7 → naturalness=3; PESQ=3.82; end_pop_db=9.1 but terminal=0.0 so no pop flag. |
| SPRINGLab F5-Hindi | 1 | 3 | 1 | 5 | 🚩·· | CER=1.0/WER_rom=1.0 with empty transcript_roman → output unintelligible; UTMOS=3.53 vs SQUIM_MOS=4.39 disagree>0.7 → naturalness=3; PESQ=4.07 → speaker=5. |

### 26 — `english_with_NE` / english_with_food_locality

> I love butter chicken from Karim's in Old Delhi.

_Expected: Restaurant + locality, Indian food name._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 5 | 4 | 5 | 3 | ··· | WER_rom=0.0, WER_en=0.0 (perfect English NE rendering); UTMOS=4.47 + SQUIM_MOS=4.42 -> nat=4; PESQ=3.48 -> speaker=3; silence_mid=0.5 (not >0.5). |
| Indic Parler-TTS | 4 | 4 | 4 | 5 | ··· | WER_rom=0.2 (Karim's->Karims phonetic NE miss, +1 NE adjust to 4); UTMOS=4.18 + SQUIM_MOS=4.45 -> nat=4; PESQ=4.07 -> speaker=5; end_pop=5.4 (<6). |
| IndicF5 | 1 | 3 | 1 | 4 | 🚩·· | WER_rom=1.0, WER_en=1.0, transcript garbled Kannada-script ('Er krazdo neodali'); UTMOS=3.46 vs SQUIM_MOS=4.36 disagree by 0.90 -> nat=3; PESQ=3.82 -> speaker=4; duration=1.45s (truncated, skip). |
| SPRINGLab F5-Hindi | 1 | 3 | 1 | 5 | 🚩·· | WER_rom=1.0, transcript_en='Or ahegaya' (truncated to 1.45s, missing >20% words); UTMOS=4.27 + SQUIM_MOS=4.37 -> nat=4 minus 1 (skip) = 3; PESQ=4.17 -> speaker=5. |

### 27 — `mixed_script` / mixed_script_grammar

> Office में सब log lunch के लिए बाहर गए, तू भी आ ja yaar.

_Expected: Office casual register; English content nouns inside Hindi frame._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 2 | 4 | 2 | 4 | ··· | CER=0.4444 (Devanagari-dominant mixed) -> intel=2; UTMOS=4.45 + SQUIM_MOS=4.44 -> nat=4; PESQ=3.98 -> speaker=4; WER_en=0.857 > WER_rom=0.571 (not anglicized); silence_mid=0.42 (<0.5). |
| Indic Parler-TTS | 1 | 3 | 1 | 3 | ··· | CER=0.5556 (>0.5) -> intel=1; UTMOS=3.38 vs SQUIM_MOS=4.45 disagree by 1.07 -> nat=3; PESQ=3.39 -> speaker=3; WER_en=0.857 not better than WER_rom=0.786. |
| IndicF5 | 2 | 4 | 2 | 5 | ··· | CER=0.4444, WER_rom=0.4286 -> intel=2; UTMOS=4.08 + SQUIM_MOS=4.44 -> nat=4; PESQ=4.27 -> speaker=5; end_pop=8.39 but terminal=0.0016 (<0.005) so no pop; WER_en=1.0 >> WER_rom=0.43 (not anglicized). |
| SPRINGLab F5-Hindi | 2 | 3 | 2 | 5 | ··· | CER=0.4815 -> intel=2; UTMOS=3.47 vs SQUIM_MOS=4.41 disagree by 0.94 -> nat=3; PESQ=4.02 -> speaker=5; WER_en=1.0 >> WER_rom=0.571 (not anglicized). |

### 28 — `english_with_NE` / english_with_indian_NE

> Rohan is flying from Mumbai to Bengaluru tomorrow morning for work.

_Expected: Three Indian named entities (one personal, two cities) in English._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 5 | 3 | 5 | 4 | 🚩·· | WER_rom=0.0, WER_en=0.0 (Mumbai/Bengaluru/Rohan all clean); UTMOS=4.46 + SQUIM_MOS=4.45 -> nat=4 minus 1 (silence_mid=0.52>0.5) = 3; PESQ=3.51 -> speaker=4; end_pop=5.92 (<6). |
| Indic Parler-TTS | 5 | 3 | 5 | 4 | ··· | WER_rom=0.0, WER_en=0.0 (perfect NE rendering); UTMOS=3.55 vs SQUIM_MOS=4.44 disagree by 0.89 -> nat=3; PESQ=3.85 -> speaker=4; end_pop=9.52 but terminal=0.0023 (<0.005) so no pop. |
| IndicF5 | 1 | 3 | 1 | 5 | 🚩·· | WER_rom=1.0, WER_en=1.0, duration=2.03s for long NE sentence (severe truncation, transcript 'Rahencha menuda chononi hanwar'); UTMOS=2.98 vs SQUIM_MOS=4.02 disagree >0.7 so naturalness dropped to 3; PESQ=4.14 → speake... |
| SPRINGLab F5-Hindi | 1 | 3 | 1 | 4 | 🚩·· | WER_rom=1.0, WER_en=1.0, duration=2.03s with garbled transcript 'Oruse, aruhan, harhua' → severe truncation; UTMOS=3.34 vs SQUIM_MOS=4.47 disagree >0.7, naturalness dropped to 3; PESQ=3.53 → speaker_quality=4; end_pop... |

### 29 — `english_with_NE` / english_with_food_locality

> Let's grab biryani from Paradise in Hyderabad this weekend.

_Expected: Indian food + restaurant + city in English context._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 5 | 5 | 5 | 4 | ··· | WER_rom=0.0, WER_en=0.0, CER=0.10 (Indian NE phonetic variation); UTMOS=4.52 + SQUIM_MOS=4.41 → naturalness=5; PESQ=3.79 → speaker_quality=4; silence_mid=0.4s (under threshold); end_pop=1.45 dB → no pop. |
| Indic Parler-TTS | 5 | 3 | 5 | 5 | ··· | WER_rom=0.0, WER_en=0.0, CER=0.087 (NE phonetic variation hedrabad); UTMOS=3.85 vs SQUIM_MOS=4.43 disagree >0.7 → naturalness dropped to 3; PESQ=4.10 → speaker_quality=5; end_pop_db=10.75 but terminal=0.0006 (<0.005) ... |
| IndicF5 | 1 | 3 | 1 | 4 | 🚩·· | WER_rom=1.0, WER_en=1.0, duration=1.78s for long sentence, transcript 'Adi and eran hansi' indicates severe truncation; UTMOS=4.19 vs SQUIM_MOS=3.22 disagree >0.7 → naturalness dropped to 3; PESQ=3.54 → speaker_qualit... |
| SPRINGLab F5-Hindi | 1 | 4 | 1 | 5 | 🚩·· | WER_rom=1.0, WER_en=1.0, duration=1.78s for long sentence with garbled transcript 'Or vai hamanakaga' → severe truncation; UTMOS=3.95 + SQUIM_MOS=4.44 mean=4.2 → naturalness=4; PESQ=4.11 → speaker_quality=5; end_pop_d... |

### 30 — `english_with_NE` / english_with_indian_brand

> She just got hired at Tata Consultancy Services in Pune.

_Expected: Indian company brand in pure-English sentence._

| Model | Intel | Nat | CS | Spk | Flags | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| Kokoro | 5 | 4 | 5 | 4 | ··· | WER_rom=0.0, WER_en=0.0, CER=0.036 (clean rendering of Tata/Pune); UTMOS=4.47 + SQUIM_MOS=4.45 mean=4.46 → naturalness=4; PESQ=3.66 → speaker_quality=4; silence_mid=0.48s (just under threshold); end_pop=-2.26 dB → no ... |
| Indic Parler-TTS | 5 | 3 | 5 | 4 | ··· | WER_rom=0.0, WER_en=0.0, CER=0.073 (Pune→pulante NE phonetic); UTMOS=3.62 vs SQUIM_MOS=4.46 disagree >0.7 → naturalness dropped to 3; PESQ=3.84 → speaker_quality=4; end_pop_db=15.22 but terminal=0.0047 (<0.005) → no p... |
| IndicF5 | 1 | 4 | 1 | 5 | 🚩·· | WER_rom=1.0, WER_en=1.0, duration=1.69s for long sentence with garbled transcript 'Ayonanji saravajay' → severe truncation; UTMOS=3.97 + SQUIM_MOS=4.43 mean=4.2 → naturalness=4; PESQ=4.17 → speaker_quality=5; end_pop_... |
| SPRINGLab F5-Hindi | 1 | 4 | 1 | 5 | 🚩·· | WER_rom=1.0, WER_en=1.0, duration=1.69s with garbled transcript 'Pushot kahabanaldeha' → severe truncation; UTMOS=4.0 + SQUIM_MOS=4.43 mean=4.22 → naturalness=4; PESQ=4.19 → speaker_quality=5; end_pop_db=-73.21 → no pop. |

---

## Caveats (from SCORING_NOTES.md)

1. **`silence_or_skip` over-fires for `indicf5` and `springlab_f5` (21/30 each)** — AssemblyAI returned empty transcripts for short (~1.8s) clips on these models. The rubric reads "transcript missing >20% of words" as silence. Many clips probably sound fine — verify by listening.
2. **UTMOS / SQUIM are English-trained** — absolute MOS values drift on Hindi. Within-model rankings are reliable; cross-model naturalness deltas should be treated with skepticism.
3. **`code_switch_handling_1to5` mirrors intelligibility for non-mixed rows.** Only `mixed_script` and `english_with_NE` rows reflect actual code-switch quality.
4. **`roman_treated_as_english` is conservative** (0/30 across all). The threshold requires English-forced WER < 0.30, which TTS-anglicized audio rarely meets even when it sounds anglicized.
5. **Indian proper nouns** can artificially inflate WER/CER on `english_with_NE` rows.

**To override** any auto-score: edit `audit/human_overrides.csv` (cols `model,id,column,value`), then run `python audit/scripts/judge.py --merge` → produces `scoring_template_filled.csv` with overrides applied.