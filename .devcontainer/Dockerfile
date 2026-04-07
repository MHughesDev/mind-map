FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

# Persist Hugging Face downloads in the image layer for faster cold starts.
ENV HF_HOME=/opt/hf-cache
ENV TRANSFORMERS_CACHE=${HF_HOME}/hub

COPY pyproject.toml /tmp/vault-pipeline/
COPY vault_pipeline /tmp/vault-pipeline/vault_pipeline
WORKDIR /tmp/vault-pipeline

# CPU-only PyTorch keeps the image smaller than default CUDA wheels from PyPI.
RUN pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -e ".[dev,llm]" \
    && python -m vault_pipeline.cache_model \
    && rm -rf /tmp/vault-pipeline
