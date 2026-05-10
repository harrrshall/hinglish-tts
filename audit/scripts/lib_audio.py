"""Audio DSP helpers for the auto-scoring pipeline.

Three signals extracted per clip:
- silence_mid_clip_s: longest silence segment inside the clip (start/end trimmed)
- end_pop_db: last-200ms peak relative to prior 200ms RMS, in dB
- terminal_sample_abs: abs(last sample) — DC-tail detector

All inputs read with soundfile (returns float64 in [-1, 1]) at the file's native sample rate.
The signal-extraction pipeline is sample-rate agnostic for these features.
"""
from __future__ import annotations

import numpy as np
import soundfile as sf


def load_wav(path: str) -> tuple[np.ndarray, int]:
    """Read a wav into a mono float32 array. Returns (samples, sr)."""
    audio, sr = sf.read(path, dtype="float32", always_2d=False)
    if audio.ndim > 1:
        audio = audio.mean(axis=1)
    return audio, sr


def longest_silence_s(audio: np.ndarray, sr: int,
                      threshold_db: float = -40.0,
                      frame_ms: int = 20,
                      trim_edges_s: float = 0.1) -> float:
    """Return the longest contiguous silence (in seconds) INSIDE the clip.

    Frames an audio signal at frame_ms windows, computes per-frame RMS in dBFS,
    and returns the longest run of frames below threshold_db. The first and last
    `trim_edges_s` of the clip are excluded so leading/trailing silence doesn't
    inflate the result — we only care about mid-clip skips.
    """
    if len(audio) == 0:
        return 0.0
    frame_len = max(1, int(sr * frame_ms / 1000))
    n_frames = len(audio) // frame_len
    if n_frames < 3:
        return 0.0
    frames = audio[: n_frames * frame_len].reshape(n_frames, frame_len)
    rms = np.sqrt((frames ** 2).mean(axis=1) + 1e-12)
    db = 20 * np.log10(rms)
    silent = db < threshold_db

    # Trim edge frames so leading/trailing silence isn't counted.
    edge_frames = max(1, int(trim_edges_s * 1000 / frame_ms))
    if 2 * edge_frames >= n_frames:
        return 0.0
    silent[:edge_frames] = False
    silent[-edge_frames:] = False

    longest = run = 0
    for s in silent:
        if s:
            run += 1
            longest = max(longest, run)
        else:
            run = 0
    return longest * frame_ms / 1000.0


def end_pop_db(audio: np.ndarray, sr: int, window_ms: int = 200) -> float:
    """Return last-window peak (dB) relative to prior-window RMS (dB).

    A clean tail has near-zero peak. A pop has peak >> prior RMS, so the
    returned value (peak_dB - prior_rms_dB) is large and positive.
    Returns 0.0 if the clip is shorter than 2 windows.
    """
    n = int(sr * window_ms / 1000)
    if len(audio) < 2 * n:
        return 0.0
    last = audio[-n:]
    prior = audio[-2 * n:-n]
    peak = np.max(np.abs(last)) + 1e-12
    prior_rms = np.sqrt((prior ** 2).mean() + 1e-12)
    return float(20 * np.log10(peak / prior_rms))


def terminal_sample_abs(audio: np.ndarray) -> float:
    """abs(last sample). >0.05 indicates DC-tail or hard cutoff."""
    if len(audio) == 0:
        return 0.0
    return float(abs(audio[-1]))


def analyze(path: str) -> dict:
    """Run all three DSP detectors on a wav file. Returns the signal dict."""
    audio, sr = load_wav(path)
    return {
        "duration_s": float(len(audio) / sr) if sr > 0 else 0.0,
        "sample_rate_hz": int(sr),
        "silence_mid_clip_s": round(longest_silence_s(audio, sr), 3),
        "end_pop_db": round(end_pop_db(audio, sr), 2),
        "terminal_sample_abs": round(terminal_sample_abs(audio), 4),
    }


if __name__ == "__main__":
    # Smoke-test against one wav per model dir.
    from pathlib import Path
    base = Path("/home/cybernovas/Desktop/hienglish/audit/results")
    for model in ["kokoro", "indic_parler", "indicf5", "springlab_f5"]:
        wav = next(iter((base / model).glob("01.wav")), None)
        if wav is None:
            print(f"{model}: no 01.wav found")
            continue
        print(f"{model:14s} {analyze(str(wav))}")
