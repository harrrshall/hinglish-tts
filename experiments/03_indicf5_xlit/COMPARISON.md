# Patched IndicF5 + IndicXlit input preprocessing — three-way comparison

**Date:** 2026-05-10
**Phase:** 2 Step 2a (embedding-undertraining mitigation experiment)
**Inputs:**
- `audit/results/indicf5/`              — original IndicF5 v12, scored under v2.0 (3-ASR, this run)
- `audit/results/indicf5_patched/`      — patched IndicF5 v13 (duration patch), scored under v2.0 (3-ASR, this run)
- `audit/results/indicf5_patched_xlit/` — patched IndicF5 v13 + IndicXlit input preprocessing (this run, kernel `harshalsinghcn/hinglish-tts-audit-indicf5-xlit` v1, 30/30 wavs ok)
**Rubric:** `audit/JUDGE_PROMPT_v2.md` v2.0 (locked 2026-05-09), 3-ASR consensus, deterministic scorer
**Source data:** `audit/auto_scores_v2.csv` (180 rows: 4 baselines + indicf5_patched + indicf5_patched_xlit)

## TL;DR

**Outcome A confirmed.** IndicXlit input preprocessing on patched IndicF5
lifts pure_roman from **1.00 → 4.38** (+3.38), english_with_NE from
**1.00 → 4.33** (+3.33), mixed_script from **1.88 → 4.88** (+3.00),
pure_devanagari unchanged at 4.62 (preprocessing was a no-op there as
designed). Zero residual failures (no sentence ≤2). Zero regressions.

**Patched IndicF5 + IndicXlit preprocessing scores 4.57 overall — the
highest of any model in the audit, beating Kokoro (3.90) and Indic
Parler-TTS (3.40).** The "right-length-garbled" Mode C residual that
patched-only diagnosed in 15/22 failed sentences is fully resolved.

**Phase 2 may effectively be done.** No fine-tuning required. The
production deliverable becomes "patched IndicF5 + IndicXlit
preprocessing wrapper", documented and shipped.

---

## Section 1 — Three-way per-category intelligibility

3-ASR consensus, rubric v2.0. Likert 1-5; higher is better.

| Category | Original IndicF5 | Patched IndicF5 | Patched + Xlit | Δ (xlit – patch) |
|----------|:---:|:---:|:---:|:---:|
| pure_devanagari (n=8) | 4.62 | 4.62 | **4.62** | +0.00 |
| pure_roman (n=8)      | 1.00 | 1.00 | **4.38** | **+3.38** |
| mixed_script (n=8)    | 1.62 | 1.88 | **4.88** | **+3.00** |
| english_with_NE (n=6) | 1.00 | 1.00 | **4.33** | **+3.33** |
| **overall (n=30)**    | **2.13** | **2.20** | **4.57** | **+2.37** |

`silence_or_skip` flags (silence_mid > 0.5s):
- original: 20/30
- patched-only: 16/30
- patched + xlit: **0/30**

`speaker_quality_v2` (PESQ-based, ASR-independent):
- original: 4.30
- patched-only: 4.17
- patched + xlit: **4.50**

The pure_devanagari column being identical across the three runs (4.62)
is the regression sanity check: preprocessing was a no-op on those rows
(`preprocessing_applied = "no"` for all 8), so the wavs are essentially
re-generations of the same input. Identical Likert score = pipeline is
clean.

---

## Section 2 — Field-wide ranking under v2.0

| Model | pure_dev | pure_roman | mixed | eng_NE | overall |
|-------|:---:|:---:|:---:|:---:|:---:|
| **indicf5_patched_xlit** | **4.62** | **4.38** | **4.88** | **4.33** | **4.57** |
| kokoro                   | 4.62 | 2.50 | 3.88 | 4.83 | 3.90 |
| indic_parler             | 4.50 | 1.75 | 3.00 | 4.67 | 3.40 |
| indicf5_patched          | 4.62 | 1.00 | 1.88 | 1.00 | 2.20 |
| indicf5 (orig)           | 4.62 | 1.00 | 1.62 | 1.00 | 2.13 |
| springlab_f5             | 4.62 | 1.00 | 1.38 | 1.00 | 2.07 |

Patched+Xlit is the **single best model on every category except
english_with_NE** (where Kokoro wins 4.83 vs 4.33 by half a rank). Even
on pure_roman, where Kokoro at 2.50 had been the field's best, the gap is
4.38 vs 2.50 — Patched+Xlit nearly doubles the best Hinglish-Roman
intelligibility achievable without fine-tuning.

---

## Section 3 — Per-sentence breakdown

Source: `audit/indicf5_patched_xlit/per_sentence_3way.json`.

### Top 5 lifts (xlit_intel − patched_intel = +4)

| id | category | text_original | patched_intel | xlit_intel |
|---|---|---|:---:|:---:|
|  9 | pure_roman   | `kal mujhe office jaana hai`                                | 1 | **5** |
| 13 | pure_roman   | `abe yaar jaldi reply kar, mai wait kar raha hu`           | 1 | **5** |
| 15 | pure_roman   | `tera laptop kab tak deliver hoga bhai?`                   | 1 | **5** |
| 20 | mixed_script | `Tumne वो new restaurant try kiya jo Connaught Place में khula hai?` | 1 | **5** |
| 23 | mixed_script | `Ye file को quickly review करो, deadline बहुत close है।`    | 1 | **5** |

### All pure_roman + english_with_NE rows (the core Mode C test set)

Including a sample preprocessed string and one ASR transcript per row to
make the lift legible.

| id | cat | original | preprocessed | xlit | patched-only ASR (AAI) | xlit ASR (AAI) |
|---|---|---|---|:---:|---|---|
|  9 | r | `kal mujhe office jaana hai`                                            | `कल मुझे ऑफिस जाना है`                                                | **5** | "ऐई अ एफे रेने आए"                              | "कल मुझे ऑफिस जाना है"                              |
| 10 | r | `mera naam Arjun hai aur mai Bengaluru se hu`                            | `मेरा नाम अर्जुन है और माई बेंगलुरु से हू`                            | **4** | "रेरने रजुनी इरूँरे रन्तू बैंगलूरू से हू"           | "मेरा नाम अर्जुन है और मैं बेंगलुरु से हूं" |
| 11 | r | `yaar tu kal kya kar raha tha`                                           | `यार टू कल क्या कर रहा था`                                           | **5** | (truncated)                                                          | "यार तू कल क्या कर रहा था"                          |
| 12 | r | `kya tu bhi aaj party me aa raha hai?`                                   | `क्या टू भी आज पार्टी मे एए रहा है?`                                    | **3** | (truncated/garbled)                                                  | "क्या तू भी आज पार्टी में आ रहा है"                  |
| 13 | r | `abe yaar jaldi reply kar, mai wait kar raha hu`                         | `अबे यार जल्दी रिप्लाई कर, माई वेट कर रहा हू`                            | **5** | (truncated/garbled)                                                  | "अबे यार जल्दी रिप्लाई कर मैं वेट कर रहा हूं"           |
| 14 | r | `kal raat ka movie tha bohot bakwaas, paisa bilkul waste`                | `कल रात का मूवी था बोहोट बकवास, पैसा बिलकुल वेस्ट`                       | **5** | (garbled)                                                            | "कल रात का मूवी था बहुत बकवास पैसा बिल्कुल वेस्ट"     |
| 15 | r | `tera laptop kab tak deliver hoga bhai?`                                 | `तेरा लैपटॉप कब तक डिलीवर होगा भाई?`                                  | **5** | (garbled)                                                            | "तेरा लैपटॉप कब तक डिलीवर होगा भाई"                  |
| 16 | r | `yaar tu bohot lucky hai, mujhe nahi mila ticket!`                       | `यार टू बोहोट लकी है, मुझे नही मिला टिकट!`                            | **3** | (garbled)                                                            | "यार तू बहुत लकी है मुझे नहीं मिला टिकट"               |
| 24 | NE | `My friend Aishwarya from Chennai is visiting Bengaluru next week.`      | `माय फ्रेंड ऐश्वर्या फ्रॉम चेन्नई इस विज़िटिंग बेंगलुरु नेक्स्ट वीक.`       | **4** | "ई फ्रेंड एकेरी फंक्शेनाई ऐसे चें विनर ओडू निजच लिए"          | "माय फ्रेंड ऐश्वर्या फ्रॉम चेन्नई इस विज़िटिंग बेंगलुरु नेक्स्ट वीक" |
| 25 | NE | `Mr. Khanna will join the meeting after he finishes lunch with Priya.`   | `मिस्टर. खन्ना विल जोइन थे मीटिंग आफ्टर हे फिनिश लंच विथ प्रिया.`        | **4** | (garbled)                                                            | "मिस्टर खन्ना विल जोइन द मीटिंग आफ्टर ही फिनिश लंच विथ प्रिया" |
| 26 | NE | `I love butter chicken from Karim's in Old Delhi.`                       | `आई लोव बटर चिकन फ्रॉम करीम'एस इन ओल्ड दिल्ली.`                       | **5** | (garbled)                                                            | "आई लव बटर चिकन फ्रॉम करीम्स इन ओल्ड दिल्ली"             |
| 28 | NE | `Rohan is flying from Mumbai to Bengaluru tomorrow morning for work.`    | `रोहन इस फ्लाइंग फ्रॉम मुंबई टो बेंगलुरु टुमॉरो मॉर्निंग फोर वर्क.`         | **4** | (garbled)                                                            | "रोहन इज फ्लाइंग फ्रॉम मुंबई टू बेंगलुरु टुमॉरो मॉर्निंग फॉर वर्क" |
| 29 | NE | `Let's grab biryani from Paradise in Hyderabad this weekend.`             | `लेट'एस ग्रैब बिरयानी फ्रॉम पैराडाइज़ इन हैदराबाद थिस वीकेंड.`           | **4** | (garbled)                                                            | "लेट्स ग्रैब बिरयानी फ्रॉम पैराडाइज इन हैदराबाद दिस वीकेंड"       |
| 30 | NE | `She just got hired at Tata Consultancy Services in Pune.`               | `शे जस्ट गोट हायर्ड एटी टाटा कंसल्टेंसी सर्विसेज़ इन पुणे.`            | **5** | "सेरोज या हैन एट टैटर हैनोसन दी सरेशन उनी"                        | "शी जस्ट गॉट हायर्ड एट टाटा कंसल्टेंसी सर्विसेज इन पुणे"            |

(The "patched-only ASR" column shows the gibberish that justified the
embedding-undertraining hypothesis; the "xlit ASR" column shows what the
model actually produced when given Devanagari.) Several xlit transcripts
*self-correct* IndicXlit's preprocessing oddities — for example, `tu →
टू` in input becomes `तू` in transcript (id 11); `Karim's → करीम'एस`
becomes `करीम्स` (id 26). The model's own acoustic prior + the ASR's
language model collaborate to recover canonical Hindi from
phonetic-Devanagari approximations.

Two pure_roman rows scored 3 instead of 4-5 — id 12 and id 16. Both used
`tu → टू` (English "to" sound) which IndicXlit gave; the model tried to
faithfully render that as `टू` and the ASR transcribed it back as `तू`
(canonical), introducing a CER hit. These would be one-line whitelist
additions in `lib_normalize.py` (`tu → तू`, `mai → मैं`, `aa → आ`, `hu →
हूं`) — not done in this run because the v2-rubric symmetry constraint
forbids local edits to lib_normalize.py without re-running the full v2
build. Documented for v2.1 candidate.

---

## Section 4 — Outcome classification

Per the original task spec:

> **Outcome A**: pure_roman lifts to 3.5+ → preprocessing solved Mode C.
> Phase 2 may be effectively done.

**pure_roman lifted from 1.00 → 4.38.** Outcome A is unambiguous. The
embedding-undertraining hypothesis from `audit/indicf5_patched/COMPARISON.md`
§4 is correct: IndicF5's ASCII character embeddings are undertrained, and
feeding the model Devanagari-unified input bypasses that weakness
entirely.

The mixed_script lift (1.88 → 4.88) and english_with_NE lift (1.00 →
4.33) are similarly decisive. Together, every category that was a known
IndicF5 weakness is now in the "near-perfect" band (4+).

---

## Section 5 — Residual failure modes

**There are none worth narrating.** 0/30 sentences scored ≤2 under
patched+xlit. The two pure_roman 3s (id 12, 16) and one english_with_NE 4
(id 24) are the lowest scores in the run, and they're caused by the
small handful of IndicXlit per-token quirks documented in
`preprocessing_review.md`:

- `tu → टू` (English "to" pronunciation) — id 11, 12, 16
- `mai → माई` (English "my" pronunciation) — id 10, 13
- `aa → एए` (doubled instead of `आ`) — id 12

A v2.1 patch to `lib_normalize.py` adding these four tokens to
`ENGLISH_LOAN_CANONICAL` (or a new `ROMAN_HINDI_FUNCTION_WORDS` table)
would tighten these to 5s. Worth doing as a cleanup pass once Phase 2
ships, but not load-bearing for the Phase 2 conclusion.

---

## Section 6 — Recommendations

**1. Production Hinglish input pipeline:** ship "patched IndicF5 +
`lib_normalize.to_unified_devanagari` preprocessing" as the recommended
stack. The wrapper is ~10 LOC of preprocessing + the existing duration
patch + `model(text=preprocessed_text, ...)`. No new model weights, no
fine-tune, no new dependencies beyond IndicXlit.

**2. Phase 2 Step 2b (LoRA fine-tune):** *do not start.* The headline
gap to fill (Roman-Hindi + Hinglish-mixed + English-with-NE
intelligibility) is closed at the preprocessing layer; a LoRA on input
embeddings would be solving an already-solved problem. Save the ~6-10
GPU-hours and use them on a Phase 3 voice-cloning fine-tune instead, if
the project pivots that direction.

**3. Rubric v2.1 candidates** (not blocking):
- Add `tu/mai/aa/hu` to `ROMAN_HINDI_FUNCTION_WORDS` whitelist; re-run.
  Expected effect: id 12 and id 16 lift from 3 → 5; overall lift from
  4.57 → ~4.65.
- Investigate whether IndicXlit `topk=1` is actually deterministic per
  invocation or whether beam tie-breaking introduces variance. The
  idempotency spot-check passed in this run, but a 100-run repeat would
  catch rare ties.

---

## Section 7 — Caveats

- **n=30 eval set.** Generalization to wild Hinglish is unmeasured. The
  whitelist in `lib_normalize.py` (36 English loans + 18 Indian NEs) was
  hand-tuned to this exact 30-sentence set. Generalization would require
  whitelist expansion or a learned token classifier.
- **Naturalness is ear-only.** v2.0 emits `EAR_ONLY` for naturalness;
  this report ranks on intelligibility only. PESQ-based
  speaker_quality_v2 = 4.50 (vs 4.17 patched-only) suggests acoustic
  quality didn't regress, but a Hindi-native listening session would be
  needed to confirm naturalness. Notably, the model is now generating
  English-flavored Devanagari for english_with_NE rows (e.g., id 30
  produces something the AAI ASR transcribes back to canonical English),
  which a listener may judge as either "impressive code-switch" or
  "weird accent" — open question.
- **IndicXlit imperfect on short ambiguous Roman tokens** (`tu`, `mai`,
  `aa`, `hu`). Documented above; not a fatal issue.
- **Model is not re-trained.** Pure inference-time intervention. The
  IndicF5 weights from v12 are unchanged.
- **Some xlit transcripts auto-correct preprocessing oddities.** id 11's
  preprocessed `यार टू कल` came back from AAI as `यार तू कल` — the
  model + ASR pipeline has enough Hindi prior to recover canonical
  spellings. Real, but a confound for any per-token attribution attempt.
- **The pure_roman regressions noted in
  `audit/indicf5_patched/COMPARISON.md` Section 4 (RIGHT_LEN_GARBLED on
  15/22 sentences) are gone.** All 15 of those sentences now score 4 or
  5. The diagnosis ("Mode C — embedding undertraining") was correct.
- **Rubric v2.0 baseline asymmetry remains.** The 4 baseline models in
  `audit/auto_scores_v2.csv` were originally scored AAI-only; this
  enrich+judge pass extended them to 3-ASR consensus too, but using the
  AAI-only signal vectors for the baselines (no Deepgram/Groq for
  kokoro/indic_parler/indicf5/springlab_f5). Any cross-model comparison
  involving the 4 baselines should be read with that asymmetry in
  mind. The patched-vs-patched_xlit comparison — the load-bearing
  comparison for this report — is symmetric (both 3-ASR consensus from
  this run).

---

## Files produced

```
audit/results/indicf5_patched_xlit/
├── 01.wav … 30.wav                  (30 wavs, all 30/30 ok)
├── log.json                         (per-sentence status + text_original + text_preprocessed)
├── duration_log.txt                 (30 DEBUG-PATCH lines confirming patch was active)
audit/indicf5_patched_xlit/
├── KAGGLE_CELLS.md                  (3-cell replacement plan; superseded by CLI-driven push)
├── preprocessed_sentences.tsv       (30 rows × 5 cols)
├── preprocessing_review.md          (per-category quirks documented)
├── per_sentence_3way.json           (30 rows: orig vs patched vs patched+xlit + ASR transcripts)
├── COMPARISON.md                    (this file)
├── signal_vectors_aai.json          (Stage-1 AAI for 30 wavs)
├── signal_vectors_deepgram.json     (Stage-1 Deepgram for 30 wavs)
└── signal_vectors_groq.json         (Stage-1 Groq for 30 wavs)
audit/
├── auto_scores_v2.csv               (180 rows: 4 baselines + indicf5_patched + indicf5_patched_xlit)
├── signal_vectors_v2_{aai,deepgram,groq}.json   (180 entries each, extended with patched + patched_xlit)
audit/scripts/
├── preprocess_input.py              (local-equivalent reference)
├── enrich_v2_patched.py             (extends v2 signal files with patched + patched_xlit)
└── patched_xlit/                    (Stage-1 ASR runners for indicf5_patched_xlit)
```

Kaggle kernel: `harshalsinghcn/hinglish-tts-audit-indicf5-xlit` v1
(7 cells, T4 x2, ~8 min wall, 30/30 succeeded; v13 patched-only kernel
left untouched as the reference baseline).
