# Front-to-End Workflow

This repository uses `PROJECT_SPEC.md` as the single controlling brief for future research-paper projects.

## Phase 1 — Human Spec Fill

1. Fill `PROJECT_SPEC.md`.
2. Prioritize Section 0, Section 3, Section 4, Section 6, Section 8, Section 9, Section 11, and Section 12 if time is limited.
3. Define figures inside the detailed figure-spec layer in `PROJECT_SPEC.md` before asking the agent to render or scaffold them.
4. Define per-figure audit criteria in `PROJECT_SPEC.md` so the agent knows what visual defects count as blockers.
5. Mark unknowns explicitly as `UNKNOWN`, `N/A`, or with the unresolved markers required by the spec.
6. Add only authorized source materials to the repository.
7. Use `templates/quick_spec_short_form.md` only as a fast-fill helper, then merge the answers back into `PROJECT_SPEC.md`.

## Phase 2 — Agent Planning

Ask the agent to:
- read `PROJECT_SPEC.md` first,
- extract the execution model from Section 0,
- summarize objective, constraints, deliverables, and blockers,
- identify missing inputs and stop conditions,
- propose a file-by-file execution plan.

Recommended prompt: `prompts/launch_cursor_agent.md`

## Phase 3 — Project Scaffolding

The agent should:
- scaffold or revise the LaTeX project under `paper/`,
- align section files with the Section 8 blueprint,
- treat the detailed figure-spec layer in `PROJECT_SPEC.md` as the only conceptual figure source,
- wire notation, theorem setup, bibliography, appendix, and optional sections consistently,
- keep all unknowns explicit,
- update workflow and status files under `docs/`.

## Phase 4 — Grounded Drafting

The agent should draft only from:
- the research content bank in Section 3,
- authorized source materials from Section 4,
- claim, citation, theorem, proof, and result constraints from Sections 5, 6, 9, and 11,
- style and PDF targets from Sections 7, 12, and 13.

If information is missing, the agent should preserve the gap instead of guessing.

## Phase 5 — Build And Render Review

Once the manuscript matches the requested draft level closely enough to compile, the agent should:
- run `python scripts/build_paper.py` or `make build`,
- run `python scripts/render_audit.py --write-full-extract` or `make render-audit-full` so `docs/PDF_TEXT_EXTRACT.md` is refreshed for full-document text search (gitignored locally; requires `pypdf` or `pdftotext` for best results),
- read `paper/main.pdf` directly (required for true layout QA),
- run `python scripts/figure_visual_audit.py` during figure-sensitive passes to export figure-bearing pages as PNGs,
- optionally run `python scripts/pdf_quality_gate.py` to fail fast on critical `main.log` issues,
- record layout, visual, notation, and bibliography issues in `docs/PDF_REVIEW.md`,
- update `docs/BUILD_STATUS.md` and `docs/PROJECT_STATUS.md`.

Optional prompts: `prompts/pdf_render_review_pass.md`, `prompts/pdf_convergence_loop.md`

## Phase 5b — Convergence Loop (repeat until clean)

Scripts cannot prove pixel-perfect PDFs. Until exit criteria in `prompts/pdf_convergence_loop.md` are met, iterate: fix LaTeX -> rebuild -> `render_audit.py --write-full-extract` -> re-read PDF -> export figure pages when relevant -> clear `docs/PDF_REVIEW.md` manual items. Use `python scripts/pdf_quality_gate.py --strict-layout` when overfull boxes must block the pass.

Fast check after a full local verify: `python scripts/pdf_quality_gate.py --skip-build` or `make verify-gate`.

## Phase 6 — Audit

Run:
- `python scripts/check_placeholders.py`
- `python scripts/check_bib_placeholders.py`
- `python scripts/project_audit.py`

Or run `python scripts/verify.py` / `make verify` to chain build, render audit, and these checks.

## Phase 7 — Specialized Passes

Use:
- `prompts/reviewer_pass.md` for critical manuscript review,
- `prompts/citation_audit_pass.md` for citation integrity and section-specific citation checks,
- `prompts/revision_pass.md` for structure, clarity, and overclaiming fixes.

## Phase 8 — Submission Prep

Complete:
- `docs/SUBMISSION_CHECKLIST.md`
- final placeholder sweep
- final citation verification
- final PDF render review
- final formatting pass against the target style requirements in `PROJECT_SPEC.md`
