from __future__ import annotations

import argparse
from pathlib import Path

from autopaper.generation import (
    build_evidence_store,
    build_figure_manifest,
    build_grounding_report,
    generate_manuscript,
    update_project_status,
)
from autopaper.spec import audit_spec, parse_spec, write_spec_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate manuscript artifacts from PROJECT_SPEC.md.")
    parser.add_argument("--spec", default="PROJECT_SPEC.md", help="Path to the controlling spec file.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    spec = parse_spec((repo_root / args.spec).resolve(), repo_root)
    findings = audit_spec(spec)
    write_spec_json(spec, repo_root / "build/spec.json")

    evidence = build_evidence_store(spec, repo_root, repo_root / "build/evidence_store.json")
    build_grounding_report(spec, evidence, repo_root / "docs/CLAIM_GROUNDING.md")
    manuscript = generate_manuscript(spec, repo_root, evidence)
    figures = build_figure_manifest(spec, repo_root)
    update_project_status(repo_root, spec, len(findings), len(evidence), manuscript, figures)

    print(f"Generated {len(manuscript.generated_files)} manuscript files.")
    print(f"Wrote {manuscript.bibliography_entries_written} bibliography entries.")
    print(f"Prepared figure manifest for {figures.figure_count} figure(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
