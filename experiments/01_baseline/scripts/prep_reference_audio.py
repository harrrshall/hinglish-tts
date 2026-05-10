#!/usr/bin/env python3
"""Prepare audit/reference_audio/hindi_ref.{wav,txt} per AUDIT_PLAN.md §2.

Tries Rasa first; falls back to IndicF5's bundled prompts. After download,
resamples to 24 kHz mono and clips to <=8 s if needed. Verifies the final
clip per §2.2.

Run:
    python audit/scripts/prep_reference_audio.py
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
OUT_DIR = REPO / "audit" / "reference_audio"
WAV = OUT_DIR / "hindi_ref.wav"
TXT = OUT_DIR / "hindi_ref.txt"


TARGET_SR = 24000  # AUDIT_PLAN.md §2.2


def _resample_and_write(audio, sr: int) -> int:
    """Resample to TARGET_SR mono and write WAV. Returns the final sr."""
    import numpy as np
    import soundfile as sf
    if audio.ndim > 1:
        audio = audio.mean(axis=1)
    if sr != TARGET_SR:
        try:
            import librosa
            audio = librosa.resample(audio.astype(np.float32), orig_sr=sr, target_sr=TARGET_SR)
        except ImportError:
            # librosa not strictly required by the prep stack; install on demand.
            print(f"[prep] librosa not installed, installing for resample {sr}->{TARGET_SR}...")
            import subprocess, sys
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "librosa"])
            import librosa
            audio = librosa.resample(audio.astype(np.float32), orig_sr=sr, target_sr=TARGET_SR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    sf.write(WAV, audio, TARGET_SR, subtype="PCM_16")
    return TARGET_SR


def _rasa() -> bool:
    try:
        from datasets import load_dataset
        ds = load_dataset("ai4bharat/Rasa", "hindi", split="train", streaming=True)
        sample = next(iter(ds))
        audio = sample["audio"]["array"]
        sr = sample["audio"]["sampling_rate"]
        text = sample.get("text") or sample.get("transcription") or ""
        if not text.strip():
            print("[prep] Rasa: empty transcript — skipping")
            return False
        final_sr = _resample_and_write(audio, sr)
        TXT.write_text(text, encoding="utf-8")
        print(f"[prep] Rasa OK: orig_sr={sr} -> {final_sr}, transcript_len={len(text)}")
        return True
    except Exception as e:
        print(f"[prep] Rasa failed: {e}")
        return False


def _springlab_indictts_hindi() -> bool:
    """Pull one Hindi clip from SPRINGLab/IndicTTS-Hindi (open dataset)."""
    try:
        from datasets import load_dataset
        ds = load_dataset("SPRINGLab/IndicTTS-Hindi", split="train", streaming=True)
        sample = next(iter(ds))
        audio = sample["audio"]["array"]
        sr = sample["audio"]["sampling_rate"]
        text = (sample.get("text") or sample.get("transcription") or
                sample.get("normalized_text") or "")
        if not text.strip():
            print("[prep] SPRINGLab/IndicTTS-Hindi: empty transcript — skipping")
            return False
        final_sr = _resample_and_write(audio, sr)
        TXT.write_text(text, encoding="utf-8")
        print(f"[prep] SPRINGLab/IndicTTS-Hindi OK: orig_sr={sr} -> {final_sr}, transcript_len={len(text)}")
        return True
    except Exception as e:
        print(f"[prep] SPRINGLab/IndicTTS-Hindi failed: {e}")
        return False


def _indicf5_bundled() -> bool:
    """Last resort: pull a clip from the IndicF5 GitHub repo's prompts/ directory.

    IndicF5 bundles Kannada/Marathi/Punjabi/Tamil samples but NO Hindi.
    This fallback intentionally fails loudly — using Kannada/Tamil as a
    "Hindi reference" would silently degrade IndicF5 + SPRINGLab F5 output.
    The script exits with a clear actionable error instead.
    """
    try:
        tmp = Path("/tmp/indicf5_audit")
        if tmp.exists():
            shutil.rmtree(tmp)
        subprocess.run(
            ["git", "clone", "--depth", "1",
             "https://github.com/AI4Bharat/IndicF5.git", str(tmp)],
            check=True, capture_output=True, text=True,
        )
        # Look ONLY for Hindi-tagged clips. Do NOT fall through to other languages.
        candidates = sorted(tmp.glob("prompts/*HIN*.wav")) + \
                     sorted(tmp.glob("prompts/*hindi*.wav"))
        if not candidates:
            print("[prep] IndicF5 bundled clips: NO Hindi clips present "
                  "(repo only ships KAN/MAR/PAN/TAM). "
                  "Will not silently use a non-Hindi clip — see error message.")
            return False
        ref = candidates[0]
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy(ref, WAV)
        sib_txt = next(iter(ref.parent.glob(ref.stem + "*.txt")), None)
        if sib_txt:
            shutil.copy(sib_txt, TXT)
        else:
            print(f"[prep] WARN: no sibling transcript for {ref.name}; "
                  "you MUST transcribe the clip and write audit/reference_audio/hindi_ref.txt before running models.")
        print(f"[prep] IndicF5 bundled fallback OK: copied {ref.name}")
        return True
    except Exception as e:
        print(f"[prep] IndicF5 bundled fallback failed: {e}")
        return False


def _verify() -> list[str]:
    problems: list[str] = []
    if not WAV.exists():
        problems.append("hindi_ref.wav missing")
    if not TXT.exists() or not TXT.read_text(encoding="utf-8").strip():
        problems.append("hindi_ref.txt missing or empty")
    if WAV.exists():
        try:
            import soundfile as sf
            info = sf.info(str(WAV))
            dur = info.frames / info.samplerate
            if not 3.0 <= dur <= 8.0:
                problems.append(f"hindi_ref.wav duration {dur:.2f}s outside 3–8 s")
            if info.channels != 1:
                problems.append(f"hindi_ref.wav has {info.channels} channels (need mono)")
            if info.samplerate != 24000:
                problems.append(f"hindi_ref.wav sr={info.samplerate} (need 24000); resample with librosa")
        except Exception as e:
            problems.append(f"could not read hindi_ref.wav: {e}")
    return problems


def main() -> int:
    # Priority order: prefer datasets that ship real Hindi audio + transcript.
    if not (_rasa() or _springlab_indictts_hindi() or _indicf5_bundled()):
        print(
            "\n[prep] FAILED: no source produced a clean Hindi reference clip.\n"
            "Manual fix:\n"
            "  1. Find ANY 3–8 s clean mono Hindi recording (your own voice is fine).\n"
            "  2. Resample to 24 kHz mono WAV:  ffmpeg -i in.* -ar 24000 -ac 1 -c:a pcm_s16le \\\n"
            "       audit/reference_audio/hindi_ref.wav\n"
            "  3. Write the EXACT Devanagari transcript to audit/reference_audio/hindi_ref.txt\n"
            "  4. Re-run audit/scripts/verify.py to confirm.\n",
            file=sys.stderr,
        )
        return 1
    problems = _verify()
    if problems:
        print("[prep] verification problems:", file=sys.stderr)
        for p in problems:
            print(f"  • {p}", file=sys.stderr)
        return 2
    print("[prep] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
