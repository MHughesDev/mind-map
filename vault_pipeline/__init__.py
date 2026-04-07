"""Vault indexing and retrieval pipeline for personal research maps."""

from .config import VaultConfig
from .indexer import build_index
from .retriever import search

__all__ = ["VaultConfig", "build_index", "search"]
