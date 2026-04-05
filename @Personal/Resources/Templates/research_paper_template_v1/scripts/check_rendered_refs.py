from __future__ import annotations

import argparse
import re
from pathlib import Path


HEADING_RE = re.compile(r"^(Definition|Theorem|Lemma|Proposition|Corollary|Conjecture|Remark|Axiom)\s+([A-Z]?\d+(?:\.\d+)*)", re.MULTILINE)
REFERENCE_RE = re.compile(r"\b(Definition|Theorem|Lemma|Proposition|Corollary|Conjecture|Remark|Axiom)\s+([A-Z]?\d+(?:\.\d+)*)\b")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check rendered PDF text for suspicious theorem-like cross-reference naming.")
    parser.add_argument("--extract", default="docs/PDF_TEXT_EXTRACT.md", help="Rendered text extract to inspect.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    extract_path = (repo_root / args.extract).resolve()
    if not extract_path.exists():
        print(f"Rendered text extract not found: {extract_path}")
        return 1

    text = extract_path.read_text(encoding="utf-8", errors="replace")
    headings: dict[str, set[str]] = {}
    refs: dict[str, set[str]] = {}
    for kind, number in HEADING_RE.findall(text):
        headings.setdefault(kind, set()).add(number)
    for kind, number in REFERENCE_RE.findall(text):
        refs.setdefault(kind, set()).add(number)

    suspicious: list[str] = []
    for kind, numbers in refs.items():
        for number in sorted(numbers):
            if number not in headings.get(kind, set()):
                suspicious.append(f"{kind} {number}")

    report_path = repo_root / "docs/RENDERED_REF_AUDIT.md"
    lines = [
        "# Rendered Reference Audit",
        "",
        "This file checks rendered PDF text for suspicious theorem-like cross-reference naming.",
        "",
    ]
    if suspicious:
        lines.extend(["## Suspicious References", ""])
        for item in suspicious:
            lines.append(f"- `{item}` appears in rendered text, but no matching heading of that type was found.")
        lines.append("")
    else:
        lines.extend(["- No suspicious theorem-like rendered references detected.", ""])
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote rendered reference audit to {report_path}")
    return 1 if suspicious else 0


if __name__ == "__main__":
    raise SystemExit(main())
