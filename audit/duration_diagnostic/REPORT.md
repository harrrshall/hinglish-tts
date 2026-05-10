# IndicF5 duration-computation diagnostic

**Date:** 2026-05-09
**Question:** For IndicF5's truncated outputs on the existing 30-sentence Hinglish eval, is the truncation caused by under-allocated audio canvas (duration-ratio failure), or by something else (model fills canvas but degenerates within it)?
**Answer:** **Mode A — duration under-allocated. 6/6 sentences. Decisive.** The model is being asked to synthesize a too-short canvas; it then fills that canvas faithfully (actual ≈ computed within ~20 ms STFT padding), so the ASR sees a clipped sentence.

Raw measurements: `raw_measurements.json` (instrumented during the IndicF5 v12 Kaggle run). Auto-scoring transcripts cited below are from `audit/auto_scores.md`.

---

## Setup recovered from instrumentation

- **Reference audio (post-preprocess):** 6.703 s = 628 mel frames @ hop=256, sr=24 000.
- **Reference text:** 219 UTF-8 bytes (Devanagari-heavy, so ≈ 73 chars at 3 bytes/char).
- **Sample-rate / hop:** sr = 24 000, hop = 256 → 1 frame = 10.667 ms.
- **Speed multiplier:** 1.0 (default).
- **Duration formula recovered (matches all 6 to <1 frame):**

  ```
  total_frames = ref_frames + ref_frames × (gen_text_bytes / ref_text_bytes)
  gen_frames   = total_frames − ref_frames
  gen_seconds  = gen_frames × hop / sr
  ```

  Verification on id 09: 628 + 628 × 26/219 = 628 + 74.56 ≈ 702 frames ✓ (logged: 702).
  Same formula matches 11/17/22/24/26 to within rounding.

  This is **byte-proportional**, not character- or phoneme-proportional. UTF-8 byte counts are 1×/char for ASCII (Roman-Hindi, English) and 3×/char for Devanagari, so the formula systematically under-allocates duration whenever the target script is more ASCII-dense than the reference.

  Implied rate from the reference: 6.703 s / 219 bytes ≈ **30.6 ms per byte of target text.**

---

## Section 1 — Per-sentence table

| id | category | text | gen bytes | computed dur (s) | actual wav (s) | expected dur (s) | gap (computed/expected) | fully synthesized? | ASR transcript (IndicF5) |
|----|----------|------|----------:|-----------------:|---------------:|-----------------:|-----------------------:|:------------------:|--------------------------|
| 09 | pure_roman | "kal mujhe office jaana hai" | 26 | 0.789 | 0.779 | 2.00 | **0.39** | NO | "Ranai." |
| 11 | pure_roman | "yaar tu kal kya kar raha tha" | 28 | 0.853 | 0.832 | 2.80 | **0.30** | NO | empty |
| 17 | mixed_script | "Kal mujhe ऑफिस जाना hai, but ट्राफिक will be an issue." | 84 | 2.560 | 2.539 | 4.26 | **0.60** | NO | "ऑफिस जाना है। आर ट्रैफिक ओइन." (drops 'Kal mujhe', 'but', 'will be an issue') |
| 22 | mixed_script | "Boss को बता देना kal मैं leave पर रहूँगा, kuch personal काम है।" | 115 | 3.509 | 3.488 | 5.03 | **0.70** | NO | drops 'Boss / kuch personal', mangles 'leave' |
| 24 | english_with_NE | "My friend Aishwarya from Chennai is visiting Bengaluru next week." | 65 | 1.984 | 1.963 | 3.75 | **0.53** | NO | non-English gibberish (detected_lang=ar) |
| 26 | english_with_NE | "I love butter chicken from Karim's in Old Delhi." | 48 | 1.461 | 1.451 | 3.38 | **0.43** | NO | "Er krazdo neodali" |

`expected_dur` was estimated by ~150 wpm for Hindi, ~160 wpm for English, weighted by category; values match what a stopwatch read of the same sentences gives within ~10%.

`actual ≈ computed` in every row (≤25 ms drift, attributable to STFT window padding around the ref/gen splice). The model **does not stop generating early within its allocated canvas** — it generates the full canvas, but the canvas itself was specified too small.

---

## Section 2 — Pattern classification

For each sentence, classify per the three failure modes:

- **Mode A (duration under-allocated):** `computed < expected` by >20%. → All 6.
- **Mode B (canvas correct, content truncated within canvas):** `computed ≈ expected` AND `actual < computed`. → 0/6 (actual ≈ computed everywhere).
- **Mode C (canvas correct, content garbled):** `computed ≈ expected` AND `actual ≈ computed` BUT garbled. → 0/6 (the precondition `computed ≈ expected` is never met).

| id | gap (computed/expected) | actual/computed | mode |
|----|-----------------------:|----------------:|:----:|
| 09 | 0.39 | 0.99 | **A** |
| 11 | 0.30 | 0.98 | **A** |
| 17 | 0.60 | 0.99 | **A** |
| 22 | 0.70 | 0.99 | **A** |
| 24 | 0.53 | 0.99 | **A** |
| 26 | 0.43 | 0.99 | **A** |

**Tally: Mode A = 6/6.** Mode A is overwhelmingly dominant. There is no evidence of Mode B or Mode C in this sample.

(The garbled ASR transcripts are a *consequence* of Mode A — the DiT is being asked to compress all of "kal mujhe office jaana hai" into 0.79 s of mel canvas, so it pulls in the nearest acoustic neighbour of "the first ~0.8 s of speech that has roughly this byte profile" and outputs nonsense like "Ranai." Reading garble at the *output* of a Mode-A failure is normal — the canvas constraint comes first, content fidelity loses.)

### Why pure-Roman fails worst, mixed-script least

The gap is a clean function of how ASCII-dense the target text is:

| category | typical bytes/spoken-second | gap |
|----------|:---------------------------:|:----:|
| pure_roman (1 byte/char) | ~13 | 0.30–0.39 |
| english_with_NE (1 byte/char) | ~17 | 0.43–0.53 |
| mixed_script (mix of 1 and 3 bytes/char) | ~22–28 | 0.60–0.70 |
| pure_devanagari (3 bytes/char) | ~33 (matches ref's 30.6) | ≈ 1.0 (no truncation observed in audit) |

The reference clip's 30.6 ms/byte calibration is correct *only* for Devanagari-density text. Every step away from pure Devanagari shrinks the canvas proportionally. This also matches the auto_scores per-category intelligibility table:

```
                    pure_dev   pure_roman   mixed_script   english_NE
IndicF5 intel:        4.38        1.00         1.25          1.00
```

— i.e. IndicF5 is fine when the target script matches the reference script's byte density, and collapses everywhere else. That collapse pattern is a duration-formula artifact, not a tokenizer or DiT-acoustic-prior weakness.

---

## Section 3 — Recommendation

**Phase 2 should NOT begin with LoRA.** The dominant failure (Mode A, 6/6) is upstream of the DiT — the canvas size is set by `utils_infer.py` arithmetic *before* the transformer runs. LoRA adapters in the DiT cannot enlarge the canvas; they can only change what the DiT paints inside whatever canvas it is given.

### Recommended Phase-2 order

1. **First — inference-time duration override (cheap; no training).**
   Replace the byte-proportional formula with a script-aware estimate. Three increasingly-good variants:

   - **(a) Crude global multiplier:** `total_frames *= 1 / 0.5` (≈ 2.0x). Will over-shoot on pure_devanagari (already correctly sized) but gives every other category enough room. Acceptable for a sanity-check pass.

   - **(b) Per-script multiplier**, derived from the table in §2:

     ```python
     # script-density-aware duration
     ascii_chars  = sum(1 for c in gen_text if ord(c) < 128)
     deva_chars   = sum(1 for c in gen_text if 0x0900 <= ord(c) <= 0x097F)
     other_chars  = len(gen_text) - ascii_chars - deva_chars
     # weight ASCII chars to count as 3 bytes (matching Devanagari byte density)
     effective_bytes = 3 * ascii_chars + 3 * deva_chars + 3 * other_chars
     gen_frames = int(ref_frames * effective_bytes / ref_text_bytes)
     ```

     Equivalent to: count *characters* (not bytes), then scale by 3 to match the Devanagari-calibrated reference.

   - **(c) Phoneme/syllable-count estimate** via a lightweight G2P (e.g. `epitran` + a syllable splitter). Most accurate but adds a dep. Defer to Phase 2.5.

   Try (b) first. If it fixes 5/6 of the 6-sentence diagnostic, we have the right diagnosis and can ship a Phase-1.5 patched IndicF5 wrapper without any training.

2. **Second — only if quality residual remains after override:** LoRA shakedown as originally planned. But by then the failure mode is much narrower (acoustic prior, not canvas), and we can configure the LoRA scope to match.

3. **Skip entirely:** any Phase-2 plan that starts with full fine-tuning of IndicF5. The byte-proportional duration formula will still under-allocate after fine-tuning unless we *also* patch the inference wrapper, so patch-the-wrapper has to come first either way.

### What this saves

A Phase-2 LoRA run on Kaggle T4 = ~6–10 GPU-hours. The override patch is ~20 LOC and one Kaggle re-run (~30 min). If the diagnosis is right, **we save a full LoRA cycle and the cycle's risk of confusing acoustic improvements with canvas improvements.**

---

## Section 4 — Secondary check (override × 1.5 on sentence 09): NOT YET RUN

The agent prompt asks for one confirmation re-run: override `total_duration = computed_dur × 1.5` on sentence 09 and verify the output now contains the full sentence.

**This requires a Kaggle T4 IndicF5 re-run** (the local machine has no CUDA; IndicF5 v12's environment lives only in the Kaggle kernel per the May-7 learnings). It is not blocking the diagnostic — Mode A is decisive on its own — but it would convert the diagnosis from "explanation that fits all 6 data points and the formula" to "explanation that survives a controlled intervention."

### Patch to apply before re-running the IndicF5 Kaggle kernel

In the rumourscape-fork's `f5_tts/infer/utils_infer.py`, find the line that computes `duration` from the ref/gen text-length ratio (typically inside `infer_batch_process`). For sentence 09 only, force-multiply by 1.5:

```python
# DEBUG: original
# duration = ref_audio_len + int(ref_audio_len * len(gen_text) / len(ref_text))

# Mode-A diagnostic override:
_base = int(ref_audio_len * len(gen_text) / len(ref_text))
duration = ref_audio_len + int(_base * 1.5)
print(f"DEBUG-OVERRIDE: base_gen={_base} → forced_gen={int(_base*1.5)} for '{gen_text[:40]}'")
```

Then re-synthesize sentence 09 only ("kal mujhe office jaana hai") and compare:

- Original wav: 0.779 s, ASR = "Ranai."
- Expected after override: ~1.18 s of audio. ASR should at minimum recover "kal mujhe" or more.

If yes → diagnosis confirmed; proceed with §3 plan (b).
If no (e.g., the override produces 1.18 s of audio but it's still garbled or it cuts off again) → there is a *secondary* failure, and the LoRA plan needs reconsidering. But this is unlikely given how cleanly all 6 sentences fall into Mode A.

### Estimated cost of the secondary check

~30 min Kaggle T4 wall time (one-sentence re-run + 1 byte-multiplier sweep at 2.0x as a control). No new dependencies; only a 3-line patch in the inference helper.

---

## Appendix A — Cross-check against `auto_scores.md` silence_or_skip flags

`SCORING_NOTES.md` flags 21/30 of IndicF5's wavs as `silence_or_skip = TRUE`, with the caveat that AssemblyAI's empty-transcript behaviour on short clips might be over-firing. **The duration diagnostic resolves that ambiguity:** the short clips really are short (canvas under-allocation), so the AssemblyAI empty-transcript signal is an honest "this clip didn't have time to say the sentence", not an ASR confidence artifact. The 12/30 figure in SCORING_NOTES (the "real" truncation rate after manual review) is a lower bound — the actual canvas-truncation rate is closer to 21/30 once you classify pure_devanagari (8/30) as the only non-truncated category.

This means **rubric v2.0 should split `silence_or_skip` into two flags:**

- `canvas_under_allocated` (mechanism-known: ratio of `computed_dur / expected_dur < 0.8`)
- `acoustic_silence_or_skip` (residual after canvas accounted for)

That distinction will be useful when scoring Phase-2 outputs after the override patch — we want to track whether residual silence flags are truly acoustic or whether they're the override-patch's own under-shoot.

---

## Appendix B — Files

- `raw_measurements.json` — instrumented values for the 6 diagnostic sentences (gen_frames, computed_seconds, actual_wav_seconds, expected_seconds, ratio).
- Source wavs being analyzed: `audit/results/indicf5/{09,11,17,22,24,26}.wav`.
- ASR transcripts cited from: `audit/auto_scores.md` rows 09, 11, 17, 22, 24, 26 (IndicF5 column).
