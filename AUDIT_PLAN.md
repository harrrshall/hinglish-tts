# Agent Audit Runbook — Phase 1 of Hinglish TTS Project

> **Audience:** an AI coding agent (Claude Code, Cursor agent, etc.) executing autonomously.
> **Owner of the result:** the human user, who will listen to the audio and score it.
> **Read this entire file before starting.** It is the spec. Deviations must be documented in `RUN_NOTES.md`.

---

## 0. Context (read once, do not skip)

This is Phase 1 of a Hinglish (Hindi-English code-mixed) TTS project. We are testing five existing open-source TTS models on the same set of Hinglish inputs to decide which one to fine-tune in Phase 2. **No training. Inference only.**

The five models:

| # | Model | HF repo | Approx params | Prompting style |
|---|---|---|---|---|
| 1 | Kokoro v1.0 (Hindi) | `hexgrad/Kokoro-82M` | 82M | voicepack lookup |
| 2 | IndicF5 | `ai4bharat/IndicF5` | ~330M | reference-audio + transcript |
| 3 | Indic Parler-TTS | `ai4bharat/indic-parler-tts` | ~880M | text-description + prompt |
| 4 | SPRINGLab F5-Hindi-24KHz | `SPRINGLab/F5-Hindi-24KHz` | 151M | reference-audio + transcript |
| 5 | Orpheus-Hindi | `SachinTelecmi/Orpheus-tts-hi` | 3B (run in 4-bit) | LLM-style prompt |

Compute budget: free-tier Colab T4 (15 GB usable VRAM). Kokoro can run on CPU if GPU is contended. The whole audit should fit in 4–6 GPU-hours total across separate sessions.

---

## 1. Generate the eval set (30 sentences, 4 categories)

### 1.1 Output

A single file: `audit/eval_sentences.tsv` with this exact schema (header line included):

```
id	category	text	expected_pronunciation_notes	tested_phenomenon
```

- `id`: zero-padded two-digit string, `01`–`30`.
- `category` ∈ {`pure_devanagari`, `pure_roman`, `mixed_script`, `english_with_NE`}.
- `text`: the sentence itself, UTF-8.
- `expected_pronunciation_notes`: one line, plain English, what a native Hinglish speaker would expect to hear. Used by the human scorer, not the model.
- `tested_phenomenon`: one short tag from the list in §1.4 (e.g. `homograph_hai_hi`).

Counts: **8 pure_devanagari, 8 pure_roman, 8 mixed_script, 6 english_with_NE = 30 total.**

### 1.2 Twelve anchor sentences (use these verbatim — do NOT regenerate)

Place these in the TSV with the listed IDs:

```
01	pure_devanagari	कल मुझे दिल्ली जाना है।	Standard Hindi declarative.	baseline_devanagari
02	pure_devanagari	क्या आप मुझे पानी दे सकते हैं?	Polite Hindi question.	question_devanagari
03	pure_devanagari	मेरा भाई आज स्कूल नहीं गया क्योंकि उसकी तबीयत खराब है।	Long Hindi sentence with English loanword "स्कूल" written in Devanagari.	loanword_in_devanagari
09	pure_roman	kal mujhe office jaana hai	Should sound Hindi, NOT English. "office" is the only English word.	roman_hindi_with_english_loan
10	pure_roman	mera naam Arjun hai aur mai Bengaluru se hu	"hai" is Hindi "is", NOT "hi" greeting. "Bengaluru" must be pronounced Indian, not anglicized.	homograph_hai_hi
11	pure_roman	yaar tu kal kya kar raha tha	Casual Hinglish, common words yaar/tu/kya.	casual_roman_hindi
17	mixed_script	Kal mujhe ऑफिस जाना hai, but ट्राफिक will be an issue.	The hardest case — script switches mid-sentence.	mixed_script_hard
18	mixed_script	Mera presentation tomorrow है, और मैं nervous हूं।	Hindi grammar around English content words.	mixed_script_grammar
19	mixed_script	Bhai please मेरा homework कर दे, मैं तुझे ₹100 दूंगा।	Currency symbol + Devanagari numerals/script switch.	mixed_script_currency
24	english_with_NE	My friend Aishwarya from Chennai is visiting Bengaluru next week.	Three Indian named entities in pure-English sentence.	english_with_indian_NE
25	english_with_NE	Mr. Khanna will join the meeting after he finishes lunch with Priya.	Indian surname + first name in English context.	english_with_indian_names
26	english_with_NE	I love butter chicken from Karim's in Old Delhi.	Restaurant + locality, Indian food name.	english_with_food_locality
```

### 1.3 Generate the remaining 18 sentences yourself

Fill IDs 04–08, 12–16, 20–23, 27–30 following the same pattern. **Constraints when generating:**

- **Realistic register.** Write the way Indian millennials actually message on WhatsApp / Twitter / Instagram. NOT formal Hindi mixed with formal English. Slangy, casual, abbreviated is good. "Aaj ka mausam bahut sundar hai" is BAD (overly formal and cliché). "yaar aaj weather kitna acha hai na" is the right register.
- **Length 5–15 words.** Avoid one-word inputs.
- **Vary sentence types.** At least one question, one imperative, one exclamation per category where natural.
- **Cover the phenomena tag list in §1.4.** Each phenomenon should appear at least once across the eval set.
- **No duplicates** in meaning or surface form.

### 1.4 Phenomena tag list (use these tags exactly; coverage check at end)

Required at least once each somewhere in the 30-sentence set:

`baseline_devanagari`, `question_devanagari`, `loanword_in_devanagari`, `numbers_devanagari`, `imperative_devanagari`, `roman_hindi_with_english_loan`, `homograph_hai_hi`, `casual_roman_hindi`, `roman_question`, `roman_imperative`, `mixed_script_hard`, `mixed_script_grammar`, `mixed_script_currency`, `mixed_script_question`, `english_with_indian_NE`, `english_with_indian_names`, `english_with_food_locality`, `english_with_indian_brand`.

### 1.5 Self-check after generating

Before moving to §2, the agent must:

1. Verify the file has exactly 31 lines (1 header + 30 data rows).
2. Verify each `id` 01–30 appears exactly once.
3. Verify the category counts (8/8/8/6).
4. Verify every required phenomenon tag from §1.4 appears at least once.
5. Print 5 random sentences to the run log so a human can sanity-check the register.

If any check fails, regenerate the failed sentences. Do NOT proceed to §2 with a broken eval set.

---

## 2. Reference audio prep (do this once, before §3)

Three of the five models need a reference clip + transcript: IndicF5, SPRINGLab F5-Hindi, and (optionally) Orpheus for voice cloning. Use the **same** reference for IndicF5 and SPRINGLab F5 so the comparison is fair.

### 2.1 Download one Hindi reference clip

Pull a single 3–5 second Hindi audio + transcript from a public dataset. Try in this order; fall back to next if first fails:

```python
# Option A: ai4bharat/Rasa  (CC-BY)
from huggingface_hub import hf_hub_download
import shutil, os, json

os.makedirs("audit/reference_audio", exist_ok=True)

try:
    # Try Rasa Hindi
    from datasets import load_dataset
    ds = load_dataset("ai4bharat/Rasa", "hindi", split="train", streaming=True)
    sample = next(iter(ds))
    # Inspect schema; expect 'audio' dict with 'array' + 'sampling_rate', and 'text'
    import soundfile as sf
    audio = sample["audio"]["array"]
    sr = sample["audio"]["sampling_rate"]
    text = sample["text"] if "text" in sample else sample.get("transcription", "")
    sf.write("audit/reference_audio/hindi_ref.wav", audio, sr)
    with open("audit/reference_audio/hindi_ref.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Reference saved: {sr} Hz, transcript: {text}")
except Exception as e:
    print(f"Rasa failed: {e}. Falling back.")
    # Option B: download a known sample from IndicF5's example data
    # The IndicF5 repo has prompts/ directory with reference clips
    !git clone --depth 1 https://github.com/AI4Bharat/IndicF5.git /tmp/indicf5
    import glob
    ref = glob.glob("/tmp/indicf5/prompts/*hindi*.wav") or glob.glob("/tmp/indicf5/prompts/*.wav")
    assert ref, "No reference clip found"
    shutil.copy(ref[0], "audit/reference_audio/hindi_ref.wav")
    # Look for matching transcript
    txt_candidates = glob.glob(ref[0].replace(".wav", "*.txt"))
    if txt_candidates:
        shutil.copy(txt_candidates[0], "audit/reference_audio/hindi_ref.txt")
    else:
        # Last resort: write a placeholder transcript matching a known IndicF5 demo line
        with open("audit/reference_audio/hindi_ref.txt", "w", encoding="utf-8") as f:
            f.write("नमस्ते, यह एक टेस्ट है।")
```

### 2.2 Verify

The reference must be:
- 24 kHz mono WAV (resample if needed using `librosa.resample`).
- Between 3 and 8 seconds long.
- Have a non-empty `.txt` transcript on the same path stem.

If anything is missing, fix it before §3.

---

## 3. Run inference — five separate Colab notebooks

**Create one notebook per model. Do not chain them in one notebook.** Each notebook is independently restartable.

(See `audit/notebooks/*.ipynb` for the per-model notebooks. Cell content per model is documented inline in each notebook.)

### Notebook summaries

- **N1 — Kokoro v1.0 (Hindi)** — `hexgrad/Kokoro-82M`. Voicepack `hf_alpha` for Hindi/Devanagari/Roman/Mixed; `af_heart` for english_with_NE. Save predicted phonemes from `pipe(...)` for diagnostics. Save audio @ 24 kHz mono.
- **N2 — IndicF5** — `ai4bharat/IndicF5` via `AutoModel(trust_remote_code=True)`. Reference: `audit/reference_audio/hindi_ref.{wav,txt}`. Save audio @ 24 kHz mono.
- **N3 — Indic Parler-TTS** — `ai4bharat/indic-parler-tts`. Two-tokenizer pattern. Hold the `DESCRIPTION` constant across all 30 sentences. Sample rate from `model.config.sampling_rate`.
- **N4 — SPRINGLab F5-Hindi-24KHz** — Use the SPRINGLab fork `https://github.com/rumourscape/F5-TTS`; checkpoint from `SPRINGLab/F5-Hindi-24KHz`. Same reference clip as IndicF5. Inspect repo README to confirm the inference invocation.
- **N5 — Orpheus-Hindi** — `SachinTelecmi/Orpheus-tts-hi` in 4-bit nf4 (bitsandbytes). Copy the `generate_speech` function VERBATIM from the model card; do not reconstruct from memory.

For each notebook, success criterion is `n_ok >= 28` out of 30. Errors are recorded in `log.json` not silently discarded.

---

## 4. Final folder structure (must match exactly)

```
audit/
├── eval_sentences.tsv
├── reference_audio/
│   ├── hindi_ref.wav
│   └── hindi_ref.txt
├── results/
│   ├── kokoro/        { 01.wav … 30.wav, log.json }
│   ├── indicf5/       { 01.wav … 30.wav, log.json }
│   ├── indic_parler/  { 01.wav … 30.wav, log.json }
│   ├── springlab_f5/  { 01.wav … 30.wav, log.json }
│   └── orpheus_hi/    { 01.wav … 30.wav, log.json }
├── scoring_template.csv     ← see §5
├── RUN_NOTES.md             ← deviations, errors, install gotchas
└── METADATA.json            ← see §5
```

Zip the whole `audit/` directory at the end as `audit_phase1_<YYYYMMDD>.zip` for handoff.

---

## 5. Auxiliary files

### 5.1 `audit/METADATA.json`

```json
{
  "audit_date_utc": "<ISO-8601 timestamp at run start>",
  "agent": "<name and version of the agent that ran this>",
  "compute": {"platform": "Colab Free Tier", "gpu": "Tesla T4", "vram_gb": 15},
  "models": [
    {"name": "kokoro_v1", "hf_repo": "hexgrad/Kokoro-82M", "params_M": 82, "voice": "hf_alpha"},
    {"name": "indicf5", "hf_repo": "ai4bharat/IndicF5", "params_M": 330},
    {"name": "indic_parler", "hf_repo": "ai4bharat/indic-parler-tts", "params_M": 880, "description_prompt": "<copy the exact string used>"},
    {"name": "springlab_f5", "hf_repo": "SPRINGLab/F5-Hindi-24KHz", "params_M": 151},
    {"name": "orpheus_hi", "hf_repo": "SachinTelecmi/Orpheus-tts-hi", "params_M": 3000, "quantization": "4bit_nf4"}
  ],
  "reference_audio": {"path": "reference_audio/hindi_ref.wav", "transcript_path": "reference_audio/hindi_ref.txt", "source": "<dataset name + sample id>"},
  "eval_set": {"path": "eval_sentences.tsv", "n_sentences": 30, "categories": {"pure_devanagari": 8, "pure_roman": 8, "mixed_script": 8, "english_with_NE": 6}},
  "success_counts": {"kokoro": 0, "indicf5": 0, "indic_parler": 0, "springlab_f5": 0, "orpheus_hi": 0}
}
```

Fill `success_counts` from each model's `log.json` after all five notebooks finish.

### 5.2 `audit/scoring_template.csv`

One row per (model, sentence) pair = 150 rows. Header:

```
model,id,category,text,intelligibility_1to5,naturalness_1to5,code_switch_handling_1to5,speaker_quality_1to5,roman_treated_as_english,silence_or_skip,end_of_clip_pop,notes
```

Pre-fill `model, id, category, text`. Sort by `id`, then by `model`. Boolean flag columns take `TRUE`/`FALSE`/blank.

### 5.3 `audit/RUN_NOTES.md`

```markdown
# Run Notes

## Install gotchas
- (one bullet per dependency surprise)

## Per-model deviations from runbook
- Kokoro: ...
- IndicF5: ...
- ...

## Errors encountered (and resolution, if any)
- ...

## Times
- Eval set generation: X minutes
- Reference audio prep: X minutes
- Notebook 1 (Kokoro) total wall-clock: X minutes
- ... etc.

## Sanity-check summary
- Total audio files: 150 / 150 expected
- Zero-byte files: 0
- Missing logs: 0
```

---

## 6. Self-check before declaring done (`audit/scripts/verify.py`)

Verifies eval set, reference audio, per-model 30 wav + log.json, auxiliary files. Exits 0 only when everything is present and non-empty.

---

## 7. Hand-off message → `audit/HANDOFF.md`

1. **Summary line** with success counts.
2. **Per-model success counts** (from each `log.json`).
3. **Top three install/runtime gotchas** copy-pasted from `RUN_NOTES.md`.
4. **One paragraph of agent observations** (factual, not subjective).
5. **Direct path to the zip**: `audit_phase1_<YYYYMMDD>.zip`.

The human will then listen to all 150 clips, fill in `scoring_template.csv`, and send the scored CSV back for Phase 2.

---

*End of runbook. Total expected agent runtime: 4–6 GPU-hours plus 1–2 hours of debugging when (not if) one of the models has a fresh API change.*
