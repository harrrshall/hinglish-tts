#!/usr/bin/env bash
# setup.sh — one-shot environment setup for the Hinglish TTS inference stack.
#
# Usage:
#   bash setup.sh
#
# What this does:
#   1. Installs system packages (Python 3.11, espeak-ng, build tools, etc.)
#   2. Creates a Python 3.11 venv at .venv/ in this directory
#   3. Installs Python dependencies (torch first, then requirements.txt)
#   4. Installs IndicF5 from GitHub
#   5. Downloads a reference audio clip for smoke tests
#   6. Optionally logs in to HuggingFace and runs a smoke test
#
# Prerequisites:
#   - Ubuntu 20.04, 22.04, or 24.04 (uses apt + deadsnakes PPA)
#   - Internet access
#   - HF_TOKEN env var set to your HuggingFace token (needed for model download)
#     The model is gated: accept terms at huggingface.co/ai4bharat/IndicF5 first.
#
# GPU users:
#   By default this installs the CPU-compatible PyTorch wheel from PyPI.
#   For GPU inference, pin torch to your CUDA version before running:
#     TORCH_INDEX=https://download.pytorch.org/whl/cu124 bash setup.sh
#
# After setup, activate the venv and run inference from the repo root:
#   source .venv/bin/activate
#   PYTHONPATH=. python inference.py "कल office jaana है" \
#     --ref-audio assets/reference_audio/PAN_F_HAPPY_00001.wav \
#     --ref-text  "ਭਹੰਪੀ ਵਿੱਚ ਸਮਾਰਕਾਂ ਦੇ ਭਵਨ ਅਤੇ ਮੰਦਰ ਹਨ।" \
#     --out /tmp/out.wav

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$REPO_ROOT/.venv"
REF_AUDIO_DIR="$REPO_ROOT/assets/reference_audio"
REF_AUDIO="$REF_AUDIO_DIR/PAN_F_HAPPY_00001.wav"

# GPU torch index: override with e.g. https://download.pytorch.org/whl/cu124
TORCH_INDEX="${TORCH_INDEX:-}"

# Use sudo only when not already root
if [ "$(id -u)" = "0" ]; then
  SUDO=""
else
  SUDO="sudo"
fi

log() { echo "[setup] $*"; }
step() { echo; echo "=== $* ==="; }

# ---------------------------------------------------------------------------
step "1/9  System packages"
# ---------------------------------------------------------------------------
export DEBIAN_FRONTEND=noninteractive

log "Installing software-properties-common + gnupg2..."
$SUDO apt-get update -qq
# gnupg2 is required for add-apt-repository to import PPA keys (gpg-agent absent
# in minimal Ubuntu Docker images even when gpg is present).
$SUDO apt-get install -y --no-install-recommends software-properties-common gnupg2

log "Adding deadsnakes PPA (Python 3.11)..."
$SUDO add-apt-repository -y ppa:deadsnakes/ppa
$SUDO apt-get update -qq

log "Installing Python 3.11 + build deps + TTS system libs..."
$SUDO apt-get install -y --no-install-recommends \
  python3.11 \
  python3.11-venv \
  python3.11-dev \
  build-essential \
  git \
  curl \
  espeak-ng \
  libsndfile1 \
  ffmpeg

python3.11 --version

# ---------------------------------------------------------------------------
step "2/9  Python venv (.venv/)"
# ---------------------------------------------------------------------------
if [ -d "$VENV" ]; then
  log "Venv already exists at $VENV — skipping creation."
else
  log "Creating venv at $VENV..."
  python3.11 -m venv "$VENV"
fi

# Activate for the rest of this script
# shellcheck disable=SC1091
source "$VENV/bin/activate"
log "Active Python: $(python --version) at $(which python)"

# ---------------------------------------------------------------------------
step "3/9  pip / wheel / setuptools"
# ---------------------------------------------------------------------------
pip install "pip==24.0" wheel "setuptools<69"
# setuptools is capped at <69 before fairseq install because fairseq's setup.py
# uses distutils APIs that were deprecated in setuptools>=70. After fairseq
# installs we restore a current setuptools.

# ---------------------------------------------------------------------------
step "4/9  Install torch (must precede fairseq / ai4bharat-transliteration)"
# ---------------------------------------------------------------------------
# fairseq reads torch during its own build. Installing torch first avoids
# build failures where fairseq tries to import torch before it exists.
if [ -n "$TORCH_INDEX" ]; then
  log "Installing torch from GPU index: $TORCH_INDEX"
  pip install "torch>=2.0,<3" "torchaudio>=2.0,<3" "numpy<2.1" \
    --index-url "$TORCH_INDEX"
else
  log "Installing CPU-only torch (~200 MB; set TORCH_INDEX for GPU e.g. cu124)..."
  # Use the PyTorch CPU index to avoid pulling 2 GB of CUDA libs onto a machine
  # that may have no GPU. GPU users: TORCH_INDEX=https://download.pytorch.org/whl/cu124
  pip install "torch>=2.0,<3" "torchaudio>=2.0,<3" "numpy<2.1" \
    --index-url https://download.pytorch.org/whl/cpu
fi

# ---------------------------------------------------------------------------
step "5/9  Install fairseq + requirements.txt"
# ---------------------------------------------------------------------------
# fairseq 0.12.2 PyPI sdist has two known bugs:
#   1. Missing fairseq/version.txt — causes FileNotFoundError during build
#   2. Missing data_utils_fast.cpp — it's Cython-generated, absent from sdist
# Fix: download sdist, inject version.txt, then build with Cython available.
# Cython must be installed before the build (--no-build-isolation uses the
# current venv, so if Cython is installed here, the build can transpile .pyx).
pip install "Cython<3"

_FSDIR=$(mktemp -d)
pip download "fairseq==0.12.2" --no-deps -d "$_FSDIR" -q
tar xzf "$_FSDIR/fairseq-0.12.2.tar.gz" -C "$_FSDIR"
printf "0.12.2\n" > "$_FSDIR/fairseq-0.12.2/fairseq/version.txt"
pip install "$_FSDIR/fairseq-0.12.2/" --no-build-isolation -q
rm -rf "$_FSDIR"

# torch/numpy/torchaudio already satisfied — pip will skip them.
# fairseq already satisfied above — pip will skip it.
pip install -r "$REPO_ROOT/requirements.txt"

# Restore a current setuptools now that fairseq has built.
pip install --upgrade setuptools

# ---------------------------------------------------------------------------
step "6/9  Install IndicF5 from GitHub"
# ---------------------------------------------------------------------------
# IndicF5 has no PyPI release. The GitHub repo includes f5_tts (the underlying
# engine) and the ai4bharat model code. Pinning to main; to reproduce exactly:
#   pip install git+https://github.com/AI4Bharat/IndicF5.git@<commit-sha>
pip install git+https://github.com/AI4Bharat/IndicF5.git

# ---------------------------------------------------------------------------
step "7/9  Download reference audio"
# ---------------------------------------------------------------------------
mkdir -p "$REF_AUDIO_DIR"
if [ -f "$REF_AUDIO" ]; then
  log "Reference audio already present — skipping download."
else
  log "Downloading PAN_F_HAPPY_00001.wav..."
  curl -fsSL \
    -o "$REF_AUDIO" \
    "https://raw.githubusercontent.com/AI4Bharat/IndicF5/main/prompts/PAN_F_HAPPY_00001.wav"
  log "Saved to $REF_AUDIO"
fi

# ---------------------------------------------------------------------------
step "8/9  HuggingFace login"
# ---------------------------------------------------------------------------
if [ -n "${HF_TOKEN:-}" ]; then
  log "Logging in to HuggingFace..."
  huggingface-cli login --token "$HF_TOKEN" --add-to-git-credential=false
else
  log "WARN: HF_TOKEN is not set."
  log "      Model download (AutoModel.from_pretrained) will fail until you set it."
  log "      Accept gating at: https://huggingface.co/ai4bharat/IndicF5"
  log "      Then: export HF_TOKEN=<your_token>  and re-run, or call inference.load_model(hf_token=...)"
fi

# ---------------------------------------------------------------------------
step "9/9  Smoke tests"
# ---------------------------------------------------------------------------

log "Smoke 1: import inference + verify duration patch is active..."
cd "$REPO_ROOT"
PYTHONPATH=. python - <<'PY'
import json, sys
import inference
s = inference._PATCH_STATUS
patched_count = len(s["patched"]) + len(s["already_patched"])
if patched_count == 0:
    print("[FAIL] Duration patch was not applied to any utils_infer.py")
    print("       no_match paths:", s["no_match"])
    print("       paths_found:",    s["paths_found"])
    sys.exit(1)
print("[OK]  Duration patch active.")
print("      patched:", s["patched"])
print("      already_patched:", s["already_patched"])
PY

log "Smoke 2: IndicXlit transliteration..."
PYTHONPATH=. python - <<'PY'
from scoring.scripts.lib_normalize import to_unified_devanagari
result = to_unified_devanagari("kal office jaana hai")
assert "ऑफिस" in result, f"Expected ऑफिस in output, got: {result!r}"
print(f"[OK]  to_unified_devanagari: 'kal office jaana hai' → {result!r}")
PY

if [ -n "${HF_TOKEN:-}" ]; then
  log "Smoke 3: full synthesis (downloads model on first run, ~1–2 GB)..."
  PYTHONPATH=. python - <<'PY'
import inference, soundfile as sf, numpy as np, sys

model = inference.load_model()
audio = inference.synthesize(
    model,
    text="नमस्ते, यह एक परीक्षण है।",
    ref_audio_path="assets/reference_audio/PAN_F_HAPPY_00001.wav",
    ref_text="ਭਹੰਪੀ ਵਿੱਚ ਸਮਾਰਕਾਂ ਦੇ ਭਵਨ ਅਤੇ ਮੰਦਰ ਹਨ।",
)
if audio is None or len(audio) == 0:
    print("[FAIL] Synthesis returned empty audio")
    sys.exit(1)
out = "/tmp/indicf5_setup_smoke.wav"
sf.write(out, audio, 24000)
duration = len(audio) / 24000
print(f"[OK]  Synthesis succeeded: {duration:.2f}s → {out}")
PY
else
  log "Smoke 3: skipped (HF_TOKEN not set — model download not attempted)."
fi

# ---------------------------------------------------------------------------
echo
echo "============================================================"
echo "  Setup complete."
echo "  Activate the environment with:"
echo "    source $VENV/bin/activate"
echo ""
echo "  Run inference from the repo root:"
echo "    PYTHONPATH=. python inference.py \"text\" \\"
echo "      --ref-audio assets/reference_audio/PAN_F_HAPPY_00001.wav \\"
echo "      --ref-text  \"<transcript of ref audio>\" \\"
echo "      --out /tmp/out.wav"
echo ""
if [ -z "${HF_TOKEN:-}" ]; then
  echo "  NOTE: Set HF_TOKEN before calling inference — the model is gated."
  echo "        Accept terms: https://huggingface.co/ai4bharat/IndicF5"
fi
echo "============================================================"
