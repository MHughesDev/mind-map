from __future__ import annotations

from pathlib import Path


def read_text_file(path: Path) -> str:
    """Best-effort read for mixed vault text files."""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        # Fallback for legacy encodings in personal vaults.
        return path.read_text(encoding="latin-1")


def relative_path(path: Path, root: Path) -> str:
    return str(path.resolve().relative_to(root.resolve()))
