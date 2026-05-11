# Listening protocol — phonetic probe

**Instructions for the user (fill this in after the Kaggle run).**

Listen to the three variants for each sentence in order: a first, then b, then c. Listen to each one twice. Then answer the four questions per sentence.

**Do not read the `expected_audible_difference` column in `test_sentences.tsv` before listening.** Fill this form from what you actually hear. The agent will compare your answers to the expectations after you submit.

Each listening session takes approximately 15–20 minutes for all 6 sentences.

**Wav locations:** `experiments/05_phonetic_probe/wavs/`

---

## Sentence 1 — Nukta dot (filed under: does ज vs ज़ sound different?)

Play: `1a.wav` → `1b.wav` → `1c.wav`

| Question | Answer |
|---|---|
| Are 1a and 1b **audibly different**? | Y / N |
| If different, describe: | |
| Are 1a and 1c **audibly different**? | Y / N |
| If different, describe: | |
| Are 1b and 1c **audibly different**? | Y / N |
| If different, describe: | |
| Which variant has the clearest /z/ sound (like English "z")? | a / b / c / none |
| Which variant would you prefer for synthesizing "Zara"? | a / b / c / all-same |

---

## Sentence 2 — Schwa elision (filed under: do halant marks change rhythm?)

Play: `2a.wav` → `2b.wav` → `2c.wav`

| Question | Answer |
|---|---|
| Are 2a and 2b **audibly different**? | Y / N |
| If different, describe: | |
| Are 2a and 2c **audibly different**? | Y / N |
| If different, describe: | |
| Are 2b and 2c **audibly different**? | Y / N |
| If different, describe: | |
| Which variant sounds most natural for this Hindi sentence? | a / b / c / all-same |
| In 2b, does the consonant cluster in "खिल्ता" sound cleaner (less vowel between ल and त)? | Y / N / can't tell |

---

## Sentence 3 — Vowel length (filed under: does ि vs ी produce different duration?)

Play: `3a.wav` → `3b.wav` → `3c.wav`

| Question | Answer |
|---|---|
| Are 3a and 3b **audibly different**? | Y / N |
| If different, describe: | |
| Are 3a and 3c **audibly different**? | Y / N |
| If different, describe: | |
| Does 3b sound noticeably more drawn-out / stretched than 3a? | Y / N / slight / can't tell |
| Does 3a sound more clipped / rushed than 3c? | Y / N / slight / can't tell |
| Which sounds most like natural Hindi? | a / b / c / all-same |

---

## Sentence 4 — Aspiration (filed under: does ख vs क sound different?)

Play: `4a.wav` → `4b.wav` → `4c.wav`

| Question | Answer |
|---|---|
| Are 4a and 4b **audibly different**? | Y / N |
| If different, describe: | |
| In 4a, is there a clear breathy /kʰ/ sound at the start of "खाना" and "खाओ"? | Y / N |
| In 4b, is the consonant harder / less breathy than 4a? | Y / N |
| In 4c, can you hear the contrast between "खाना" (aspirated) and "काओ" (unaspirated)? | Y / N / subtle |
| Overall aspiration distinction: clearly audible / slightly audible / not audible |  |

---

## Sentence 5 — Script register (filed under: does Roman "office" vs ऑफिस vs आफ़ीस differ?)

Play: `5a.wav` → `5b.wav` → `5c.wav`

| Question | Answer |
|---|---|
| Does 5a ("office" in Roman) produce garbled / wrong output? | Y / N / partial |
| Are 5b and 5c **audibly different**? | Y / N |
| If different, describe: | |
| Is the vowel in 5c (आफ़ीस) noticeably longer than in 5b (ऑफिस)? | Y / N / can't tell |
| Is there an audible /f/ sound (not /ph/) in 5c due to the nukta on फ़? | Y / N / can't tell |
| Which rendering of "office" sounds more natural in a Hindi sentence? | 5b / 5c / both ok |

---

## Sentence 6 — Prosody emphasis (filed under: do repetition and punctuation shift delivery?)

Play: `6a.wav` → `6b.wav` → `6c.wav`

| Question | Answer |
|---|---|
| Does 6b ("बहुत बहुत") sound more emphatic than 6a ("बहुत")? | Y / N / slightly |
| If yes, how does the emphasis manifest? (louder / longer / higher pitch / none) | |
| Does 6c (ellipsis + exclamation) sound different in pacing from 6a? | Y / N |
| If yes, is it: slower / faster / more dramatic / no difference? | |
| Does the final word "हूं!" in 6c have a higher pitch than in 6a? | Y / N / can't tell |
| Overall: did any punctuation/structure cue visibly change the delivery? | Y / N |

---

## Global questions (answer after all 6)

| Question | Answer |
|---|---|
| Sentence where you heard the **clearest** variant difference: | 1 / 2 / 3 / 4 / 5 / 6 |
| Sentence where variants sounded **most identical**: | 1 / 2 / 3 / 4 / 5 / 6 |
| Aspiration contrast (sentence 4): audible? | clearly / slightly / not at all |
| Nukta contrast (sentences 1 and 5): audible? | clearly / slightly / not at all |
| Vowel length contrast (sentence 3): audible? | clearly / slightly / not at all |
| Overall impression: does the model attend to fine phonetic detail, or does it collapse to coarser graphemes? | fine / coarse / mixed |

---

## Notes (free text)

Any observations not captured above — unexpected artefacts, surprising quality differences, anything that would help interpret the FINDINGS.md classification:

```
(fill in here)
```
