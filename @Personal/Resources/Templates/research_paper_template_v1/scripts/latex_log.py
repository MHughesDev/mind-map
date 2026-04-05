"""Shared LaTeX log parsing for render audit and quality gates."""

from __future__ import annotations

FINDING_ORDER = [
    ("errors", "Build Errors"),
    ("missing_files", "Missing Files"),
    ("undefined_citations", "Undefined Citations"),
    ("undefined_references", "Undefined References"),
    ("overfull_boxes", "Overfull Boxes"),
    ("underfull_boxes", "Underfull Boxes"),
    ("package_warnings", "Package Warnings"),
]


def dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def parse_log(text: str) -> dict[str, list[str]]:
    findings: dict[str, list[str]] = {
        "errors": [],
        "missing_files": [],
        "undefined_citations": [],
        "undefined_references": [],
        "overfull_boxes": [],
        "underfull_boxes": [],
        "package_warnings": [],
    }

    lines = text.splitlines()
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if "LaTeX Error: File `" in line:
            findings["missing_files"].append(line)
        elif line.startswith("! "):
            findings["errors"].append(line)
        elif "Citation `" in line and "undefined" in line:
            findings["undefined_citations"].append(line)
        elif "Reference `" in line and "undefined" in line:
            findings["undefined_references"].append(line)
        elif line.startswith("Overfull \\hbox") or line.startswith("Overfull \\vbox"):
            findings["overfull_boxes"].append(line)
        elif line.startswith("Underfull \\hbox") or line.startswith("Underfull \\vbox"):
            findings["underfull_boxes"].append(line)
        elif "Warning:" in line and line.startswith("Package "):
            findings["package_warnings"].append(line)

    for key in findings:
        findings[key] = dedupe(findings[key])
    return findings


def critical_failure(findings: dict[str, list[str]]) -> bool:
    return bool(
        findings["errors"]
        or findings["missing_files"]
        or findings["undefined_citations"]
        or findings["undefined_references"]
    )
