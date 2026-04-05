from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    manifest_path = repo_root / "build/figure_specs.json"
    review_path = repo_root / "docs/FIGURE_AUDIT.md"
    review_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Figure Audit",
        "",
        "This file records structured checks for figure readiness and figure-spec completeness.",
        "",
    ]
    if not manifest_path.exists():
        lines.extend(["- No figure manifest was found. Run `python scripts/generate_from_spec.py` first.", ""])
        review_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        print("Figure manifest not found.")
        return 1

    figures = json.loads(manifest_path.read_text(encoding="utf-8"))
    unresolved = 0
    if not figures:
        lines.extend(["- No figures were parsed from the spec.", ""])
    for figure in figures:
        missing_fields = [
            field
            for field in (
                "Structural Description",
                "Semantic Mapping",
                "Layout Constraints",
                "Mathematical Correspondence",
                "Rendering Instructions",
                "Caption Requirements",
                "Audit Criteria",
            )
            if not figure.get("detailed_fields", {}).get(field, "").strip()
        ]
        lines.extend([f"## {figure.get('id', 'unknown')}", "", f"- Title: `{figure.get('title', 'untitled')}`"])
        if missing_fields:
            unresolved += 1
            lines.append(f"- Missing detailed fields: {', '.join(missing_fields)}")
        else:
            lines.append("- Detailed specification appears complete.")
        lines.append("")

    lines.extend(
        [
            "## Summary",
            "",
            f"- Total figures: `{len(figures)}`",
            f"- Incomplete figures: `{unresolved}`",
            "",
        ]
    )
    review_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote figure audit to {review_path}")
    return 0 if unresolved == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
