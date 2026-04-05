# Figure Visual Audit

This folder supports a closed visual audit loop for figures:

1. build the paper
2. export figure-bearing pages as PNGs
3. inspect the PNGs
4. edit figure source files
5. rebuild and repeat

Key files:
- `manifest.json`: optional figure-label to source-file mapping
- `exports/`: generated `page-NNN.png` files
- `LAST_EXPORT.md`: last exported labels, pages, and image paths

Typical commands:

```text
python scripts/figure_visual_audit.py
python scripts/figure_visual_audit.py --skip-build
python scripts/export_figure_pages.py
```
