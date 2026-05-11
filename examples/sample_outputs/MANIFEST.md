# Sample outputs

12 clips produced by the IndicF5 + IndicXlit stack (v2.1), drawn from the
30-sentence evaluation set. These are the evaluated outputs — the same files
that contribute to the reported 4.70/5 intelligibility score.

**Model:** ai4bharat/IndicF5 v12 (330M params, weights unchanged)  
**Duration patch:** character-count proportional (Mode A fix)  
**Preprocessing:** `to_unified_devanagari()` — IndicXlit + whitelist (v2.1)  
**Reference voice:** `data/reference_audio/hindi_ref.wav` (7.15s, 24 kHz mono)  
**Sample rate:** 24 kHz mono PCM

---

## pure_devanagari

Standard Hindi in Devanagari script. No preprocessing applied (input already
in target script). Scores shown as AAI / Deepgram / Groq intelligibility (1–5).

| File | Text | Score | Dur |
|---|---|:---:|---:|
| `01_pure_devanagari__brother_school.wav` | मेरा भाई आज स्कूल नहीं गया क्योंकि उसकी तबीयत खराब है। | 5/5/5 | 4.19s |
| `02_pure_devanagari__casual_come_on.wav` | जल्दी आओ यार, सब तेरा इंतज़ार कर रहे हैं। | 5/5/5 | 3.15s |
| `03_pure_devanagari__meeting_question.wav` | तुझे पता है कल मीटिंग कितने बजे है? | 5/5/5 | 2.67s |

---

## pure_roman

Colloquial Hinglish written entirely in Roman script. IndicXlit converts every
token to Devanagari before synthesis; the function-word whitelist ensures
`tu → तू` (not `टू`) and `mai → मैं` (not `माई`).

| File | Text | Score | Dur |
|---|---|:---:|---:|
| `04_pure_roman__party_question.wav` | kya tu bhi aaj party me aa raha hai? | 5/5/5 | 2.38s |
| `05_pure_roman__laptop_delivery.wav` | tera laptop kab tak deliver hoga bhai? | 5/5/5 | 2.67s |
| `06_pure_roman__casual_yesterday.wav` | yaar tu kal kya kar raha tha | 1/5/5† | 1.71s |

†AAI returns empty on clips ≤1.7s; Deepgram + Groq consensus = 5.

---

## mixed_script

Mid-sentence Devanagari ↔ Roman code-switching — the hardest category for
both preprocessing and synthesis. Script switches preserved; English loans
converted via whitelist (`deadline → डेडलाइन`, `leave → लीव`).

| File | Text | Score | Dur |
|---|---|:---:|---:|
| `07_mixed_script__restaurant_question.wav` | Tumne वो new restaurant try kiya jo Connaught Place में khula hai? | 5/5/5 | 4.86s |
| `08_mixed_script__file_review_deadline.wav` | Ye file को quickly review करो, deadline बहुत close है। | 5/5/5 | 4.29s |
| `09_mixed_script__boss_leave_message.wav` | Boss को बता देना kal मैं leave पर रहूँगा, kuch personal काम है। | 5/5/4 | 4.19s |

---

## english_with_NE

English sentences containing Indian named entities (people, cities, brands).
Every token passes through IndicXlit; Indian NEs receive canonical Devanagari
forms. Output sounds like Hindi-accented English — expected behaviour, since
the model was trained on Indic speech.

| File | Text | Score | Dur |
|---|---|:---:|---:|
| `10_english_with_NE__khanna_meeting.wav` | Mr. Khanna will join the meeting after he finishes lunch with Priya. | 5/5/5 | 4.96s |
| `11_english_with_NE__aishwarya_bengaluru.wav` | My friend Aishwarya from Chennai is visiting Bengaluru next week. | 5/5/1† | 5.54s |
| `12_english_with_NE__tata_pune.wav` | She just got hired at Tata Consultancy Services in Pune. | 4/4/5 | 4.58s |

†Groq scored 1 on this clip (long sentence, Groq CER on transliterated English
is noisy); AAI + Deepgram consensus = 5.

---

## Notes

- Naturalness is not numerically scored (see EVALUATION_REPORT.md §2 for why).
  These clips represent the best intelligibility scores in each category; they
  are not necessarily the most natural-sounding.
- `english_with_NE` clips sound Hindi-accented because IndicXlit transliterates
  English words to Devanagari phonetics before synthesis. This is documented
  as a known limitation (EVALUATION_REPORT.md §4).
- Inference is non-deterministic (diffusion with no fixed seed). Re-running
  `inference.py` on the same text will produce a slightly different clip.
