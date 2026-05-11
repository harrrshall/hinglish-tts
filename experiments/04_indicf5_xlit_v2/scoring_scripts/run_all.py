"""Stage-1 signal extraction for indicf5_patched_xlit_v2 (rubric v2.1).

Reads:
  experiments/04_indicf5_xlit_v2/wavs/*.wav   (30 wavs from Kaggle v3 run)
  data/eval_sentences.tsv                      (ground-truth text)

Writes:
  experiments/04_indicf5_xlit_v2/scores/signal_vectors_aai.json
  experiments/04_indicf5_xlit_v2/scores/signal_vectors_deepgram.json
  experiments/04_indicf5_xlit_v2/scores/signal_vectors_groq.json
  experiments/04_indicf5_xlit_v2/scores/signal_vectors_v2.json  (enriched, v2.1 norm)

Run from repo root:
  cd ~/Desktop/hienglish
  source .env && ./venv-scoring/bin/python experiments/04_indicf5_xlit_v2/scoring_scripts/run_all.py
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
import re
import string

import numpy as np

REPO = Path(__file__).resolve().parents[3]
SCRIPTS = REPO / "scoring" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import lib_audio
import lib_asr
import lib_asr_deepgram
import lib_asr_groq
import lib_mos
import jiwer
from lib_normalize import to_unified_devanagari

WAVS = REPO / "experiments" / "04_indicf5_xlit_v2" / "wavs"
SCORES = REPO / "experiments" / "04_indicf5_xlit_v2" / "scores"
EVAL = REPO / "data" / "eval_sentences.tsv"
MODEL = "indicf5_patched_xlit_v2"

ASR_PARALLEL = 4
_MOS_LOCK = threading.Lock()

_PUNCT = string.punctuation + "।॥,।'\"‍‌"


def _strip_punct(text: str) -> str:
    out = "".join(" " if ch in _PUNCT else ch for ch in text)
    return re.sub(r"\s+", " ", out).strip()


def _cer(ref: str, hyp: str) -> float:
    ref = _strip_punct(ref)
    hyp = _strip_punct(hyp)
    if not ref:
        return 1.0
    return float(jiwer.cer(ref, hyp))


def _wer(ref: str, hyp: str) -> float:
    ref = _strip_punct(ref)
    hyp = _strip_punct(hyp)
    if not ref:
        return 1.0
    return float(jiwer.wer(ref, hyp))


def _token_overlap(ref_norm: str, hyp_norm: str) -> float:
    ref_toks = {t for t in _strip_punct(ref_norm).split() if len(t) > 1}
    hyp_toks = {t for t in _strip_punct(hyp_norm).split() if len(t) > 1}
    if not ref_toks:
        return 1.0
    return len(ref_toks & hyp_toks) / len(ref_toks)


def load_eval_set() -> dict[str, dict]:
    rows = {}
    with EVAL.open(encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            rid = str(r["id"]).strip()
            rows[rid] = r
    if len(rows) != 30:
        raise RuntimeError(f"eval_sentences.tsv has {len(rows)} rows, expected 30")
    return rows


def extract_one_aai(wav_path: Path, gt: dict) -> dict:
    audio, sr = lib_audio.load_wav(str(wav_path))
    dsp = {
        "duration_s":          float(len(audio) / sr) if sr > 0 else 0.0,
        "sample_rate_hz":      int(sr),
        "silence_mid_clip_s":  round(lib_audio.longest_silence_s(audio, sr), 3),
        "end_pop_db":          round(lib_audio.end_pop_db(audio, sr), 2),
        "terminal_sample_abs": round(lib_audio.terminal_sample_abs(audio), 4),
    }
    text = (gt.get("text") or "").strip()
    transcripts = lib_asr.transcribe_all(str(wav_path))
    asr = {
        "transcript_hi":        transcripts["transcript_hi"],
        "transcript_en_forced": transcripts["transcript_en_forced"],
        "transcript_roman":     transcripts["transcript_roman"],
        "detected_lang":        transcripts.get("detected_lang", ""),
        "cer_devanagari":  round(_cer(text, transcripts["transcript_hi"]), 4),
        "wer_roman":       round(_wer(text, transcripts["transcript_roman"]), 4),
        "wer_en_forced":   round(_wer(text, transcripts["transcript_en_forced"]), 4),
    }
    with _MOS_LOCK:
        mos = lib_mos.all_mos_signals(audio, sr)
    return {
        "model": MODEL, "id": wav_path.stem,
        "category": gt.get("category"), "text": text,
        "expected_pronunciation_notes": gt.get("expected_pronunciation_notes", ""),
        "tested_phenomenon": gt.get("tested_phenomenon", ""),
        **dsp, **asr, **mos,
    }


def extract_one_deepgram(wav_path: Path, gt: dict) -> dict:
    audio, sr = lib_audio.load_wav(str(wav_path))
    text = (gt.get("text") or "").strip()
    transcripts = lib_asr_deepgram.transcribe_all(str(wav_path))
    dsp = {
        "duration_s":          float(len(audio) / sr) if sr > 0 else 0.0,
        "sample_rate_hz":      int(sr),
        "silence_mid_clip_s":  round(lib_audio.longest_silence_s(audio, sr), 3),
        "end_pop_db":          round(lib_audio.end_pop_db(audio, sr), 2),
        "terminal_sample_abs": round(lib_audio.terminal_sample_abs(audio), 4),
    }
    asr = {
        "transcript_hi":        transcripts.get("transcript_hi", ""),
        "transcript_en_forced": transcripts.get("transcript_en_forced", ""),
        "transcript_roman":     transcripts.get("transcript_roman", ""),
        "detected_lang":        transcripts.get("detected_lang", ""),
        "cer_devanagari":  round(_cer(text, transcripts.get("transcript_hi", "")), 4),
        "wer_roman":       round(_wer(text, transcripts.get("transcript_roman", "")), 4),
        "wer_en_forced":   round(_wer(text, transcripts.get("transcript_en_forced", "")), 4),
    }
    with _MOS_LOCK:
        mos = lib_mos.all_mos_signals(audio, sr)
    return {
        "model": MODEL, "id": wav_path.stem,
        "category": gt.get("category"), "text": text,
        **dsp, **asr, **mos,
    }


def extract_one_groq(wav_path: Path, gt: dict) -> dict:
    audio, sr = lib_audio.load_wav(str(wav_path))
    text = (gt.get("text") or "").strip()
    transcripts = lib_asr_groq.transcribe_all(str(wav_path))
    dsp = {
        "duration_s":          float(len(audio) / sr) if sr > 0 else 0.0,
        "sample_rate_hz":      int(sr),
        "silence_mid_clip_s":  round(lib_audio.longest_silence_s(audio, sr), 3),
        "end_pop_db":          round(lib_audio.end_pop_db(audio, sr), 2),
        "terminal_sample_abs": round(lib_audio.terminal_sample_abs(audio), 4),
    }
    asr = {
        "transcript_hi":        transcripts.get("transcript_hi", ""),
        "transcript_en_forced": transcripts.get("transcript_en_forced", ""),
        "transcript_roman":     transcripts.get("transcript_roman", ""),
        "detected_lang":        transcripts.get("detected_lang", ""),
        "cer_devanagari":  round(_cer(text, transcripts.get("transcript_hi", "")), 4),
        "wer_roman":       round(_wer(text, transcripts.get("transcript_roman", "")), 4),
        "wer_en_forced":   round(_wer(text, transcripts.get("transcript_en_forced", "")), 4),
    }
    with _MOS_LOCK:
        mos = lib_mos.all_mos_signals(audio, sr)
    return {
        "model": MODEL, "id": wav_path.stem,
        "category": gt.get("category"), "text": text,
        **dsp, **asr, **mos,
    }


def enrich_v2(entry: dict, asr_backend: str) -> dict:
    text = entry.get("text", "") or ""
    th = entry.get("transcript_hi", "") or ""
    tr = entry.get("transcript_roman", "") or ""

    text_norm = to_unified_devanagari(text)
    th_norm = to_unified_devanagari(th)
    tr_norm = to_unified_devanagari(tr)

    silence_mid = float(entry.get("silence_mid_clip_s", 0.0))
    overlap = _token_overlap(text_norm, th_norm)
    skip_norm = silence_mid > 0.5

    out = dict(entry)
    out.update({
        "text_normalized": text_norm,
        "transcript_hi_normalized": th_norm,
        "transcript_roman_normalized": tr_norm,
        "cer_devanagari_norm": round(_cer(text_norm, th_norm), 4),
        "wer_roman_norm": round(_wer(text_norm, tr_norm), 4),
        "asr_backend": asr_backend,
        "silence_or_skip_norm": skip_norm,
        "_token_overlap_norm": round(overlap, 4),
    })
    return out


def run_backend(name: str, extract_fn, eval_rows: dict, wavs: list[Path]) -> list[dict]:
    print(f"\n=== {name} ASR: {len(wavs)} clips ===")
    t0 = time.time()
    jobs = [(w, eval_rows[w.stem]) for w in wavs if w.stem in eval_rows]
    out = [None] * len(jobs)
    done = 0

    with _MOS_LOCK:
        pass  # ensure lock created in main thread

    with ThreadPoolExecutor(max_workers=ASR_PARALLEL) as exe:
        futures = {exe.submit(extract_fn, w, g): (i, w)
                   for i, (w, g) in enumerate(jobs)}
        for fut in as_completed(futures):
            idx, wav = futures[fut]
            try:
                entry = fut.result()
            except Exception as e:
                print(f"  [ERR] {wav.stem}: {type(e).__name__}: {e}", flush=True)
                continue
            out[idx] = entry
            done += 1
            print(f"  [{done:3d}/{len(jobs)}] id={wav.stem:>2s}  "
                  f"CER={entry['cer_devanagari']:.3f}  "
                  f"dur={entry['duration_s']:.2f}s",
                  flush=True)

    out = [e for e in out if e is not None]
    out.sort(key=lambda r: int(r["id"]) if r["id"].isdigit() else 99)
    print(f"  Done in {(time.time()-t0)/60:.1f}m — {len(out)} entries")
    return out


def main() -> int:
    SCORES.mkdir(parents=True, exist_ok=True)
    eval_rows = load_eval_set()
    wavs = sorted(WAVS.glob("*.wav"), key=lambda p: int(p.stem) if p.stem.isdigit() else 99)
    if len(wavs) != 30:
        print(f"WARNING: found {len(wavs)} wavs, expected 30")

    # Pre-warm MOS models
    print("[main] pre-warming MOS predictors...")
    audio0, sr0 = lib_audio.load_wav(str(wavs[0]))
    _ = lib_mos.all_mos_signals(audio0, sr0)
    print("[main] pre-warm OK")

    # Run all three ASR backends
    aai_vectors  = run_backend("AAI",      extract_one_aai,      eval_rows, wavs)
    dg_vectors   = run_backend("Deepgram", extract_one_deepgram, eval_rows, wavs)
    groq_vectors = run_backend("Groq",     extract_one_groq,     eval_rows, wavs)

    # Write raw signal vectors
    (SCORES / "signal_vectors_aai.json").write_text(
        json.dumps(aai_vectors, ensure_ascii=False, indent=1))
    (SCORES / "signal_vectors_deepgram.json").write_text(
        json.dumps(dg_vectors, ensure_ascii=False, indent=1))
    (SCORES / "signal_vectors_groq.json").write_text(
        json.dumps(groq_vectors, ensure_ascii=False, indent=1))
    print(f"\nWrote raw signal vectors to {SCORES}")

    # v2 enrichment (normalized CER/WER using v2.1 lib_normalize)
    enriched = []
    for e in aai_vectors:
        enriched.append(enrich_v2(e, "aai"))
    for e in dg_vectors:
        enriched.append(enrich_v2(e, "deepgram"))
    for e in groq_vectors:
        enriched.append(enrich_v2(e, "groq"))
    enriched.sort(key=lambda r: (int(r["id"]) if r["id"].isdigit() else 99, r["asr_backend"]))

    (SCORES / "signal_vectors_v2.json").write_text(
        json.dumps(enriched, ensure_ascii=False, indent=1))
    print(f"Wrote enriched signal vectors ({len(enriched)} entries)")

    # Quick summary
    print("\n=== CER_norm summary by backend ===")
    for backend in ("aai", "deepgram", "groq"):
        rows = [e for e in enriched if e["asr_backend"] == backend]
        if rows:
            mean_cer = np.mean([r["cer_devanagari_norm"] for r in rows])
            skip = sum(1 for r in rows if r["silence_or_skip_norm"])
            print(f"  {backend:8s}: mean_cer_norm={mean_cer:.3f}  silence_or_skip={skip}/{len(rows)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
