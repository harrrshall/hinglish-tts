#!/usr/bin/env python3
"""Run Indic Parler-TTS inference on the eval set (CPU, local machine).

Mirrors 03_indic_parler.ipynb cells. Saves to audit/results/indic_parler/.

Usage:
    AUDIT_DIR=/home/cybernovas/Desktop/hienglish/audit \
    /tmp/parler-venv/bin/python audit/scripts/run_indic_parler_cpu.py
"""
from __future__ import annotations
import csv
import json
import os
import time
import traceback
from pathlib import Path

AUDIT = Path(os.environ.get("AUDIT_DIR", Path(__file__).resolve().parents[1]))
assert AUDIT.is_dir(), f"AUDIT_DIR={AUDIT} missing"
print(f"AUDIT_DIR = {AUDIT}")

rows = list(csv.DictReader((AUDIT / "eval_sentences.tsv").open(encoding="utf-8"), delimiter="\t"))
assert len(rows) == 30, f"expected 30, got {len(rows)}"
print(f"Loaded {len(rows)} sentences.")

import torch
import soundfile as sf
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer

MODEL_NAME = "indic_parler"
OUT = AUDIT / "results" / MODEL_NAME
OUT.mkdir(parents=True, exist_ok=True)

device = "cuda" if torch.cuda.is_available() else "cpu"
dtype  = torch.float32  # always float32 on CPU

REPO = "ai4bharat/indic-parler-tts"
print(f"Loading model {REPO} on {device} / {dtype} ...")
t_load = time.time()
model     = ParlerTTSForConditionalGeneration.from_pretrained(REPO, torch_dtype=dtype).to(device)
tok       = AutoTokenizer.from_pretrained(REPO)
desc_tok  = AutoTokenizer.from_pretrained(model.config.text_encoder._name_or_path)
SR = int(model.config.sampling_rate)
print(f"Model loaded in {time.time()-t_load:.1f}s. sampling_rate={SR}")

DESCRIPTION = (
    "A female speaker delivers a clear, moderately-paced Hindi speech "
    "with neutral expression. The recording is high quality with no background noise."
)
desc_input_ids = desc_tok(DESCRIPTION, return_tensors="pt").input_ids.to(device)

log = []
for i, r in enumerate(rows):
    rid, cat, text = r["id"], r["category"], r["text"]
    t0 = time.time()
    try:
        prompt_input_ids = tok(text, return_tensors="pt").input_ids.to(device)
        with torch.no_grad():
            gen = model.generate(input_ids=desc_input_ids, prompt_input_ids=prompt_input_ids)
        audio = gen.cpu().to(torch.float32).numpy().squeeze()
        out_path = OUT / f"{rid}.wav"
        sf.write(out_path, audio, SR)
        entry = {
            "id": rid, "category": cat, "sr": SR,
            "duration_s": float(len(audio) / SR),
            "elapsed_s": time.time() - t0,
            "status": "ok",
        }
        log.append(entry)
        print(f"  [ok]  {rid} ({cat:<16}) dur={entry['duration_s']:.2f}s in {entry['elapsed_s']:.1f}s  ({i+1}/30)")
    except Exception as e:
        log.append({"id": rid, "category": cat, "status": "error", "error": str(e)})
        print(f"  [ERR] {rid} ({cat}): {e}")
        traceback.print_exc()

(OUT / "log.json").write_text(json.dumps(log, ensure_ascii=False, indent=2))
n_ok = sum(1 for x in log if x["status"] == "ok")
print(f"\nIndic Parler-TTS CPU: {n_ok}/30 succeeded — log at {OUT/'log.json'}")
