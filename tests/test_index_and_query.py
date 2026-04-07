from __future__ import annotations

from pathlib import Path

from vault_pipeline.config import VaultConfig
from vault_pipeline.indexer import build_index
from vault_pipeline.retriever import search


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_index_and_query_roundtrip(tmp_path: Path) -> None:
    root = tmp_path / "vault"
    db = tmp_path / "db"
    _write(
        root / "Core Domains/Mathematics/Algebra/Linear Algebra/Eigen.md",
        "Eigenvalues and eigenvectors are central in spectral graph theory.",
    )
    _write(
        root / "Core Domains/Mathematics/Discrete Math/Graph Theory/Spectral.md",
        "The Laplacian matrix has real eigenvalues and orthogonal eigenvectors.",
    )
    _write(root / "@Personal/notes.txt", "Personal idea: connect category theory to RL.")

    cfg = VaultConfig(
        root_dir=root,
        db_dir=db,
        chunk_size=80,
        chunk_overlap=10,
        include_hidden=False,
        extensions={".md", ".txt"},
    )
    stats = build_index(cfg, use_fallback_embedder=True)
    assert stats.files_seen == 3
    assert stats.files_indexed == 3
    assert stats.chunks_indexed >= 3
    assert stats.folders_indexed >= 3

    out = search(cfg, "eigenvalue spectral graph", use_fallback_embedder=True)
    assert out["chunks"], "Expected chunk-level hits"
    assert out["files"], "Expected file-level hits"
    assert out["folders"], "Expected folder-level hits"

    top_file_paths = [row.metadata.get("path", "") for row in out["files"]]
    assert any("Eigen.md" in p or "Spectral.md" in p for p in top_file_paths)
