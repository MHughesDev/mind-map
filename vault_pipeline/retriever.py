from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .config import VaultConfig
from .embedder import make_embedder
from .vector_store import open_collections


@dataclass(slots=True)
class SearchResult:
    level: str
    id: str
    score: float
    document: str
    metadata: dict[str, Any]


def _query_collection(collection: Any, query_embedding: list[float], top_k: int) -> list[SearchResult]:
    out = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["distances", "documents", "metadatas"],
    )
    ids = out.get("ids", [[]])[0]
    distances = out.get("distances", [[]])[0]
    docs = out.get("documents", [[]])[0]
    metas = out.get("metadatas", [[]])[0]

    results: list[SearchResult] = []
    for rid, dist, doc, meta in zip(ids, distances, docs, metas):
        # For cosine/L2 style distances lower is better; convert to score.
        score = 1.0 / (1.0 + float(dist))
        level = str(meta.get("level", "unknown")) if isinstance(meta, dict) else "unknown"
        results.append(
            SearchResult(
                level=level,
                id=rid,
                score=score,
                document=doc or "",
                metadata=meta or {},
            )
        )
    return results


def search(
    config: VaultConfig,
    query: str,
    top_k_chunks: int = 8,
    top_k_files: int = 4,
    top_k_folders: int = 3,
    use_fallback_embedder: bool = False,
) -> dict[str, list[SearchResult]]:
    cfg = config.normalize()
    collections = open_collections(str(cfg.db_dir))
    embedder = make_embedder(cfg.embedding_model, use_fallback_embedder)
    query_vec = embedder.encode([query])[0]

    return {
        "chunks": _query_collection(collections.chunks, query_vec, top_k_chunks),
        "files": _query_collection(collections.files, query_vec, top_k_files),
        "folders": _query_collection(collections.folders, query_vec, top_k_folders),
    }
