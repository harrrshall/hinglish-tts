#!/usr/bin/env bash
# Idempotent installer for the Indic Parler-TTS conda env.
# Usage: bash research/indic_parler/install.sh
set -euo pipefail

ENV_NAME="${ENV_NAME:-tts-indic-parler}"
PY_VER="${PY_VER:-3.11}"
TORCH_INDEX="${TORCH_INDEX:-https://download.pytorch.org/whl/cu121}"

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
pip install "torch>=2.1" --index-url "$TORCH_INDEX" || pip install "torch>=2.1"
pip install git+https://github.com/huggingface/parler-tts.git
pip install "transformers>=4.46,<4.50" soundfile sentencepiece accelerate descript-audio-codec

python - <<'PY'
import torch, soundfile as sf
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
MODEL_ID = "ai4bharat/indic-parler-tts"
device = "cuda:0" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device.startswith("cuda") else torch.float32
model = ParlerTTSForConditionalGeneration.from_pretrained(MODEL_ID, torch_dtype=dtype).to(device)
ptok = AutoTokenizer.from_pretrained(MODEL_ID)
dtok = AutoTokenizer.from_pretrained(model.config.text_encoder._name_or_path)
desc = dtok("Rohit speaks at a moderate pace, very clear audio.", return_tensors="pt").to(device)
txt  = ptok("This is a smoke test.", return_tensors="pt").to(device)
with torch.inference_mode():
    gen = model.generate(input_ids=desc.input_ids, attention_mask=desc.attention_mask,
                         prompt_input_ids=txt.input_ids, prompt_attention_mask=txt.attention_mask,
                         do_sample=True, temperature=1.0, repetition_penalty=1.1)
audio = gen.cpu().to(torch.float32).numpy().squeeze()
sf.write("/tmp/indic_parler_smoke.wav", audio, model.config.sampling_rate)
print(f"[indic_parler] smoke OK, {len(audio)/model.config.sampling_rate:.2f}s -> /tmp/indic_parler_smoke.wav")
PY

echo "[indic_parler] env '$ENV_NAME' ready"
