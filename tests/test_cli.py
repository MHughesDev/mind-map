from __future__ import annotations

import json
import subprocess
from pathlib import Path


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_cli_index_query_stats(tmp_path: Path) -> None:
    root = tmp_path / "vault"
    db = tmp_path / "db"
    _write(root / "a.md", "Graph theory and eigenvalues.")
    _write(root / "folder/b.md", "Knowledge graphs and embeddings.")

    base = [
        "python3",
        "-m",
        "vault_pipeline.cli",
        "--root",
        str(root),
        "--db",
        str(db),
        "--fallback-embedder",
    ]

    index_proc = subprocess.run(
        [*base, "index"],
        check=True,
        capture_output=True,
        text=True,
    )
    index_payload = json.loads(index_proc.stdout)
    assert index_payload["files_indexed"] == 2

    stats_proc = subprocess.run(
        [*base, "stats"],
        check=True,
        capture_output=True,
        text=True,
    )
    stats_payload = json.loads(stats_proc.stdout)
    assert stats_payload["chunk_vectors"] > 0
    assert stats_payload["file_vectors"] == 2
    assert stats_payload["folder_vectors"] >= 1

    query_proc = subprocess.run(
        [*base, "query", "eigenvalue graph"],
        check=True,
        capture_output=True,
        text=True,
    )
    query_payload = json.loads(query_proc.stdout)
    assert query_payload["chunks"]
    assert query_payload["files"]
    assert query_payload["folders"]
