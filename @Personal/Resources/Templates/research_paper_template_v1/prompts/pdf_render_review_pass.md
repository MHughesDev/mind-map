Review the rendered manuscript PDF in `paper/main.pdf`.

Workflow:
1. Run `python scripts/build_paper.py` if the PDF is missing or stale.
2. Run `python scripts/render_audit.py`.
3. Read `paper/main.pdf` directly.
4. Update `docs/PDF_REVIEW.md` with page-level issues and fixes needed.
5. Update `docs/PROJECT_STATUS.md` with the current render-review state.

Focus on:
- overlapping text,
- cropped or distorted figures,
- tables spilling off the page,
- unreadable captions or labels,
- equation overflow,
- awkward whitespace or broken page breaks,
- bibliography formatting issues,
- anything visually inconsistent with the requested draft level,
- mismatch with the PDF style and typography targets in `PROJECT_SPEC.md`.

Do not claim the PDF is ready if visible render issues remain.
