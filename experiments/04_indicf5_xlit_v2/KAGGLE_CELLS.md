# Kaggle cells — IndicF5 patched + IndicXlit v2.1 whitelist

**Rubric:** v2.1 (2026-05-11). Identical to v2.0 except four tokens added to
`ROMAN_HINDI_FUNCTION_WORDS`: `tu → तू`, `mai → मैं`, `aa → आ`, `hu → हूं`.

**Changed rows vs v2.0 TSV:** ids 10, 11, 12, 13, 16 (all pure_roman).
All other 25 rows are byte-for-byte identical to `experiments/03_indicf5_xlit/preprocessed_sentences.tsv`.

**Kernel:** reuse `harshalsinghcn/hinglish-tts-audit-indicf5` (patch already
applied in v13). Output goes to `results/indicf5_patched_xlit_v2/` — do NOT
overwrite `results/indicf5_patched_xlit/` (the v2.0 reference must stay intact).

## Cell ordering

Same structure as `experiments/03_indicf5_xlit/KAGGLE_CELLS.md`.

| Position | Action |
|---|---|
| Cell 1 | `pip install … IndicF5.git` — keep as-is |
| Cell 2 | `AUDIT_DIR` setup — keep as-is |
| Cell 3 | **REPLACE** with `PREPROCESSED_INPUT_CELL_V2` below |
| Cell 3.5 | **KEEP** `PATCH_VERIFICATION_CELL` from v2.0 (unchanged) |
| Cell 4 | model load — keep as-is |
| Cell 5 | **REPLACE** with `INFERENCE_CELL_V2` below |

---

## PREPROCESSED_INPUT_CELL_V2 (replaces Cell 3)

TSV is inlined — no upload or paste step needed.

```python
# === Cell 3: Load v2.1-preprocessed sentences (tu/mai/aa/hu whitelist fix) ===
# Rubric v2.1 (2026-05-11). Five rows changed vs v2.0: ids 10, 11, 12, 13, 16.
# All pure_devanagari rows are still unchanged (preprocessing_applied = "no").
import csv, io

PREPROCESSED_TSV = """\
id\tcategory\ttext_original\ttext_preprocessed\tpreprocessing_applied
1\tpure_devanagari\tकल मुझे दिल्ली जाना है।\tकल मुझे दिल्ली जाना है।\tno
2\tpure_devanagari\tक्या आप मुझे पानी दे सकते हैं?\tक्या आप मुझे पानी दे सकते हैं?\tno
3\tpure_devanagari\tमेरा भाई आज स्कूल नहीं गया क्योंकि उसकी तबीयत खराब है।\tमेरा भाई आज स्कूल नहीं गया क्योंकि उसकी तबीयत खराब है।\tno
4\tpure_devanagari\tमेरे पास सिर्फ़ तीन सौ रुपये हैं, बस इतने में चला लो।\tमेरे पास सिर्फ़ तीन सौ रुपये हैं, बस इतने में चला लो।\tno
5\tpure_devanagari\tजल्दी आओ यार, सब तेरा इंतज़ार कर रहे हैं।\tजल्दी आओ यार, सब तेरा इंतज़ार कर रहे हैं।\tno
6\tpure_devanagari\tआज बहुत थक गया हूँ, बस सीधा सोना चाहता हूँ।\tआज बहुत थक गया हूँ, बस सीधा सोना चाहता हूँ।\tno
7\tpure_devanagari\tतुझे पता है कल मीटिंग कितने बजे है?\tतुझे पता है कल मीटिंग कितने बजे है?\tno
8\tpure_devanagari\tअरे यार, मेरा फ़ोन कहाँ रखा था?!\tअरे यार, मेरा फ़ोन कहाँ रखा था?!\tno
9\tpure_roman\tkal mujhe office jaana hai\tकल मुझे ऑफिस जाना है\tyes
10\tpure_roman\tmera naam Arjun hai aur mai Bengaluru se hu\tमेरा नाम अर्जुन है और मैं बेंगलुरु से हूं\tyes
11\tpure_roman\tyaar tu kal kya kar raha tha\tयार तू कल क्या कर रहा था\tyes
12\tpure_roman\tkya tu bhi aaj party me aa raha hai?\tक्या तू भी आज पार्टी मे आ रहा है?\tyes
13\tpure_roman\tabe yaar jaldi reply kar, mai wait kar raha hu\tअबे यार जल्दी रिप्लाई कर, मैं वेट कर रहा हूं\tyes
14\tpure_roman\tkal raat ka movie tha bohot bakwaas, paisa bilkul waste\tकल रात का मूवी था बोहोट बकवास, पैसा बिलकुल वेस्ट\tyes
15\tpure_roman\ttera laptop kab tak deliver hoga bhai?\tतेरा लैपटॉप कब तक डिलीवर होगा भाई?\tyes
16\tpure_roman\tyaar tu bohot lucky hai, mujhe nahi mila ticket!\tयार तू बोहोट लकी है, मुझे नही मिला टिकट!\tyes
17\tmixed_script\tKal mujhe ऑफिस जाना hai, but ट्राफिक will be an issue.\tकल मुझे ऑफिस जाना है, बट ट्राफिक विल बे एएन इश्यू.\tyes
18\tmixed_script\tMera presentation tomorrow है, और मैं nervous हूं।\tमेरा प्रेज़ेंटेशन टुमॉरो है, और मैं नर्वस हूं।\tyes
19\tmixed_script\tBhai please मेरा homework कर दे, मैं तुझे ₹100 दूंगा।\tभाई प्लीज़ मेरा होमवर्क कर दे, मैं तुझे ₹100 दूंगा।\tyes
20\tmixed_script\tTumne वो new restaurant try kiya jo Connaught Place में khula hai?\tतुमने वो न्यू रेस्टोरेंट ट्राई किया जो कनॉट प्लेस में खुला है?\tyes
21\tmixed_script\tकल का event cancel हो गया, सबको message कर देना please।\tकल का इवेंट कैंसल हो गया, सबको मैसेज कर देना प्लीज़।\tyes
22\tmixed_script\tBoss को बता देना kal मैं leave पर रहूँगा, kuch personal काम है।\tबॉस को बता देना कल मैं लीव पर रहूँगा, कुच पर्सनल काम है।\tyes
23\tmixed_script\tYe file को quickly review करो, deadline बहुत close है।\tये फाइल को क्विकली रिव्यू करो, डेडलाइन बहुत क्लोज़ है।\tyes
24\tenglish_with_NE\tMy friend Aishwarya from Chennai is visiting Bengaluru next week.\tमाय फ्रेंड ऐश्वर्या फ्रॉम चेन्नई इस विज़िटिंग बेंगलुरु नेक्स्ट वीक.\tyes
25\tenglish_with_NE\tMr. Khanna will join the meeting after he finishes lunch with Priya.\tमिस्टर. खन्ना विल जोइन थे मीटिंग आफ्टर हे फिनिश लंच विथ प्रिया.\tyes
26\tenglish_with_NE\tI love butter chicken from Karim's in Old Delhi.\tआई लोव बटर चिकन फ्रॉम करीम'एस इन ओल्ड दिल्ली.\tyes
27\tmixed_script\tOffice में सब log lunch के लिए बाहर गए, तू भी आ ja yaar.\tऑफिस में सब लॉग लंच के लिए बाहर गए, तू भी आ जा यार.\tyes
28\tenglish_with_NE\tRohan is flying from Mumbai to Bengaluru tomorrow morning for work.\tरोहन इस फ्लाइंग फ्रॉम मुंबई टो बेंगलुरु टुमॉरो मॉर्निंग फोर वर्क.\tyes
29\tenglish_with_NE\tLet's grab biryani from Paradise in Hyderabad this weekend.\tलेट'एस ग्रैब बिरयानी फ्रॉम पैराडाइज़ इन हैदराबाद थिस वीकेंड.\tyes
30\tenglish_with_NE\tShe just got hired at Tata Consultancy Services in Pune.\tशे जस्ट गोट हायर्ड एटी टाटा कंसल्टेंसी सर्विसेज़ इन पुणे.\tyes
"""

rows = list(csv.DictReader(io.StringIO(PREPROCESSED_TSV), delimiter="\t"))
assert len(rows) == 30, f"Expected 30 rows, got {len(rows)}"

# Sanity: pure_devanagari rows must be unchanged.
for r in rows:
    if r["category"] == "pure_devanagari" and r["preprocessing_applied"] == "yes":
        raise AssertionError(f"id={r['id']}: pure_devanagari row was changed — abort.")

# Spot-check the 5 changed rows vs v2.0.
V21_CHANGES = {
    "10": "मेरा नाम अर्जुन है और मैं बेंगलुरु से हूं",
    "11": "यार तू कल क्या कर रहा था",
    "12": "क्या तू भी आज पार्टी मे आ रहा है?",
    "13": "अबे यार जल्दी रिप्लाई कर, मैं वेट कर रहा हूं",
    "16": "यार तू बोहोट लकी है, मुझे नही मिला टिकट!",
}
for r in rows:
    if r["id"] in V21_CHANGES:
        expected = V21_CHANGES[r["id"]]
        assert r["text_preprocessed"] == expected, (
            f"id={r['id']}: expected {expected!r}, got {r['text_preprocessed']!r}"
        )
        print(f"  [v2.1 check OK] id={r['id']}: {r['text_preprocessed']}")

n_changed = sum(1 for r in rows if r["preprocessing_applied"] == "yes")
print(f"\nLoaded {len(rows)} sentences ({n_changed} changed, {len(rows)-n_changed} unchanged).")
print("Rubric v2.1 — 5 rows differ from v2.0 (ids 10, 11, 12, 13, 16).")
```

**Expected stdout:**
```
  [v2.1 check OK] id=10: मेरा नाम अर्जुन है और मैं बेंगलुरु से हूं
  [v2.1 check OK] id=11: यार तू कल क्या कर रहा था
  [v2.1 check OK] id=12: क्या तू भी आज पार्टी मे आ रहा है?
  [v2.1 check OK] id=13: अबे यार जल्दी रिप्लाई कर, मैं वेट कर रहा हूं
  [v2.1 check OK] id=16: यार तू बोहोट लकी है, मुझे नही मिला टिकट!

Loaded 30 sentences (22 changed, 8 unchanged).
Rubric v2.1 — 5 rows differ from v2.0 (ids 10, 11, 12, 13, 16).
```

---

## INFERENCE_CELL_V2 (replaces Cell 5)

Identical to v2.0 inference cell except output directory is `indicf5_patched_xlit_v2`.

```python
# === Cell 5: Run patched IndicF5 on v2.1-preprocessed inputs ===
# Output: results/indicf5_patched_xlit_v2/  (do NOT touch results/indicf5_patched_xlit/)
import io, sys, time, json
from pathlib import Path
import numpy as np, soundfile as sf, torch

OUT = Path(AUDIT_DIR) / "results" / "indicf5_patched_xlit_v2"
OUT.mkdir(parents=True, exist_ok=True)
log_path = OUT / "duration_log.txt"
results_log = []

class Tee:
    def __init__(self, *streams): self.streams = streams
    def write(self, s):
        for st in self.streams: st.write(s)
    def flush(self):
        for st in self.streams: st.flush()

with open(log_path, "w", encoding="utf-8") as logf:
    real_stdout = sys.stdout
    sys.stdout = Tee(real_stdout, logf)
    try:
        for r in rows:
            rid = r["id"]
            cat = r["category"]
            text_orig = r["text_original"]
            text_in   = r["text_preprocessed"]
            print(f"\n--- {rid} [{cat}] ---")
            print(f"  original:    {text_orig}")
            print(f"  preprocessed: {text_in}")
            t0 = time.time()
            try:
                with torch.inference_mode():
                    audio = model(text=text_in, ref_audio_path=REF_AUDIO, ref_text=REF_TEXT)
                if isinstance(audio, torch.Tensor):
                    audio = audio.cpu().numpy()
                if audio.dtype == np.int16:
                    audio = audio.astype(np.float32) / 32768.0
                audio = np.asarray(audio, dtype=np.float32).squeeze()
                out_path = OUT / f"{rid}.wav"
                sf.write(out_path, audio, 24000)
                results_log.append({
                    "id": rid, "category": cat,
                    "text_original": text_orig,
                    "text_preprocessed": text_in,
                    "rubric_version": "2.1",
                    "duration_s": float(len(audio) / 24000),
                    "elapsed_s": time.time() - t0,
                    "status": "ok",
                })
                print(f"    ok: {len(audio)/24000:.3f}s wav, {time.time()-t0:.1f}s wall")
            except Exception as e:
                results_log.append({
                    "id": rid, "category": cat,
                    "text_original": text_orig, "text_preprocessed": text_in,
                    "rubric_version": "2.1", "status": "error", "error": str(e),
                })
                print(f"    [error] {e}")
    finally:
        sys.stdout = real_stdout

with open(OUT / "log.json", "w", encoding="utf-8") as f:
    json.dump(results_log, f, ensure_ascii=False, indent=2)

n_ok = sum(1 for x in results_log if x["status"] == "ok")
print(f"\nindicf5_patched_xlit_v2: {n_ok}/30 succeeded")
print(f"  wavs: {OUT}")
print(f"  log:  {OUT / 'log.json'}")
```

**Expected:** `indicf5_patched_xlit_v2: 30/30 succeeded`.

Only 5 wavs (ids 10, 11, 12, 13, 16) will differ meaningfully from the v2.0 run.
The other 25 are the same inputs → the model is deterministic → the wavs should
be byte-identical or within floating-point rounding. Scoring them all 30 is
cleaner than trying to splice 5 wavs into the existing set.

---

## After the run — bundle to bring back

```bash
tar czf indicf5_patched_xlit_v2.tgz results/indicf5_patched_xlit_v2/
```

Contents:
```
results/indicf5_patched_xlit_v2/
├── 01.wav … 30.wav
├── duration_log.txt
└── log.json
```

Drop wavs into `experiments/04_indicf5_xlit_v2/wavs/` locally. Scoring
(`extract_signals_v2.py` + `judge_v2.py`) and `COMPARISON.md` follow.
