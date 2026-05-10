#!/usr/bin/env bash
# Idempotent installer for SPRINGLab F5-Hindi-24kHz.
# Usage: bash research/springlab_f5/install.sh
set -euo pipefail

ENV_NAME="${ENV_NAME:-tts-springlab-f5}"
PY_VER="${PY_VER:-3.11}"
TORCH_INDEX="${TORCH_INDEX:-https://download.pytorch.org/whl/cu124}"
CKPT_DIR="${CKPT_DIR:-$PWD/ckpts/F5-Hindi-24KHz}"

if ! conda env list | awk '{print $1}' | grep -qx "$ENV_NAME"; then
  conda create -n "$ENV_NAME" "python=$PY_VER" -y
fi

# shellcheck disable=SC1091
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$ENV_NAME"

conda install -c conda-forge ffmpeg -y || true
pip install --upgrade pip
pip install "torch==2.4.1" "torchaudio==2.4.1" --extra-index-url "$TORCH_INDEX" || pip install "torch>=2.4" torchaudio
pip install f5-tts huggingface_hub

mkdir -p "$CKPT_DIR"
huggingface-cli download SPRINGLab/F5-Hindi-24KHz \
  model_2500000.safetensors vocab.txt \
  samples/output1.wav samples/output2.wav samples/output3.wav \
  --local-dir "$CKPT_DIR" --local-dir-use-symlinks False

python - <<PY
from f5_tts.api import F5TTS
import os
ckpt  = os.path.join("$CKPT_DIR", "model_2500000.safetensors")
vocab = os.path.join("$CKPT_DIR", "vocab.txt")
ref   = os.path.join("$CKPT_DIR", "samples", "output1.wav")
tts = F5TTS(model="F5TTS_Base", ckpt_file=ckpt, vocab_file=vocab, use_ema=True, device="cuda")
wav, sr, _ = tts.infer(
    ref_file=ref,
    ref_text="शिवगढ़ी गाँव, एक बड़ा गाँव था",
    gen_text="नमस्ते, यह एक परीक्षण है।",
    nfe_step=32, cfg_strength=2.0, sway_sampling_coef=-1.0, speed=1.0,
    remove_silence=True, seed=42, file_wave="/tmp/springlab_f5_smoke.wav",
)
print(f"[springlab_f5] smoke OK, sr={sr} -> /tmp/springlab_f5_smoke.wav")
PY

echo "[springlab_f5] env '$ENV_NAME' ready (ckpts in $CKPT_DIR)"
