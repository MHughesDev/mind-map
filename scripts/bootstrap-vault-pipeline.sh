#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export HF_HOME="${HF_HOME:-$ROOT/.cache/huggingface}"
export TRANSFORMERS_CACHE="${TRANSFORMERS_CACHE:-$HF_HOME/hub}"
mkdir -p "$HF_HOME"
python3 -m pip install -U pip
python3 -m pip install torch --index-url https://download.pytorch.org/whl/cpu
python3 -m pip install -e ".[dev,llm]"
python3 -m vault_pipeline.cache_model
python3 -m vault_pipeline.cli --help
