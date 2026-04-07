from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable


WHITESPACE_RE = re.compile(r"\s+")


@dataclass(slots=True)
class TextChunk:
    index: int
    text: str
    start_char: int
    end_char: int


def normalize_text(text: str) -> str:
    stripped = text.strip()
    return WHITESPACE_RE.sub(" ", stripped)


def chunk_text(text: str, chunk_size: int, overlap: int) -> Iterable[TextChunk]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap < 0:
        raise ValueError("overlap must be >= 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    normalized = normalize_text(text)
    if not normalized:
        return []

    chunks: list[TextChunk] = []
    start = 0
    idx = 0
    length = len(normalized)

    while start < length:
        end = min(length, start + chunk_size)
        # Try to split at nearby whitespace for better semantic chunks.
        if end < length:
            split = normalized.rfind(" ", start, end)
            if split > start + int(chunk_size * 0.5):
                end = split

        piece = normalized[start:end].strip()
        if piece:
            chunks.append(TextChunk(index=idx, text=piece, start_char=start, end_char=end))
            idx += 1

        if end >= length:
            break
        start = max(end - overlap, start + 1)

    return chunks
