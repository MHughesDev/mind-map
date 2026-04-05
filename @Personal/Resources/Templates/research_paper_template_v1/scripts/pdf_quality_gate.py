#!/usr/bin/env python3
"""Pass/fail gate after build: critical log issues optional layout strictness, refresh render audit."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from latex_log import critical_failure, parse_log  # noqa: E402

LOG_PATH = ROOT / "paper" / "main.log"
PDF_PATH = ROOT / "paper" / "main.pdf"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build (optional), run render audit with full text extract, fail on critical LaTeX log issues.",
    )
    parser.add_argument("--skip-build", action="store_true", help="Do not run scripts/build_paper.py first.")
    parser.add_argument(
        "--strict-layout",
        action="store_true",
        help="Also fail when overfull boxes are present in the log.",
    )
    parser.add_argument(
        "--no-full-extract",
        action="store_true",
        help="Do not pass --write-full-extract to render_audit (faster; less context for agents).",
    )
    parser.add_argument(
        "--preview-pages",
        type=int,
        default=2,
        help="Forwarded to render_audit --preview-pages (default: 2).",
    )
    args = parser.parse_args()

    if not args.skip_build:
        build = subprocess.run([sys.executable, str(SCRIPTS / "build_paper.py")], cwd=ROOT, check=False)
        if build.returncode != 0:
            print("pdf_quality_gate: build failed (see docs/BUILD_STATUS.md).")
            return 1

    if not PDF_PATH.exists():
        print("pdf_quality_gate: paper/main.pdf is missing after build.")
        return 1

    audit_cmd = [
        sys.executable,
        str(SCRIPTS / "render_audit.py"),
        "--preview-pages",
        str(args.preview_pages),
    ]
    if not args.no_full_extract:
        audit_cmd.append("--write-full-extract")

    audit = subprocess.run(audit_cmd, cwd=ROOT, check=False)
    if audit.returncode != 0:
        print("pdf_quality_gate: render_audit failed.")
        return 1

    rendered_ref_audit = subprocess.run([sys.executable, str(SCRIPTS / "check_rendered_refs.py")], cwd=ROOT, check=False)
    if rendered_ref_audit.returncode != 0:
        print("pdf_quality_gate: FAILED - suspicious rendered theorem-like references detected.")
        print("See docs/RENDERED_REF_AUDIT.md for details.")
        return 1

    log_text = LOG_PATH.read_text(encoding="utf-8", errors="replace") if LOG_PATH.exists() else ""
    findings = parse_log(log_text)

    if critical_failure(findings):
        print("pdf_quality_gate: FAILED — critical issues in paper/main.log (errors, missing files, or undefined cites/refs).")
        print("See docs/PDF_REVIEW.md for parsed details.")
        return 1

    if args.strict_layout and findings["overfull_boxes"]:
        print("pdf_quality_gate: FAILED — strict-layout: overfull boxes present.")
        for line in findings["overfull_boxes"][:12]:
            print(f"  {line}")
        if len(findings["overfull_boxes"]) > 12:
            print(f"  ... and {len(findings['overfull_boxes']) - 12} more")
        return 1

    print("pdf_quality_gate: PASSED — no critical log issues.")
    if findings["overfull_boxes"] and not args.strict_layout:
        print(f"  Note: {len(findings['overfull_boxes'])} overfull box warning(s); use --strict-layout to fail on these.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
