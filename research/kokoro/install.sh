#!/usr/bin/env bash
# Idempotent installer for the Kokoro v1.0 conda env.
# Usage: bash research/kokoro/install.sh
set -euo pipefail

ENV_NAME="${ENV_NAME:-tts-kokoro}"
PY_VER="${PY_VER:-3.11}"

# 1. system deps
if ! command -v espeak-ng >/dev/null 2>&1; then
  echo "[kokoro] installing espeak-ng (sudo required)"
  sudo apt-get update -qq
  sudo apt-get install -y espeak-ng libsndfile1 ffmpeg
fi

# 2. conda env
if ! conda env list | awk '{print $1}' | grep -qx "$ENV_NAME"; then
  conda create -n "$ENV_NAME" "python=$PY_VER" -y
fi

# 3. python deps inside the env
# shellcheck disable=SC1091
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$ENV_NAME"

pip install --upgrade pip
pip install "kokoro>=0.9.4" soundfile numpy

# 4. smoke test
python - <<'PY'
from kokoro import KPipeline
import numpy as np, soundfile as sf
pipe = KPipeline(lang_code='a')
audio = np.concatenate([c for _, _, c in pipe("Kokoro install smoke test.", voice="af_heart")])
sf.write("/tmp/kokoro_smoke.wav", audio, 24000)
print(f"[kokoro] smoke OK, {len(audio)/24000:.2f}s -> /tmp/kokoro_smoke.wav")
PY

echo "[kokoro] env '$ENV_NAME' ready"
