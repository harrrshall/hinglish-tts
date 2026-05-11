"""Phonetic probe — Stage 1 signal extraction.

Reads:
  experiments/05_phonetic_probe/wavs/*.wav  (18 wavs from Kaggle phonetic probe run)
  experiments/05_phonetic_probe/test_sentences.tsv

Writes:
  experiments/05_phonetic_probe/scores/signal_vectors_aai.json
  experiments/05_phonetic_probe/scores/signal_vectors_deepgram.json
  experiments/05_phonetic_probe/scores/signal_vectors_groq.json
  experiments/05_phonetic_probe/scores/auto_scores.csv

Does NOT compute Likert intelligibility scores — rubric v2.1 is designed for
reference-text comparison, and these variants have intentionally different
texts. This script extracts:
  - Raw ASR transcripts from all 3 backends (primary data)
  - Duration and acoustic features (F0, spectral centroid)
  - Cross-ASR agreement per variant
  - Cross-variant transcript consistency per sentence

Run:
  cd ~/Desktop/hienglish
  source .env && ./venv-scoring/bin/python experiments/05_phonetic_probe/scoring_scripts/run_scoring.py
"""
from __future__ import annotations

import csv
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[3]
SCRIPTS = REPO / "scoring" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import lib_audio
import lib_asr
import lib_asr_deepgram
import lib_asr_groq

PROBE = REPO / "experiments" / "05_phonetic_probe"
WAVS  = PROBE / "wavs"
TSV   = PROBE / "test_sentences.tsv"
OUT   = PROBE / "scores"

ASR_PARALLEL = 4


def load_probe_set() -> dict[str, dict]:
    rows = {}
    with TSV.open(encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            output_id = f"{r['sentence_id']}{r['variant']}"
            rows[output_id] = r
    if len(rows) != 18:
        raise RuntimeError(f"test_sentences.tsv has {len(rows)} rows, expected 18")
    return rows


def extract_f0_mean(audio: np.ndarray, sr: int) -> float:
    """Mean voiced F0 in Hz. Returns 0.0 if librosa unavailable or no voiced frames."""
    try:
        import librosa
        f0 = librosa.yin(audio.astype(np.float32), fmin=60, fmax=400, sr=sr)
        voiced = f0[f0 > 0]
        return float(np.mean(voiced)) if len(voiced) > 0 else 0.0
    except Exception:
        return 0.0


def extract_spectral_centroid_mean(audio: np.ndarray, sr: int) -> float:
    """Mean spectral centroid in Hz."""
    try:
        import librosa
        sc = librosa.feature.spectral_centroid(y=audio.astype(np.float32), sr=sr)
        return float(np.mean(sc))
    except Exception:
        return 0.0


def extract_one(wav_path: Path, row: dict, backend: str) -> dict:
    audio, sr = lib_audio.load_wav(str(wav_path))
    dsp = {
        "duration_s":          round(float(len(audio) / sr), 3),
        "sample_rate_hz":      int(sr),
        "silence_mid_clip_s":  round(lib_audio.longest_silence_s(audio, sr), 3),
        "end_pop_db":          round(lib_audio.end_pop_db(audio, sr), 2),
        "terminal_sample_abs": round(lib_audio.terminal_sample_abs(audio), 4),
        "mean_f0_hz":          round(extract_f0_mean(audio, sr), 1),
        "mean_spectral_centroid_hz": round(extract_spectral_centroid_mean(audio, sr), 1),
    }

    if backend == "aai":
        tr = lib_asr.transcribe_all(str(wav_path))
    elif backend == "deepgram":
        tr = lib_asr_deepgram.transcribe_all(str(wav_path))
    elif backend == "groq":
        tr = lib_asr_groq.transcribe_all(str(wav_path))
    else:
        raise ValueError(f"Unknown backend: {backend}")

    output_id = f"{row['sentence_id']}{row['variant']}"
    return {
        "output_id":     output_id,
        "sentence_id":   row["sentence_id"],
        "variant":       row["variant"],
        "category":      row["category"],
        "text":          row["text"],
        "phonetic_distinction_tested": row["phonetic_distinction_tested"],
        "asr_backend":   backend,
        **dsp,
        "transcript_hi":        tr.get("transcript_hi", ""),
        "transcript_roman":     tr.get("transcript_roman", ""),
        "transcript_en_forced": tr.get("transcript_en_forced", ""),
        "detected_lang":        tr.get("detected_lang", ""),
    }


def run_backend(name: str, extract_fn, probe_rows: dict,
                wavs: list[Path]) -> list[dict]:
    print(f"\n=== {name} ASR: {len(wavs)} clips ===")
    t0 = time.time()
    jobs = [(w, probe_rows[w.stem]) for w in wavs if w.stem in probe_rows]
    if len(jobs) < len(wavs):
        missing = [w.stem for w in wavs if w.stem not in probe_rows]
        print(f"  WARNING: no TSV row for: {missing}")

    results: list[dict | None] = [None] * len(jobs)
    done = 0

    with ThreadPoolExecutor(max_workers=ASR_PARALLEL) as exe:
        futures = {exe.submit(extract_fn, w, row, name): (i, w)
                   for i, (w, row) in enumerate(jobs)}
        for fut in as_completed(futures):
            idx, wav = futures[fut]
            try:
                entry = fut.result()
            except Exception as e:
                print(f"  [ERR] {wav.stem}: {type(e).__name__}: {e}", flush=True)
                continue
            results[idx] = entry
            done += 1
            print(f"  [{done:2d}/{len(jobs)}] {wav.stem:4s}  "
                  f"dur={entry['duration_s']:.2f}s  "
                  f"f0={entry['mean_f0_hz']:.0f}Hz  "
                  f"transcript={entry['transcript_hi'][:30]!r}",
                  flush=True)

    out = [e for e in results if e is not None]
    out.sort(key=lambda r: (r["sentence_id"], r["variant"]))
    print(f"  Done in {(time.time()-t0)/60:.1f}m — {len(out)} entries")
    return out


def build_summary_csv(
    aai_vec: list[dict],
    dg_vec:  list[dict],
    groq_vec: list[dict],
    probe_rows: dict,
) -> list[dict]:
    """One row per (output_id). Transcripts from each backend + agreement flags."""
    by_id: dict[str, dict] = {}
    for entry in aai_vec:
        by_id.setdefault(entry["output_id"], {})["aai"] = entry
    for entry in dg_vec:
        by_id.setdefault(entry["output_id"], {})["deepgram"] = entry
    for entry in groq_vec:
        by_id.setdefault(entry["output_id"], {})["groq"] = entry

    rows = []
    for output_id in sorted(by_id.keys()):
        backends = by_id[output_id]
        aai  = backends.get("aai", {})
        dg   = backends.get("deepgram", {})
        groq = backends.get("groq", {})

        t_aai  = aai.get("transcript_hi", "")
        t_dg   = dg.get("transcript_hi", "")
        t_groq = groq.get("transcript_hi", "")

        all_same_asr = (t_aai == t_dg == t_groq) if (t_aai and t_dg and t_groq) else False

        rows.append({
            "output_id":         output_id,
            "sentence_id":       aai.get("sentence_id", output_id[:-1]),
            "variant":           aai.get("variant", output_id[-1]),
            "category":          aai.get("category", ""),
            "text":              aai.get("text", ""),
            "phonetic_distinction_tested": aai.get("phonetic_distinction_tested", ""),
            "duration_s":        aai.get("duration_s", ""),
            "mean_f0_hz":        aai.get("mean_f0_hz", ""),
            "mean_spectral_centroid_hz": aai.get("mean_spectral_centroid_hz", ""),
            "transcript_aai":    t_aai,
            "transcript_dg":     t_dg,
            "transcript_groq":   t_groq,
            "transcripts_identical_across_asrs": all_same_asr,
            # filled in second pass:
            "transcripts_identical_across_variants": "",
        })

    # Per-sentence: do all three variants get the same transcript from AAI?
    # Flag per variant row (all three in a sentence group get the same boolean).
    by_sentence: dict[str, list[dict]] = {}
    for r in rows:
        by_sentence.setdefault(r["sentence_id"], []).append(r)

    for sid, sent_rows in by_sentence.items():
        # For each ASR backend, check if all variants produce the same transcript.
        for backend, field in [("aai", "transcript_aai"),
                               ("deepgram", "transcript_dg"),
                               ("groq", "transcript_groq")]:
            transcripts = [r[field] for r in sent_rows if r[field]]
            if not transcripts:
                continue
            all_same = len(set(transcripts)) == 1
            col = f"transcripts_identical_across_variants_{backend}"
            for r in sent_rows:
                r[col] = all_same

        # Summary: True only if identical across variants on ALL three backends.
        all_backends_same = all(
            r.get(f"transcripts_identical_across_variants_{b}", False)
            for b in ("aai", "deepgram", "groq")
            for r in sent_rows
            if r.get(f"transcripts_identical_across_variants_{b}") != ""
        )
        for r in sent_rows:
            r["transcripts_identical_across_variants"] = all_backends_same

    return rows


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    probe_rows = load_probe_set()
    wavs = sorted(WAVS.glob("*.wav"), key=lambda p: (p.stem[:-1], p.stem[-1]))
    if len(wavs) != 18:
        print(f"WARNING: found {len(wavs)} wavs in {WAVS}, expected 18")
        if len(wavs) == 0:
            print("  Run the Kaggle kernel and download wavs first.")
            return 1

    def aai_fn(w, row, b):   return extract_one(w, row, "aai")
    def dg_fn(w, row, b):    return extract_one(w, row, "deepgram")
    def groq_fn(w, row, b):  return extract_one(w, row, "groq")

    aai_vec  = run_backend("AAI",      aai_fn,  probe_rows, wavs)
    dg_vec   = run_backend("Deepgram", dg_fn,   probe_rows, wavs)
    groq_vec = run_backend("Groq",     groq_fn, probe_rows, wavs)

    (OUT / "signal_vectors_aai.json").write_text(
        json.dumps(aai_vec, ensure_ascii=False, indent=1))
    (OUT / "signal_vectors_deepgram.json").write_text(
        json.dumps(dg_vec, ensure_ascii=False, indent=1))
    (OUT / "signal_vectors_groq.json").write_text(
        json.dumps(groq_vec, ensure_ascii=False, indent=1))
    print(f"\nWrote raw signal vectors to {OUT}")

    rows = build_summary_csv(aai_vec, dg_vec, groq_vec, probe_rows)

    fieldnames = [
        "output_id", "sentence_id", "variant", "category", "text",
        "phonetic_distinction_tested",
        "duration_s", "mean_f0_hz", "mean_spectral_centroid_hz",
        "transcript_aai", "transcript_dg", "transcript_groq",
        "transcripts_identical_across_asrs",
        "transcripts_identical_across_variants",
        "transcripts_identical_across_variants_aai",
        "transcripts_identical_across_variants_deepgram",
        "transcripts_identical_across_variants_groq",
    ]

    csv_path = OUT / "auto_scores.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {csv_path} — {len(rows)} rows")

    # Summary diagnostic
    print("\n=== Key diagnostic: cross-variant transcript consistency ===")
    print("(TRUE = all 3 variants in the sentence produced the SAME transcript → model is insensitive to the distinction)")
    print()
    by_sentence: dict[str, list] = {}
    for r in rows:
        by_sentence.setdefault(r["sentence_id"], []).append(r)

    for sid in sorted(by_sentence.keys()):
        sent_rows = by_sentence[sid]
        cat = sent_rows[0]["phonetic_distinction_tested"].split(":")[0].strip()
        identical = sent_rows[0]["transcripts_identical_across_variants"]
        print(f"  Sentence {sid} [{cat}]: identical_across_variants = {identical}")
        for r in sent_rows:
            print(f"    {r['output_id']}  dur={r['duration_s']:.2f}s  "
                  f"f0={r['mean_f0_hz']:.0f}Hz  "
                  f"aai={r['transcript_aai'][:35]!r}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
