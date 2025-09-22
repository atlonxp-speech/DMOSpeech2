#!/usr/bin/env bash
# download_ckpts.sh — fetch model checkpoints

set -euo pipefail
mkdir -p ckpts
cd ckpts

if [ ! -f model_85000.pt ]; then
  wget https://huggingface.co/yl4579/DMOSpeech2/resolve/main/model_85000.pt
fi
if [ ! -f model_1500.pt ]; then
  wget https://huggingface.co/yl4579/DMOSpeech2/resolve/main/model_1500.pt
fi

echo "✅ Checkpoints ready in $(pwd)"
