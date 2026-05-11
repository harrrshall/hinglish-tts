# Phonetic probe — Findings

**Status: PENDING** — waiting for Kaggle run + auto-scoring + user listening session.

Fill this file after:
1. Kaggle phonetic probe run complete (18/18 wavs ok)
2. `scoring_scripts/run_scoring.py` run locally → `scores/auto_scores.csv`
3. User completes `listening_protocol.md`

---

## Section 1 — Quantitative summary

Per sentence: fill in after auto-scoring and listening session.

| sentence_id | distinction | ASR detects difference (Y/N per pair) | Ear detects difference (Y/N per pair) | Duration Δ (a→b→c) | F0 Δ (a→b→c) | Outcome |
|:---:|---|---|---|---|---|---|
| 1 | nukta /z/ vs /j/ | a-b: ? / a-c: ? / b-c: ? | a-b: ? / a-c: ? / b-c: ? | ? | ? | ? |
| 2 | schwa elision / halant | a-b: ? / a-c: ? / b-c: ? | a-b: ? / a-c: ? / b-c: ? | ? | ? | ? |
| 3 | vowel length ि vs ी | a-b: ? / a-c: ? / b-c: ? | a-b: ? / a-c: ? / b-c: ? | ? | ? | ? |
| 4 | aspiration ख vs क | a-b: ? / a-c: ? / b-c: ? | a-b: ? / a-c: ? / b-c: ? | ? | ? | ? |
| 5 | script register | a-b: ? / a-c: ? / b-c: ? | a-b: ? / a-c: ? / b-c: ? | ? | ? | ? |
| 6 | prosody / emphasis | a-b: ? / a-c: ? / b-c: ? | a-b: ? / a-c: ? / b-c: ? | ? | ? | ? |

Outcome per sentence: **Phonetics-sensitive** / **Partial** / **Insensitive** (see criteria below).

---

## Section 1.5 — Internal reproducibility check

Sentence 1 variants 1a and 1c have identical input text (`मेरा नाम ज़ारा है।`).
They should produce identical (or near-identical) wavs.

| Check | Result |
|---|---|
| 1a duration vs 1c duration | ? (expected: within 10 ms) |
| 1a transcript_aai vs 1c transcript_aai | ? (expected: identical) |
| 1a and 1c sound identical to ear | ? |

If 1a ≠ 1c in any of the above: something is non-deterministic in the inference setup. Flag before interpreting sentence 1 results.

---

## Section 2 — Overall outcome

Classification criteria (from task spec):

- **Outcome A (phonetics-sensitive):** ≥ 4/6 sentences are phonetics-sensitive. Model attends to fine phonetic markers. Direction 3 (pronunciation dictionary) is viable.
- **Outcome B (partial sensitivity):** 2–3/6 phonetics-sensitive AND 2–4/6 partial. Catalog which markers work; build a constrained dictionary around those.
- **Outcome C (grapheme-bound):** ≥ 4/6 insensitive. Model collapses fine-grained distinctions. Path B must include explicit phonemic representation.

**Count:**
- Phonetics-sensitive: ? / 6
- Partial: ? / 6
- Insensitive: ? / 6

**→ Outcome: [A / B / C / mixed — fill in after listening session]**

---

## Section 3 — Implications

*(Fill in after outcome classification. Template paragraphs below — choose the appropriate one and edit.)*

### If Outcome A

The model attends to fine-grained Devanagari phonetic markers at inference time. Nukta, halant, and vowel matra distinctions produce audibly different acoustic outputs. This means a per-word pronunciation dictionary — a lookup table mapping tokens to phonetically-specified Devanagari — can lift quality at zero training cost, by giving the model more precise input than IndicXlit's default transliterations provide.

**Direction 3** (pronunciation dictionary experiment) is viable. Estimated lift: the v2.1 stack scores 4.70 overall; specific phonetic respelling of the highest-frequency ambiguous tokens could plausibly push the residual-4 sentences to 5. Recommend a focused Direction 3 run before committing to Path B's LoRA fine-tune — it's cheaper by 6–10 GPU-hours.

Path B's naturalness fine-tune can also use the dictionary's phonetic forms as the training-time input representation, improving teacher signal for the LoRA.

### If Outcome B

The model is selectively sensitive: some Devanagari distinctions register, others don't. The findings section should catalog which markers work (e.g., "aspiration clearly audible, nukta ambiguous, halant indistinct") and which don't. A constrained pronunciation dictionary can be built around the reliable markers only. Tokens where the marker distinction is unreliable should fall back to the current IndicXlit rendering.

**Direction 3** is viable but scoped: only use phonetic markers that scored phonetics-sensitive or partial in this probe. Over-reliance on markers the model doesn't attend to will degrade rather than improve quality.

### If Outcome C

The model's learned representation is grapheme-bound: fine-grained Devanagari distinctions (nukta, halant, matra length) are silently collapsed to coarser phoneme classes. A per-word pronunciation dictionary written in Devanagari will not improve quality without also changing the model's input representation layer.

**Direction 3** is not viable without retraining. The pronunciation dictionary approach requires either: (a) an explicit G2P layer upstream of the model (feeding phoneme tokens rather than character tokens), or (b) a fine-tune that teaches the model the phonetic distinctions it currently ignores.

**Implication for Path B architecture:** the LoRA target must include the input character embedding layer (not just upper DiT layers), because the bottleneck is at character-to-representation mapping, not at the acoustic generation stage. Data preparation for Phase 3 should include a G2P step from day zero.

---

## Section 4 — Caveats

*(Standard — fill in sentence-specific caveats after reviewing scores and listening notes.)*

- 6 sentences is a small probe. Outcome confidence is moderate. A follow-up with 20+ minimal pairs would be needed to make a strong claim.
- Aspiration (sentence 4) is the most basic phonetic test. If the model fails aspiration, Outcomes B and C are strongly supported regardless of other sentences.
- Sentence 1a and 1c are identical inputs — they test reproducibility, not phonetics. Don't count them as a phonetics-sensitive or insensitive data point for the overall tally.
- Sentence 5a (Roman "office") may produce garbled output (Mode C for ASCII). That's expected and expected to score as insensitive for a different reason than the other sentences. Score it separately.
- Sentence 6 (prosody/punctuation) is a longshot: DiT-based TTS models generally don't attend to punctuation for prosodic control. An insensitive result there doesn't affect the overall outcome classification.
- The model was not retrained. Results apply to IndicF5 v12 weights + duration patch. Other F5-TTS variants may differ.

---

## Files referenced

```
experiments/05_phonetic_probe/
├── test_sentences.tsv           (18 rows — inputs)
├── KAGGLE_CELLS.md              (inference cells)
├── wavs/
│   ├── 1a.wav … 6c.wav         (18 wavs from Kaggle)
│   ├── duration_log.txt
│   └── log.json
├── scores/
│   ├── signal_vectors_aai.json
│   ├── signal_vectors_deepgram.json
│   ├── signal_vectors_groq.json
│   └── auto_scores.csv         (primary quantitative data)
├── listening_protocol.md        (ear evaluation — user fills in)
└── FINDINGS.md                  (this file)
```
