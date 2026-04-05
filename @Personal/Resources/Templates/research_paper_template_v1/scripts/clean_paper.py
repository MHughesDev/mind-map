from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER_DIR = ROOT / "paper"

PATTERNS = [
    "*.aux",
    "*.bbl",
    "*.blg",
    "*.fdb_latexmk",
    "*.fls",
    "*.log",
    "*.out",
    "*.pdf",
    "*.toc",
    "*.synctex.gz",
]


def main() -> int:
    removed = 0
    for pattern in PATTERNS:
        for path in PAPER_DIR.glob(pattern):
            if path.is_file():
                path.unlink()
                removed += 1
    print(f"Removed {removed} generated file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
