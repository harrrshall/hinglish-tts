"""MOS predictors for naturalness + speaker quality.

Primary (always available):
- Torchaudio SQUIM_SUBJECTIVE → predicted MOS (NORESQA-MOS, ICASSP 2023)
- Torchaudio SQUIM_OBJECTIVE → predicted PESQ + STOI + SI-SDR (no reference)

Optional (skipped if not installed/available):
- UTMOS via tarepan/SpeechMOS torch.hub. The 392MB GitHub release download
  is slow on some networks; if torch.hub.load fails, we set utmos=NaN and the
  Claude judge falls back to SQUIM_MOS only.

Both predictors are English-trained, so absolute scores drift on Hindi but
relative ranking across the 4 models on the same sentence is the useful signal.

All operations are deterministic.
"""
from __future__ import annotations

import functools
import io
from contextlib import redirect_stdout, redirect_stderr

import numpy as np
import torch
import torchaudio


# ─────────────────────────────────────────────────────────────────────────────
# Sample-rate normalization
# ─────────────────────────────────────────────────────────────────────────────

def _resample_if_needed(audio: np.ndarray, sr: int, target_sr: int) -> np.ndarray:
    """Resample audio (numpy float32 mono) to target_sr if needed."""
    if sr == target_sr:
        return audio
    tensor = torch.from_numpy(audio).unsqueeze(0)  # [1, T]
    resampled = torchaudio.functional.resample(tensor, sr, target_sr)
    return resampled.squeeze(0).numpy()


# ─────────────────────────────────────────────────────────────────────────────
# UTMOS via speechmos
# ─────────────────────────────────────────────────────────────────────────────

@functools.lru_cache(maxsize=1)
def _utmos_predictor():
    """Try to load tarepan/SpeechMOS UTMOS22 via torch.hub. None if unavailable."""
    try:
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            predictor = torch.hub.load(
                "tarepan/SpeechMOS:v1.2.0", "utmos22_strong",
                trust_repo=True, verbose=False,
            )
        return predictor
    except Exception as e:
        print(f"[lib_mos] UTMOS unavailable ({e}); will report utmos=NaN")
        return None


def utmos_score(audio: np.ndarray, sr: int) -> float:
    """Predicted MOS via UTMOS22, or NaN if predictor unavailable."""
    predictor = _utmos_predictor()
    if predictor is None:
        return float("nan")
    audio16 = _resample_if_needed(audio, sr, 16000).astype(np.float32)
    tensor = torch.from_numpy(audio16).unsqueeze(0)
    with torch.no_grad():
        score = predictor(tensor, sr=16000)
    return float(score.item() if torch.is_tensor(score) else score)


# ─────────────────────────────────────────────────────────────────────────────
# SQUIM (subjective MOS + objective PESQ/STOI/SI-SDR)
# ─────────────────────────────────────────────────────────────────────────────

@functools.lru_cache(maxsize=1)
def _squim_subjective():
    """SQUIM_SUBJECTIVE pipeline — predicts MOS using non-matching reference."""
    from torchaudio.pipelines import SQUIM_SUBJECTIVE
    return SQUIM_SUBJECTIVE.get_model().eval()


@functools.lru_cache(maxsize=1)
def _squim_objective():
    """SQUIM_OBJECTIVE pipeline — predicts PESQ, STOI, SI-SDR (no reference)."""
    from torchaudio.pipelines import SQUIM_OBJECTIVE
    return SQUIM_OBJECTIVE.get_model().eval()


@functools.lru_cache(maxsize=1)
def _nmr_audio() -> tuple[torch.Tensor, int]:
    """Load a single non-matching reference for SQUIM_SUBJECTIVE (any clean speech).

    SQUIM-SUBJECTIVE needs a clean reference audio that does NOT match the input;
    it's a perceptual baseline. We use a short Kokoro clip (we know it's clean and
    English-grade) as the NMR. Cached.
    """
    import soundfile as sf
    import os
    # Try to use a Kokoro 24kHz clip as NMR (known clean)
    paths = [
        "/home/cybernovas/Desktop/hienglish/audit/results/kokoro/01.wav",
        "/home/cybernovas/Desktop/hienglish/audit/reference_audio/hindi_ref.wav",
    ]
    for p in paths:
        if os.path.exists(p):
            audio, sr = sf.read(p, dtype="float32", always_2d=False)
            if audio.ndim > 1:
                audio = audio.mean(axis=1)
            tensor = torch.from_numpy(_resample_if_needed(audio, sr, 16000)).unsqueeze(0)
            return tensor, 16000
    raise RuntimeError("No NMR audio file available")


@torch.no_grad()
def squim_scores(audio: np.ndarray, sr: int) -> dict[str, float]:
    """Run SQUIM-SUBJECTIVE and SQUIM-OBJECTIVE on the audio.

    Returns: {squim_mos, squim_pesq, squim_stoi, squim_sisdr}.
    SQUIM expects 16 kHz mono. Resamples internally.
    """
    audio16 = _resample_if_needed(audio, sr, 16000).astype(np.float32)
    tensor = torch.from_numpy(audio16).unsqueeze(0)  # [1, T]

    # Objective: PESQ, STOI, SI-SDR
    obj_model = _squim_objective()
    stoi_t, pesq_t, sisdr_t = obj_model(tensor)
    out = {
        "squim_pesq": float(pesq_t.item()),
        "squim_stoi": float(stoi_t.item()),
        "squim_sisdr": float(sisdr_t.item()),
    }

    # Subjective MOS (needs non-matching reference)
    try:
        sub_model = _squim_subjective()
        nmr, _ = _nmr_audio()
        # Lengths must be reasonable for the model; pad/truncate NMR to input length
        if nmr.shape[1] != tensor.shape[1]:
            min_len = min(nmr.shape[1], tensor.shape[1])
            mos_t = sub_model(tensor[:, :min_len], nmr[:, :min_len])
        else:
            mos_t = sub_model(tensor, nmr)
        out["squim_mos"] = float(mos_t.item())
    except Exception as e:
        print(f"[lib_mos] SQUIM_SUBJECTIVE failed: {e}; setting squim_mos=NaN")
        out["squim_mos"] = float("nan")

    return {k: round(v, 3) for k, v in out.items()}


# ─────────────────────────────────────────────────────────────────────────────
# Convenience: full MOS extraction
# ─────────────────────────────────────────────────────────────────────────────

def all_mos_signals(audio: np.ndarray, sr: int) -> dict[str, float]:
    """Run UTMOS + SQUIM together. Returns combined dict."""
    out = {"utmos": round(utmos_score(audio, sr), 3)}
    out.update(squim_scores(audio, sr))
    return out


if __name__ == "__main__":
    # Smoke-test on the 4 sample wavs
    import soundfile as sf
    from pathlib import Path
    base = Path("/home/cybernovas/Desktop/hienglish/audit/results")
    for model in ["kokoro", "indic_parler", "indicf5", "springlab_f5"]:
        wav = base / model / "01.wav"
        if not wav.exists():
            continue
        audio, sr = sf.read(str(wav), dtype="float32", always_2d=False)
        if audio.ndim > 1:
            audio = audio.mean(axis=1)
        scores = all_mos_signals(audio, sr)
        print(f"{model:14s} sr={sr:5d}  {scores}")
