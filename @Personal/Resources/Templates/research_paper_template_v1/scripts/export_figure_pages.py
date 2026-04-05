from __future__ import annotations

import argparse
import re
from pathlib import Path


NEWLABEL_RE = re.compile(r"\\newlabel\{(?P<label>fig:[^}]+)\}\{\{[^}]*\}\{(?P<page>\d+)\}")


def parse_aux(aux_path: Path) -> list[tuple[str, int]]:
    labels: list[tuple[str, int]] = []
    for line in aux_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        match = NEWLABEL_RE.search(line)
        if match:
            labels.append((match.group("label"), int(match.group("page"))))
    seen: set[tuple[str, int]] = set()
    deduped: list[tuple[str, int]] = []
    for item in labels:
        if item not in seen:
            seen.add(item)
            deduped.append(item)
    return deduped


def export_pages(pdf_path: Path, exports_dir: Path, labels: list[tuple[str, int]], dpi: int) -> list[Path]:
    try:
        import fitz
    except ImportError as exc:
        raise SystemExit(
            "PyMuPDF is required. Install it with `pip install -r requirements-figure-audit.txt`."
        ) from exc

    pdf = fitz.open(pdf_path)
    exports_dir.mkdir(parents=True, exist_ok=True)
    scale = dpi / 72.0
    written: list[Path] = []
    pages = sorted({page for _, page in labels})
    for page_num in pages:
        if page_num < 1 or page_num > len(pdf):
            continue
        page = pdf[page_num - 1]
        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
        output_path = exports_dir / f"page-{page_num:03d}.png"
        pix.save(output_path)
        written.append(output_path)
    return written


def write_last_export(output_path: Path, labels: list[tuple[str, int]], written: list[Path]) -> None:
    lines = [
        "# Last Figure Export",
        "",
        "## Labels",
        "",
    ]
    if not labels:
        lines.extend(["- No `fig:` labels were found in `paper/main.aux`.", ""])
    else:
        for label, page in labels:
            lines.append(f"- `{label}` -> page `{page}`")
        lines.append("")

    lines.extend(["## PNGs", ""])
    if not written:
        lines.extend(["- No page images were written.", ""])
    else:
        for path in written:
            lines.append(f"- `{path.as_posix()}`")
        lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Export figure-bearing PDF pages as PNGs using LaTeX figure labels.")
    parser.add_argument("--aux", default="paper/main.aux", help="Path to the LaTeX aux file.")
    parser.add_argument("--pdf", default="paper/main.pdf", help="Path to the built PDF.")
    parser.add_argument("--exports-dir", default="audit/figure_visual/exports", help="Directory for PNG exports.")
    parser.add_argument("--last-export", default="audit/figure_visual/LAST_EXPORT.md", help="Where to write export metadata.")
    parser.add_argument("--dpi", type=int, default=180, help="Rasterization DPI.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    aux_path = (repo_root / args.aux).resolve()
    pdf_path = (repo_root / args.pdf).resolve()
    exports_dir = (repo_root / args.exports_dir).resolve()
    last_export_path = (repo_root / args.last_export).resolve()

    if not aux_path.exists():
        print(f"AUX file not found: {aux_path}")
        return 1
    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}")
        return 1

    labels = parse_aux(aux_path)
    written = export_pages(pdf_path, exports_dir, labels, args.dpi)
    write_last_export(last_export_path, labels, written)
    print(f"Exported {len(written)} page image(s) to {exports_dir}")
    return 0 if written else 1


if __name__ == "__main__":
    raise SystemExit(main())
