#!/usr/bin/env bash
# Idempotent installer for IndicF5.
# Usage: bash research/indicf5/install.sh
# NOTE: ai4bharat/IndicF5 is gated — accept terms on HF and set HF_TOKEN.
set -euo pipefail

ENV_NAME="${ENV_NAME:-tts-indicf5}"
PY_VER="${PY_VER:-3.10}"

if ! command -v ffmpeg >/dev/null 2>&1; then
  sudo apt-get update -qq && sudo apt-get install -y ffmpeg libsndfile1
fi

if ! conda env list | awk '{print $1}' | grep -qx "$ENV_NAME"; then
  conda create -n "$ENV_NAME" "python=$PY_VER" -y
fi

# shellcheck disable=SC1091
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$ENV_NAME"

pip install --upgrade pip
pip install "torch>=2.0" "torchaudio>=2.0" "numpy<=1.26.4"
pip install git+https://github.com/AI4Bharat/IndicF5.git

if [[ -n "${HF_TOKEN:-}" ]]; then
  huggingface-cli login --token "$HF_TOKEN" || true
else
  echo "[indicf5] WARN: HF_TOKEN not set; first AutoModel.from_pretrained may fail with GatedRepoError"
fi

# Pre-cache one bundled reference clip so smoke tests run offline next time.
mkdir -p research/indicf5/reference_audio
curl -fsSL -o research/indicf5/reference_audio/PAN_F_HAPPY_00001.wav \
  https://raw.githubusercontent.com/AI4Bharat/IndicF5/main/prompts/PAN_F_HAPPY_00001.wav

python - <<'PY'
import numpy as np, soundfile as sf, torch
from transformers import AutoModel

device = "cuda" if torch.cuda.is_available() else "cpu"
model = AutoModel.from_pretrained("ai4bharat/IndicF5", trust_remote_code=True).to(device).eval()
audio = model(
    "नमस्ते, यह एक परीक्षण है।",
    ref_audio_path="research/indicf5/reference_audio/PAN_F_HAPPY_00001.wav",
    # Approximate Punjabi transcript; replace with exact text once we transcribe the bundled clip.
    ref_text="ਭਹੰਪੀ ਵਿੱਚ ਸਮਾਰਕਾਂ ਦੇ ਭਵਨ ਅਤੇ ਮੰਦਰ ਹਨ।",
)
if audio.dtype == np.int16:
    audio = audio.astype(np.float32) / 32768.0
sf.write("/tmp/indicf5_smoke.wav", np.asarray(audio, dtype=np.float32).squeeze(), 24000)
print(f"[indicf5] smoke OK -> /tmp/indicf5_smoke.wav")
PY

echo "[indicf5] env '$ENV_NAME' ready"
