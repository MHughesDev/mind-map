from __future__ import annotations

import argparse
import re
from pathlib import Path


INPUT_RE = re.compile(r"\\input\{([^}]+)\}")


def normalize_tex_path(raw: str) -> str:
    path = raw.strip()
    if not path.endswith(".tex"):
        path += ".tex"
    return path.replace("/", "\\")


def collect_inputs(tex_path: Path, paper_root: Path, seen: set[Path]) -> set[Path]:
    if tex_path in seen or not tex_path.exists():
        return seen
    seen.add(tex_path)
    text = tex_path.read_text(encoding="utf-8", errors="replace")
    for raw in INPUT_RE.findall(text):
        candidate = (paper_root / normalize_tex_path(raw)).resolve()
        collect_inputs(candidate, paper_root, seen)
    return seen


def classify_tex_files(paper_root: Path, active: set[Path]) -> tuple[list[Path], list[Path]]:
    tex_files = sorted(path.resolve() for path in paper_root.rglob("*.tex"))
    active_sorted = [path for path in tex_files if path in active]
    inactive_sorted = [path for path in tex_files if path not in active]
    return active_sorted, inactive_sorted


def write_reports(active_files: list[Path], inactive_files: list[Path], repo_root: Path) -> None:
    docs = repo_root / "docs"
    docs.mkdir(parents=True, exist_ok=True)

    active_lines = [
        "# Active Manuscript Files",
        "",
        "These files are currently reachable from `paper/main.tex` via `\\input{...}`.",
        "",
    ]
    for path in active_files:
        active_lines.append(f"- `{path.relative_to(repo_root).as_posix()}`")
    active_lines.append("")
    (docs / "ACTIVE_MANUSCRIPT_FILES.md").write_text("\n".join(active_lines), encoding="utf-8")

    inactive_lines = [
        "# Legacy Manuscript Files",
        "",
        "These `.tex` files exist under `paper/` but are not currently reachable from `paper/main.tex`.",
        "",
        "Review them before using them as source-of-truth. They may be legacy, archived, or inactive scaffolds.",
        "",
    ]
    for path in inactive_files:
        inactive_lines.append(f"- `{path.relative_to(repo_root).as_posix()}`")
    inactive_lines.append("")
    (docs / "LEGACY_MANUSCRIPT_FILES.md").write_text("\n".join(inactive_lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Map active manuscript files and list inactive legacy .tex files.")
    parser.add_argument("--main", default="paper/main.tex", help="Main LaTeX entrypoint.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    main_tex = (repo_root / args.main).resolve()
    paper_root = main_tex.parent
    if not main_tex.exists():
        print(f"Main manuscript not found: {main_tex}")
        return 1

    active = collect_inputs(main_tex, paper_root, set())
    active_files, inactive_files = classify_tex_files(paper_root, active)
    write_reports(active_files, inactive_files, repo_root)
    print(f"Mapped {len(active_files)} active and {len(inactive_files)} inactive manuscript files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
