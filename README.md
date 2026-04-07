# Mind Map Vault Vector Pipeline

This repository now includes a local-first indexing and retrieval pipeline for your personal vault and research corpus.

## What it does

- Indexes all readable text-like files (including all `.md` files by default).
- Builds **chunk-level vectors** for granular retrieval.
- Builds **file-level vectors** for document context.
- Builds **folder-level vectors** (including root `.`) for high-level context routing.
- Stores vectors in a persistent local ChromaDB directory.
- Provides a CLI for indexing, querying, and index stats.

## Architecture

The pipeline implements a 3-layer semantic representation:

1. `vault_chunks` collection
   - One embedding per chunk.
   - Metadata includes source path, chunk index, char offsets, extension, folder.
2. `vault_files` collection
   - One embedding per file-level summary.
   - Metadata includes source path, extension, folder, chunk count.
3. `vault_folders` collection
   - One embedding per folder summary (aggregated from child file excerpts).
   - Includes a root folder vector at path `.`.

## Install

Use Python 3.10+.

- Core install:
  - `python3 -m pip install -e .`
- Optional LLM embeddings (recommended):
  - `python3 -m pip install -e .[llm]`
- Dev/test:
  - `python3 -m pip install -e .[dev]`

## CLI usage

Index the vault:

- `python3 -m vault_pipeline.cli --root . --db .vault_index/chroma index`

Query semantically:

- `python3 -m vault_pipeline.cli --root . --db .vault_index/chroma query "spectral graph eigenvalue methods"`

Get collection stats:

- `python3 -m vault_pipeline.cli --root . --db .vault_index/chroma stats`

### Fallback mode

If transformer embeddings are not available in the environment, use:

- `python3 -m vault_pipeline.cli --root . --db .vault_index/chroma --fallback-embedder index`

This uses a deterministic hashing embedder for local/offline smoke usage.

## Configuration knobs

- `--chunk-size` (default: `800`)
- `--chunk-overlap` (default: `120`)
- `--extensions` comma-separated list (default includes `.md`, `.txt`, `.py`, `.json`, `.yaml`, `.toml`, `.tex`, `.csv`, etc.)
- `--extensions "*"` to index all readable file extensions (still bounded by max file size and decoding)
- `--include-hidden` to include hidden paths
- `--embedding-model` to set sentence-transformers model

## Agent retrieval strategy

For your paper generator and MATH Vault workflows, use this retrieval sequence:

1. Query `vault_folders` to route to relevant domain folders.
2. Query `vault_files` in selected folders for shortlist.
3. Query `vault_chunks` on shortlisted files for exact evidence snippets.
4. Return provenance metadata (`path`, `chunk_index`, offsets) with each citation candidate.

This provides both broad context and precise supporting evidence for downstream drafting and verification agents.
