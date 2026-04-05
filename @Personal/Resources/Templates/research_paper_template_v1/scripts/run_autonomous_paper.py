from __future__ import annotations

import argparse
import json
from pathlib import Path

from autopaper.pipeline import AutonomousPaperRunner


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the autonomous paper pipeline from PROJECT_SPEC.md.")
    parser.add_argument("--spec", default="PROJECT_SPEC.md", help="Path to the controlling spec file.")
    parser.add_argument("--dry-run", action="store_true", help="Parse, audit, ingest, and generate without building the PDF.")
    parser.add_argument("--skip-build", action="store_true", help="Generate outputs but skip LaTeX build and audits.")
    parser.add_argument("--summary-output", default="build/autonomous_run_summary.json", help="Where to write the JSON run summary.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    runner = AutonomousPaperRunner(repo_root=repo_root, spec_path=(repo_root / args.spec).resolve())
    result = runner.run(dry_run=args.dry_run, skip_build=args.skip_build)

    summary_path = (repo_root / args.summary_output).resolve()
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(f"Wrote autonomous run summary to {summary_path}")
    print(f"Spec findings: {len(result['findings'])}")
    print(f"Generated files: {len(result['generated_files'])}")
    if result["failure_classes"]:
        print("Build failure classes:", ", ".join(result["failure_classes"]))
    return 1 if any(item["severity"] == "error" for item in result["findings"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
