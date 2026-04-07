from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Collections:
    chunks: Any
    files: Any
    folders: Any


def open_collections(db_dir: str) -> Collections:
    try:
        import chromadb
    except ImportError as exc:
        raise RuntimeError("chromadb is required. Install with: pip install chromadb") from exc

    client = chromadb.PersistentClient(path=db_dir)
    chunks = client.get_or_create_collection(
        name="vault_chunks",
        metadata={"description": "Chunk-level vectors for vault files"},
    )
    files = client.get_or_create_collection(
        name="vault_files",
        metadata={"description": "File-level summary vectors for vault files"},
    )
    folders = client.get_or_create_collection(
        name="vault_folders",
        metadata={"description": "Folder-level summary vectors for vault folders"},
    )
    return Collections(chunks=chunks, files=files, folders=folders)
