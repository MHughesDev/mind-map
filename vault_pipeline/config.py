from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


DEFAULT_TEXT_EXTENSIONS = {
    ".md",
    ".txt",
    ".rst",
    ".py",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".tex",
    ".csv",
}


@dataclass(slots=True)
class VaultConfig:
    root_dir: Path
    db_dir: Path
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chunk_size: int = 800
    chunk_overlap: int = 120
    max_file_bytes: int = 2_000_000
    include_hidden: bool = False
    extensions: set[str] = field(default_factory=lambda: set(DEFAULT_TEXT_EXTENSIONS))

    def normalize(self) -> "VaultConfig":
        normalized_exts: set[str] = set()
        for ext in self.extensions:
            cleaned = ext.strip()
            if cleaned == "*":
                normalized_exts.add("*")
                continue
            normalized_exts.add(cleaned if cleaned.startswith(".") else f".{cleaned}")
        return VaultConfig(
            root_dir=self.root_dir.resolve(),
            db_dir=self.db_dir.resolve(),
            embedding_model=self.embedding_model,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            max_file_bytes=self.max_file_bytes,
            include_hidden=self.include_hidden,
            extensions=normalized_exts,
        )

    def should_index(self, path: Path) -> bool:
        if not path.is_file():
            return False
        if not self.include_hidden and any(part.startswith(".") for part in path.parts):
            return False
        if "*" not in self.extensions and path.suffix.lower() not in self.extensions:
            return False
        try:
            return path.stat().st_size <= self.max_file_bytes
        except OSError:
            return False

    def iter_indexable_files(self) -> Iterable[Path]:
        for p in self.root_dir.rglob("*"):
            if self.should_index(p):
                yield p
