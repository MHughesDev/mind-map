from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .config import DEFAULT_TEXT_EXTENSIONS, VaultConfig
from .indexer import build_index
from .retriever import search
from .vector_store import open_collections


def _build_config(args: argparse.Namespace) -> VaultConfig:
    exts = set(DEFAULT_TEXT_EXTENSIONS)
    if args.extensions:
        exts = {e.strip() for e in args.extensions.split(",") if e.strip()}
    return VaultConfig(
        root_dir=Path(args.root),
        db_dir=Path(args.db),
        embedding_model=args.embedding_model,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        include_hidden=args.include_hidden,
        extensions=exts,
    )


def _cmd_index(args: argparse.Namespace) -> int:
    cfg = _build_config(args)
    stats = build_index(cfg, use_fallback_embedder=args.fallback_embedder)
    print(
        json.dumps(
            {
                "root": str(cfg.root_dir.resolve()),
                "db": str(cfg.db_dir.resolve()),
                "files_seen": stats.files_seen,
                "files_indexed": stats.files_indexed,
                "chunks_indexed": stats.chunks_indexed,
                "folders_indexed": stats.folders_indexed,
                "fallback_embedder": args.fallback_embedder,
            },
            indent=2,
        )
    )
    return 0


def _cmd_query(args: argparse.Namespace) -> int:
    cfg = _build_config(args)
    out = search(
        config=cfg,
        query=args.query,
        top_k_chunks=args.top_k_chunks,
        top_k_files=args.top_k_files,
        top_k_folders=args.top_k_folders,
        use_fallback_embedder=args.fallback_embedder,
    )
    payload: dict[str, list[dict[str, Any]]] = {}
    for level, rows in out.items():
        payload[level] = [
            {
                "id": row.id,
                "score": round(row.score, 6),
                "metadata": row.metadata,
                "document_preview": row.document[: args.preview_chars],
            }
            for row in rows
        ]
    print(json.dumps(payload, indent=2))
    return 0


def _cmd_stats(args: argparse.Namespace) -> int:
    cfg = _build_config(args)
    collections = open_collections(str(cfg.db_dir.resolve()))
    print(
        json.dumps(
            {
                "root": str(cfg.root_dir.resolve()),
                "db": str(cfg.db_dir.resolve()),
                "chunk_vectors": collections.chunks.count(),
                "file_vectors": collections.files.count(),
                "folder_vectors": collections.folders.count(),
            },
            indent=2,
        )
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Vault vector pipeline CLI")
    parser.add_argument("--root", default=".", help="Vault root directory to index")
    parser.add_argument("--db", default=".vault_index/chroma", help="Persistent vector DB directory")
    parser.add_argument(
        "--embedding-model",
        default="sentence-transformers/all-MiniLM-L6-v2",
        help="Embedding model name for sentence-transformers",
    )
    parser.add_argument("--chunk-size", type=int, default=800, help="Chunk size in characters")
    parser.add_argument("--chunk-overlap", type=int, default=120, help="Chunk overlap in characters")
    parser.add_argument(
        "--extensions",
        default="",
        help="Comma-separated file extensions to index (default indexes common text/code/md types)",
    )
    parser.add_argument("--include-hidden", action="store_true", help="Include hidden files/folders")
    parser.add_argument(
        "--fallback-embedder",
        action="store_true",
        help="Use deterministic hashing embedder (no transformer model required)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_index = sub.add_parser("index", help="Build or update vault index")
    p_index.set_defaults(func=_cmd_index)

    p_query = sub.add_parser("query", help="Query chunks/files/folders by semantic similarity")
    p_query.add_argument("query", help="Semantic query string")
    p_query.add_argument("--top-k-chunks", type=int, default=8)
    p_query.add_argument("--top-k-files", type=int, default=4)
    p_query.add_argument("--top-k-folders", type=int, default=3)
    p_query.add_argument("--preview-chars", type=int, default=240)
    p_query.set_defaults(func=_cmd_query)

    p_stats = sub.add_parser("stats", help="Report vector counts in all collections")
    p_stats.set_defaults(func=_cmd_stats)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

