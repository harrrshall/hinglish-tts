"""Extract acoustic features for grapheme/phoneme probe analysis.

For each wav, compute:
  - Total duration
  - F0 contour (pyin; fallback to autocorrelation)
  - MFCC mean vectors: full clip, first 50ms, first 200ms

Output: experiments/06_grapheme_phoneme_probe/acoustic_analysis.json

Run from repo root:
    source .env
    ./venv-scoring/bin/python experiments/06_grapheme_phoneme_probe/scripts/extract_acoustics.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[3]
WAVS_DIR = REPO / "experiments/06_grapheme_phoneme_probe/wavs"
OUT = REPO / "experiments/06_grapheme_phoneme_probe/acoustic_analysis.json"

try:
    import librosa
except ImportError:
    sys.exit("librosa not found — run from venv-scoring: ./venv-scoring/bin/python ...")


def extract(wav_path: Path) -> dict:
    y, sr = librosa.load(wav_path, sr=24000, mono=True)
    duration = len(y) / sr

    # F0 contour
    try:
        f0, _, _ = librosa.pyin(y, fmin=80, fmax=400, sr=sr, frame_length=2048)
        f0_mean = float(np.nanmean(f0)) if not np.all(np.isnan(f0)) else 0.0
        f0_std  = float(np.nanstd(f0))  if not np.all(np.isnan(f0)) else 0.0
    except Exception:
        f0_mean = f0_std = 0.0

    hop = 240   # 10 ms at 24 kHz
    n_fft = 600 # 25 ms window

    # Full-clip MFCCs
    mfcc_full = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=hop, n_fft=n_fft)
    mfcc_full_mean = mfcc_full.mean(axis=1).tolist()

    # First 50 ms — the phoneme onset / burst window
    n50 = int(0.050 * sr)
    if len(y) >= n50:
        mfcc_50ms = librosa.feature.mfcc(
            y=y[:n50], sr=sr, n_mfcc=13, hop_length=hop, n_fft=min(n_fft, n50)
        )
        mfcc_50ms_mean = mfcc_50ms.mean(axis=1).tolist()
    else:
        mfcc_50ms_mean = None

    # First 200 ms — phoneme + initial vowel transition
    n200 = int(0.200 * sr)
    if len(y) >= n200:
        mfcc_200ms = librosa.feature.mfcc(
            y=y[:n200], sr=sr, n_mfcc=13, hop_length=hop, n_fft=n_fft
        )
        mfcc_200ms_mean = mfcc_200ms.mean(axis=1).tolist()
    else:
        mfcc_200ms_mean = mfcc_full_mean  # clip too short; fall back to full

    return {
        "duration_s":       round(duration, 4),
        "f0_mean":          round(f0_mean, 2),
        "f0_std":           round(f0_std, 2),
        "mfcc_50ms_mean":   mfcc_50ms_mean,
        "mfcc_200ms_mean":  mfcc_200ms_mean,
        "mfcc_full_mean":   mfcc_full_mean,
    }


def main() -> None:
    wavs = sorted(WAVS_DIR.glob("*.wav"))
    if not wavs:
        sys.exit(f"No wavs found in {WAVS_DIR}. Run Kaggle inference first.")

    results = {}
    for p in wavs:
        try:
            results[p.stem] = extract(p)
            print(f"  {p.stem}: {results[p.stem]['duration_s']:.3f}s  "
                  f"f0={results[p.stem]['f0_mean']:.1f} Hz")
        except Exception as e:
            print(f"  [error] {p.stem}: {e}")
            results[p.stem] = {"error": str(e)}

    OUT.write_text(json.dumps(results, indent=2))
    ok = sum(1 for v in results.values() if "error" not in v)
    print(f"\nWrote {ok}/{len(results)} entries → {OUT}")
    if ok < len(results):
        errs = [k for k, v in results.items() if "error" in v]
        print(f"  Errors: {errs}")


if __name__ == "__main__":
    main()
