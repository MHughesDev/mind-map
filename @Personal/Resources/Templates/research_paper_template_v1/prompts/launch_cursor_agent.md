Execute this project. Follow the instructions strictly. Do not ask questions unless required by `PROJECT_SPEC.md`. Begin by generating a plan, then proceed to implementation.

Read `PROJECT_SPEC.md` first and treat it as the controlling specification.

Extract and respect:
- the execution model in Section 0,
- the research content bank in Section 3,
- the source priority and conflict rules in Section 4,
- the claim and evidence map in Section 5,
- the citation policy in Section 6,
- the section blueprint in Section 8,
- the mathematical and proof controls in Section 9,
- the evaluation limits in Section 11,
- the figure/table/PDF-style requirements in Sections 12 and 13,
- and the detailed figure-spec layer as the only conceptual source for figures.

Then do the following in order:

1. Summarize the paper objective, deliverables, constraints, blockers, and missing inputs.
2. Create a file-by-file execution plan.
3. Update `docs/PROJECT_STATUS.md` with the current objective and planned phase.
4. Update `docs/MISSING_INPUTS.md` with blockers and unresolved citation/proof/result gaps.
5. Build or revise the LaTeX project under `paper/`.
6. Preserve all unknowns explicitly with the strongest available unresolved marker.
7. If a figure is needed, derive it only from the matching detailed figure-spec entry in `PROJECT_SPEC.md` or leave a placeholder.
8. When the draft is ready enough to compile, run:
   - `python scripts/build_paper.py`
   - `python scripts/render_audit.py --write-full-extract` (refreshes `docs/PDF_TEXT_EXTRACT.md` for full-text search; optional if the environment lacks PDF text tools)
   - `python scripts/pdf_quality_gate.py --skip-build` (optional pass/fail check on `paper/main.log` after the above)
9. Read `paper/main.pdf` directly and cross-check `docs/PDF_TEXT_EXTRACT.md` when present; record layout, style-target, notation, and rendering problems in `docs/PDF_REVIEW.md`. If issues remain, follow `prompts/pdf_convergence_loop.md` and repeat until exit criteria there are satisfied or blockers are explicit.
10. Run:
   - `python scripts/check_placeholders.py`
   - `python scripts/check_bib_placeholders.py`
   - `python scripts/project_audit.py`
11. Report:
   - files changed
   - sections drafted or revised
   - build/render issues found
   - blockers remaining
   - unresolved placeholders by severity
   - missing inputs still needed
   - recommended next action

Non-negotiable:
- do not invent citations, experiments, results, proofs, numbers, venue rules, or affiliations
- do not invent figure structure outside `PROJECT_SPEC.md`
- do not treat legacy spec files as co-equal sources of truth
- do not claim completion if placeholders or blockers remain
