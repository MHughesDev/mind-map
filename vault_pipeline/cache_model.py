"""Pre-download sentence-transformers weights into the Hugging Face cache."""

from __future__ import annotations


def main() -> None:
    from sentence_transformers import SentenceTransformer

    SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


if __name__ == "__main__":
    main()
