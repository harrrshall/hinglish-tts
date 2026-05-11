# FINDINGS — Direction 2: Grapheme vs Phoneme Representation Probe

**Date:** 2026-05-11 (v1) / 2026-05-11 (v2 — corrected analysis)  
**Experiment:** `06_grapheme_phoneme_probe`  
**Kernel:** `harshalsinghcn/hinglish-tts-audit-indicf5` v15, T4 GPU  
**Status:** COMPLETE — 32/32 wavs produced, acoustic analysis v2 done

**v2 analysis scripts:** `extract_acoustics_v2.py`, `analyse_results_v2.py`  
**v2 data:** `acoustic_analysis_v2.json`, `scores/analysis_results_v2.json`

---

## Section 1: Quantitative Results

### Methodological note — v1 bugs and v2 fixes

The v1 analysis had three compounding bugs. All three are fixed in v2.

**Bug 1 — C0 dominance.** C0 is the energy/loudness MFCC coefficient. Clips with
a silent lead-in have C0 ≈ −1015 in the first 50ms; short clips with immediate
onset have C0 ≈ +4. When C0 is included in cosine similarity, it dominates:
two "−1015" silence windows give cosine ≈ 1.0; a silence window vs a speech
window gives cosine ≈ −1.0. All v2 comparisons use **C1–C12 only**.

**Bug 2 — Fixed 50ms window captures silence, not speech.** Clips > ~200ms have
a silent lead-in. The first 50ms (used in v1 Tests B and C) is silence for most
clips. This caused (a) all Test C similarities = 1.0 — all silence windows look
identical; (b) Test B to show a bimodal distribution (mean 0.439, std 0.52),
splitting into +1.0 within each silence/speech group and −0.05 between groups.
**v2 fix:** detect speech onset via `librosa.effects.split(top_db=40)`, strip
the silent prefix, then extract the first 50ms / 100ms of actual speech.

**Bug 3 — Voiced-frames vs full-clip mean for Test A.** Using the full-clip MFCC
mean averages voiced speech and silence together, partially re-introducing the
silence confound. **v2 fix:** use voiced-frames-only MFCC mean (frames where
pyin detected F0 > 0) for Test A.

**Residual confound — reference-audio spectral dominance.** All 32 inputs share
the same `REF_AUDIO` (hindi_ref.wav). This imprints a common spectral envelope,
raising the baseline MFCC similarity between *unrelated* clips to **0.895**
(voiced MFCC, C1–C12). Any matched-pair similarity must substantially exceed
this to be meaningful.

### Test A — Cross-script homophone similarity (v2: voiced MFCC C1–C12)

| Pair | Devanagari | Roman | Sim voiced C1-12 | F0 Deva (Hz) | F0 Roman (Hz) | Note |
|------|-----------|-------|-----------------|-------------|--------------|------|
| A1 | कल | kal | 0.997 | 93 | 94 | Both 93 Hz short-clip mode |
| A2 | दिल्ली | Delhi | 0.964 | 172 | 188 | Close F0, high sim |
| A3 | मेरा नाम | mera naam | 0.979 | 167 | 182 | High sim despite F0 gap |
| A4 | पानी | paani | 0.908 | 194 | **93** | Mode C confirmed |
| A5 | कितना | kitna | 0.907 | 183 | **93** | Mode C confirmed |
| A6 | भाई | bhai | 0.997 | 93 | 94 | Both 93 Hz short-clip mode |
| A7 | धन्यवाद | dhanyavaad | **0.887** | 177 | 170 | **Below baseline** |
| A8 | नमस्ते | namaste | 0.935 | 179 | 147 | Above baseline |
| **Mean matched** | | | **0.947** | | | |
| **Baseline (unrelated Deva pairs)** | | | **0.895** | | | |
| **Delta** | | | **+0.052** | | | |

**Key revision from v1:** A7 (dhanyavaad) voiced MFCC sim = 0.887, which is **below
the 0.895 baseline**. The v1 claim of "partial phoneme access for high-frequency
romanized words" was based on F0 similarity alone (170 vs 177 Hz). The voiced MFCC
does not support that claim for A7. A8 (namaste, 0.935) remains marginally above
baseline. The F0 similarity for A7 appears coincidental, not a sign of shared
phoneme content.

**F0 groupings — Roman inputs (unchanged from v1):**

| Group | Test IDs | F0 | Interpretation |
|-------|---------|-----|----------------|
| Failure-mode Roman | A4_roman, A5_roman | ~93 Hz | Mode C: undertrained ASCII embeddings → low-pitch garbage attractor |
| Both short-clip 93 Hz | A1, A6 pairs | ~93 Hz | Devanagari and Roman both in short-clip low-energy mode; high sim is template-driven |
| Near-Devanagari F0 | A7_roman (170 Hz), A8_roman (147 Hz) | 147–170 Hz | F0 close but MFCC sim at or below baseline; F0 similarity insufficient evidence for phoneme access |

### Test B — /k/ onset consistency within Hindi

**v1 result (invalidated):** mean 0.985, std 0.014 — degenerate; all comparisons
were silence vs silence due to Bug 2 above.

**v2 result (onset-50ms after silence strip, C1–C12):**

| Clip | Word | Speech onset | F0 | /k/ vowel context |
|------|------|-------------|-----|-------------------|
| B1 | कल | 0 ms | 93 Hz | /k/ + /ʌ/ (back-low) |
| B2 | कान | 0 ms | 93 Hz | /k/ + /aː/ (back-low) |
| B3 | किताब | 293 ms | 121 Hz | /k/ + /ɪ/ (front) |
| B4 | कुत्ता | 101 ms | 162 Hz | /k/ + /ʊ/ (back-round) |
| B5 | केला | 69 ms | 165 Hz | /k/ + /eː/ (mid-front) |
| B6 | कोल्ड | 219 ms | 219 Hz | /k/ + /oː/ (mid-round) |
| B7 | क्या | 0 ms | 93 Hz | /kj/ cluster |
| B8 | कितना अच्छा | 176 ms | 196 Hz | /k/ + /ɪ/ (longer context) |

Pairwise onset-50ms MFCC similarities (C1–C12): **mean 0.827, std 0.103**  
Range: 0.650 (B5_B6) – 0.998 (B2_B7). No negative values. Distribution is
unimodal (0 pairs < 0).

Selected pairs:
- B1_B2: 0.997, B1_B7: 0.995, B2_B7: 0.998 — all 93 Hz /k/ variants, very similar
- B3_B4: 0.881, B3_B6: 0.878 — cross-vowel, moderate similarity
- B5_B6: 0.650, B5_B8: 0.968, B4_B5: 0.681 — B5 (केला) is the most distinct onset

**F0 coarticulation pattern (unchanged — phonetically valid across both analyses):**

| /k/ + vowel context | Clips | F0 range |
|---------------------|-------|---------|
| /k/ + /ʌ/, /aː/ (back-low) | B1 (कल), B2 (कान) | 91–93 Hz |
| /kj/ cluster | B7 (क्या) | 92 Hz |
| /k/ + /ɪ/, /ʊ/, /eː/, /oː/ (front/round) | B3–B6 | 121–211 Hz |
| /k/ in longer context | B8 (कितना अच्छा) | 196 Hz |

F0 varies systematically by vowel context — coarticulation pattern confirms the
phonological organization finding. v2 MFCC now also supports this: mean 0.827
across all /k/ contexts, with no pair falling below 0.60.

### Test C — Cross-language /k/ phoneme transfer

**v1 result (invalidated):** all similarities = 1.0 — degenerate due to Bug 1
(C0 dominance) and Bug 2 (silence windows). Root cause confirmed: C1 onset-100ms
vector has C0 = −1016 (silence); after stripping silence, C1 and C4 have L2
distance = 66.7 — they are genuinely different vectors.

**v2 result (onset-100ms after silence strip, C1–C12):**

| Clip | Text | Context | Speech onset | F0 |
|------|------|---------|------------|-----|
| C1 | कल मैं जाऊंगा | Hindi Deva | 165 ms | 176 Hz |
| C2 | मेरा computer है | Mixed Roman | 203 ms | 181 Hz |
| C3 | kal main jaunga | Roman Hindi | 181 ms | 204 Hz |
| C4 | Cat is sitting | Pure English | 229 ms | 175 Hz |
| C5 | कैसे हो? | Hindi Deva | 112 ms | 224 Hz |
| C6 | Coffee पीते हो? | Mixed Roman | 192 ms | 230 Hz |
| C7 | kya tum theek ho? | Roman Hindi | 272 ms | 215 Hz |
| C8 | Karen और मैं | Mixed Roman | 144 ms | 174 Hz |

Selected pairwise onset-100ms MFCC sims (C1–C12):

| Pair | Sim | Notes |
|------|-----|-------|
| C3_C8 | 0.994 | Roman Hindi / Mixed Roman — highest pair |
| C4_C6 | 0.993 | English / Mixed Roman |
| C3_C6 | 0.968 | Roman Hindi / Mixed Roman |
| C4_C8 | 0.978 | English / Mixed Roman |
| C1_C4 | 0.926 | Hindi Deva / English |
| C1_C5 | 0.901 | **within** Hindi Deva |
| C2_C3 | 0.724 | Mixed Roman / Roman Hindi |
| C3_C7 | 0.604 | **within** Roman Hindi — lowest pair |
| C7_C8 | 0.664 | Roman Hindi / Mixed Roman |

Clustering (2-cluster): {C1:1, C2:2, C3:1, C4:1, C5:2, C6:1, C7:2, C8:1}  
Within Hindi-Deva sim: 0.901  
Within English sim: 0.856  
Between Hindi/English sim: **0.916** — *higher* than within-group

**Tokenization finding (unchanged):** The model accepts pure English input
("Cat is sitting") without error and produces 1.131s of audio. IndicF5's
tokenizer does not reject ASCII characters — they pass through to the
undertrained embedding subspace.

---

## Section 2: Interpretation Per Test

### Test A — Cross-script homophone similarity

**Outcome: WEAK_SIGNAL — delta = +0.052 (voiced MFCC C1–C12). Same
classification as v1, but the internal structure has changed.**

- A4/A5 (paani/kitna Roman): confirmed as real outliers, not analysis artifacts.
  Roman inputs hit Mode C (F0 ≈ 93 Hz) vs Devanagari at 183–194 Hz. Similarity
  0.907–0.908 is above baseline only because the voiced MFCC spectral shape is
  partially shared even when pitch differs.
- A7 (dhanyavaad): sim = 0.887, **below the 0.895 baseline**. The v1 claim of
  "partial phoneme access" for this word based on F0 similarity (170 vs 177 Hz)
  is not supported by voiced MFCC. Retracted.
- A1/A6 (कल/kal, भाई/bhai): sims 0.997 — both pairs in the 93 Hz short-clip
  mode regardless of script. High similarity reflects a shared duration-driven
  template, not phoneme content.
- The remaining high pairs (A2, A3, A8) have genuine spectral similarity; whether
  this reflects shared phoneme content or reference-audio imprinting is unclear.

**Conclusion for Test A (v2):** Predominantly grapheme-bound behavior for novel
Roman words. The v1 claim of "partial phoneme access for dhanyavaad/namaste" is
retracted — A7's voiced MFCC sim falls below baseline. A8 (namaste, 0.935)
remains marginally above baseline but is insufficient alone. F0 similarity for
these words may reflect prosodic patterns shared with the reference audio rather
than phoneme-mediated access.

### Test B — /k/ phoneme consistency within Hindi

**Outcome (v2): CONSISTENT_K — mean onset-50ms MFCC sim = 0.827 > 0.70 threshold.**

With silence stripped and C0 excluded, the /k/ onset across all eight vowel
contexts shows genuine spectral consistency:
- Mean 0.827, std 0.103 — unimodal, no negative pairs
- All 28 pairwise similarities are positive (range 0.650–0.998)
- The F0 coarticulation pattern is corroborated by the MFCC evidence

The lowest pairs involve B5 (केला, /k/+/eː/) as the most spectrally distinct
/k/ onset. The highest pairs are within the back-vowel group (B1/B2/B7, all
93 Hz). The within-group structure reflects vowel coarticulation, consistent
with phoneme-mediated organization.

**Conclusion for Test B (v2):** The Devanagari /k/ phoneme shows strong spectral
consistency (mean 0.827) across diverse vowel contexts once silence is removed.
Both the MFCC and F0 evidence support phoneme-mediated organization within the
Devanagari space. This is a stronger positive result than the F0-only analysis
in v1 allowed.

### Test C — Cross-language /k/ phoneme transfer

**Outcome (v2): MIXED_OR_UNCLEAR — MFCC now non-degenerate; structure does not
support language-segregation.**

After fixing the silence bug, C1 and C4 have L2 distance = 66.7 (not identical).
Pairwise sims range from 0.604 to 0.994. The 2-cluster assignment does not
separate by language:
- C7 (Roman Hindi "kya tum theek ho?") is most isolated — lowest sims with C3
  (another Roman Hindi clip, 0.604) and C8 (Mixed, 0.664)
- Between-group Hindi/English sim (0.916) is HIGHER than within Hindi-Deva
  (0.901) — opposite of language-segregation
- C3_C8 (Roman Hindi / Mixed Roman) sim = 0.994 — highest pair in Test C

The data do not support language-specific phoneme inventories. The absence of
language clustering and the high between-group similarity are consistent with
a single undertrained embedding subspace that produces similar spectral patterns
regardless of script/language context.

**Conclusion for Test C (v2):** No language segregation. The between-group
similarity exceeding within-group similarity suggests language-agnostic (or more
precisely, language-indifferent) behavior in the ASCII/Roman embedding subspace.
C7's outlier status (low sim to all other clips) warrants investigation — it
may produce a qualitatively different acoustic output that deserves manual
listening.

---

## Section 3: Synthesis (v2)

**Overall classification: PHONEME-MEDIATED within Devanagari (strengthened) /
GRAPHEME-BOUND for Roman inputs (unchanged) / "Partial access" claim retracted**

1. **Within Devanagari: phoneme-mediated (now supported by both F0 and MFCC).**
   Test B v2 shows /k/ onset spectral consistency mean 0.827 (unimodal, all pairs
   positive) across 8 distinct vowel contexts, corroborating the F0 coarticulation
   pattern. Two independent measures now agree on phoneme-mediated organization
   within the Hindi Devanagari space.

2. **For novel Roman input: grapheme-bound behavior.** Most Roman words produce
   the ~93 Hz failure-mode output regardless of phoneme content. The ASCII
   embedding subspace is so undertrained that it doesn't connect to the Devanagari
   phoneme layer for novel inputs.

3. **"Partial phoneme access for high-frequency romanized words" — RETRACTED.**
   v1 claimed dhanyavaad and namaste showed partial phoneme access based on F0
   similarity. v2 shows dhanyavaad's voiced MFCC sim (0.887) is below the 0.895
   baseline. F0 similarity for these words was a coincidence, not evidence of
   phoneme access. The claim is retracted; all Roman inputs should be treated as
   going through the same undertrained embedding path until stronger evidence is
   available.

4. **Test C: no language segregation.** Between-group Hindi/English sim (0.916)
   exceeds within-group Hindi-Deva sim (0.901). The model does not maintain
   language-specific phoneme inventories — it has one shared (undertrained) ASCII
   path that produces language-indifferent output for Roman/English input.

The Mode C explanation holds, but point 3 removes a claimed exception: IndicF5's
ASCII embedding subspace is uniformly undertrained; there is no evidence of
preferential access for any subset of common Roman words from the probe data.

---

## Section 3a: A4/A5 sanity check (v2)

A4 and A5 were the "low similarity outliers" in v1. They are **real findings,
not analysis artifacts**:

| Pair | Voiced MFCC sim | Deva F0 | Roman F0 | Diagnosis |
|------|----------------|---------|---------|-----------|
| A4 पानी/paani | 0.908 | 194 Hz | **93 Hz** | Mode C: Roman hits garbage attractor |
| A5 कितना/kitna | 0.907 | 183 Hz | **93 Hz** | Mode C: Roman hits garbage attractor |
| A7 धन्यवाद/dhanyavaad | 0.887 | 177 Hz | 170 Hz | F0 match but sim **below baseline** |
| A8 नमस्ते/namaste | 0.935 | 179 Hz | 147 Hz | Marginally above baseline |

Counterintuitively, A4/A5 (Mode C, huge F0 divergence) have *higher* MFCC sim
than A7 (close F0). This is because: voiced Mode C output still produces
speech-like spectral content; the voiced frames share some reference-audio
spectral shape with the Devanagari output. A7's longer Roman output (87 voiced
frames vs 53 Devanagari) introduces duration mismatch that reduces the voiced
MFCC mean. The sim difference is small (0.907 vs 0.887) and within the noise
floor of this experiment.

**For manual listening priority:** C7 ("kya tum theek ho?") is the highest-
priority clip to listen to — it is the outlier in Test C with the lowest pairwise
sims (0.604–0.731 to other clips), suggesting it may produce qualitatively
different output worth documenting.

---
   in F0 to their Devanagari equivalents. The access path exists for these specific
   lexical items — consistent with interpolation 2/3 (phoneme-mediated with some
   ASCII access paths trained for common words).

**The Mode C explanation holds:** IndicF5 has Devanagari phoneme representations
that are well-organized and internally consistent. ASCII/Roman characters mostly
fail to access these representations — not because phoneme representations are
absent, but because the ASCII→phoneme embedding mapping is undertrained (with
exceptions for high-frequency romanized words seen during training). IndicXlit
preprocessing works by routing Roman input through Devanagari, thus bypassing
the undertrained ASCII access path entirely.

---

## Section 4: Implications for Path B

**The phoneme representation exists — use it through Devanagari.**

The finding that Devanagari-conditioned /k/ shows phonological organization
(coarticulation by vowel context) means PL-BERT-style phoneme conditioning IS
exploitable — but only after input is normalized to Devanagari. Feeding Roman or
English text directly to a phoneme-conditioning layer will fail for the same
reason Mode C failed: the ASCII embedding subspace doesn't connect to the phoneme
layer.

**Concrete Path B guidance:**

| If Path B uses... | Viability | Condition |
|-------------------|-----------|-----------|
| PL-BERT over Devanagari text | ✅ High | Input must be IndicXlit-preprocessed first |
| PL-BERT over Roman/English text | ✗ Low | Same ASCII access-path problem as Mode C |
| External G2P (misaki/espeak-ng) producing Devanagari phoneme sequences | ✅ Viable | If G2P output is Devanagari-script phoneme tokens |
| External G2P producing IPA/ARPABET tokens | ⚠ Unknown | Depends whether IPA chars are in vocab |
| Direct Roman→phoneme tokenization | ✗ Unlikely | Would need fine-tuning to train the missing embedding subspace |

**LoRA fine-tuning target if Path B includes training:** Focus on the ASCII
character embedding subspace (LoRA on the text encoder's embedding table for
ASCII positions). This would teach the model to route ASCII tokens through the
existing Devanagari phoneme representations rather than into the random embedding
subspace. Training data needed: paired (Roman text, Devanagari-preprocessed audio)
where the Roman text is fed raw (without IndicXlit) and the audio is from the
well-trained Devanagari pipeline.

**This probe does NOT change Path A.** IndicXlit preprocessing is still the
correct production approach — it solves Mode C by routing around the undertrained
ASCII access path, consistent with the phoneme representations existing
behind Devanagari characters.

---

## Section 5: Implications for Direction 1

Direction 1 (`05_phonetic_probe`) result: **Outcome A — Phonetics-sensitive (6/6)**  
(auto-metrics underestimated; ear evaluation is the authoritative source; see D1 FINDINGS.md)

**D1 × D2 joint interpretation — actual row:**

| D1 result | D2 result | Joint interpretation |
|-----------|-----------|---------------------|
| **D1 sensitive** ✓ | **D2 phoneme-mediated within Devanagari** ✓ | **→ Row 1 applies** |
| D1 insensitive | D2 phoneme-mediated (partial) | (not this row) |
| D1 sensitive | D2 grapheme-bound | (not this row) |
| D1 insensitive | D2 grapheme-bound | (not this row) |

**Row 1 interpretation: Path B via Devanagari-input PL-BERT is viable.
Direction 3 (pronunciation dictionary) is confirmed worth pursuing.**

Specific joint conclusions:

1. **The model responds to fine phonetic distinctions in Devanagari input (D1)
   AND has well-organized internal phoneme representations for Devanagari (D2).**
   These two findings together mean the text→phoneme mapping is bidirectionally
   intact within the Devanagari space: the model both reads fine-grained input
   distinctions AND produces phonologically organized output. A pronunciation
   dictionary that corrects input at the Devanagari level can expect reliable
   acoustic output.

2. **Roman/ASCII input bypasses the phoneme layer entirely (D2), confirmed as
   the mechanism for Mode C failures (D1 S5).** D1 directly observed this in
   sentence 5: Roman "office" → garbled output. D2 explains why: the ASCII
   embedding subspace doesn't route through the Devanagari phoneme representations.
   IndicXlit preprocessing is the correct architectural fix (routes Roman → Devanagari
   before hitting the model).

3. **Halant marks have sub-phonemic but audible effects (D1 S2).** This is a
   nuance D2 didn't probe — D2 tested cross-script representations, not within-
   script sub-phonemic markers. D1 shows the model produces cleaner consonant
   clusters when halant is explicit, but the effect doesn't reach ASR level.
   Dictionary entries for heavy-cluster words (e.g., words with ल्+consonant,
   न्+consonant) should include explicit halant for best output quality.

4. **Aspiration is reliably audible (D1 S4 confirmed by ear).** D2's /k/ probe
   showed consistent onset features (mean 0.827 MFCC similarity across vowel
   contexts). D1 shows the aspirated/unaspirated distinction is audible to a
   native listener even in 0.65s clips. Together: the model's Devanagari /k/
   representations are both internally consistent and externally distinguishable.

---

## Section 6: Caveats (v2)

**Fixed in v2 (no longer caveats):**
- ~~MFCC analysis invalidated by silent lead-ins~~ — fixed by speech-onset stripping
- ~~Test C all-1.0 degenerate~~ — fixed by C0 exclusion + onset stripping
- ~~Test B bimodal distribution masking real signal~~ — fixed; now unimodal mean 0.827
- ~~"Partial phoneme access" claim for dhanyavaad~~ — retracted based on MFCC evidence

**Remaining caveats:**

1. **Reference audio spectral dominance** raises the baseline MFCC similarity to
   0.895, keeping the Test A delta small (+0.052). A multi-reference design
   (different ref clips per input) would test whether the similarity pattern holds
   without the shared spectral envelope.

2. **Speech onset detector is heuristic.** `librosa.effects.split(top_db=40)`
   may misplace the onset boundary, especially for clips with low-energy onsets.
   A forced-aligner (MFA, WhisperAlign) would give exact phoneme boundaries and
   is the right tool for a follow-up /k/-burst isolation experiment.

3. **F0 + MFCC are phonetic proxies**, not direct measurements of model-internal
   phoneme representations. "Phoneme-mediated" here means "acoustically consistent
   with phoneme organization," not "the model has an explicit phoneme layer."

4. **n=8 per test.** Statistical confidence is low. The Test B result (mean 0.827
   across vowel contexts) should be replicated with ≥20 items before drawing strong
   conclusions about /k/ consistency vs other phonemes.

5. **C7 ("kya tum theek ho?") is an unexplained outlier in Test C.** Lowest pairwise
   sims of any Test C clip (0.604–0.731). Manual listening is needed to determine
   whether it produces qualitatively different output or the onset detection
   misaligned on this clip.

6. **"Cat is sitting" (C4) produced valid audio** (1.131s, F0 = 175 Hz, no error).
   This means IndicF5 does not hard-reject pure-English input. Whether the audio
   content is phonetically meaningful or garbled requires manual listening — not
   assessed here.

---

## Appendix: Raw data

**v2 (current):**
- `acoustic_analysis_v2.json` — full MFCC vectors + F0 + speech onset per clip
- `scores/analysis_results_v2.json` — v2 analysis (C0-excluded, onset-aligned)
- `scripts/extract_acoustics_v2.py` — extraction with speech-onset detection
- `scripts/analyse_results_v2.py` — analysis with voiced MFCC, onset windows

**v1 (archived, do not use for conclusions):**
- `acoustic_analysis.json` — v1 features (C0 included, silence windows)
- `scores/analysis_results.json` — v1 outputs (bimodal B, degenerate C)
- `log.json` — Kaggle inference log (32 entries, 32 ok, 0 errors)
- `wavs/` — 32 WAV files (unchanged)
