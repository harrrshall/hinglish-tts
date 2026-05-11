# Phonetic probe — Findings

**Status: COMPLETE (ASR + ear evaluation)**  
Kaggle kernel v4 — 18/18 wavs ok.  
ASR scoring: Deepgram + Groq (AAI returned empty transcripts on all clips — sub-2s Hindi audio below AAI's reliable range).  
Listening session: completed; protocol filled in `listening_protocol.md`.

---

## Section 1 — Quantitative summary (auto-metrics)

Primary metric: `transcripts_identical_across_variants` per backend. See Section 1.6 for
the ear-based revision of each outcome.

| sentence_id | distinction | DG all-same | Groq all-same | Duration Δ a→b→c (s) | F0 mean a/b/c (Hz) | Spectral centroid a/b/c (Hz) | Auto outcome |
|:---:|---|:---:|:---:|---|---|---|---|
| 1 | nukta /z/ vs /j/ | N | N | 1.42 / 1.32 / 1.42 | 148 / 160 / 154 | 1631 / 1568 / 1820 | Sensitive |
| 2 | schwa elision / halant | Y | Y | 1.51 / 1.71 / 1.61 | 179 / 169 / 172 | 1606 / **1718** / 1618 | Insensitive |
| 3 | vowel length ि vs ी | N | N | 1.51 / 1.51 / 1.71 | 161 / 170 / 181 | 2014 / 1907 / 1990 | Sensitive |
| 4 | aspiration ख vs क | N | N | 0.65 / 0.65 / 0.65 | 140 / 155 / 134 | 2201 / 1630 / 1607 | Partial |
| 5 | script register | N | N | 1.61 / 1.42 / 1.51 | 172 / 175 / 166 | 1899 / 2307 / 2401 | Sensitive |
| 6 | prosody / emphasis | N | N | 1.32 / 1.71 / 1.90 | 151 / 169 / 146 | 2157 / 1828 / 2071 | Partial |

### Per-sentence ASR detail

**S1 — Nukta (ज़ vs ज):**
- 1a/1c (ज़ारा with nukta): DG=`मेरा नाम ज़ारा है.` / Groq=`मेरा नाम जारा है`
- 1b (जारा, no nukta): DG=`मेरा नाम जा रहा है.` / Groq=`मेरा नाम जा रहा है` — different utterance
- The no-nukta form collapses 'जारा' → common verb phrase 'जा रहा है'. This is OOV-driven, but the acoustic output IS clearly different.
- **Auto outcome: Sensitive** (OOV collapse, not pure phonetic distinction)

**S2 — Schwa elision / Halant (्):**
- 2a/2b/2c: DG=`कमल का फ़ूल खिलता है.` all three / Groq=`कमल का फूल खिलता है` all three
- Duration and F0 vary (1.51 / 1.71 / 1.61), but ASR content is identical
- Spectral centroid: 2b is noticeably higher (1718 Hz) vs 2a (1606 Hz) and 2c (1618 Hz) — a sub-phonemic quality shift that ASR cannot resolve
- **Auto outcome: Insensitive** — but spectral centroid suggests a real acoustic change below ASR resolution

**S3 — Vowel length (ि vs ी):**
- 3a (all-short ि): DG=`मिट्टी की किताब लिखी.` / Groq=`मिटी की किताब लिखी`
- 3b (all-long ी): DG=`Meety की किताब लिखी.` / Groq=`मीटी की कीताब लिखी` — clearly distorted
- 3c (correct): DG=`मिट्टी की किताब लिखी.` / Groq=`मिट्टी की किताब लिखी`
- **Auto outcome: Sensitive**

**S4 — Aspiration (ख vs क):**
- 4a (खाना खाओ, all-aspirated): DG=`खाना खा` (truncated) / Groq=`कानाका` (garbled merge)
- 4b (काना काओ, all-unaspirated): DG=`गाना खाओ.` / Groq=`काना काओ`
- 4c (खाना काओ, mixed): DG=`खाना खाओ.` / Groq=`खाना काओ` — Groq correctly captures ख/क contrast
- 0.65s clips are at the limit of reliable Hindi ASR. Groq 4c correctly reads ख vs क; 4a ASR is noisy at this length.
- **Auto outcome: Partial** (ASR noise-limited; Groq 4c is the best signal)

**S5 — Script register:**
- 5a (Roman "office"): DG=`मुझे आहे जाना है.` / Groq=`मुझे आहे जाना है` — garbled (Mode C, expected)
- 5b (ऑफिस): DG=`मुझे office जाना है.` / Groq=`मुझे ओफिस जाना है.`
- 5c (आफ़ीस): DG=`मुझे office जाना है.` / Groq=`मुझे आफिस जाना है`
- Groq captures ओफिस vs आफिस (ऑ vs आ vowel is audible); nukta on फ़ → /f/ not confirmed by ASR
- **Auto outcome: Sensitive** for 5a vs Devanagari; Partial for 5b vs 5c (vowel audible, nukta unconfirmed)

**S6 — Prosody / emphasis:**
- 6a (neutral): DG=`मैं बहुत खुश हूं.` / Groq=`मैं बहुत खुश हूँ.`
- 6b (बहुत बहुत): DG=`मैं बहुत बहुत खुश हूं.` / Groq=`मैं बहुत-बहुत खुश हूँ.` — repetition captured ✓
- 6c (ellipsis + !): DG=`मैं बहुत खुश हूं.` / Groq=`मैं बहुत खुश हूँ` — **identical to 6a** in transcript
- Duration: 6c is noticeably longer (1.90s vs 6a 1.32s) — suggests pacing change below ASR resolution
- **Auto outcome: Partial** — content repetition (6b) works; punctuation-driven prosody (6c) invisible to ASR

---

## Section 1.5 — Internal reproducibility check

Sentence 1 variants 1a and 1c have identical input text (`मेरा नाम ज़ारा है।`).

| Check | Result |
|---|---|
| 1a duration vs 1c duration | 1.42s vs 1.42s — identical ✓ |
| 1a DG transcript vs 1c DG | `मेरा नाम ज़ारा है.` vs `मेरा नाम ज़ारा है.` — identical ✓ |
| 1a Groq vs 1c Groq | `मेरा नाम जारा है` vs `मेरा नाम जारा है.` — identical ✓ |
| Waveform sample diff | max_sample_diff = 0.798 → **non-deterministic inference** |

The model is stochastic (diffusion sampling without fixed seed). Duration and
transcript are consistent for identical inputs, but raw waveforms differ. Duration
deltas between variants may include noise — treat with caution.

---

## Section 1.6 — Per-sentence reconciliation: auto-metrics vs ear

Filled from `listening_protocol.md` (user listening session, all 18 clips).

| S | Distinction | Auto outcome | Ear evidence (key quotes) | Ear outcome | Direction of change |
|:---:|---|---|---|---|---|
| 1 | nukta /z/ | Sensitive | "1b speaker is zaraa, 1a is zara"; 1a has clearest /z/; prefers a+c for "Zara" | **Sensitive** | Confirms ASR |
| 2 | schwa elision | Insensitive | "2b is lil calmer than 2a"; "cleaner consonant cluster in खिल्ता — Y"; "2b is most natural" | **Sensitive** | **Ear overrides ASR** |
| 3 | vowel length | Sensitive | "3a more correct, 3b is something stretched"; "3a clipped vs 3c — Y"; 3c is most natural | **Sensitive** | Confirms + strengthens |
| 4 | aspiration | Partial | "4a more like khana, 4b is kana"; "clear /kʰ/ in 4a — Y"; "harder in 4b — Y"; "ख/क contrast in 4c — Y"; overall: clearly audible | **Sensitive** | **Ear upgrades Partial** |
| 5 | script register | Sensitive (partial) | "5a is wrong output"; "5b vs 5c different — Y"; "5c vowel longer — Y"; "audible /f/ in 5c — **Y**" | **Sensitive** | Confirms + extends (nukta /f/ now confirmed) |
| 6 | prosody/emphasis | Partial | "6b emphasis: slightly or No"; "6c pacing different — Y, slower"; "6c हूं! higher pitch — Y"; "punctuation changed delivery — Y" | **Sensitive** | **Ear upgrades Partial** |

**Ear count: 6/6 Sensitive → Outcome A**

### Where auto-metrics underestimated sensitivity:

**S2 — halant is audible, ASR is blind to consonant quality:**
ASR transcribed 2a/2b/2c identically (`कमल का फूल खिलता है`), but the spectral
centroid of 2b (1718 Hz) is 112 Hz higher than 2a/2c (1606/1618 Hz). The user heard
2b as "lil calmer" and confirmed the खिल्ता consonant cluster sounds cleaner.
ASR operates at the lexical level and cannot distinguish the schwa-suppressed
/खिल्ता/ [kʰɪlta] from the schwa-present /खिलता/ [kʰɪlɪta] when both decode to
the same word. The model DOES respond to explicit halant — it just doesn't change
words, only consonant quality.

**S4 — aspiration is clear to the ear, not to 0.65s ASR:**
Groq got `कानाका` for 4a (aspirated) — a garbled merge. The user heard clear /kʰ/
on 4a and confirmed all three clips are distinguishable. The 0.65s clip length is
below the reliable floor for Hindi ASR (Groq performs better on ≥1.5s). The
acoustic signal is real; the measurement instrument failed.

**S6 — punctuation shifts prosody below lexical ASR resolution:**
6c (`मैं... बहुत... खुश हूं!`) and 6a (`मैं बहुत खुश हूं।`) produce identical
transcripts, but 6c is 1.90s vs 6a 1.32s (44% longer), and the user hears slower
pacing and a pitch rise on the final हूं!. The ellipsis and exclamation DO affect
delivery — they change timing and terminal pitch, not words. ASR is insensitive to
these sub-lexical prosodic changes by design.

---

## Section 2 — Overall outcome

**→ Outcome A (phonetics-sensitive)** — based on ear evaluation.  
Auto-metrics alone gave Outcome B (3/6 sensitive, 2 partial, 1 insensitive).
Ear evaluation shows all 6 distinctions are audible.

| Outcome | Auto-metric count | Ear count |
|---|---|---|
| Sensitive | 3 / 6 | **6 / 6** |
| Partial | 2 / 6 | 0 / 6 |
| Insensitive | 1 / 6 | 0 / 6 |

**Summary per distinction (ear-based):**

| Distinction | Audible? | Quality of evidence |
|---|---|---|
| Vowel length (ि vs ी) | Yes — clearly | Both ASR and ear confirm; 3b clearly distorted |
| Aspiration (ख vs क) | Yes — clearly | Ear overrides noisy 0.65s ASR; user hears /kʰ/ vs /k/ without ambiguity |
| Nukta fricative (ज़ vs ज) | Yes — OOV-driven | 1b collapses to 'जा रहा है'; distinction is real but caused by lexical collision, not /z/→/j/ phoneme switch |
| Script register (Roman vs Devanagari) | Yes — clearly | Mode C garble on 5a; ऑ vs आ vowel audible; nukta /f/ confirmed by ear |
| Schwa elision / halant (्) | Yes — subtle | Consonant quality change (cleaner cluster); spectral centroid shift; not visible to ASR |
| Prosody / punctuation (ellipsis + !) | Yes — pacing/pitch | 6c slower pacing + pitch rise on हूं!; 6b repetition = emphatic content, not dramatically different delivery |

---

## Section 3 — Implications (revised for Outcome A)

**Outcome A applies. The model is phonetics-sensitive across all six tested dimensions.**

This strengthens the case for Direction 3 (pronunciation dictionary) beyond the
Outcome B scope. Specific guidance per dimension:

**Confirmed effective levers:**
- **Vowel length matras (ि vs ी):** use freely in pronunciation dictionary. The model
  clearly distinguishes short and long /i/. Correcting common matra errors (e.g.,
  मिट्टी vs मिटी) will produce audibly different output.
- **Aspiration (ख vs क):** confirmed audible. Include aspirated/unaspirated minimal
  pairs in the dictionary (खाना/काना, ख़बर/कबर, etc.). The effect is clear
  even in 0.65s clips — short tokens like खा/का will reliably differ.
- **Nukta for fricatives (ज़, फ़):** use where it prevents OOV collapse (ज → जा रहा है)
  or where the /f/ vs /ph/ distinction matters (5c confirms audible /f/ from फ़).
  Nukta on proper nouns like Zara is high-value.
- **Script normalisation (ऑ vs आ vowel):** ऑफिस vs आफ़ीस produce audibly distinct
  vowels. The dictionary should standardise English loanwords to the ऑ form where
  the anglicised vowel is preferred in natural Hinglish.

**Confirmed effective, sub-phonemic only:**
- **Halant / schwa elision (्):** the model responds — consonant quality improves,
  spectral centroid shifts — but the effect is subtle (user: "lil calmer"). The
  change is real but below the threshold where ASR or a naive listener would notice.
  Worth including in a dictionary for sentences where the schwa intrusion is
  conspicuous (heavy consonant clusters), but do not expect dramatic quality lift.

**Confirmed effective, prosody only:**
- **Repetition for emphasis (बहुत बहुत):** works. Generates more speech. The
  delivery is not dramatically more emphatic (user: "slightly or No"), but the
  content repetition is a natural Hindi emphasis pattern worth using.
- **Ellipsis + exclamation for pacing (मैं... बहुत...):** works — produces slower
  pacing and a pitch rise on the final word. Effect is subtle and sub-lexical.
  Useful for dramatic TTS applications; not a controlled prosody lever.

**Direction 3 scope revision (vs Outcome B estimate):**  
Under Outcome B, expected lift was from 4.70 toward ~4.80 on pure_dev sentences
via a 20-item dictionary. Under Outcome A, the model is more sensitive than
estimated, which means:
1. The dictionary can be broader (6 dimensions, not 3).
2. Halant corrections are now worth including for high-cluster sentences.
3. Aspiration corrections in the dictionary are reliable, not speculative.
4. The ceiling is higher — a well-crafted 50-item dictionary could plausibly reach
   4.85+ on pure_dev, and close the gap on eng_NE sentences via nukta + script
   normalisation.

---

## Section 4 — Caveats

- **Auto-metrics systematically underestimated sensitivity** for sub-phonemic
  (S2 halant) and prosodic (S6 punctuation) dimensions. For any future phonetic
  probe with IndicF5, ear evaluation is required — ASR-only analysis will
  under-classify the model.
- **S1 sensitivity is OOV-driven, not a clean phoneme test.** 'जारा' without nukta
  is not in the model's vocabulary as a name and collapses to 'जा रहा है'. If the
  goal is testing /j/ vs /z/ phoneme production in isolation, a probe item where
  both forms exist as words is needed (e.g., जल vs ज़ल, though the second may also
  be OOV).
- **Non-deterministic inference.** max_sample_diff = 0.798 on identical 1a/1c inputs.
  Duration deltas between variants are not reliable evidence of phonetic sensitivity
  (except for S6 where the 6c duration jump to 1.90s is too large to be noise).
- **n=1 listener, no inter-rater reliability.** The ear evaluation is a single session
  by a native speaker. Some observations (especially S2 "lil calmer", S6 "slightly
  emphatic") should be treated as suggestive, not definitive. A 5-listener ABX test
  would confirm the subtle effects.
- **S4 clips at 0.65s.** ASR is unreliable at this length for Hindi. A redesigned
  aspiration probe with 1.5s+ clips (e.g., full sentences with aspirated stops in
  multiple positions) would give cleaner ASR confirmation.
- Results apply to IndicF5 v12 weights + duration patch. Other F5-TTS variants
  or base model versions may differ.

---

## Section 5 — ASR Backend Notes

AssemblyAI returned empty transcripts for all 18 clips. Likely cause: AAI's Hindi
model has a minimum duration threshold higher than 0.65–1.90s, or `language_code="hi"`
was not propagated correctly in `lib_asr.py`. The phonetic probe results rely on
Deepgram and Groq only. For future short-clip experiments, prefer Groq (Whisper-based,
more robust to short audio) as primary backend.

---

## Files referenced

```
experiments/05_phonetic_probe/
├── test_sentences.tsv              (18 rows — inputs)
├── KAGGLE_CELLS.md                 (inference cells used in kernel v4)
├── listening_protocol.md           (ear evaluation — COMPLETE)
├── wavs/
│   ├── 1a.wav … 6c.wav            (18 wavs — Kaggle kernel v4)
│   ├── duration_log.txt
│   └── log.json                   (18/18 ok, 0 errors)
├── scores/
│   ├── signal_vectors_aai.json    (empty transcripts — AAI failed on short clips)
│   ├── signal_vectors_deepgram.json
│   ├── signal_vectors_groq.json
│   └── auto_scores.csv            (18 rows — primary quantitative data)
└── FINDINGS.md                    (this file)
```
