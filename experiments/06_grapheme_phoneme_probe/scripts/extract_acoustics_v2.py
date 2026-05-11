"""Extract acoustic features v2 — speech-onset-aligned, voiced-frames only.

Adds to each clip:
  mfcc_voiced_mean    — MFCC mean over voiced frames only (F0 > 0 from pyin)
  mfcc_onset50ms_mean — MFCC over first 50ms of speech after silence removal
  mfcc_onset100ms_mean— MFCC over first 100ms of speech (better /k/ window)
  speech_onset_ms     — ms at which first voiced frame occurs

All MFCC vectors have 13 coefficients (C0–C12). Analyses should use C1–C12
(indices 1:) to exclude the energy coefficient, which dominates cosine
similarity whenever silent and non-silent clips are compared.

Run from repo root:
    source .env
    ./venv-scoring/bin/python experiments/06_grapheme_phoneme_probe/scripts/extract_acoustics_v2.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[3]
WAVS_DIR = REPO / "experiments/06_grapheme_phoneme_probe/wavs"
OUT = REPO / "experiments/06_grapheme_phoneme_probe/acoustic_analysis_v2.json"

try:
    import librosa
except ImportError:
    sys.exit("librosa not found — run from venv-scoring: ./venv-scoring/bin/python ...")

SR = 24000
HOP = 240    # 10 ms
N_FFT = 600  # 25 ms window


def speech_onset_sample(y: np.ndarray, sr: int = SR, top_db: float = 40.0) -> int:
    """Return sample index of first voiced frame, or 0 if clip is all speech."""
    intervals = librosa.effects.split(y, top_db=top_db, frame_length=512, hop_length=128)
    if len(intervals) == 0:
        return 0
    return int(intervals[0][0])


def extract(wav_path: Path) -> dict:
    y, sr = librosa.load(wav_path, sr=SR, mono=True)
    duration = len(y) / sr

    # ── F0 contour ───────────────────────────────────────────────────────────
    try:
        f0, voiced_flag, _ = librosa.pyin(y, fmin=80, fmax=400, sr=sr,
                                          frame_length=2048, hop_length=HOP)
        f0_voiced = f0[voiced_flag] if voiced_flag is not None else f0[~np.isnan(f0)]
        f0_voiced = f0_voiced[~np.isnan(f0_voiced)]
        f0_mean = float(np.mean(f0_voiced)) if len(f0_voiced) > 0 else 0.0
        f0_std  = float(np.std(f0_voiced))  if len(f0_voiced) > 0 else 0.0
        voiced_frame_count = int(np.sum(voiced_flag)) if voiced_flag is not None else 0
    except Exception:
        f0, voiced_flag, f0_mean, f0_std, voiced_frame_count = None, None, 0.0, 0.0, 0

    # ── Full-clip MFCC (baseline, same as v1) ────────────────────────────────
    mfcc_full = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=HOP, n_fft=N_FFT)
    mfcc_full_mean = mfcc_full.mean(axis=1).tolist()

    # ── Speech onset detection ────────────────────────────────────────────────
    onset_samp = speech_onset_sample(y)
    onset_ms   = round(onset_samp / sr * 1000, 1)
    y_speech   = y[onset_samp:]  # trim silence prefix

    # ── MFCC over voiced frames only (using pyin voiced_flag) ────────────────
    if voiced_flag is not None and np.any(voiced_flag):
        # pyin frames align with hop=HOP; index voiced_flag into mfcc_full frames
        n_frames = mfcc_full.shape[1]
        vf_aligned = voiced_flag[:n_frames]
        voiced_mfcc_frames = mfcc_full[:, vf_aligned]
        mfcc_voiced_mean = voiced_mfcc_frames.mean(axis=1).tolist() if voiced_mfcc_frames.shape[1] > 0 else mfcc_full_mean
    else:
        mfcc_voiced_mean = mfcc_full_mean  # fallback if pyin found nothing

    # ── MFCC over first 50ms of speech (after silence removal) ───────────────
    n50 = int(0.050 * sr)
    if len(y_speech) >= n50:
        seg = y_speech[:n50]
        mfcc_onset50 = librosa.feature.mfcc(y=seg, sr=sr, n_mfcc=13,
                                             hop_length=HOP, n_fft=min(N_FFT, n50))
        mfcc_onset50ms_mean = mfcc_onset50.mean(axis=1).tolist()
    else:
        mfcc_onset50ms_mean = None  # clip too short after onset strip

    # ── MFCC over first 100ms of speech ──────────────────────────────────────
    n100 = int(0.100 * sr)
    if len(y_speech) >= n100:
        seg = y_speech[:n100]
        mfcc_onset100 = librosa.feature.mfcc(y=seg, sr=sr, n_mfcc=13,
                                              hop_length=HOP, n_fft=N_FFT)
        mfcc_onset100ms_mean = mfcc_onset100.mean(axis=1).tolist()
    elif len(y_speech) >= n50:
        mfcc_onset100ms_mean = mfcc_onset50ms_mean
    else:
        mfcc_onset100ms_mean = None

    # ── Legacy windows from extract_acoustics.py (kept for comparability) ────
    n50_abs = int(0.050 * sr)
    n200_abs = int(0.200 * sr)
    if len(y) >= n50_abs:
        mfcc_50ms_abs = librosa.feature.mfcc(y=y[:n50_abs], sr=sr, n_mfcc=13,
                                              hop_length=HOP, n_fft=min(N_FFT, n50_abs))
        mfcc_50ms_mean = mfcc_50ms_abs.mean(axis=1).tolist()
    else:
        mfcc_50ms_mean = None

    if len(y) >= n200_abs:
        mfcc_200ms_abs = librosa.feature.mfcc(y=y[:n200_abs], sr=sr, n_mfcc=13,
                                               hop_length=HOP, n_fft=N_FFT)
        mfcc_200ms_mean = mfcc_200ms_abs.mean(axis=1).tolist()
    else:
        mfcc_200ms_mean = mfcc_full_mean

    return {
        "duration_s":           round(duration, 4),
        "speech_onset_ms":      onset_ms,
        "voiced_frame_count":   voiced_frame_count,
        "f0_mean":              round(f0_mean, 2),
        "f0_std":               round(f0_std, 2),
        "mfcc_voiced_mean":     mfcc_voiced_mean,
        "mfcc_onset50ms_mean":  mfcc_onset50ms_mean,
        "mfcc_onset100ms_mean": mfcc_onset100ms_mean,
        "mfcc_50ms_mean":       mfcc_50ms_mean,
        "mfcc_200ms_mean":      mfcc_200ms_mean,
        "mfcc_full_mean":       mfcc_full_mean,
    }


def main() -> None:
    wavs = sorted(WAVS_DIR.glob("*.wav"))
    if not wavs:
        sys.exit(f"No wavs found in {WAVS_DIR}")

    results = {}
    for p in wavs:
        try:
            r = extract(p)
            results[p.stem] = r
            print(f"  {p.stem:22s}: {r['duration_s']:.3f}s  "
                  f"onset={r['speech_onset_ms']:5.1f}ms  "
                  f"voiced_frames={r['voiced_frame_count']:3d}  "
                  f"f0={r['f0_mean']:.1f} Hz")
        except Exception as e:
            print(f"  [error] {p.stem}: {e}")
            results[p.stem] = {"error": str(e)}

    OUT.write_text(json.dumps(results, indent=2))
    ok = sum(1 for v in results.values() if "error" not in v)
    print(f"\nWrote {ok}/{len(results)} entries → {OUT}")


if __name__ == "__main__":
    main()
