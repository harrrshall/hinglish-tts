# Kaggle cells — Direction 2: Grapheme vs Phoneme Representation Probe

**Experiment:** `06_grapheme_phoneme_probe`  
**Kernel:** `harshalsinghcn/hinglish-tts-audit-indicf5` (patched, NO IndicXlit)  
**Goal:** 32 inference runs across 3 test types to probe IndicF5's internal representation.  
**CRITICAL:** No preprocessing on ANY input. Raw text → model. Roman/English will produce
garbled audio; that is expected and not a problem.

## Cell ordering

| Position | Action |
|---|---|
| Cells 0–5 | Keep exactly as-is (pip install / paths / HF token / eval rows / patch / model load) |
| Cell 6 | **REPLACE** with `PROBE_INFERENCE_CELL` below |

Cell 3 (eval rows) is not used in the inference but has no side effects — leave it.  
Cell 5 sets `REF_AUDIO` and `REF_TEXT` — these are reused by Cell 6.

---

## PROBE_INFERENCE_CELL (Cell 6)

Paste this in full, replacing the existing Cell 6 (music refs) if present.

```python
# === Cell 6: Direction 2 — Grapheme/Phoneme Probe — 32 inference runs ===
# CRITICAL: NO preprocessing. Every input is fed RAW to the model.
# Roman/English inputs will likely produce garbled audio — that is expected.
# We are probing acoustic STRUCTURE, not quality.
import sys, time, json
from pathlib import Path
import numpy as np, soundfile as sf, torch

PROBE_INPUTS = [
    # Test A — cross-script homophone pairs (8 pairs × 2 variants = 16 wavs)
    {"test_id":"A1_devanagari","test_type":"A","pair_id":"A1","text":"कल",               "script":"devanagari"},
    {"test_id":"A1_roman",     "test_type":"A","pair_id":"A1","text":"kal",               "script":"roman"},
    {"test_id":"A2_devanagari","test_type":"A","pair_id":"A2","text":"दिल्ली",            "script":"devanagari"},
    {"test_id":"A2_roman",     "test_type":"A","pair_id":"A2","text":"Delhi",             "script":"roman"},
    {"test_id":"A3_devanagari","test_type":"A","pair_id":"A3","text":"मेरा नाम",          "script":"devanagari"},
    {"test_id":"A3_roman",     "test_type":"A","pair_id":"A3","text":"mera naam",         "script":"roman"},
    {"test_id":"A4_devanagari","test_type":"A","pair_id":"A4","text":"पानी",             "script":"devanagari"},
    {"test_id":"A4_roman",     "test_type":"A","pair_id":"A4","text":"paani",            "script":"roman"},
    {"test_id":"A5_devanagari","test_type":"A","pair_id":"A5","text":"कितना",            "script":"devanagari"},
    {"test_id":"A5_roman",     "test_type":"A","pair_id":"A5","text":"kitna",            "script":"roman"},
    {"test_id":"A6_devanagari","test_type":"A","pair_id":"A6","text":"भाई",             "script":"devanagari"},
    {"test_id":"A6_roman",     "test_type":"A","pair_id":"A6","text":"bhai",            "script":"roman"},
    {"test_id":"A7_devanagari","test_type":"A","pair_id":"A7","text":"धन्यवाद",         "script":"devanagari"},
    {"test_id":"A7_roman",     "test_type":"A","pair_id":"A7","text":"dhanyavaad",      "script":"roman"},
    {"test_id":"A8_devanagari","test_type":"A","pair_id":"A8","text":"नमस्ते",           "script":"devanagari"},
    {"test_id":"A8_roman",     "test_type":"A","pair_id":"A8","text":"namaste",         "script":"roman"},
    # Test B — /k/ phoneme isolation in Hindi Devanagari (8 wavs)
    {"test_id":"B1","test_type":"B","pair_id":"B1","text":"कल",              "script":"devanagari"},
    {"test_id":"B2","test_type":"B","pair_id":"B2","text":"कान",             "script":"devanagari"},
    {"test_id":"B3","test_type":"B","pair_id":"B3","text":"किताब",           "script":"devanagari"},
    {"test_id":"B4","test_type":"B","pair_id":"B4","text":"कुत्ता",          "script":"devanagari"},
    {"test_id":"B5","test_type":"B","pair_id":"B5","text":"केला",            "script":"devanagari"},
    {"test_id":"B6","test_type":"B","pair_id":"B6","text":"कोल्ड",           "script":"devanagari"},
    {"test_id":"B7","test_type":"B","pair_id":"B7","text":"क्या",            "script":"devanagari"},
    {"test_id":"B8","test_type":"B","pair_id":"B8","text":"कितना अच्छा",    "script":"devanagari"},
    # Test C — /k/ cross-language phoneme transfer (8 wavs)
    {"test_id":"C1","test_type":"C","pair_id":"C1","text":"कल मैं जाऊंगा", "script":"devanagari"},
    {"test_id":"C2","test_type":"C","pair_id":"C2","text":"मेरा computer है","script":"mixed_roman"},
    {"test_id":"C3","test_type":"C","pair_id":"C3","text":"kal main jaunga","script":"roman"},
    {"test_id":"C4","test_type":"C","pair_id":"C4","text":"Cat is sitting",  "script":"english"},
    {"test_id":"C5","test_type":"C","pair_id":"C5","text":"कैसे हो?",        "script":"devanagari"},
    {"test_id":"C6","test_type":"C","pair_id":"C6","text":"Coffee पीते हो?", "script":"mixed_roman"},
    {"test_id":"C7","test_type":"C","pair_id":"C7","text":"kya tum theek ho?","script":"roman"},
    {"test_id":"C8","test_type":"C","pair_id":"C8","text":"Karen और मैं",    "script":"mixed_roman"},
]

OUT = Path(AUDIT_DIR) / "results" / "grapheme_phoneme_probe"
OUT.mkdir(parents=True, exist_ok=True)
run_log = []

class Tee:
    def __init__(self, *streams): self.streams = streams
    def write(self, s):
        for st in self.streams: st.write(s)
    def flush(self):
        for st in self.streams: st.flush()

with open(OUT / "run_log.txt", "w", encoding="utf-8") as logf:
    _stdout = sys.stdout
    sys.stdout = Tee(_stdout, logf)
    try:
        for inp in PROBE_INPUTS:
            tid    = inp["test_id"]
            ttype  = inp["test_type"]
            text   = inp["text"]
            script = inp["script"]
            print(f"\n--- {tid} [{ttype}|{script}] ---")
            print(f"    text: {text!r}")
            t0 = time.time()
            try:
                with torch.inference_mode():
                    audio = model(text=text, ref_audio_path=REF_AUDIO, ref_text=REF_TEXT)
                if isinstance(audio, torch.Tensor):
                    audio = audio.cpu().numpy()
                if audio.dtype == np.int16:
                    audio = audio.astype(np.float32) / 32768.0
                audio = np.asarray(audio, dtype=np.float32).squeeze()
                out_path = OUT / f"{tid}.wav"
                sf.write(out_path, audio, 24000)
                elapsed = time.time() - t0
                print(f"    ok: {len(audio)/24000:.3f}s wav, {elapsed:.1f}s wall")
                run_log.append({**inp, "duration_s": float(len(audio)/24000),
                                "elapsed_s": round(elapsed, 2), "status": "ok"})
            except Exception as e:
                elapsed = time.time() - t0
                print(f"    [error] {e}")
                run_log.append({**inp, "status": "error", "error": str(e),
                                "elapsed_s": round(elapsed, 2)})
    finally:
        sys.stdout = _stdout

with open(OUT / "log.json", "w", encoding="utf-8") as f:
    json.dump(run_log, f, ensure_ascii=False, indent=2)

n_ok  = sum(1 for x in run_log if x["status"] == "ok")
n_err = sum(1 for x in run_log if x["status"] == "error")
errs  = [x["test_id"] for x in run_log if x["status"] == "error"]
print(f"\nDONE: {n_ok}/32 ok, {n_err} errors")
if errs:
    print(f"  Errors (expected for English/Roman inputs): {errs}")
print(f"  output: {OUT}")
```

---

## Expected outcome

**32 wavs in `results/grapheme_phoneme_probe/`:**
- `A1_devanagari.wav` … `A8_devanagari.wav` — clean Hindi (16 Devanagari wavs)
- `A1_roman.wav` … `A8_roman.wav` — garbled (Mode C), **expected**
- `B1.wav` … `B8.wav` — clean Hindi
- `C1.wav`, `C5.wav` — clean Hindi
- `C2.wav`, `C3.wav`, `C4.wav`, `C6.wav`, `C7.wav`, `C8.wav` — likely garbled

**If any input throws a tokenization exception:** document in `log.json`, proceed
with the rest. The error message is itself a finding.

---

## Downloading results

```bash
/home/cybernovas/Desktop/hienglish/venv-scoring/bin/kaggle kernels output \
  harshalsinghcn/hinglish-tts-audit-indicf5 \
  -p /tmp/kaggle_out_probe

cp /tmp/kaggle_out_probe/audit/results/grapheme_phoneme_probe/*.wav \
   ~/Desktop/hienglish/experiments/06_grapheme_phoneme_probe/wavs/
```

Then run local acoustic analysis:
```bash
cd ~/Desktop/hienglish
source .env
./venv-scoring/bin/python experiments/06_grapheme_phoneme_probe/scripts/extract_acoustics.py
./venv-scoring/bin/python experiments/06_grapheme_phoneme_probe/scripts/analyse_results.py
```
