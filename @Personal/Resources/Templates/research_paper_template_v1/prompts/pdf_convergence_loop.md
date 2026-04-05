# PDF convergence loop (repeat until clean)

Use this after a draft compiles, or whenever `docs/PDF_REVIEW.md` still lists issues.

Automated scripts cannot guarantee pixel-perfect layout; this loop combines **log-based gates**, **full-text extraction for search**, and **direct PDF inspection** until quality targets are met.

## Exit criteria (all must be true for “render clean”)

1. `python scripts/pdf_quality_gate.py` exits **0** (no critical `main.log` issues; optional `--strict-layout` for overfull boxes).
2. `docs/PDF_REVIEW.md`: automated sections show no unresolved critical log lines; **Manual Findings** and the **Direct Visual Review Checklist** are cleared or explicitly deferred with a reason.
3. `paper/main.pdf` opened in the editor: no overlapping text, cropped figures, spilled tables, or broken equations in margins.
4. `python scripts/verify.py` exits **0** (placeholders and project checks as configured).

## Iteration (repeat until exit criteria pass)

1. Run `python scripts/build_paper.py` if the PDF is missing or sources changed materially.
2. Run `python scripts/pdf_quality_gate.py`  
   - Omit `--skip-build` for a full rebuild + `docs/PDF_TEXT_EXTRACT.md` refresh.  
   - Add `--strict-layout` when overfull boxes must block the pass.
3. Read `docs/PDF_TEXT_EXTRACT.md` for full-document text search (equations/figures may be partial).
4. Read `paper/main.pdf` directly for visual issues not visible in text extraction.
5. If figures or diagrams are involved, run `python scripts/figure_visual_audit.py` and inspect the PNGs under `audit/figure_visual/exports/`.
6. Edit LaTeX under `paper/` (and `paper/bib/` if needed). Prefer minimal fixes: line breaks, `\sloppy`/`microtype`, resizebox only when justified, fix cite keys and refs.
7. Update `docs/PDF_REVIEW.md` **Manual Findings** with what you fixed or what remains blocked.
8. If placeholders or citations are involved, run `python scripts/check_placeholders.py`, `python scripts/check_bib_placeholders.py`.
9. Go to step 1 until steps in **Exit criteria** pass.

## Fast path after a full `verify`

```text
python scripts/pdf_quality_gate.py --skip-build
```

This re-runs render audit (including full extract by default) and checks the log without rebuilding.

## When the loop must stop on content, not layout

If `PROJECT_SPEC.md` marks `[BLOCKER: ...]` or missing evidence, finish those inputs before chasing marginal overfull warnings.
