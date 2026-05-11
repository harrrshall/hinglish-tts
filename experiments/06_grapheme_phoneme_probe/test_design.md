# Test Design — Direction 2: Grapheme vs Phoneme Representation Probe

**Date:** 2026-05-11  
**Experiment:** `06_grapheme_phoneme_probe`  
**Base model:** patched IndicF5 (duration fix applied, NO IndicXlit preprocessing)  
**Kernel:** `harshalsinghcn/hinglish-tts-audit-indicf5`  

---

## Framing

Mode C (Phase 2b) showed that ASCII characters produce garbled acoustic output.
IndicXlit preprocessing (Devanagari routing) eliminated the garbling — without
touching the model weights. Two interpretations explain this:

1. **Grapheme-bound**: क and k index into *separate, independent* learned acoustic
   trajectories. There is no shared /k/ phoneme layer. ASCII is undertrained, so its
   trajectory is garbage; Devanagari is well-trained. IndicXlit fixes it by
   routing everything through Devanagari trajectories. Path B implication: the model
   has no phoneme abstraction to exploit — Path B needs explicit external phoneme
   tokenization (G2P → phoneme tokens → model).

2. **Phoneme-mediated**: Both क and k map to an internal /k/ phoneme representation.
   The acoustic trajectory for /k/ is well-learned from Devanagari training data.
   ASCII's *access path* to /k/ was undertrained (the embedding for "k" points to a
   near-random location in phoneme space). IndicXlit fixes it by routing through the
   well-trained Devanagari access path. Path B implication: the phoneme representation
   is exploitable — PL-BERT-style conditioning or explicit phoneme tokenization will
   work because the destination (phoneme layer) already exists.

These three tests isolate different aspects of this question.

---

## Note on input count vs wav count

The task header says "24 inputs / 24 wavs". The correct count is:

- Test A: 8 pairs × 2 variants (Devanagari + Roman) = **16 wavs**
- Test B: 8 inputs = **8 wavs**
- Test C: 8 inputs = **8 wavs**
- **Total: 32 wavs**

The "24" refers to the number of unique test *cases* (8 per test type). Each
Test A case produces 2 wavs (one per script variant). All other cases produce 1 wav.

---

## Test A — Cross-script homophone similarity (the core probe)

**Question:** Do Devanagari and Roman homophones produce acoustically similar
outputs even though the Roman access path is severely undertrained?

**Logic:** If the model is grapheme-bound, `कल` and `kal` index into completely
different lookup tables. Their acoustic outputs will be unrelated — `कल` will
produce good Hindi speech, `kal` will produce garbled noise, and the two will
have no acoustic structure in common (low MFCC cosine similarity).

If the model is phoneme-mediated, both `कल` and `kal` attempt to access the
same internal /kʌl/ phoneme sequence. `कल` succeeds (trained path). `kal` fails
to pronounce correctly (undertrained path produces garbled output), but the
*attempt* may leave acoustic fingerprints — partial consonant bursts, formant
transitions in approximately the right direction, partial duration alignment.
The key question is whether the garbled Roman output is *acoustically related*
to the Devanagari output (even if mangled), or whether it is truly random noise.

**Metric:** Cosine similarity of `mfcc_full_mean` vectors (sentence-level) and
`mfcc_200ms_mean` vectors (phoneme onset region) between Devanagari and Roman
variants of each pair. Baseline: similarity between *unrelated* Devanagari clips
(e.g., A1 vs A5). If matched-pair similarity ≥ 0.15 above unrelated baseline,
phoneme-mediated interpretation is supported.

**Critical instruction:** Feed both variants *directly* to the model. No preprocessing.
Roman outputs will likely be garbled. That is expected and not a problem — we're
looking at acoustic structure, not quality.

**8 pairs → 16 wavs:**

| pair_id | devanagari | roman | phonetic content |
|---------|-----------|-------|-----------------|
| A1 | कल | kal | basic homophone, /kʌl/ |
| A2 | दिल्ली | Delhi | proper noun, well-known |
| A3 | मेरा नाम | mera naam | two-word phrase |
| A4 | पानी | paani | common content word |
| A5 | कितना | kitna | aspirate + nasal |
| A6 | भाई | bhai | aspirated stop |
| A7 | धन्यवाद | dhanyavaad | complex word |
| A8 | नमस्ते | namaste | well-known greeting |

---

## Test B — Phoneme isolation: /k/ consistency within Hindi

**Question:** When the model generates a /k/ phoneme in different vowel contexts
(all in Devanagari), does it produce an acoustically consistent /k/ across
those contexts, or does each grapheme-context combination produce an independent,
unrelated trajectory?

**Logic:** If phoneme-mediated, the initial burst of /k/ before the vowel onset
should be acoustically similar across B1–B8, because they all access the same /k/
phoneme. Coarticulation will make the later vowel-transition part differ
(k+a vs k+i vs k+u are different), but the initial burst (first ~50ms) should
be consistent. If grapheme-bound, "कल" and "कान" are two separate lookup entries
with no shared structure — their /k/ onsets will be as different as any two
random audio clips.

**Metric:** Pairwise cosine similarity of `mfcc_50ms_mean` (the phoneme burst
window) across all 28 pairs of B1–B8. Mean similarity > 0.7 → consistent /k/
representation (phoneme-mediated). 0.4–0.7 → partial (coarticulation effects
dominate). < 0.4 → no /k/ abstraction (grapheme-bound).

All inputs are pure Devanagari — no Mode C effects expected. These should all
produce clean, good-quality audio.

**8 inputs → 8 wavs:**

| test_id | text | /k/ context |
|---------|------|-------------|
| B1 | कल | /k/ + /ʌ/ |
| B2 | कान | /k/ + /aː/ |
| B3 | किताब | /k/ + /ɪ/ |
| B4 | कुत्ता | /k/ + /ʊ/ |
| B5 | केला | /k/ + /eː/ |
| B6 | कोल्ड | /k/ + /oː/ |
| B7 | क्या | /k/ in cluster /kj/ |
| B8 | कितना अच्छा | /k/ at sentence start, complex context |

---

## Test C — Cross-language phoneme transfer

**Question:** Does the model's /k/ phoneme representation generalize across
language contexts (pure Hindi, Roman Hindi, mixed, pure English), or is it
language-specific?

**Logic:** C1 (pure Devanagari Hindi) and C5/C8 (mixed with Devanagari /k/)
will produce clean audio. C3 and C7 (Roman Hindi) will likely garble. C2, C4, C6
(English-context /k/) are the interesting cases.

If the model has language-agnostic phoneme abstraction, all /k/ onsets should
cluster together. If language-specific, Devanagari-Hindi /k/ will cluster
separately from Roman/English-context /k/. If grapheme-bound, no clustering.

**Three expected cluster structures:**
- All 8 cluster (high within-cluster, low between-cluster) → language-agnostic /k/ phoneme
- Two clusters (Hindi-context vs English-context) → language-specific phonemes
- Random structure / no clustering → grapheme-bound

**8 inputs → 8 wavs:**

| test_id | text | language context | /k/ instance |
|---------|------|-----------------|-------------|
| C1 | कल मैं जाऊंगा | pure Hindi Devanagari | initial /k/ |
| C2 | मेरा computer है | mixed, English word "computer" — feed Roman directly, no preprocessing | /k/ in English word |
| C3 | kal main jaunga | pure Roman Hindi | initial /k/ |
| C4 | Cat is sitting | pure English — feed directly | English /k/ |
| C5 | कैसे हो? | Hindi with /kɛ/ | /kɛ/ |
| C6 | Coffee पीते हो? | English-initial mixed | English /k/ |
| C7 | kya tum theek ho? | Roman Hindi | initial /k/ |
| C8 | Karen और मैं | proper noun /k/ in mixed | English name /k/ |

---

## Expected quality by input type

| input type | expected audio quality | reason |
|-----------|----------------------|--------|
| Pure Devanagari (all B, C1, C5) | Clean, good quality | Well-trained embeddings |
| Roman Hindi (A roman halves, C3, C7) | Garbled, Mode C | Undertrained ASCII embeddings |
| English (C2, C4, C6, C8) | Likely garbled, or tokenization error | Same as Roman |
| Proper nouns (A2, A3) | Devanagari: good; Roman: garbled | Same Mode C pattern |

Quality is not the variable of interest. Acoustic structure is.

---

## Analysis plan summary

| test | metric | key comparison | threshold |
|------|--------|---------------|-----------|
| A | MFCC cosine similarity (full + 200ms onset) | matched Deva/Roman pairs vs unrelated Deva pairs | paired ≥ 0.15 above baseline → phoneme-mediated |
| B | MFCC cosine similarity (50ms onset) | pairwise /k/ burst across vowel contexts | mean > 0.7 → consistent /k/ representation |
| C | Hierarchical clustering on 50ms MFCC | cluster structure across language contexts | all-1-cluster → language-agnostic; 2-cluster → language-specific |

---

## Caveats (pre-registered)

1. MFCC similarity is a proxy for phonetic similarity. It is not the phoneme
   representation itself. Within-model comparisons are valid; claims about
   cross-model structure require different methods.
2. /k/ was chosen for being acoustically distinctive (clear burst). Results may
   not generalize to vowels, fricatives, or low-frequency phonemes.
3. n=8 per test is small. Confidence intervals are wide; treat findings as
   directional, not confirmatory.
4. This probe tests *representation*, not quality. Even a strongly phoneme-mediated
   model can produce bad audio.
5. If any inputs produce tokenization errors (model rejects the input), document
   the error as a finding — input-level rejection is itself evidence about the
   model's vocabulary structure.
