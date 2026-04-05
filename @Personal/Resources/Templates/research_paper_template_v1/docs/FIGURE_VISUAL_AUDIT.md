# Figure Visual Audit

This workflow lets an agent audit figure layout without relying on a human to open the PDF.

It is meant for the late-stage loop:

`build -> export figure pages -> inspect PNGs -> edit figure source -> rebuild -> repeat`

## Purpose

Text extraction and log checks do not reliably catch:
- label collisions
- arrow/text overlap
- node/text overlap
- cramped legends
- dashed boxes striking through labels
- subtle crowding inside TikZ figures

For figure-heavy papers, rendered page images are required for release-quality review.

## Files

- `audit/figure_visual/manifest.json`
- `audit/figure_visual/exports/`
- `audit/figure_visual/LAST_EXPORT.md`
- `scripts/export_figure_pages.py`
- `scripts/figure_visual_audit.py`
- `prompts/figure_visual_audit_loop.md`

## Dependency

Install:

```text
pip install -r requirements-figure-audit.txt
```

PyMuPDF is used to rasterize the figure-bearing pages.

## How It Works

1. `scripts/export_figure_pages.py` reads `paper/main.aux` and extracts figure labels with page numbers.
2. It rasterizes those pages from `paper/main.pdf` into `audit/figure_visual/exports/page-NNN.png`.
3. `scripts/figure_visual_audit.py` optionally builds first, then exports, then writes `audit/figure_visual/LAST_EXPORT.md`.
4. The agent opens the PNGs directly in the editor and compares them against the figure audit criteria declared in `PROJECT_SPEC.md`.

## Limits

- This is visual inspection, not automatic overlap detection.
- Page numbers can change when floats move, so export must be re-run after layout shifts.
- The PNG export is only as current as the latest successful build.
- If a figure has no `fig:` label in the LaTeX source, it may not be exported automatically.

## Required Agent Behavior

During figure-only passes and final PDF convergence:
- do not rely on source code alone for figure quality
- inspect the exported PNGs
- compare each figure against its audit criteria in `PROJECT_SPEC.md`
- make only scoped figure/layout edits
- re-export after each material fix
