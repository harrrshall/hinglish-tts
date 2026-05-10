#!/usr/bin/env python3
"""Build the 5 Colab notebooks under audit/notebooks/ from in-script content.

Source-of-truth lives here, not in the .ipynb files (regenerate by re-running).
Each notebook is independently restartable on a fresh Colab runtime — installs,
loads model, reads `audit/eval_sentences.tsv`, writes `audit/results/<model>/`.

Run:
    python audit/scripts/build_notebooks.py
"""
from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "audit" / "notebooks"


def md(src: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": src.splitlines(keepends=True)}


def code(src: str) -> dict:
    return {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": src.splitlines(keepends=True),
    }


def write_notebook(name: str, cells: list[dict]) -> Path:
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.10"},
            "colab": {"provenance": [], "gpuType": "T4"},
            "accelerator": "GPU",
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{name}.ipynb"
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1))
    return path


# ── Shared cells ───────────────────────────────────────────────────────────
COLAB_BOOTSTRAP = """\
# Mount Drive (or skip if running locally) and clone the audit folder.
# Adjust this cell to point AUDIT_DIR at wherever audit/ lives in your runtime.
import os
from pathlib import Path

# Two common patterns:
#   1. Colab + Drive: AUDIT_DIR = "/content/drive/MyDrive/hienglish/audit"
#   2. Colab + git clone:
#         !git clone https://github.com/<you>/hienglish.git /content/hienglish
#         AUDIT_DIR = "/content/hienglish/audit"
#   3. Local: AUDIT_DIR = str(Path.cwd().parent / "audit")  (if launched from notebooks/)

AUDIT_DIR = os.environ.get("AUDIT_DIR", "/content/audit")
assert Path(AUDIT_DIR).is_dir(), f"AUDIT_DIR={AUDIT_DIR} missing — set it before running."
print(f"AUDIT_DIR = {AUDIT_DIR}")
"""

LOAD_EVAL = """\
import csv
from pathlib import Path

EVAL_TSV = Path(AUDIT_DIR) / "eval_sentences.tsv"
with open(EVAL_TSV, encoding="utf-8") as f:
    rows = list(csv.DictReader(f, delimiter="\\t"))

assert len(rows) == 30, f"expected 30 sentences, got {len(rows)}"
print(f"Loaded {len(rows)} sentences from {EVAL_TSV}")
print(rows[0])
"""

WRAP_AND_SAVE_LOG = """\
import json
out_log = Path(OUT) / "log.json"
with open(out_log, "w", encoding="utf-8") as f:
    json.dump(log, f, ensure_ascii=False, indent=2)

n_ok = sum(1 for x in log if x["status"] == "ok")
print(f"{MODEL_NAME}: {n_ok}/30 succeeded — log at {out_log}")
"""


# ── 1. Kokoro v1.0 (Hindi) ─────────────────────────────────────────────────
def kokoro_cells() -> list[dict]:
    return [
        md("""\
# Notebook 1 — Kokoro v1.0 (Hindi)

- Repo: https://github.com/hexgrad/kokoro
- Model: https://huggingface.co/hexgrad/Kokoro-82M
- Voices: https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md
- Hindi voices: `hf_alpha`, `hf_beta` (female), `hm_omega`, `hm_psi` (male)

> Kokoro saw only ~6 hours of Hindi at training. Set expectations low for naturalness.
> If `lang_code='h'` rejects Roman-script Hinglish, **the error becomes the data point** —
> catch and log it; do NOT silently fall back to English.
"""),
        code("# === Cell 1: install ===\n"
             "!pip install -q \"kokoro>=0.9.4\" soundfile\n"
             "!apt-get -qq -y install espeak-ng > /dev/null"),
        code(COLAB_BOOTSTRAP),
        code(LOAD_EVAL),
        code("""\
# === Cell 4: build pipelines ===
from pathlib import Path
import time, json
import numpy as np
import soundfile as sf
from kokoro import KPipeline

MODEL_NAME = "kokoro"
OUT = Path(AUDIT_DIR) / "results" / MODEL_NAME
OUT.mkdir(parents=True, exist_ok=True)

# Two pipelines: Hindi for everything Devanagari/Hindi-leaning,
# American English ONLY for english_with_NE category.
pipe_hi = KPipeline(lang_code="h")
pipe_en = KPipeline(lang_code="a")

VOICE_HI = "hf_alpha"   # female Hindi
VOICE_EN = "af_heart"   # female American English
"""),
        code("""\
# === Cell 5: run inference, save audio + log ===
log = []
for r in rows:
    rid, cat, text = r["id"], r["category"], r["text"]
    t0 = time.time()
    try:
        if cat == "english_with_NE":
            pipe, voice = pipe_en, VOICE_EN
        else:
            # Hindi pipeline for ALL non-English categories — including pure_roman
            # and mixed_script. We want to see if it copes or breaks.
            pipe, voice = pipe_hi, VOICE_HI

        gen = pipe(text, voice=voice, speed=1.0)
        chunks, phonemes = [], []
        for gs, ps, audio in gen:
            chunks.append(audio); phonemes.append(ps)
        full = np.concatenate(chunks) if chunks else np.zeros(1, dtype=np.float32)
        out_path = OUT / f"{rid}.wav"
        sf.write(out_path, full, 24000)
        log.append({
            "id": rid, "category": cat, "voice": voice,
            "phonemes": " ".join(phonemes),
            "duration_s": float(len(full) / 24000),
            "elapsed_s": time.time() - t0,
            "status": "ok",
        })
    except Exception as e:
        log.append({"id": rid, "category": cat, "status": "error", "error": str(e)})
        print(f"  [error] {rid}: {e}")
"""),
        code(WRAP_AND_SAVE_LOG),
        code("""\
# === Cell 7: sanity check ===
n_ok = sum(1 for x in log if x["status"] == "ok")
assert n_ok >= 28, f"Too many failures: {30 - n_ok}. Inspect log.json before declaring done."
"""),
    ]


# ── 2. IndicF5 ─────────────────────────────────────────────────────────────
def indicf5_cells() -> list[dict]:
    return [
        md("""\
# Notebook 2 — IndicF5

- Repo: https://github.com/AI4Bharat/IndicF5
- Model: https://huggingface.co/ai4bharat/IndicF5  (gated — accept terms + `huggingface-cli login`)
- Reference-audio prompted (F5-TTS family). Output 24 kHz mono.
- Trained on Indic only, no Hinglish — pure Roman / English-NE inputs are out-of-distribution by design.
"""),
        code("""\
# === Cell 1: install ===
!pip install -q transformers soundfile
!pip install -q git+https://github.com/AI4Bharat/IndicF5.git

# Login if needed (paste your HF token):
# from huggingface_hub import login; login()
"""),
        code(COLAB_BOOTSTRAP),
        code(LOAD_EVAL),
        code("""\
# === Cell 4: load model + reference clip ===
from pathlib import Path
import time, json
import numpy as np
import soundfile as sf
import torch
from transformers import AutoModel

MODEL_NAME = "indicf5"
OUT = Path(AUDIT_DIR) / "results" / MODEL_NAME
OUT.mkdir(parents=True, exist_ok=True)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = AutoModel.from_pretrained("ai4bharat/IndicF5", trust_remote_code=True).to(device)

REF_AUDIO = str(Path(AUDIT_DIR) / "reference_audio" / "hindi_ref.wav")
with open(Path(AUDIT_DIR) / "reference_audio" / "hindi_ref.txt", encoding="utf-8") as f:
    REF_TEXT = f.read().strip()
assert REF_TEXT, "reference transcript is empty"
print(f"REF_AUDIO={REF_AUDIO}")
print(f"REF_TEXT={REF_TEXT}")
"""),
        code("""\
# === Cell 5: run inference ===
log = []
for r in rows:
    rid, cat, text = r["id"], r["category"], r["text"]
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
        log.append({
            "id": rid, "category": cat,
            "duration_s": float(len(audio) / 24000),
            "elapsed_s": time.time() - t0,
            "status": "ok",
        })
    except Exception as e:
        log.append({"id": rid, "category": cat, "status": "error", "error": str(e)})
        print(f"  [error] {rid}: {e}")
"""),
        code(WRAP_AND_SAVE_LOG),
    ]


# ── 3. Indic Parler-TTS ────────────────────────────────────────────────────
def indic_parler_cells() -> list[dict]:
    return [
        md("""\
# Notebook 3 — Indic Parler-TTS

- Repo: https://github.com/huggingface/parler-tts
- Model: https://huggingface.co/ai4bharat/indic-parler-tts
- Description-prompted; **two-tokenizer pattern** (description ↔ Flan-T5 tokenizer; transcript ↔ model prompt tokenizer).
- The DESCRIPTION string is **held constant** across all 30 sentences — varying it per sentence would confound the comparison.
- Strongest Hinglish prior of the five (joint Indic + English 1806 h corpus).
"""),
        code("""\
# === Cell 1: install ===
!pip install -q git+https://github.com/huggingface/parler-tts.git
!pip install -q "transformers>=4.46,<4.50" accelerate soundfile sentencepiece
"""),
        code(COLAB_BOOTSTRAP),
        code(LOAD_EVAL),
        code("""\
# === Cell 4: load ===
from pathlib import Path
import time, json
import torch
import soundfile as sf
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer

MODEL_NAME = "indic_parler"
OUT = Path(AUDIT_DIR) / "results" / MODEL_NAME
OUT.mkdir(parents=True, exist_ok=True)

device = "cuda" if torch.cuda.is_available() else "cpu"
dtype  = torch.float16 if device == "cuda" else torch.float32

REPO = "ai4bharat/indic-parler-tts"
model     = ParlerTTSForConditionalGeneration.from_pretrained(REPO, torch_dtype=dtype).to(device)
tok       = AutoTokenizer.from_pretrained(REPO)
desc_tok  = AutoTokenizer.from_pretrained(model.config.text_encoder._name_or_path)
SR = int(model.config.sampling_rate)

# Held constant for fair comparison across all 30 sentences:
DESCRIPTION = (
    "A female speaker delivers a clear, moderately-paced Hindi speech "
    "with neutral expression. The recording is high quality with no background noise."
)
desc_input_ids = desc_tok(DESCRIPTION, return_tensors="pt").input_ids.to(device)
print(f"sampling_rate={SR}, dtype={dtype}, device={device}")
"""),
        code("""\
# === Cell 5: run inference ===
log = []
for r in rows:
    rid, cat, text = r["id"], r["category"], r["text"]
    t0 = time.time()
    try:
        prompt_input_ids = tok(text, return_tensors="pt").input_ids.to(device)
        with torch.no_grad():
            gen = model.generate(input_ids=desc_input_ids, prompt_input_ids=prompt_input_ids)
        audio = gen.cpu().to(torch.float32).numpy().squeeze()
        out_path = OUT / f"{rid}.wav"
        sf.write(out_path, audio, SR)
        log.append({
            "id": rid, "category": cat, "sr": SR,
            "duration_s": float(len(audio) / SR),
            "elapsed_s": time.time() - t0,
            "status": "ok",
        })
    except Exception as e:
        log.append({"id": rid, "category": cat, "status": "error", "error": str(e)})
        print(f"  [error] {rid}: {e}")
        # If OOM on long sentences: clear cache and continue
        torch.cuda.empty_cache()
"""),
        code(WRAP_AND_SAVE_LOG),
    ]


# ── 4. SPRINGLab F5-Hindi-24KHz ────────────────────────────────────────────
def springlab_cells() -> list[dict]:
    return [
        md("""\
# Notebook 4 — SPRINGLab F5-Hindi-24KHz

- Repo (SPRINGLab fork): https://github.com/rumourscape/F5-TTS
- Model: https://huggingface.co/SPRINGLab/F5-Hindi-24KHz
- 151 M params, F5 "small" config, **Hindi-only training**. Roman / English will be heavily OOD; record failures, don't paper over.

> The exact CLI flags and checkpoint filenames may have shifted since this notebook was written.
> **Open the model card and `/tmp/f5_hi/README.md` first** — copy whatever the canonical example currently says.
"""),
        code("""\
# === Cell 1: clone repo + install ===
!rm -rf /tmp/f5_hi
!git clone --depth 1 https://github.com/rumourscape/F5-TTS /tmp/f5_hi
%cd /tmp/f5_hi
!pip install -q -e .
!pip install -q huggingface_hub soundfile
"""),
        code("""\
# === Cell 2: download checkpoint ===
from huggingface_hub import snapshot_download
import os
model_dir = snapshot_download("SPRINGLab/F5-Hindi-24KHz", local_dir="/tmp/f5hi_ckpt")
# Inspect what was downloaded so we can wire up the right --ckpt_file path.
print(os.listdir(model_dir))
"""),
        code(COLAB_BOOTSTRAP),
        code(LOAD_EVAL),
        code("""\
# === Cell 5: prepare paths + reference clip ===
from pathlib import Path
import time, json, subprocess

MODEL_NAME = "springlab_f5"
OUT = Path(AUDIT_DIR) / "results" / MODEL_NAME
OUT.mkdir(parents=True, exist_ok=True)

REF_AUDIO = str(Path(AUDIT_DIR) / "reference_audio" / "hindi_ref.wav")
with open(Path(AUDIT_DIR) / "reference_audio" / "hindi_ref.txt", encoding="utf-8") as f:
    REF_TEXT = f.read().strip()

# Pick the right safetensors / .pt file. The canonical name on the model card is
# `model_2500000.safetensors` but verify against the directory listing above.
import glob
ckpt_candidates = glob.glob(f"{model_dir}/model_*.safetensors") or glob.glob(f"{model_dir}/model_*.pt")
assert ckpt_candidates, "No SPRINGLab checkpoint file found"
CKPT = ckpt_candidates[0]
VOCAB = f"{model_dir}/vocab.txt"
print(f"CKPT={CKPT}\\nVOCAB={VOCAB}")
"""),
        code("""\
# === Cell 6: run inference via the F5-TTS CLI ===
# This is the documented invocation in the SPRINGLab fork. If the fork changes,
# fall back to the Python API:
#     from f5_tts.api import F5TTS
#     tts = F5TTS(model="F5TTS_Base", ckpt_file=CKPT, vocab_file=VOCAB, use_ema=True, device="cuda")
#     wav, sr, _ = tts.infer(ref_file=REF_AUDIO, ref_text=REF_TEXT, gen_text=text,
#                            nfe_step=32, cfg_strength=2.0, sway_sampling_coef=-1.0,
#                            speed=1.0, remove_silence=True, seed=42, file_wave=str(out_path))
log = []
for r in rows:
    rid, cat, text = r["id"], r["category"], r["text"]
    t0 = time.time()
    out_path = OUT / f"{rid}.wav"
    try:
        cmd = [
            "f5-tts_infer-cli",
            "--model", "F5TTS_Base",
            "--ckpt_file", CKPT,
            "--vocab_file", VOCAB,
            "--ref_audio", REF_AUDIO,
            "--ref_text", REF_TEXT,
            "--gen_text", text,
            "--output_dir", str(OUT),
            "--output_file", out_path.name,
            "--nfe_step", "32", "--cfg_strength", "2.0", "--speed", "1.0",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if result.returncode != 0 or not out_path.exists():
            raise RuntimeError(result.stderr[-500:])
        log.append({"id": rid, "category": cat, "elapsed_s": time.time() - t0, "status": "ok"})
    except Exception as e:
        log.append({"id": rid, "category": cat, "status": "error", "error": str(e)})
        print(f"  [error] {rid}: {e}")
"""),
        code(WRAP_AND_SAVE_LOG),
    ]


# ── 5. Orpheus-Hindi (SachinTelecmi/Orpheus-tts-hi) ────────────────────────
def orpheus_cells() -> list[dict]:
    return [
        md("""\
# Notebook 5 — Orpheus-Hindi (SachinTelecmi/Orpheus-tts-hi)

- Model: https://huggingface.co/SachinTelecmi/Orpheus-tts-hi
- Base: Llama-3 + SNAC codec. Fine-tuned on Hindi + English **with code-mixed support**.
- 4-bit quantization (bitsandbytes nf4) is mandatory on T4. Budget ~20 s/sentence.

> **DO NOT reconstruct `generate_speech` from memory.**
> Open the model card on HF and copy the function VERBATIM.
> The SNAC token unpacking is fiddly and the special-token IDs are version-sensitive.
"""),
        code("""\
# === Cell 1: install ===
!pip install -q transformers torch torchaudio bitsandbytes accelerate
!pip install -q snac soundfile
"""),
        code(COLAB_BOOTSTRAP),
        code(LOAD_EVAL),
        code("""\
# === Cell 4: load model + SNAC decoder in 4-bit ===
from pathlib import Path
import time, json
import torch
import soundfile as sf
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from snac import SNAC

MODEL_NAME = "orpheus_hi"
OUT = Path(AUDIT_DIR) / "results" / MODEL_NAME
OUT.mkdir(parents=True, exist_ok=True)

quant_cfg = BitsAndBytesConfig(
    load_in_4bit=True, bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16, bnb_4bit_use_double_quant=True,
)
REPO = "SachinTelecmi/Orpheus-tts-hi"
model = AutoModelForCausalLM.from_pretrained(
    REPO, quantization_config=quant_cfg, device_map="auto", trust_remote_code=True,
)
tok = AutoTokenizer.from_pretrained(REPO, trust_remote_code=True)
snac_model = SNAC.from_pretrained("hubertsiuzdak/snac_24khz").eval().cuda()

# Special-token IDs from the model card (verify against current card before running):
END_OF_SPEECH_TOKEN     = 128258
START_OF_HUMAN_TOKEN    = 128259
END_OF_HUMAN_TOKEN      = 128260
START_OF_AI_TOKEN       = 128261
END_OF_AI_TOKEN         = 128262
AUDIO_CODE_BASE_OFFSET  = 128266
"""),
        code("""\
# === Cell 5: PASTE generate_speech VERBATIM from the HF model card ===
# https://huggingface.co/SachinTelecmi/Orpheus-tts-hi
#
# The function constructs the Llama prompt with the special tokens above,
# samples until END_OF_SPEECH_TOKEN, regroups the SNAC codes (3 codebooks),
# and decodes via snac_model.decode -> 24 kHz waveform.
#
# DO NOT REWRITE THIS FROM MEMORY. Copy the canonical version. Stub below
# only documents the contract — replace it before running:

def generate_speech(text: str, temperature: float = 0.4) -> "np.ndarray":
    \"\"\"Returns a numpy float32 mono waveform at 24000 Hz.\"\"\"
    raise NotImplementedError(
        "Replace this stub with the verbatim generate_speech() from the model card "
        "at https://huggingface.co/SachinTelecmi/Orpheus-tts-hi"
    )
"""),
        code("""\
# === Cell 6: run inference ===
log = []
for r in rows:
    rid, cat, text = r["id"], r["category"], r["text"]
    t0 = time.time()
    try:
        audio = generate_speech(text, temperature=0.4)
        out_path = OUT / f"{rid}.wav"
        sf.write(out_path, audio, 24000)
        log.append({
            "id": rid, "category": cat,
            "elapsed_s": time.time() - t0,
            "duration_s": float(len(audio) / 24000),
            "status": "ok",
        })
    except Exception as e:
        log.append({"id": rid, "category": cat, "status": "error", "error": str(e)})
        print(f"  [error] {rid}: {e}")
"""),
        code(WRAP_AND_SAVE_LOG),
    ]


# ── main ───────────────────────────────────────────────────────────────────
def main() -> int:
    targets = {
        "01_kokoro":       kokoro_cells(),
        "02_indicf5":      indicf5_cells(),
        "03_indic_parler": indic_parler_cells(),
        "04_springlab_f5": springlab_cells(),
        "05_orpheus_hi":   orpheus_cells(),
    }
    for name, cells in targets.items():
        path = write_notebook(name, cells)
        print(f"  wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
