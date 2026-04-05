from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> int:
    result = subprocess.run(cmd, cwd=cwd)
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the paper if needed, then export figure-bearing pages as PNGs.")
    parser.add_argument("--skip-build", action="store_true", help="Skip the build step and export from the current PDF.")
    parser.add_argument("--dpi", type=int, default=180, help="Rasterization DPI.")
    parser.add_argument("--all-pages", action="store_true", help="Reserved for future use; currently exports labeled figure pages only.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    if not args.skip_build:
        code = run([sys.executable, "scripts/build_paper.py"], repo_root)
        if code != 0:
            return code

    export_cmd = [sys.executable, "scripts/export_figure_pages.py", "--dpi", str(args.dpi)]
    if args.all_pages:
        print("`--all-pages` is not yet implemented; exporting labeled figure pages only.")
    return run(export_cmd, repo_root)


if __name__ == "__main__":
    raise SystemExit(main())
