"""IndicF5 inference wrapper — duration-patched, preprocessing-enabled.

Public API
----------
load_model(hf_token=None, device=None) -> model
    Load IndicF5 from HuggingFace. Raises if f5_tts is not installed.

synthesize(model, text, ref_audio_path, ref_text,
           preprocess=True, speed=1.0) -> np.ndarray
    Generate speech. Returns float32 audio at 24 000 Hz.
    preprocess=True (default): passes text through to_unified_devanagari()
        before feeding to the model. This is the production path.
    preprocess=False: feeds text verbatim. Use for phonetic probe experiments
        where the caller deliberately wants raw Devanagari markers.

_PATCH_STATUS : dict
    Module-level record of what the duration patch did on import.
    Keys: "paths_found", "patched", "already_patched", "no_match".
    Inspect this to confirm the patch is active before running inference.

The duration patch (Mode A fix)
--------------------------------
IndicF5 v12 computes the output audio canvas size from UTF-8 byte counts of
the reference and generation texts (f5_tts/infer/utils_infer.py, ~line 451):

    ref_text_len = len(ref_text.encode("utf-8"))   # BUG
    gen_text_len = len(gen_text.encode("utf-8"))   # BUG

Devanagari encodes as ~3 bytes per character; ASCII encodes as 1 byte. For
Roman-script input, the formula allocates ~3× less canvas than needed,
truncating the output audio. This is "Mode A" failure, diagnosed at
diagnostics/duration_diagnostic/REPORT.md.

Fix: count non-whitespace *characters* instead of bytes:

    ref_text_len = sum(1 for c in ref_text if not c.isspace())
    gen_text_len = sum(1 for c in gen_text if not c.isspace())

This module applies the fix at import time by rewriting utils_infer.py
in site-packages. The patch:
  - Is idempotent: checks for the "DEBUG-PATCH" sentinel before modifying.
  - Is safe to apply when the module is already patched (no-op).
  - Emits a WARNING (not an error) if f5_tts is not installed, so this
    module can be imported for preprocessing-only use without the model.
  - Patches every copy of utils_infer.py found on sys.path (handles editable
    installs that may have multiple copies).

The patched code prints one "DEBUG-PATCH:" line per synthesize() call to
stdout. This is intentional diagnostic output: it lets you verify the
character count formula is active and see gen_frames before audio is written.
Redirect stdout if you want to suppress it.
"""
from __future__ import annotations

import glob
import sys
import warnings
from pathlib import Path
from typing import Optional

import numpy as np


# ---------------------------------------------------------------------------
# Duration patch — applied at module import time
# ---------------------------------------------------------------------------

# These strings must match the IndicF5 v12 source exactly, including indentation.
# The else: block inside infer_process() uses 12-space indentation.
_ORIG_BLOCK = (
    '            # Calculate duration\n'
    '            ref_text_len = len(ref_text.encode("utf-8"))\n'
    '            gen_text_len = len(gen_text.encode("utf-8"))\n'
    '            duration = ref_audio_len + int(ref_audio_len / ref_text_len * gen_text_len / speed)\n'
)

# The DEBUG-PATCH sentinel in the first line is how we detect an already-patched
# file — do not remove it. The print() call is intentional diagnostic output.
_PATCHED_BLOCK = (
    '            # PATCHED — character-count proportional duration (Mode A fix)\n'
    '            # UTF-8 byte counts under-allocate canvas for Devanagari:ASCII mixes.\n'
    '            # See diagnostics/duration_diagnostic/REPORT.md\n'
    '            ref_text_len = sum(1 for c in ref_text if not c.isspace())  # DEBUG-PATCH\n'
    '            gen_text_len = sum(1 for c in gen_text if not c.isspace())\n'
    '            duration = ref_audio_len + int(ref_audio_len / ref_text_len * gen_text_len / speed)\n'
    '            print(f"DEBUG-PATCH: ref_chars={ref_text_len} gen_chars={gen_text_len} "\n'
    '                  f"ref_frames={ref_audio_len} gen_frames={duration - ref_audio_len} "\n'
    '                  f"text={gen_text[:50]!r}")\n'
)

_PATCH_SENTINEL = "DEBUG-PATCH"


def _apply_duration_patch() -> dict:
    """Find utils_infer.py in site-packages and apply the duration fix.

    Called once at module import. Returns a status dict so callers can
    verify the patch is active (inspect _PATCH_STATUS).
    """
    status: dict = {
        "paths_found": [],
        "patched": [],
        "already_patched": [],
        "no_match": [],
    }

    candidates: list[str] = []
    for root in [p for p in sys.path if p]:
        candidates.extend(
            glob.glob(f"{root}/**/f5_tts/infer/utils_infer.py", recursive=True)
        )
    candidates = sorted(set(candidates))
    status["paths_found"] = candidates

    if not candidates:
        warnings.warn(
            "inference.py: f5_tts not found on sys.path — duration patch not applied. "
            "Install IndicF5 before calling load_model().",
            ImportWarning,
            stacklevel=2,
        )
        return status

    for path in candidates:
        src = Path(path).read_text(encoding="utf-8")

        if _PATCH_SENTINEL in src:
            status["already_patched"].append(path)
            continue

        if _ORIG_BLOCK not in src:
            # The source doesn't match — different IndicF5 version or already modified.
            status["no_match"].append(path)
            warnings.warn(
                f"inference.py: duration patch target block not found in {path}. "
                "The file may be a different IndicF5 version. Inspect manually.",
                RuntimeWarning,
                stacklevel=2,
            )
            continue

        new_src = src.replace(_ORIG_BLOCK, _PATCHED_BLOCK, 1)
        Path(path).write_text(new_src, encoding="utf-8")
        status["patched"].append(path)

    return status


# Apply once at import. Results are visible via _PATCH_STATUS.
_PATCH_STATUS: dict = _apply_duration_patch()


def _check_patch_active() -> None:
    """Raise if the patch was not applied to any utils_infer.py."""
    if not _PATCH_STATUS["paths_found"]:
        raise RuntimeError(
            "f5_tts is not installed. Run:\n"
            "  pip install git+https://github.com/AI4Bharat/IndicF5.git"
        )
    active = _PATCH_STATUS["patched"] + _PATCH_STATUS["already_patched"]
    if not active:
        raise RuntimeError(
            "Duration patch could not be applied — utils_infer.py source did not "
            "match the expected IndicF5 v12 block. Check _PATCH_STATUS['no_match'] "
            "for the file path and inspect manually.\n"
            f"  no_match: {_PATCH_STATUS['no_match']}"
        )


# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------

def load_model(
    hf_token: Optional[str] = None,
    device: Optional[str] = None,
) -> object:
    """Load IndicF5 from HuggingFace.

    Parameters
    ----------
    hf_token:
        HuggingFace access token. Required if the repo is gated.
        Falls back to the HF_TOKEN environment variable if not provided.
    device:
        "cuda", "cpu", or None (auto: CUDA if available, else CPU).

    Returns
    -------
    The loaded model (AutoModel instance), moved to `device`.

    Notes
    -----
    Verifies the duration patch is active before loading. The model imports
    utils_infer at load time, so the patch must be in place beforehand.
    """
    _check_patch_active()

    import os
    import torch
    from transformers import AutoModel

    if hf_token is None:
        hf_token = os.environ.get("HF_TOKEN")

    if hf_token:
        import huggingface_hub
        huggingface_hub.login(token=hf_token, add_to_git_credential=False)

    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    model = AutoModel.from_pretrained(
        "ai4bharat/IndicF5",
        trust_remote_code=True,
    ).to(device)

    return model


# ---------------------------------------------------------------------------
# Inference
# ---------------------------------------------------------------------------

def synthesize(
    model: object,
    text: str,
    ref_audio_path: str,
    ref_text: str,
    *,
    preprocess: bool = True,
    speed: float = 1.0,
) -> np.ndarray:
    """Generate speech from `text` using IndicF5.

    Parameters
    ----------
    model:
        Loaded IndicF5 model (from load_model()).
    text:
        Input text to synthesize. Any Hinglish script mix.
    ref_audio_path:
        Path to reference audio WAV (the voice to clone).
    ref_text:
        Transcript of the reference audio.
    preprocess:
        If True (default), apply to_unified_devanagari() before inference.
        Set False for phonetic probe experiments where you want raw Devanagari
        markers passed verbatim to the model.
    speed:
        Speaking rate multiplier (1.0 = reference speed).

    Returns
    -------
    np.ndarray
        float32 audio array at 24 000 Hz, shape (n_samples,).

    Raises
    ------
    ValueError
        If text is empty after preprocessing.
    RuntimeError
        If the model returns an unexpected type.
    """
    import torch

    if not text or not text.strip():
        raise ValueError("text is empty")

    input_text = text
    if preprocess:
        from scoring.scripts.lib_normalize import to_unified_devanagari
        input_text = to_unified_devanagari(text)
        if not input_text.strip():
            raise ValueError(
                f"Text became empty after preprocessing: {text!r}"
            )

    with torch.inference_mode():
        audio = model(
            text=input_text,
            ref_audio_path=str(ref_audio_path),
            ref_text=ref_text,
            speed=speed,
        )

    # Normalise output type — model may return Tensor, ndarray, or list
    if hasattr(audio, "cpu"):
        audio = audio.cpu().numpy()
    audio = np.asarray(audio, dtype=np.float32).squeeze()

    # int16 PCM → float32 [-1, 1]
    if audio.dtype == np.int16:
        audio = audio.astype(np.float32) / 32768.0

    if audio.ndim != 1:
        raise RuntimeError(
            f"Expected 1-D audio array after squeeze, got shape {audio.shape}"
        )

    return audio


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _main() -> int:
    import argparse
    import soundfile as sf

    parser = argparse.ArgumentParser(
        description="Synthesize speech with IndicF5 (duration-patched).",
    )
    parser.add_argument("text", help="Text to synthesize.")
    parser.add_argument("--ref-audio", required=True, help="Reference audio WAV path.")
    parser.add_argument("--ref-text", required=True, help="Reference audio transcript.")
    parser.add_argument("--out", required=True, help="Output WAV path.")
    parser.add_argument(
        "--no-preprocess",
        action="store_true",
        help="Skip to_unified_devanagari() preprocessing (phonetic probe mode).",
    )
    parser.add_argument("--hf-token", default=None, help="HuggingFace access token.")
    parser.add_argument("--device", default=None, help="cuda or cpu (default: auto).")
    parser.add_argument("--speed", type=float, default=1.0, help="Speed multiplier.")
    parser.add_argument(
        "--patch-status",
        action="store_true",
        help="Print duration patch status and exit.",
    )
    args = parser.parse_args()

    if args.patch_status:
        import json
        print(json.dumps(_PATCH_STATUS, indent=2))
        return 0

    model = load_model(hf_token=args.hf_token, device=args.device)
    audio = synthesize(
        model,
        args.text,
        ref_audio_path=args.ref_audio,
        ref_text=args.ref_text,
        preprocess=not args.no_preprocess,
        speed=args.speed,
    )

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(out_path), audio, 24000)
    print(f"Wrote {out_path}  ({len(audio)/24000:.2f}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
