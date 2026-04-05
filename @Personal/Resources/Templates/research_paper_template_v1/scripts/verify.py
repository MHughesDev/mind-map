from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_step(title: str, command: list[str]) -> int:
    print(f"==> {title}")
    completed = subprocess.run(command, cwd=ROOT, check=False)
    print()
    return completed.returncode


def main() -> int:
    all_placeholders = "--all-placeholders" in sys.argv[1:]

    steps: list[tuple[str, list[str]]] = [
        ("Build paper", [sys.executable, "scripts/build_paper.py"]),
        ("Render audit", [sys.executable, "scripts/render_audit.py"]),
        ("Placeholder audit", [sys.executable, "scripts/check_placeholders.py"]),
        ("Bibliography audit", [sys.executable, "scripts/check_bib_placeholders.py"]),
        ("Project audit", [sys.executable, "scripts/project_audit.py"]),
    ]
    if all_placeholders:
        steps[2] = (
            "Placeholder audit (all template files)",
            [sys.executable, "scripts/check_placeholders.py", "--all"],
        )

    failed = False
    for title, command in steps:
        if run_step(title, command) != 0:
            failed = True
            break

    if failed:
        print("Verification failed.")
        return 1

    print("Verification completed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
