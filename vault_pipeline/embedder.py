from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol


class Embedder(Protocol):
    def encode(self, texts: list[str]) -> list[list[float]]:
        ...


@dataclass(slots=True)
class HashingEmbedder:
    """Deterministic lightweight fallback when transformer model is unavailable."""

    dims: int = 256

    def encode(self, texts: list[str]) -> list[list[float]]:
        vectors: list[list[float]] = []
        for text in texts:
            vec = [0.0] * self.dims
            for token in text.lower().split():
                idx = hash(token) % self.dims
                vec[idx] += 1.0
            norm = sum(v * v for v in vec) ** 0.5
            if norm > 0:
                vec = [v / norm for v in vec]
            vectors.append(vec)
        return vectors


class SentenceTransformerEmbedder:
    def __init__(self, model_name: str) -> None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise RuntimeError(
                "sentence-transformers is not installed. Install with: pip install sentence-transformers"
            ) from exc
        self._model = SentenceTransformer(model_name)

    def encode(self, texts: list[str]) -> list[list[float]]:
        embeddings = self._model.encode(texts, normalize_embeddings=True)
        return [list(map(float, row)) for row in embeddings]


def make_embedder(model_name: str, use_fallback: bool) -> Embedder:
    if use_fallback:
        return HashingEmbedder()
    return SentenceTransformerEmbedder(model_name)
