#!/usr/bin/env bash
# Idempotent installer for Orpheus TTS (vLLM path).
# Usage: bash research/orpheus/install.sh
# NOTE: needs HF_TOKEN env var since canopylabs/orpheus-3b-0.1-ft is gated.
set -euo pipefail

ENV_NAME="${ENV_NAME:-tts-orpheus}"
PY_VER="${PY_VER:-3.10}"

if ! conda env list | awk '{print $1}' | grep -qx "$ENV_NAME"; then
  conda create -n "$ENV_NAME" "python=$PY_VER" -y
fi

# shellcheck disable=SC1091
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$ENV_NAME"

pip install --upgrade pip
pip install orpheus-speech
pip install "vllm==0.7.3"
pip install snac transformers torch torchaudio soundfile huggingface_hub

if [[ -n "${HF_TOKEN:-}" ]]; then
  huggingface-cli login --token "$HF_TOKEN" || true
else
  echo "[orpheus] WARN: HF_TOKEN not set; gated repos may fail"
fi

# Light smoke (HF transformers path, avoids vLLM startup time during install)
python - <<'PY'
import torch
from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained("canopylabs/orpheus-3b-0.1-ft")
print(f"[orpheus] tokenizer loaded, vocab_size={tok.vocab_size}")
PY

echo "[orpheus] env '$ENV_NAME' ready (run inference test separately — vLLM start is heavy)"
