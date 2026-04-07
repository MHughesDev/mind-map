from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .chunking import chunk_text
from .config import VaultConfig
from .embedder import make_embedder
from .io_utils import read_text_file, relative_path
from .vector_store import open_collections


@dataclass(slots=True)
class IndexStats:
    files_seen: int
    files_indexed: int
    chunks_indexed: int
    folders_indexed: int


def _folder_candidates(paths: Iterable[Path], root: Path) -> dict[str, list[str]]:
    folder_to_texts: dict[str, list[str]] = {}
    for p in paths:
        rel = p.resolve().relative_to(root.resolve())
        parts = rel.parts[:-1]
        content = read_text_file(p).strip()
        if not content:
            continue
        for i in range(1, len(parts) + 1):
            folder = str(Path(*parts[:i]))
            folder_to_texts.setdefault(folder, []).append(content[:600])
        # Index the vault root as a folder-level semantic anchor.
        folder_to_texts.setdefault(".", []).append(content[:600])
    return folder_to_texts


def build_index(config: VaultConfig, use_fallback_embedder: bool = False) -> IndexStats:
    cfg = config.normalize()
    cfg.db_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(cfg.iter_indexable_files())
    folders = _folder_candidates(files, cfg.root_dir)
    collections = open_collections(str(cfg.db_dir))
    embedder = make_embedder(cfg.embedding_model, use_fallback_embedder)

    chunk_ids: list[str] = []
    chunk_docs: list[str] = []
    chunk_meta: list[dict[str, str | int]] = []

    file_ids: list[str] = []
    file_docs: list[str] = []
    file_meta: list[dict[str, str | int]] = []

    for f in files:
        rel = relative_path(f, cfg.root_dir)
        text = read_text_file(f)
        chunks = list(chunk_text(text, chunk_size=cfg.chunk_size, overlap=cfg.chunk_overlap))
        if not chunks:
            continue

        for ch in chunks:
            cid = f"{rel}::chunk::{ch.index}"
            chunk_ids.append(cid)
            chunk_docs.append(ch.text)
            chunk_meta.append(
                {
                    "level": "chunk",
                    "path": rel,
                    "chunk_index": ch.index,
                    "start_char": ch.start_char,
                    "end_char": ch.end_char,
                    "ext": f.suffix.lower(),
                    "folder": str(Path(rel).parent),
                }
            )

        joined = " ".join(ch.text for ch in chunks[:10])
        file_ids.append(f"{rel}::file")
        file_docs.append(joined)
        file_meta.append(
            {
                "level": "file",
                "path": rel,
                "ext": f.suffix.lower(),
                "chunk_count": len(chunks),
                "folder": str(Path(rel).parent),
            }
        )

    folder_ids: list[str] = []
    folder_docs: list[str] = []
    folder_meta: list[dict[str, str | int]] = []
    for folder, texts in folders.items():
        folder_ids.append(f"{folder}::folder")
        folder_docs.append(" ".join(texts[:20]))
        folder_meta.append({"level": "folder", "path": folder, "file_count_hint": len(texts)})

    if chunk_docs:
        chunk_embeddings = embedder.encode(chunk_docs)
        collections.chunks.upsert(
            ids=chunk_ids,
            embeddings=chunk_embeddings,
            documents=chunk_docs,
            metadatas=chunk_meta,
        )
    if file_docs:
        file_embeddings = embedder.encode(file_docs)
        collections.files.upsert(
            ids=file_ids,
            embeddings=file_embeddings,
            documents=file_docs,
            metadatas=file_meta,
        )
    if folder_docs:
        folder_embeddings = embedder.encode(folder_docs)
        collections.folders.upsert(
            ids=folder_ids,
            embeddings=folder_embeddings,
            documents=folder_docs,
            metadatas=folder_meta,
        )

    return IndexStats(
        files_seen=len(files),
        files_indexed=len(file_docs),
        chunks_indexed=len(chunk_docs),
        folders_indexed=len(folder_docs),
    )
