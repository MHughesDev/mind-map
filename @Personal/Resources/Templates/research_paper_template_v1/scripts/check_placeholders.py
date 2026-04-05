from __future__ import annotations

import sys
from pathlib import Path

DEFAULT_ROOTS = ["paper"]
ALL_ROOTS = ["paper", "docs", "templates"]
TOKENS = [
    "[PLACEHOLDER",
    "[BLOCKER",
    "[NEEDS_CITATION",
    "[NEEDS_PROOF",
    "[NEEDS_RESULT",
    "[OPTIONAL_LATER",
    "TODO:",
    "UNVERIFIED",
]

def main():
    hits = []
    roots = ALL_ROOTS if "--all" in sys.argv[1:] else DEFAULT_ROOTS
    for root in roots:
        base = Path(root)
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file():
                try:
                    text = path.read_text(encoding="utf-8")
                except Exception:
                    continue
                for token in TOKENS:
                    if token in text:
                        for idx, line in enumerate(text.splitlines(), start=1):
                            if token in line:
                                hits.append((str(path), idx, line.strip()))
    if hits:
        print("Placeholder / TODO hits found:")
        for path, line_no, line in hits:
            print(f"{path}:{line_no}: {line}")
    else:
        print("No placeholder tokens found.")

if __name__ == "__main__":
    main()
