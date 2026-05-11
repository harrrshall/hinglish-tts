# Phonetic probe — Findings

**Status: COMPLETE (ASR-based)**
Kaggle kernel v4 — 18/18 wavs ok. ASR scoring: Deepgram + Groq (AAI returned empty transcripts on all clips — sub-2s Hindi audio below AAI's reliable range). Listening session still open.

---

## Section 1 — Quantitative summary

Primary metric: `transcripts_identical_across_variants` per backend (True = all 3 variants → same transcript = model is insensitive to the distinction). Duration data reported but de-weighted due to non-deterministic inference (see Section 1.5).

| sentence_id | distinction | DG all-same | Groq all-same | Duration Δ a→b→c (s) | F0 mean a/b/c (Hz) | Outcome |
|:---:|---|:---:|:---:|---|---|---|
| 1 | nukta /z/ vs /j/ | N | N | 1.42 / 1.32 / 1.42 | 148 / 160 / 154 | **Sensitive** |
| 2 | schwa elision / halant | Y | Y | 1.51 / 1.71 / 1.61 | 179 / 169 / 172 | **Insensitive** |
| 3 | vowel length ि vs ी | N | N | 1.51 / 1.51 / 1.71 | 161 / 170 / 181 | **Sensitive** |
| 4 | aspiration ख vs क | N | N | 0.65 / 0.65 / 0.65 | 140 / 155 / 134 | **Partial** |
| 5 | script register | N | N | 1.61 / 1.42 / 1.51 | 172 / 175 / 166 | **Sensitive** |
| 6 | prosody / emphasis | N | N | 1.32 / 1.71 / 1.90 | 151 / 169 / 146 | **Partial** |

### Per-sentence detail

**S1 — Nukta (ज़ vs ज):**
- 1a/1c (ज़ारा with nukta): DG=`मेरा नाम ज़ारा है.` / Groq=`मेरा नाम जारा है` — consistent
- 1b (जारा, no nukta): DG=`मेरा नाम जा रहा है.` / Groq=`मेरा नाम जा रहा है` — completely different utterance
- The absence of nukta causes the model to render 'जारा' as the common phrase 'जा रहा है' (going). This is likely OOV collapse rather than a clean /j/→/z/ phoneme distinction, but the acoustic output IS clearly different.
- **Outcome: Sensitive** (with caveat: OOV-driven, not pure phonetic sensitivity)

**S2 — Schwa elision / Halant (्):**
- 2a/2b/2c: DG=`कमल का फ़ूल खिलता है.` all three / Groq=`कमल का फूल खिलता है` all three
- Duration varies (1.51 / 1.71 / 1.61) but content is acoustically identical to ASR
- **Outcome: Insensitive** — halant marks have no effect on acoustic output

**S3 — Vowel length (ि vs ी):**
- 3a (all-short ि): DG=`मिट्टी की किताब लिखी.` / Groq=`मिटी की किताब लिखी`
- 3b (all-long ी): DG=`Meety की किताब लिखी.` / Groq=`मीटी की कीताब लिखी` — clearly distorted
- 3c (correct): DG=`मिट्टी की किताब लिखी.` / Groq=`मिट्टी की किताब लिखी`
- 3b produces detectably different (distorted) output when all vowels are forced long. 3c (correct) sounds the same as 3a to ASR, but Groq correctly captures मिट्टी geminate in 3c where it writes मिटी in 3a.
- **Outcome: Sensitive** — vowel length distinctions produce different acoustic output

**S4 — Aspiration (ख vs क):**
- 4a (खाना खाओ, all-aspirated): DG=`खाना खा` (truncated) / Groq=`कानाका` (garbled merge)
- 4b (काना काओ, all-unaspirated): DG=`गाना खाओ.` / Groq=`काना काओ`
- 4c (खाना काओ, mixed): DG=`खाना खाओ.` / Groq=`खाना काओ` — Groq correctly captures ख vs क contrast!
- The 0.65s clips are at the limit of reliable ASR. Groq 4c result (`खाना काओ`) is the clearest signal: the aspirated ख in खाना and unaspirated क in काओ are both correctly transcribed, demonstrating that the model produces distinguishable /kʰ/ vs /k/ sounds.
- **Outcome: Partial** — aspiration IS audible (4c shows ख/क contrast), but ASR is noisy at 0.65s

**S5 — Script register (Roman / Devanagari):**
- 5a (Roman "office"): DG=`मुझे आहे जाना है.` / Groq=`मुझे आहे जाना है` — garbled (Mode C as predicted)
- 5b (ऑफिस): DG=`मुझे office जाना है.` / Groq=`मुझे ओफिस जाना है.`
- 5c (आफ़ीस): DG=`मुझे office जाना है.` / Groq=`मुझे आफिस जाना है`
- 5a clearly garbled — Roman ASCII input underperforms (expected). 5b vs 5c: Groq captures 'ओफिस' vs 'आफिस' (ऑ vs आ vowel difference is audible); nukta on फ़ is not captured by either ASR.
- **Outcome: Sensitive** for 5a vs Devanagari; **Partial** for 5b vs 5c (vowel audible, nukta not confirmed)

**S6 — Prosody / emphasis:**
- 6a (neutral): DG=`मैं बहुत खुश हूं.` / Groq=`मैं बहुत खुश हूँ.`
- 6b (बहुत बहुत repetition): DG=`मैं बहुत बहुत खुश हूं.` / Groq=`मैं बहुत-बहुत खुश हूँ.` — repetition captured ✓
- 6c (ellipsis + exclamation): DG=`मैं बहुत खुश हूं.` / Groq=`मैं बहुत खुश हूँ` — identical to 6a
- Lexical repetition (6b) generates a longer utterance — the model literally produces more speech. Punctuation-driven prosody (6c) produces no change.
- **Outcome: Partial** — content/repetition cues work; punctuation/prosody cues do not

---

## Section 1.5 — Internal reproducibility check

Sentence 1 variants 1a and 1c have identical input text (`मेरा नाम ज़ारा है।`).

| Check | Result |
|---|---|
| 1a duration vs 1c duration | 1.42s vs 1.42s — identical (within 0ms) ✓ |
| 1a transcript_dg vs 1c transcript_dg | `मेरा नाम ज़ारा है.` vs `मेरा नाम ज़ारा है.` — identical ✓ |
| 1a transcript_groq vs 1c transcript_groq | `मेरा नाम जारा है` vs `मेरा नाम जारा है.` — effectively identical ✓ |
| Waveform sample diff (from kernel log) | max_sample_diff = 0.798 → **WARNING: non-deterministic inference** |

The model is stochastic (diffusion sampling without fixed seed). Duration and transcript are consistent for identical inputs, but raw waveforms differ. This means:
- Duration deltas in Section 1 may reflect noise, not phonetics — treat with caution
- Transcript comparison is the reliable primary metric
- Any sentence where DG and Groq both agree across variants is a strong insensitive signal

---

## Section 2 — Overall outcome

**Count:**
- Phonetics-sensitive: **3 / 6** (S1 nukta, S3 vowel length, S5 script register)
- Partial: **2 / 6** (S4 aspiration, S6 prosody)
- Insensitive: **1 / 6** (S2 halant/schwa)

**→ Outcome: B (partial sensitivity)**

3 sensitive is one below the A threshold (≥4). Key finding: two of the three "sensitive" results are not clean phonetic sensitivity — S1 is OOV-driven (model collapses an unknown name to a common phrase), and S5 is largely Mode C failure vs clean Devanagari. The one unambiguously clean phonetic result is S3 (vowel length). S4 (aspiration) shows partial sensitivity in the best-case reading of the Groq 4c transcript.

---

## Section 3 — Implications

**Outcome B applies.**

The model is selectively sensitive. Markers that register:
- **Vowel length matras** (ि vs ी): clearly audible. A pronunciation dictionary can reliably use matra-based forms to specify vowel duration.
- **Nukta** (ज़ vs ज): the model reacts, but via OOV collapse rather than a clean phoneme switch. Nukta on common words (फ़, ज़) is worth including in a dictionary for words where the nukta-absent form is a common different word. Avoid relying on nukta for subtle /z/ vs /j/ distinctions in rare proper nouns.
- **Aspiration** (ख vs क): partial evidence (Groq 4c). Worth including in the pronunciation dictionary for the most frequent aspirated-vs-unaspirated minimal pairs (e.g., खाना/काना, पहले/पले).

Markers that do NOT register:
- **Halant / schwa elision** (्): completely ignored. Do not use halant placement in pronunciation dictionary entries — it has no effect on output.
- **Punctuation for prosody** (ellipsis, exclamation): ignored. No mechanism for prosody control through text markers at this time.

**Direction 3 (pronunciation dictionary) is viable but scoped:**
Use the dictionary for: (1) vowel length corrections (common words with ि vs ी errors), (2) nukta corrections on high-frequency words where absence causes wrong word (जा vs ज़ा, फ vs फ़), (3) aspiration corrections on frequent minimal pairs. Do NOT use the dictionary to specify halant placement or punctuation-driven prosody — those levers don't exist.

Expected lift: The v2.1 stack scores 4.70 overall. The residual errors cluster in pure_dev and eng_NE sentences. A focused dictionary on the top-20 most frequent mispronounced tokens could plausibly push pure_dev from 4.62 toward 4.8.

---

## Section 4 — Caveats

- ASR scoring only (AAI returned empty transcripts on all 18 clips — sub-2s audio below reliable threshold). Primary data is Deepgram + Groq. Listening session still pending — fill `listening_protocol.md` to confirm/override the ASR-based classifications.
- Non-deterministic inference (max_sample_diff=0.798 on identical 1a/1c inputs). Duration deltas between variants are not reliable evidence of phonetic sensitivity. Transcript comparison is the robust metric.
- Sentence 4 clips are 0.65s — at the lower limit of reliable ASR for Hindi. The aspiration classification is tentative. A clean aspiration test would use 1.5s+ clips with aspirated vs unaspirated stops in multiple positions.
- Sentence 1 "sensitive" classification is OOV-driven: 'जारा' without nukta → model generates 'जा रहा है' (a common verbal phrase), not a modified pronunciation of the name. This is not phonetic sensitivity in the acoustic sense — it's a lexical-level lookup failure.
- Sentence 5 sensitive classification conflates two effects: Mode C failure (5a Roman input) and register-level Devanagari differences (5b vs 5c). Only 5b vs 5c tests phonetic sensitivity; the nukta on फ़ is not confirmed to produce audible /f/ vs /ph/.
- 6 sentences is a small probe. Outcome confidence is moderate. Recommend extending with 20+ minimal pairs before committing to Direction 3 scope.
- Results apply to IndicF5 v12 weights + duration patch. Other F5-TTS variants may differ.

---

## Section 5 — ASR Backend Notes

AssemblyAI returned empty transcripts for all 18 clips. Likely cause: AAI's Hindi model has a minimum audio duration threshold higher than 0.65–1.90s, or the API call configuration in `lib_asr.py` does not specify `language_code="hi"` explicitly. The phonetic probe results rely on Deepgram and Groq only. For future short-clip experiments, prefer Groq (Whisper-based, more robust to short audio) as primary backend.

---

## Files referenced

```
experiments/05_phonetic_probe/
├── test_sentences.tsv              (18 rows — inputs)
├── KAGGLE_CELLS.md                 (inference cells used in kernel v4)
├── wavs/
│   ├── 1a.wav … 6c.wav            (18 wavs — Kaggle kernel v4)
│   ├── duration_log.txt
│   └── log.json                   (18/18 ok, 0 errors)
├── scores/
│   ├── signal_vectors_aai.json    (empty transcripts — AAI failed on short clips)
│   ├── signal_vectors_deepgram.json
│   ├── signal_vectors_groq.json
│   └── auto_scores.csv            (18 rows — primary quantitative data)
├── listening_protocol.md          (ear evaluation — PENDING user fill-in)
└── FINDINGS.md                    (this file)
```
