"""Stage 1 (Deepgram variant): extract per-clip signal vectors for all 120 wavs.

Mirror of extract_signals.py but with the Deepgram Nova-3 ASR backend. Writes
to a separate output file so the AssemblyAI signals stay intact for comparison.

Reads:
  audit/results/{kokoro,indic_parler,indicf5,springlab_f5}/*.wav
  audit/eval_sentences.tsv (ground truth)

Writes:
  audit/signal_vectors_deepgram.json — list of 120 dicts, one per (model, sentence) pair.

Run:
  export DEEPGRAM_API_KEY='...'
  python audit/scripts/extract_signals_deepgram.py
"""
from __future__ import annotations

import csv
import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import soundfile as sf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import lib_audio
import lib_asr_deepgram as lib_asr  # ← Deepgram backend
import lib_mos


REPO = Path(__file__).resolve().parents[2]
AUDIT = REPO / "audit"
RESULTS = AUDIT / "results"
EVAL = AUDIT / "eval_sentences.tsv"
OUT = AUDIT / "signal_vectors_deepgram.json"

MODELS = ["kokoro", "indic_parler", "indicf5", "springlab_f5"]

# Deepgram pre-recorded concurrency: 50. We use 5 — same as AssemblyAI for fair comparison.
ASR_PARALLEL = 5
_MOS_LOCK = threading.Lock()


def load_eval_set() -> dict[str, dict]:
    rows = {}
    with EVAL.open(encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            rid = str(r["id"]).strip()
            if rid.isdigit() and len(rid) == 1:
                rid = "0" + rid
            rows[rid] = r
    if len(rows) != 30:
        raise RuntimeError(f"eval_sentences.tsv has {len(rows)} rows, expected 30")
    return rows


def extract_one(model: str, wav_path: Path, gt: dict) -> dict:
    audio, sr = lib_audio.load_wav(str(wav_path))

    dsp = {
        "duration_s": float(len(audio) / sr) if sr > 0 else 0.0,
        "sample_rate_hz": int(sr),
        "silence_mid_clip_s": round(lib_audio.longest_silence_s(audio, sr), 3),
        "end_pop_db": round(lib_audio.end_pop_db(audio, sr), 2),
        "terminal_sample_abs": round(lib_audio.terminal_sample_abs(audio), 4),
    }

    transcripts = lib_asr.transcribe_all(str(wav_path))
    text = (gt.get("text") or "").strip()
    asr = {
        "transcript_hi":         transcripts["transcript_hi"],
        "transcript_en_forced":  transcripts["transcript_en_forced"],
        "transcript_roman":      transcripts["transcript_roman"],
        "detected_lang":         transcripts.get("detected_lang", ""),
        "cer_devanagari":  round(lib_asr.cer(text, transcripts["transcript_hi"]), 4),
        "wer_roman":       round(lib_asr.wer(text, transcripts["transcript_roman"]), 4),
        "wer_en_forced":   round(lib_asr.wer(text, transcripts["transcript_en_forced"]), 4),
    }

    with _MOS_LOCK:
        mos = lib_mos.all_mos_signals(audio, sr)

    return {
        "model": model,
        "id": wav_path.stem,
        "category": gt.get("category"),
        "text": text,
        "expected_pronunciation_notes": gt.get("expected_pronunciation_notes", ""),
        "tested_phenomenon": gt.get("tested_phenomenon", ""),
        **dsp,
        **asr,
        **mos,
        "_asr_backend": "deepgram-nova-3",
    }


def main() -> int:
    eval_rows = load_eval_set()
    t0 = time.time()

    jobs = []
    for model in MODELS:
        d = RESULTS / model
        wavs = sorted(d.glob("*.wav"))
        if len(wavs) != 30:
            print(f"[skip] {model}: {len(wavs)} wavs (expected 30)")
            continue
        for wav in wavs:
            gt = eval_rows.get(wav.stem)
            if gt is None:
                print(f"[skip] {model}/{wav.stem}: no eval-set entry")
                continue
            jobs.append((model, wav, gt))

    total = len(jobs)
    print(f"=== Extracting signals for {total} clips with {ASR_PARALLEL} parallel ASR workers (Deepgram Nova-3) ===\n")
    out = [None] * total

    print("[main] pre-warming MOS predictors...", flush=True)
    audio, sr = lib_audio.load_wav(str(jobs[0][1]))
    _ = lib_mos.all_mos_signals(audio, sr)
    print("[main] pre-warm OK\n", flush=True)

    done = 0
    with ThreadPoolExecutor(max_workers=ASR_PARALLEL) as exe:
        futures = {exe.submit(extract_one, m, w, g): (i, m, w)
                   for i, (m, w, g) in enumerate(jobs)}
        for fut in as_completed(futures):
            idx, model, wav = futures[fut]
            try:
                entry = fut.result()
            except Exception as e:
                print(f"  [ERR] {model}/{wav.stem}: {type(e).__name__}: {e}", flush=True)
                continue
            out[idx] = entry
            done += 1
            elapsed_total = time.time() - t0
            eta = elapsed_total / done * (total - done) if done > 0 else 0
            print(f"  [{done:3d}/{total}] {model:14s}/{wav.stem}  "
                  f"({entry['category']:18s})  "
                  f"CER={entry['cer_devanagari']:.2f} "
                  f"WER_rom={entry['wer_roman']:.2f} "
                  f"WER_en={entry['wer_en_forced']:.2f} "
                  f"UTMOS={entry['utmos']:.2f}  ETA {eta/60:.1f}m",
                  flush=True)

    out = [e for e in out if e is not None]
    model_order = {m: i for i, m in enumerate(MODELS)}
    out.sort(key=lambda r: (r["id"], model_order.get(r["model"], 99)))

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(f"\nWrote {OUT} — {len(out)} entries in {(time.time() - t0)/60:.1f} min")

    print("\n=== Per-model summary (Deepgram Nova-3) ===")
    for model in MODELS:
        rows = [r for r in out if r["model"] == model]
        if not rows:
            continue
        mean_cer = np.mean([r["cer_devanagari"] for r in rows])
        mean_wer = np.mean([r["wer_roman"] for r in rows])
        mean_utmos = np.mean([r["utmos"] for r in rows])
        print(f"  {model:14s}  mean CER={mean_cer:.3f}  WER_rom={mean_wer:.3f}  "
              f"UTMOS={mean_utmos:.2f}  ({len(rows)} clips)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
