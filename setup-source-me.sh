#!/usr/bin/env bash
# setup-source-me.sh — activate uv environment for DMOSpeech2
set -euo pipefail

# Ensure we're in repo root
cd "$(dirname "${BASH_SOURCE[0]}")"

# Create the virtual environment explicitly with uv
uv venv --python 3.10 .venv

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies from requirements.txt using uv's pip compatibility
uv pip install -r requirements.txt

