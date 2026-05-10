#!/usr/bin/env python3
"""Debug-runner for notebook 1 (Kokoro) on CPU.

Mirrors the cells in `audit/notebooks/01_kokoro.ipynb` but takes a `--limit`
so we can smoke-test without burning ~30 min of CPU time on the full 30
sentences. Useful for the laptop-only debug pass before the executing agent
runs the real notebook on Colab T4.

Usage:
    AUDIT_DIR=/home/cybernovas/Desktop/hienglish/audit \
    ~/colab-runtime/bin/python audit/scripts/debug_kokoro_cpu.py --limit 4
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import time
import traceback
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit-dir", default=os.environ.get("AUDIT_DIR"))
    ap.add_argument("--limit", type=int, default=4,
                    help="run on only the first N sentences (CPU is slow)")
    ap.add_argument("--out-suffix", default="_cpudebug",
                    help="suffix appended to results dir to avoid clobbering Colab output")
    args = ap.parse_args()

    AUDIT = Path(args.audit_dir or Path(__file__).resolve().parents[1])
    assert AUDIT.is_dir(), f"AUDIT_DIR={AUDIT} missing"
    print(f"AUDIT_DIR = {AUDIT}")

    # Load eval set
    rows = list(csv.DictReader((AUDIT / "eval_sentences.tsv").open(encoding="utf-8"),
                               delimiter="\t"))
    assert len(rows) == 30, f"expected 30 sentences, got {len(rows)}"
    print(f"Loaded {len(rows)} sentences. Running on first {args.limit}.")
    rows = rows[: args.limit]

    # Imports — surfacing install issues here so the user sees them immediately
    try:
        import numpy as np
        import soundfile as sf
        from kokoro import KPipeline
    except Exception as e:
        print(f"\n[import error] {type(e).__name__}: {e}")
        traceback.print_exc()
        return 2

    MODEL_NAME = "kokoro" + args.out_suffix
    OUT = AUDIT / "results" / MODEL_NAME
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"Output dir: {OUT}")

    # Build two pipelines (Hindi + American English) — same as notebook
    print("\nBuilding Hindi pipeline (lang_code='h')...")
    pipe_hi = KPipeline(lang_code="h")
    print("Building English pipeline (lang_code='a')...")
    pipe_en = KPipeline(lang_code="a")
    VOICE_HI, VOICE_EN = "hf_alpha", "af_heart"

    log = []
    for r in rows:
        rid, cat, text = r["id"], r["category"], r["text"]
        t0 = time.time()
        try:
            if cat == "english_with_NE":
                pipe, voice = pipe_en, VOICE_EN
            else:
                pipe, voice = pipe_hi, VOICE_HI

            chunks, phonemes = [], []
            for gs, ps, audio in pipe(text, voice=voice, speed=1.0):
                chunks.append(audio); phonemes.append(ps)
            full = np.concatenate(chunks) if chunks else np.zeros(1, dtype=np.float32)
            out_path = OUT / f"{rid}.wav"
            sf.write(out_path, full, 24000)
            entry = {
                "id": rid, "category": cat, "voice": voice,
                "phonemes": " ".join(phonemes),
                "duration_s": float(len(full) / 24000),
                "elapsed_s": time.time() - t0,
                "status": "ok",
            }
            log.append(entry)
            print(f"  [ok]  {rid} ({cat:<16}) wav={out_path.stat().st_size}B "
                  f"dur={entry['duration_s']:.2f}s in {entry['elapsed_s']:.1f}s "
                  f"phonemes={entry['phonemes']!r}")
        except Exception as e:
            log.append({"id": rid, "category": cat, "status": "error", "error": f"{type(e).__name__}: {e}"})
            print(f"  [ERR] {rid} ({cat}): {type(e).__name__}: {e}")
            traceback.print_exc()

    (OUT / "log.json").write_text(json.dumps(log, ensure_ascii=False, indent=2))
    n_ok = sum(1 for x in log if x["status"] == "ok")
    print(f"\nKokoro CPU smoke: {n_ok}/{len(log)} succeeded — log at {OUT/'log.json'}")
    return 0 if n_ok == len(log) else 1


if __name__ == "__main__":
    raise SystemExit(main())
