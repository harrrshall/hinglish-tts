# Kaggle cells — IndicF5 duration patch + 30-sentence re-run

Drop these cells into the existing `harshalsinghcn/hinglish-tts-audit-indicf5` kernel (or any kernel that already has the IndicF5 v12 environment working — T4 GPU, `transformers==4.49.0`, `accelerate==0.33.0`, `safetensors==0.4.3`).

The patch is a 4-line block change in **one file**: `f5_tts/infer/utils_infer.py:449-452`. Bytes-of-text → chars-of-text (whitespace-stripped).

## Order of cells (vs. existing notebook 02_indicf5.ipynb)

| Position | Existing cell | Action |
|----------|---------------|--------|
| Cell 1 | `pip install … IndicF5.git` | **keep as-is** |
| Cell 2 | `AUDIT_DIR` setup | **keep as-is** |
| Cell 3 | load eval_sentences.tsv | **keep as-is** |
| **Cell 3.5 (NEW)** | — | **Insert PATCH_CELL below** |
| Cell 4 | model load | **keep as-is** |
| **Cell 4.5 (NEW)** | — | **Insert SANITY_CELL below** — DO NOT proceed if it fails |
| Cell 5 | inference loop on all 30 | **REPLACE with INFERENCE_CELL below** |
| Cell 6 | save log.json | replaced by INFERENCE_CELL (writes its own log) |

The patch must land **after `pip install`** (so the file exists) but **before `AutoModel.from_pretrained`** (so the model imports the patched code). Putting it at Cell 3.5 satisfies both.

---

## PATCH_CELL (insert as Cell 3.5)

```python
# === Cell 3.5: Patch f5_tts duration formula (Mode A fix) ===
# See audit/duration_diagnostic/REPORT.md for the diagnostic that justifies this.
# Replaces byte-proportional duration arithmetic with character-count proportional.
# The whitespace strip avoids penalizing texts with extra spaces.
import sys, glob, importlib

# Locate the utils_infer.py(s) in site-packages. There can be more than one
# (e.g. an editable install + a wheel install); patch all of them.
candidates = []
for root in [p for p in sys.path if p]:
    candidates.extend(glob.glob(f"{root}/**/f5_tts/infer/utils_infer.py", recursive=True))
candidates = sorted(set(candidates))
print(f"Found {len(candidates)} utils_infer.py file(s):")
for c in candidates:
    print(f"  - {c}")
assert candidates, "No f5_tts/infer/utils_infer.py found on sys.path. Did Cell 1 install IndicF5?"

ORIG_BLOCK = (
    '            # Calculate duration\n'
    '            ref_text_len = len(ref_text.encode("utf-8"))\n'
    '            gen_text_len = len(gen_text.encode("utf-8"))\n'
    '            duration = ref_audio_len + int(ref_audio_len / ref_text_len * gen_text_len / speed)\n'
)
PATCHED_BLOCK = (
    '            # PATCHED 2026-05-09 — character-count proportional (Mode A fix)\n'
    '            # See audit/duration_diagnostic/REPORT.md\n'
    '            ref_text_len = sum(1 for c in ref_text if not c.isspace())\n'
    '            gen_text_len = sum(1 for c in gen_text if not c.isspace())\n'
    '            duration = ref_audio_len + int(ref_audio_len / ref_text_len * gen_text_len / speed)\n'
    "            print(f\"DEBUG-PATCH: ref_chars={ref_text_len} gen_chars={gen_text_len} \"\n"
    "                  f\"ref_frames={ref_audio_len} gen_frames={duration - ref_audio_len} \"\n"
    "                  f\"text={gen_text[:50]!r}\")\n"
)

n_patched = 0
for path in candidates:
    with open(path, encoding="utf-8") as f:
        src = f.read()
    if "DEBUG-PATCH" in src:
        print(f"  [skip] already patched: {path}")
        continue
    if ORIG_BLOCK not in src:
        print(f"  [no-match] expected block not in {path}; inspect manually")
        continue
    new_src = src.replace(ORIG_BLOCK, PATCHED_BLOCK)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_src)
    print(f"  [PATCHED] {path}")
    n_patched += 1

assert n_patched > 0, (
    "No file was patched. The original block was not found.\n"
    "Inspect utils_infer.py manually around `ref_text_len = len(ref_text.encode(\"utf-8\"))`.\n"
    "If the formula has drifted (e.g. surrounding whitespace differs), "
    "adjust ORIG_BLOCK above to match exactly and retry."
)

# Drop any already-imported f5_tts modules from sys.modules so the next
# `import` (in Cell 4) picks up the patched source.
to_drop = [m for m in sys.modules if m.startswith("f5_tts")]
for m in to_drop:
    del sys.modules[m]
print(f"\nCleared {len(to_drop)} f5_tts module(s) from sys.modules. Cell 4 will re-import patched code.")
```

**Expected output:**
- One or more `[PATCHED] …/utils_infer.py` lines.
- Final assertion does **not** trip.

If no candidate is found, Cell 1 didn't install IndicF5 yet; run it. If `[no-match]` appears, the block whitespace differs in your fork — open the file at `f5_tts/infer/utils_infer.py:449` and copy the exact 4-line block (including the `# Calculate duration` comment) into `ORIG_BLOCK`.

---

## SANITY_CELL (insert as Cell 4.5, after model load)

This runs **only sentence 09** ("kal mujhe office jaana hai") and asserts the patch took effect. Stop here if it fails — running 30 inferences with a broken patch wastes 30+ minutes of T4 time.

```python
# === Cell 4.5: Sanity check — sentence 09 with patched duration ===
# Original behaviour (from audit/duration_diagnostic/raw_measurements.json):
#   gen_frames = 74, computed_dur = 0.789 s, transcript = "Ranai." (mangled)
# Expected with patch:
#   ref_text has ~73 chars (no whitespace), gen "kal mujhe office jaana hai" has 22 chars.
#   gen_frames ≈ 628 × 22 / 73 ≈ 189, computed_dur ≈ 2.02 s.
#   Audio should now contain (most of) the full sentence.
import io, time, numpy as np, soundfile as sf, torch

SANITY_TEXT = "kal mujhe office jaana hai"
print(f"Sanity input: {SANITY_TEXT!r}")
print(f"Stripped char count: {sum(1 for c in SANITY_TEXT if not c.isspace())}  (expected: 22)")

t0 = time.time()
with torch.inference_mode():
    audio = model(text=SANITY_TEXT, ref_audio_path=REF_AUDIO, ref_text=REF_TEXT)
elapsed = time.time() - t0

if isinstance(audio, torch.Tensor):
    audio = audio.cpu().numpy()
if audio.dtype == np.int16:
    audio = audio.astype(np.float32) / 32768.0
audio = np.asarray(audio, dtype=np.float32).squeeze()
dur_s = len(audio) / 24000.0
print(f"\nGenerated {dur_s:.3f}s of audio in {elapsed:.1f}s wall.")

# Save sanity wav to AUDIT_DIR/results/indicf5_patched/_sanity_09.wav so we can listen.
from pathlib import Path
patched_dir = Path(AUDIT_DIR) / "results" / "indicf5_patched"
patched_dir.mkdir(parents=True, exist_ok=True)
sanity_path = patched_dir / "_sanity_09.wav"
sf.write(sanity_path, audio, 24000)
print(f"Saved sanity wav to {sanity_path}")

# Hard checks:
assert dur_s >= 1.5, (
    f"PATCH FAILED: audio is only {dur_s:.2f}s; expected ~2.0s. "
    f"DEBUG-PATCH log line should have printed ref_chars/gen_chars/gen_frames — "
    f"if it did NOT, the patched code is not in the call path. "
    f"If it DID and gen_frames is much lower than ~189, the formula is wrong somewhere."
)
assert dur_s <= 3.0, (
    f"PATCH OVER-CORRECTED: audio is {dur_s:.2f}s; expected ~2.0s. "
    f"Listen to the wav — if there's silence at the end, the canvas is too generous."
)
print(f"\n✓ Sanity passed: {dur_s:.2f}s is in [1.5, 3.0]. Proceed to full 30-sentence run.")
print("(Listen to _sanity_09.wav once before the long run, just to confirm content quality.)")
```

**Expected stdout** (in order):
1. `DEBUG-PATCH: ref_chars=<N> gen_chars=22 ref_frames=<M> gen_frames=<~189> text='kal mujhe office jaana hai'`
2. `Generated 2.0s …` (anywhere in 1.8–2.2)
3. `✓ Sanity passed`

If `DEBUG-PATCH` does **not** appear, the model is reaching the duration formula via a different code path than `f5_tts/infer/utils_infer.py:infer_batch_process`. In that case, stop and report — don't try to brute-force a fix. Most likely culprit: the IndicF5 HF wrapper has its own copy of the formula in a `transformers_modules/ai4bharat/IndicF5/<hash>/modeling_*.py` file that gets downloaded by `from_pretrained`. To find it:
```python
import inspect, sys
for m in sys.modules.values():
    try:
        f = inspect.getsourcefile(m)
        if f and "IndicF5" in f and f.endswith(".py"):
            print(f, "::", m.__name__)
    except Exception:
        pass
```

---

## INFERENCE_CELL (replaces existing Cell 5)

Writes to `audit/results/indicf5_patched/` (NOT the original `audit/results/indicf5/`, which must be preserved for comparison) and captures DEBUG-PATCH lines into `duration_log.txt`.

```python
# === Cell 5 (replacement): Run patched IndicF5 on all 30 eval sentences ===
import io, sys, time, json, contextlib
from pathlib import Path
import numpy as np, soundfile as sf, torch

OUT = Path(AUDIT_DIR) / "results" / "indicf5_patched"
OUT.mkdir(parents=True, exist_ok=True)
log_path = OUT / "duration_log.txt"
results_log = []

# Tee stdout so DEBUG-PATCH lines (printed inside utils_infer.py) get captured.
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
            rid, cat, text = r["id"], r["category"], r["text"]
            print(f"\n--- {rid} [{cat}] {text[:60]} ---")
            t0 = time.time()
            try:
                with torch.inference_mode():
                    audio = model(text=text, ref_audio_path=REF_AUDIO, ref_text=REF_TEXT)
                if isinstance(audio, torch.Tensor):
                    audio = audio.cpu().numpy()
                if audio.dtype == np.int16:
                    audio = audio.astype(np.float32) / 32768.0
                audio = np.asarray(audio, dtype=np.float32).squeeze()
                out_path = OUT / f"{rid}.wav"
                sf.write(out_path, audio, 24000)
                results_log.append({
                    "id": rid, "category": cat, "text": text,
                    "duration_s": float(len(audio) / 24000),
                    "elapsed_s": time.time() - t0,
                    "status": "ok",
                })
                print(f"    ok: {len(audio)/24000:.3f}s wav, {time.time()-t0:.1f}s wall")
            except Exception as e:
                results_log.append({
                    "id": rid, "category": cat, "text": text,
                    "status": "error", "error": str(e),
                })
                print(f"    [error] {e}")
    finally:
        sys.stdout = real_stdout

with open(OUT / "log.json", "w", encoding="utf-8") as f:
    json.dump(results_log, f, ensure_ascii=False, indent=2)

n_ok = sum(1 for x in results_log if x["status"] == "ok")
print(f"\nindicf5_patched: {n_ok}/30 succeeded")
print(f"  wavs: {OUT}")
print(f"  duration log (DEBUG-PATCH lines): {log_path}")
print(f"  inference log: {OUT / 'log.json'}")
```

**Expected output:**
- 30 lines of `DEBUG-PATCH: …` interleaved with per-sentence success messages.
- `indicf5_patched: 30/30 succeeded`.

If <30 succeed, share `log.json` — most likely cause would be a flaky reference clip read or transient HF Hub error, both retryable.

---

## After the run — what to bring back

Bundle and download these from `<AUDIT_DIR>/results/indicf5_patched/`:

```
01.wav … 30.wav         (30 patched outputs)
_sanity_09.wav          (the sentence-09 sanity wav)
duration_log.txt        (all 30 DEBUG-PATCH lines + per-sentence wall times)
log.json                (status of each sentence)
```

Easiest method on Kaggle: just `tar czf indicf5_patched.tgz audit/results/indicf5_patched/` and download from the Kaggle file browser, or push as a Kaggle dataset. The local re-scoring + comparison report take that bundle as input.

---

## Quick smoke check before re-running

If you want to be extra-careful, re-confirm the original formula one more time before patching by running this **before** Cell 3.5:

```python
import sys, glob, re
for root in [p for p in sys.path if p]:
    for path in glob.glob(f"{root}/**/f5_tts/infer/utils_infer.py", recursive=True):
        with open(path) as f:
            src = f.read()
        for line in src.splitlines():
            if "ref_text.encode" in line or "gen_text.encode" in line or ("duration" in line and "ref_audio_len" in line):
                print(f"{path}: {line}")
```

If you see the byte-encode lines around the `duration = ref_audio_len + int(...)` block, the patch will land cleanly. If they're gone or look different, paste the actual block back to me before patching.
