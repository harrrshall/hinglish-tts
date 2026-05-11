# Kaggle cells — IndicF5 phonetic probe

**Experiment:** Direction 1 — phonetic sensitivity probe
**Kernel:** new version of `harshalsinghcn/hinglish-tts-audit-indicf5-xlit`
  (reuse patched kernel — duration fix must remain active)
**Input:** 18 sentences (6 × 3 variants) from `test_sentences.tsv`
**Critical difference from all prior experiments:**
  `lib_normalize.to_unified_devanagari` is NOT called. Each variant's text
  is fed to `model(text=...)` EXACTLY as written. The whole hypothesis
  depends on passing phonetic distinctions through directly.

## Cell ordering

| Position | Action |
|---|---|
| Cell 1 | `pip install …` — keep as-is |
| Cell 2 | `AUDIT_DIR` setup — keep as-is |
| Cell 3 | **REPLACE** with `PROBE_INPUT_CELL` below |
| Cell 3.5 | **KEEP** `PATCH_VERIFICATION_CELL` from v3 (patch must be active) |
| Cell 4 | model load — keep as-is |
| Cell 5 | **REPLACE** with `PROBE_INFERENCE_CELL` below |

Do NOT call `to_unified_devanagari()` anywhere in Cell 3 or Cell 5.
Do NOT import `lib_normalize` in this kernel.

---

## PROBE_INPUT_CELL (replaces Cell 3)

```python
# === Cell 3: Load phonetic probe sentences (NO preprocessing) ===
# 18 sentences: 6 phonetic distinctions × 3 variants each.
# Text is fed to the model EXACTLY as written — no IndicXlit, no normalization.
# This is intentional: the hypothesis is that fine-grained Devanagari markers
# (nukta, halant, vowel matras) affect acoustic output when fed directly.
import csv, io

PROBE_TSV = """\
sentence_id\tvariant\tcategory\ttext\tphonetic_distinction_tested\texpected_audible_difference
1\ta\tnukta_fricative\tमेरा नाम ज़ारा है।\tnukta baseline\treference
1\tb\tnukta_fricative\tमेरा नाम जारा है।\tno nukta: ज → /j/\t/j/ not /z/
1\tc\tnukta_fricative\tमेरा नाम ज़ारा है।\texplicit nukta: ज़ → /z/\t/z/ fricative
2\ta\tschwa_elision\tकमल का फूल खिलता है।\timplicit schwa elision\treference
2\tb\tschwa_elision\tकमल् का फूल खिल्ता है।\texplicit halant throughout\tcleaner clusters
2\tc\tschwa_elision\tकमल का फूल खिल्ता है।\tmixed: halant only on खिल्ता\tintermediate
3\ta\tvowel_length\tमिटी की किताब लिखी।\tshort i matra\tclipped vowels
3\tb\tvowel_length\tमीटी की कीताब लीखी।\tall long i matra\tstretched vowels
3\tc\tvowel_length\tमिट्टी की किताब लिखी।\tcorrect Hindi spelling\treference
4\ta\taspiration\tखाना खाओ\taspirated ख /kʰ/\tbreathy plosive
4\tb\taspiration\tकाना काओ\tunaspirated क /k/\tharder plosive
4\tc\taspiration\tखाना काओ\tmixed: aspirated then unaspirated\taudible contrast in same clip
5\ta\tscript_register\tमुझे office जाना है।\tRoman in Devanagari context\tlikely garbled (Mode C baseline)
5\tb\tscript_register\tमुझे ऑफिस जाना है।\tstandard Hinglish rendering\tऑ vowel, canonical
5\tc\tscript_register\tमुझे आफ़ीस जाना है।\tHindi-ized: आ + nukta + ई\tlonger vowels, fricative फ़
6\ta\tprosody_emphasis\tमैं बहुत खुश हूं।\tneutral declarative\tflat prosody reference
6\tb\tprosody_emphasis\tमैं बहुत बहुत खुश हूं।\trepetition emphasis\tmore emphatic
6\tc\tprosody_emphasis\tमैं... बहुत... खुश हूं!\tellipsis + exclamation\tslower pacing, higher final pitch
"""

rows = list(csv.DictReader(io.StringIO(PROBE_TSV), delimiter="\t"))
assert len(rows) == 18, f"Expected 18 rows, got {len(rows)}"

# Build output ID: "1a", "1b", ..., "6c"
for r in rows:
    r["output_id"] = f"{r['sentence_id']}{r['variant']}"

# Sanity: assert no preprocessing needed (texts are all Devanagari or mixed as intended)
print(f"Loaded {len(rows)} probe sentences.")
print("\nVariants per sentence:")
from collections import defaultdict
by_sent = defaultdict(list)
for r in rows:
    by_sent[r['sentence_id']].append(r['variant'])
for sid in sorted(by_sent):
    texts = [r['text'] for r in rows if r['sentence_id'] == sid]
    print(f"  Sentence {sid}: variants {by_sent[sid]}")
    for v, t in zip(by_sent[sid], texts):
        print(f"    {v}: {t}")
```

**Expected stdout:**
```
Loaded 18 probe sentences.

Variants per sentence:
  Sentence 1: variants ['a', 'b', 'c']
    a: मेरा नाम ज़ारा है।
    b: मेरा नाम जारा है।
    c: मेरा नाम ज़ारा है।
  Sentence 2: variants ['a', 'b', 'c']
    a: कमल का फूल खिलता है।
    b: कमल् का फूल खिल्ता है।
    c: कमल का फूल खिल्ता है।
  Sentence 3: variants ['a', 'b', 'c']
    a: मिटी की किताब लिखी।
    b: मीटी की कीताब लीखी।
    c: मिट्टी की किताब लिखी।
  Sentence 4: variants ['a', 'b', 'c']
    a: खाना खाओ
    b: काना काओ
    c: खाना काओ
  Sentence 5: variants ['a', 'b', 'c']
    a: मुझे office जाना है।
    b: मुझे ऑफिस जाना है।
    c: मुझे आफ़ीस जाना है।
  Sentence 6: variants ['a', 'b', 'c']
    a: मैं बहुत खुश हूं।
    b: मैं बहुत बहुत खुश हूं।
    c: मैं... बहुत... खुश हूं!
```

---

## PROBE_INFERENCE_CELL (replaces Cell 5)

```python
# === Cell 5: Run patched IndicF5 on phonetic probe sentences ===
# NO preprocessing. text fed to model exactly as written.
# Output: results/phonetic_probe/<output_id>.wav  (e.g., 1a.wav, 1b.wav, ...)
import io, sys, time, json
from pathlib import Path
import numpy as np, soundfile as sf, torch

OUT = Path(AUDIT_DIR) / "results" / "phonetic_probe"
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
            oid      = r["output_id"]    # e.g. "1a"
            sid      = r["sentence_id"]  # e.g. "1"
            variant  = r["variant"]      # "a", "b", "c"
            cat      = r["category"]
            text     = r["text"]         # fed to model AS-IS — no normalization
            print(f"\n--- {oid} [{cat}] ---")
            print(f"  text: {text}")
            t0 = time.time()
            try:
                with torch.inference_mode():
                    audio = model(text=text, ref_audio_path=REF_AUDIO, ref_text=REF_TEXT)
                if isinstance(audio, torch.Tensor):
                    audio = audio.cpu().numpy()
                if audio.dtype == np.int16:
                    audio = audio.astype(np.float32) / 32768.0
                audio = np.asarray(audio, dtype=np.float32).squeeze()
                out_path = OUT / f"{oid}.wav"
                sf.write(out_path, audio, 24000)
                results_log.append({
                    "output_id": oid, "sentence_id": sid, "variant": variant,
                    "category": cat, "text": text,
                    "duration_s": float(len(audio) / 24000),
                    "elapsed_s": round(time.time() - t0, 2),
                    "status": "ok",
                })
                print(f"    ok: {len(audio)/24000:.3f}s wav, {time.time()-t0:.1f}s wall")
            except Exception as e:
                results_log.append({
                    "output_id": oid, "sentence_id": sid, "variant": variant,
                    "category": cat, "text": text,
                    "status": "error", "error": str(e),
                })
                print(f"    [ERROR] {type(e).__name__}: {e}")
                print(f"    >>> STOP AND REPORT THIS — may indicate tokenization failure <<<")
    finally:
        sys.stdout = real_stdout

with open(OUT / "log.json", "w", encoding="utf-8") as f:
    json.dump(results_log, f, ensure_ascii=False, indent=2)

n_ok  = sum(1 for x in results_log if x["status"] == "ok")
n_err = sum(1 for x in results_log if x["status"] == "error")
print(f"\nphonetic_probe: {n_ok}/18 succeeded, {n_err}/18 errors")
if n_err:
    print("ERROR ROWS:")
    for x in results_log:
        if x["status"] == "error":
            print(f"  {x['output_id']}: {x['error']}")
print(f"  wavs: {OUT}")
print(f"  log:  {OUT / 'log.json'}")
```

**Expected:** `phonetic_probe: 18/18 succeeded, 0/18 errors`.

**Stop and report if:**
- Any `[ERROR]` appears — especially for sentence 5a (`मुझे office जाना है।`). A tokenization
  error on Roman input is itself a finding (Outcome C evidence); a timeout error is
  a different problem. Report the exact error string before proceeding.
- More than 2/18 errors for any other reason.
- Any `duration_s < 0.5` — would suggest canvas under-allocation, which shouldn't happen
  since all inputs are Devanagari-heavy (duration patch calibrated correctly).

---

## After the run — download

```bash
# In Kaggle output panel, download:
results/phonetic_probe/
├── 1a.wav   1b.wav   1c.wav
├── 2a.wav   2b.wav   2c.wav
├── 3a.wav   3b.wav   3c.wav
├── 4a.wav   4b.wav   4c.wav
├── 5a.wav   5b.wav   5c.wav
├── 6a.wav   6b.wav   6c.wav
├── duration_log.txt
└── log.json
```

Place the 18 wavs in `experiments/05_phonetic_probe/wavs/`.

Then run `experiments/05_phonetic_probe/scoring_scripts/run_scoring.py` locally
(see that file for invocation). It will produce `scores/auto_scores.csv`.

**Note on sentence 1:** variants 1a and 1c have identical text (`मेरा नाम ज़ारा है।`).
This is intentional — the model is deterministic given the same input and reference
audio, so 1a.wav ≈ 1c.wav at the byte level. They serve as an internal reproducibility
check: if 1a and 1c differ significantly in ASR transcripts or F0, something is
wrong with the inference setup. 1b (`जारा` without nukta) is the actual contrast.
