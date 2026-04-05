from __future__ import annotations

import argparse
from pathlib import Path

from autopaper.spec import audit_spec, parse_spec, write_spec_audit_json, write_spec_audit_markdown


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit PROJECT_SPEC.md readiness for autonomous execution.")
    parser.add_argument("--spec", default="PROJECT_SPEC.md", help="Path to the controlling spec file.")
    parser.add_argument("--markdown-output", default="docs/SPEC_AUDIT.md", help="Markdown report output path.")
    parser.add_argument("--json-output", default="build/spec_audit.json", help="JSON report output path.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    spec = parse_spec((repo_root / args.spec).resolve(), repo_root)
    findings = audit_spec(spec)

    markdown_output = (repo_root / args.markdown_output).resolve()
    json_output = (repo_root / args.json_output).resolve()
    write_spec_audit_markdown(findings, markdown_output)
    write_spec_audit_json(findings, json_output)

    error_count = sum(1 for item in findings if item.severity == "error")
    warning_count = sum(1 for item in findings if item.severity == "warning")
    print(f"Wrote spec audit to {markdown_output}")
    print(f"Errors: {error_count}")
    print(f"Warnings: {warning_count}")
    return 1 if error_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
