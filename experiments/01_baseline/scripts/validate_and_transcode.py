"""Validate human mp3 recordings and transcode to 24 kHz mono PCM wav.

Reads:
  uploads/human_NN.mp3 (8 files, 44.1 kHz stereo @ 224 kbps)

Writes:
  audit/human_groundtruth/wavs/human_NN.wav (24 kHz mono PCM_16)
  audit/human_groundtruth/validation_report.csv

For each clip: native_sr, channels, duration, peak_amp, clipped flag,
silence-share (top_db=30), SNR-status flag, transcode result.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf

REPO = Path(__file__).resolve().parents[3]
UPLOADS = REPO / "uploads"
OUT_DIR = REPO / "audit" / "human_groundtruth" / "wavs"
REPORT = REPO / "audit" / "human_groundtruth" / "validation_report.csv"

TARGET_SR = 24_000  # match TTS model output SR

DUR_MIN, DUR_MAX = 1.5, 10.0
CLIP_THRESH = 0.99
TOP_DB = 30
SILENCE_FRACTION_FAIL = 0.30


def validate_one(mp3_path: Path) -> dict:
    audio_native, native_sr = librosa.load(str(mp3_path), sr=None, mono=False)

    if audio_native.ndim == 2:
        channels = audio_native.shape[0]
        audio_mono = librosa.to_mono(audio_native)
    else:
        channels = 1
        audio_mono = audio_native

    duration = len(audio_mono) / native_sr
    peak = float(np.max(np.abs(audio_mono)))
    clipped = peak >= CLIP_THRESH

    intervals = librosa.effects.split(audio_mono, top_db=TOP_DB)
    speech_samples = sum(end - start for start, end in intervals)
    silence_share = 1.0 - (speech_samples / len(audio_mono))
    snr_flag = "OK" if silence_share <= SILENCE_FRACTION_FAIL else "NOISY/SILENT"

    dur_flag = "OK" if DUR_MIN <= duration <= DUR_MAX else "OUT_OF_RANGE"

    audio_24k = librosa.resample(audio_mono, orig_sr=native_sr, target_sr=TARGET_SR)
    out_path = OUT_DIR / (mp3_path.stem + ".wav")
    sf.write(str(out_path), audio_24k, TARGET_SR, subtype="PCM_16")

    return {
        "filename": mp3_path.name,
        "native_sr": native_sr,
        "channels": channels,
        "duration_s": round(duration, 3),
        "peak_amp": round(peak, 4),
        "clipped": clipped,
        "silence_share": round(silence_share, 3),
        "snr_flag": snr_flag,
        "dur_flag": dur_flag,
        "resampled_to_hz": TARGET_SR,
        "out_wav": str(out_path.relative_to(REPO)),
    }


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    mp3s = sorted(UPLOADS.glob("human_*.mp3"))
    if len(mp3s) != 8:
        print(f"[fatal] expected 8 mp3s in {UPLOADS}, found {len(mp3s)}", file=sys.stderr)
        return 2

    rows = []
    fails = 0
    for p in mp3s:
        r = validate_one(p)
        rows.append(r)
        is_fail = r["clipped"] or r["snr_flag"] != "OK" or r["dur_flag"] != "OK"
        if is_fail:
            fails += 1

    print(f"\n{'file':<16} {'sr':>6} {'ch':>3} {'dur':>6} {'peak':>6} "
          f"{'clip':>5} {'sil%':>5} {'snr':>12} {'dur':>13}")
    for r in rows:
        print(f"{r['filename']:<16} {r['native_sr']:>6} {r['channels']:>3} "
              f"{r['duration_s']:>6.2f} {r['peak_amp']:>6.3f} "
              f"{str(r['clipped']):>5} {r['silence_share']*100:>4.1f}% "
              f"{r['snr_flag']:>12} {r['dur_flag']:>13}")

    with REPORT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"\nWrote {REPORT.relative_to(REPO)}")
    print(f"Wavs in {OUT_DIR.relative_to(REPO)}/")
    print(f"Fail count: {fails}/{len(rows)} (stop threshold = 3)")
    return 0 if fails < 3 else 3


if __name__ == "__main__":
    raise SystemExit(main())
