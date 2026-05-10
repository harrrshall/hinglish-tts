# Kaggle cells — IndicF5 (patched) + IndicXlit input preprocessing

Phase 2 Step 2a. Hypothesis: IndicF5's character embeddings for ASCII are
undertrained (Mode C in the patched-only diagnosis); feeding the model
Devanagari-only input via IndicXlit preprocessing should let it use
characters it has seen during training.

This re-uses the existing patched kernel
`harshalsinghcn/hinglish-tts-audit-indicf5` (last successful run = v13 with
the duration patch already applied). Preprocessing is **already done locally**
— `audit/indicf5_patched_xlit/preprocessed_sentences.tsv` (6.5 KB, 30 rows)
contains the input we want IndicF5 to see. Just paste it into the kernel
inline.

The ONLY changes vs v13:

- **Skip the patch cell** — the file is already patched. Verify the marker.
- **New input cell** loads preprocessed sentences from a TSV string instead
  of `eval_sentences.tsv`.
- **Inference cell** reads `text_preprocessed` and writes to
  `results/indicf5_patched_xlit/` (NOT `results/indicf5_patched/`, which must
  stay intact for comparison).

## Cell ordering

| Position | v13 cell | Action for v14 |
|----------|----------|----------------|
| Cell 1 | `pip install … IndicF5.git` | **keep as-is** |
| Cell 2 | `AUDIT_DIR` setup | **keep as-is** |
| Cell 3 | load `eval_sentences.tsv` | **REPLACE with PREPROCESSED_INPUT_CELL below** |
| Cell 3.5 | duration patch | **REPLACE with PATCH_VERIFICATION_CELL below** (assert-only, no rewrite) |
| Cell 4 | model load | **keep as-is** |
| Cell 4.5 | sanity (sentence 09) | **DELETE** (already validated in v13; saves T4 time) |
| Cell 5 | inference loop | **REPLACE with INFERENCE_CELL below** |

The patched kernel's site-packages persists across kernel sessions on Kaggle
unless Cell 1 re-installs from scratch, so the DEBUG-PATCH marker should
still be present when you re-open. Verification takes <100 ms.

---

## PREPROCESSED_INPUT_CELL (replaces existing Cell 3)

The TSV is small (6.5 KB / 30 rows), so paste it inline. Open
`audit/indicf5_patched_xlit/preprocessed_sentences.tsv` locally and paste
the **full content** between the triple quotes below before saving the
kernel.

```python
# === Cell 3 (replacement): Load IndicXlit-preprocessed sentences ===
# Source: audit/indicf5_patched_xlit/preprocessed_sentences.tsv (generated locally
# 2026-05-10 by audit/scripts/preprocess_input.py using lib_normalize.to_unified_devanagari).
# Phase 2 Step 2a — see audit/indicf5_patched_xlit/preprocessing_review.md for the
# per-category review of what changed.
import csv, io

PREPROCESSED_TSV = """\
<<< PASTE THE FULL CONTENTS OF preprocessed_sentences.tsv HERE — including the header row >>>
"""

rows = list(csv.DictReader(io.StringIO(PREPROCESSED_TSV), delimiter="\t"))
assert len(rows) == 30, f"Expected 30 rows, got {len(rows)} — TSV paste truncated?"
required_cols = {"id", "category", "text_original", "text_preprocessed", "preprocessing_applied"}
missing = required_cols - set(rows[0].keys())
assert not missing, f"Missing columns: {missing}"

# Sanity: pure_devanagari rows must be unchanged by preprocessing.
for r in rows:
    if r["category"] == "pure_devanagari" and r["preprocessing_applied"] == "yes":
        raise AssertionError(
            f"id={r['id']}: pure_devanagari row was changed by preprocessing — "
            f"this would invalidate the comparison.\n"
            f"  original:    {r['text_original']!r}\n"
            f"  preprocessed: {r['text_preprocessed']!r}"
        )

n_changed = sum(1 for r in rows if r["preprocessing_applied"] == "yes")
print(f"Loaded {len(rows)} preprocessed sentences "
      f"({n_changed} changed by IndicXlit, {len(rows) - n_changed} unchanged).")
print("Per-category counts:")
from collections import Counter
for cat, cnt in sorted(Counter(r["category"] for r in rows).items()):
    print(f"  {cat:20s} {cnt}")
```

**Expected stdout:**
```
Loaded 30 preprocessed sentences (22 changed by IndicXlit, 8 unchanged).
Per-category counts:
  english_with_NE      6
  mixed_script         8
  pure_devanagari      8
  pure_roman           8
```

---

## PATCH_VERIFICATION_CELL (replaces existing Cell 3.5 — verify only, no rewrite)

```python
# === Cell 3.5 (replacement): VERIFY the duration patch is still in place ===
# The patch was applied in v13. Site-packages persists; do not re-patch.
import sys, glob

candidates = []
for root in [p for p in sys.path if p]:
    candidates.extend(glob.glob(f"{root}/**/f5_tts/infer/utils_infer.py", recursive=True))
candidates = sorted(set(candidates))
assert candidates, "No f5_tts/infer/utils_infer.py found. Did Cell 1 install IndicF5?"

n_patched = 0
for path in candidates:
    with open(path, encoding="utf-8") as f:
        src = f.read()
    if "DEBUG-PATCH" in src:
        n_patched += 1
        print(f"  [OK] DEBUG-PATCH marker present in {path}")
    else:
        print(f"  [MISSING] {path}")

assert n_patched > 0, (
    "Duration patch is NOT present in any f5_tts/infer/utils_infer.py.\n"
    "This kernel may have been re-installed since v13. Re-run the original\n"
    "patched kernel's PATCH_CELL (audit/indicf5_patched/KAGGLE_CELLS.md) before continuing.\n"
    "Otherwise this run will reproduce the original Mode-A truncation, not the patched-only baseline."
)
print(f"\n✓ Patch present in {n_patched}/{len(candidates)} file(s). Safe to proceed.")

# Drop any cached f5_tts modules so the model load picks up the patched source.
to_drop = [m for m in sys.modules if m.startswith("f5_tts")]
for m in to_drop:
    del sys.modules[m]
print(f"Cleared {len(to_drop)} f5_tts module(s) from sys.modules.")
```

**Expected output:**
```
  [OK] DEBUG-PATCH marker present in /opt/conda/lib/python3.X/site-packages/f5_tts/infer/utils_infer.py
✓ Patch present in 1/1 file(s). Safe to proceed.
Cleared N f5_tts module(s) from sys.modules.
```

If `[MISSING]` appears, stop. Re-run the original patch cell from
`audit/indicf5_patched/KAGGLE_CELLS.md` PATCH_CELL section before continuing.

---

## INFERENCE_CELL (replaces existing Cell 5)

Reads `text_preprocessed` (NOT `text_original`) and writes wavs to
`audit/results/indicf5_patched_xlit/`. Each per-sentence log entry records
both `text_original` and `text_preprocessed` so the comparison report can
trace what the model actually saw.

```python
# === Cell 5 (replacement): Run patched IndicF5 on IndicXlit-preprocessed inputs ===
import io, sys, time, json
from pathlib import Path
import numpy as np, soundfile as sf, torch

OUT = Path(AUDIT_DIR) / "results" / "indicf5_patched_xlit"
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
            rid = r["id"]
            cat = r["category"]
            text_orig = r["text_original"]
            text_in   = r["text_preprocessed"]   # <<< THIS is what the model sees
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
                    "preprocessing_applied": r["preprocessing_applied"],
                    "duration_s": float(len(audio) / 24000),
                    "elapsed_s": time.time() - t0,
                    "status": "ok",
                })
                print(f"    ok: {len(audio)/24000:.3f}s wav, {time.time()-t0:.1f}s wall")
            except Exception as e:
                results_log.append({
                    "id": rid, "category": cat,
                    "text_original": text_orig,
                    "text_preprocessed": text_in,
                    "preprocessing_applied": r["preprocessing_applied"],
                    "status": "error", "error": str(e),
                })
                print(f"    [error] {e}")
    finally:
        sys.stdout = real_stdout

with open(OUT / "log.json", "w", encoding="utf-8") as f:
    json.dump(results_log, f, ensure_ascii=False, indent=2)

n_ok = sum(1 for x in results_log if x["status"] == "ok")
print(f"\nindicf5_patched_xlit: {n_ok}/30 succeeded")
print(f"  wavs: {OUT}")
print(f"  duration log (DEBUG-PATCH lines): {log_path}")
print(f"  inference log: {OUT / 'log.json'}")
```

**Expected output:**
- 30 lines of `DEBUG-PATCH` from `utils_infer.py`, interleaved with
  per-sentence success messages (showing both original and preprocessed).
- `indicf5_patched_xlit: 30/30 succeeded`.
- pure_devanagari rows produce wavs near-identical to the existing
  patched-only outputs (preprocessing was a no-op there). pure_roman /
  mixed_script / english_with_NE rows are the actual test.

**Stop and report if** more than 5/30 rows hit `[error]`. That would
suggest the preprocessed strings contain characters or sequences the model
can't tokenize — itself a finding, but it kills the comparison.

---

## After the run — bundle to bring back

```
audit/results/indicf5_patched_xlit/
├── 01.wav … 30.wav         (30 wavs from preprocessed inputs)
├── duration_log.txt        (30 DEBUG-PATCH lines + per-sentence wall times + orig/preprocessed text)
└── log.json                (per-sentence status with text_original AND text_preprocessed)
```

Bundle:
```bash
tar czf indicf5_patched_xlit.tgz audit/results/indicf5_patched_xlit/
```

Download from Kaggle file browser. Local Phase 4 (re-score under v2 rubric)
and Phase 5 (three-way comparison report) take this as input.

## Quick smoke check before the long run

If you want to sanity-check the preprocessed input cell without running 30
inferences, drop this temporary cell after Cell 3:

```python
# Print id=09 and id=24 to confirm the preprocessed text is what we expect
for rid in ["9", "24"]:
    r = next(r for r in rows if r["id"] == rid)
    print(f"id={rid} ({r['category']}):")
    print(f"  original:    {r['text_original']}")
    print(f"  preprocessed: {r['text_preprocessed']}")
```

Expected output:
```
id=9 (pure_roman):
  original:    kal mujhe office jaana hai
  preprocessed: कल मुझे ऑफिस जाना है
id=24 (english_with_NE):
  original:    My friend Aishwarya from Chennai is visiting Bengaluru next week.
  preprocessed: माय फ्रेंड ऐश्वर्या फ्रॉम चेन्नई इस विज़िटिंग बेंगलुरु नेक्स्ट वीक.
```
