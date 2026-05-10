# Preprocessing review — Phase 2 Step 2a

**Date:** 2026-05-10
**Source:** `preprocessed_sentences.tsv` (30 rows; 8 unchanged + 22 changed)
**Generator:** `audit/scripts/preprocess_input.py` invoking
`lib_normalize.to_unified_devanagari` (sha256 `26cb5c0a…`) — same function
used symmetrically by rubric v2.0 on ASR transcripts.

## Summary

Per-category preprocessing behaves as designed. **22/30 sentences changed,
8/30 (all `pure_devanagari`) unchanged.** No `pure_devanagari` row was
modified — the assertion in the script and the v2-symmetry property are
both intact. Idempotency spot-checks passed (id=17, id=24). No sentence is
broken in a way I'd call un-runnable. There are a handful of minor IndicXlit
quirks worth noting before scoring, listed by category below.

**Decision:** proceed with the Kaggle inference run. None of the issues
below cross the "5+ broken in unfixable ways" threshold from the task spec.

## pure_devanagari (8/8 unchanged)

All eight rows pass through `to_unified_devanagari` unchanged — they have
no ASCII alphabetic tokens for the function to act on. Devanagari
codepoints, punctuation, and whitespace pass through verbatim. **What we
expect:** when the patched IndicF5 sees these inputs, it should produce
near-identical audio to the existing `audit/results/indicf5_patched/`
outputs (preprocessing is a no-op here). The pure_devanagari column in the
upcoming COMPARISON.md is essentially a regression check — any drift
indicates ASR variance, not a real change.

## pure_roman (8/8 changed)

All eight Roman-Hindi sentences become full Devanagari. Whitelisted English
loans render canonically: `office → ऑफिस`, `Bengaluru → बेंगलुरु`,
`Arjun → अर्जुन`, `movie → मूवी`, `laptop → लैपटॉप`, `party → पार्टी`,
`reply → रिप्लाई`, `wait → वेट`, `lucky → लकी`, `ticket → टिकट`,
`deliver → डिलीवर`, `waste → वेस्ट`. Non-whitelisted Hindi-in-Roman
function words go through IndicXlit, with mostly-correct outputs
(`kal → कल`, `mujhe → मुझे`, `kar → कर`, `raha → रहा`, `tha → था`, `bhai →
भाई`, `mera → मेरा`, `naam → नाम`, `aur → और`, `bhi → भी`, `kya → क्या`,
`yaar → यार`, `jaldi → जल्दी`, `abe → अबे`).

**Quirks worth flagging** (none blocking):
- `tu → टू` (id 11, 12, 16) — IndicXlit treats Roman "tu" as the English
  word "to" (`टू`); the canonical Hindi pronoun "तू" never surfaces. This
  could shift the model's prosody on "तू" forms.
- `mai → माई` (id 10, 13) — same pattern; "mai" gets the English "my"
  sound rather than the canonical Hindi "मैं" / "मई".
- `aa → एए` (id 12) — the bare two-letter "aa" produces a doubled `एए`
  rather than `आ`. Visually awkward but likely still audible as approx-`आ`.
- `hu → हू` (id 10, 13) — close to canonical `हूं` but loses the nasal.

These four token-level shifts are systematic IndicXlit behaviour on short
ambiguous Roman tokens. They would each be one-line whitelist additions in
`lib_normalize.py` if we wanted to lock them down, but doing so now would
break v2-rubric symmetry (rubric v2.0 transcripts go through the same
function), so leaving them as-is is the right call. Documented for
COMPARISON.md residual analysis.

## mixed_script (8/8 changed)

Roman tokens become Devanagari; Devanagari tokens already in the input pass
through. Whitelist hits dominate (English loans like `presentation →
प्रेज़ेंटेशन`, `tomorrow → टुमॉरो`, `nervous → नर्वस`, `please → प्लीज़`,
`homework → होमवर्क`, `restaurant → रेस्टोरेंट`, `try → ट्राई`, `event →
इवेंट`, `cancel → कैंसल`, `message → मैसेज`, `boss → बॉस`, `leave → लीव`,
`personal → पर्सनल`, `file → फाइल`, `quickly → क्विकली`, `review → रिव्यू`,
`deadline → डेडलाइन`, `close → क्लोज़`, `office → ऑफिस`, `log → लॉग`,
`lunch → लंच`, `new → न्यू`, `Connaught → कनॉट`, `Place → प्लेस`).

**Quirks worth flagging** (none blocking):
- `an → एएन` (id 17) — IndicXlit reads "an" as the spelled-out letters
  "A.N." rather than the article. "बट ट्राफिक विल बे एएन इश्यू" is
  technically correct Devanagari but reads awkward; a Hindi listener
  would parse this as "be a-n issue" sound-by-sound.
- `but → बट` (id 17) — phonetically matches English "but"; acceptable.
- `be → बे` (id 17) — IndicXlit chose `बे` over `बी`; minor.
- `kuch → कुच` (id 22) — close to canonical `कुछ` but misses the aspirated
  consonant `छ`. Audible as a slightly soft "kuch".
- `Bhai please → भाई प्लीज़` (id 19) — both whitelisted; clean.

Overall mixed_script preprocessing looks the cleanest of the three
non-Devanagari categories — most tokens are common Hinglish and hit the
whitelist directly.

## english_with_NE (6/6 changed) — Option A applied

Per the task spec, **Option A (full Devanagari with whitelist for NEs)** is
the design. Result: all proper nouns render canonically from the
`INDIAN_NE_CANONICAL` table (`Aishwarya → ऐश्वर्या`, `Chennai → चेन्नई`,
`Bengaluru → बेंगलुरु`, `Khanna → खन्ना`, `Priya → प्रिया`, `Mr → मिस्टर`,
`Karim → करीम`, `Old → ओल्ड`, `Delhi → दिल्ली`, `Mumbai → मुंबई`, `Rohan
→ रोहन`, `Hyderabad → हैदराबाद`, `Paradise → पैराडाइज़`, `Tata → टाटा`,
`Consultancy → कंसल्टेंसी`, `Services → सर्विसेज़`, `Pune → पुणे`). English
loans from `ENGLISH_LOAN_CANONICAL` also hit (`butter → बटर`, `chicken →
चिकन`, `lunch → लंच`, `tomorrow → टुमॉरो`, `biryani → बिरयानी`).

The remaining surrounding English words go through IndicXlit and produce
reasonable phonetic Devanagari for English: `My → माय`, `friend → फ्रेंड`,
`from → फ्रॉम`, `is → इस`, `visiting → विज़िटिंग`, `next → नेक्स्ट`, `week
→ वीक`, `will → विल`, `meeting → मीटिंग`, `after → आफ्टर`, `finish →
फिनिश`, `with → विथ`, `flying → फ्लाइंग`, `morning → मॉर्निंग`, `work →
वर्क`, `grab → ग्रैब`, `this → थिस`, `weekend → वीकेंड`, `just → जस्ट`,
`got → गोट`, `hired → हायर्ड`, `in → इन`.

**Quirks worth flagging** (none blocking):
- `Karim's → करीम'एस` (id 26) — the apostrophe-tokenizer in
  `lib_normalize` splits "Karim's" into ["Karim", "'", "s"]; "Karim" hits
  the NE whitelist (`करीम`), the apostrophe passes through, "s" gets
  IndicXlit-transliterated to `एस`. Audible as "Karim's" with a glottal
  break + "es" — close enough, but funky-looking.
- `Let's → लेट'एस` (id 29) — same pattern.
- `to → टो` (id 28) — IndicXlit gave `टो` over `टू`; minor.
- `at → एटी` (id 30) — gives a two-character render; functions as an
  approximate two-syllable "ay-tee".
- `love → लोव` (id 26) — the canonical English-in-Devanagari is `लव`;
  IndicXlit's `लोव` will sound like "loav" rather than "luv".

These are exactly the kind of "English-in-Devanagari is phonetic best-effort"
artifacts the task spec flagged as the test case for Outcome C ("IndicXlit
transliterates poorly enough"). Whether the model produces audible English
from these phonetic strings is the empirical question — the cleanest test
of the embedding-undertraining hypothesis is still to feed the patched
IndicF5 these inputs and see what comes out.

## What this means for COMPARISON.md

- **pure_devanagari**: should be a near-no-op; large delta indicates
  problem with the preprocessing pipeline or ASR variance.
- **pure_roman**: cleanest expected lift. Most tokens transliterated well;
  the `tu/mai/aa/hu` quirks may produce minor phoneme drift but the model
  has Devanagari to work with.
- **mixed_script**: should also lift cleanly; the `an → एएन` artifact in
  id 17 is worth listening for in the output wav.
- **english_with_NE**: highest-uncertainty category. The proper nouns
  render canonically (so Hindi-NE-pronunciation is plausible), but the
  English-as-phonetic-Devanagari interleaving is exactly what the
  hypothesis is testing. Listening will be informative on whether the
  model produces understandable English when fed phonetic Devanagari.

No sentences look so degraded that I'd skip the run. Proceeding with the
Kaggle inference cells in `KAGGLE_CELLS.md`.
