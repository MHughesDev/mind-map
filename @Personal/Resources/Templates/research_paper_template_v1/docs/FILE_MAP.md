# File Map

## Root
- `README.md` — high-level overview and operating model
- `PROJECT_SPEC.md` — expanded single controlling brief
- `AGENTS.md` — repository-level agent instructions
- `Makefile` — build and audit entrypoints
- `.gitignore` — standard ignores

## `.cursor/`
- `.cursor/rules/` — persistent workflow, citation, and LaTeX rules
- `.cursor/agents/` — reusable subagent roles

## `templates/`
- `quick_spec_short_form.md` — fast-fill companion that maps back into `PROJECT_SPEC.md`
- `ai_research_paper_builder_instructions.md` — copy-paste execution instructions aligned with the new spec
- `paper_structure_spec_master.md` — deprecated legacy intake template retained for migration only

## `prompts/`
- `launch_cursor_agent.md` — main autonomous execution prompt
- `pdf_render_review_pass.md` — rendered PDF review prompt
- `pdf_convergence_loop.md` — repeat until PDF/log checks and manual review exit criteria pass
- `figure_visual_audit_loop.md` — rendered figure-page PNG audit loop
- `revision_pass.md` — revision prompt
- `reviewer_pass.md` — critical review prompt
- `citation_audit_pass.md` — citation integrity prompt

## `docs/`
- `FRONT_TO_END_WORKFLOW.md` — repository workflow from spec fill through submission prep
- `PROJECT_STATUS.md` — current objective, mode, phase, and status summary
- `BUILD_STATUS.md` — latest LaTeX build attempt and findings
- `PDF_REVIEW.md` — rendered PDF review, style drift, and layout issue log
- `PDF_TEXT_EXTRACT.md` — generated full-text extract (local only; gitignored) from `render_audit.py --write-full-extract`
- `FIGURE_VISUAL_AUDIT.md` — figure PNG export workflow and limits
- `ACTIVE_MANUSCRIPT_FILES.md` — files reachable from `paper/main.tex`
- `LEGACY_MANUSCRIPT_FILES.md` — inactive `.tex` files still present under `paper/`
- `RENDERED_REF_AUDIT.md` — rendered theorem-like cross-reference naming audit
- `MISSING_INPUTS.md` — blockers and unresolved citation/proof/result inputs
- `DECISIONS_LOG.md` — source conflicts and meaningful structural decisions
- `REVIEW_RUBRIC.md` — review criteria
- `SUBMISSION_CHECKLIST.md` — pre-submission integrity and formatting checks
- `RELEASE_CHECKLIST.md` — pre-release packaging checklist
- `RELEASE_NOTES.md` — release summary template
- `ARXIV_ABSTRACT.txt` — release-facing abstract text
- `paper_structure_spec_filled.md` — deprecated legacy stub retained for migration only
- `OPTIONAL_CURSOR_SETUP.md` — optional editor setup notes
- `examples/TEMPLATE_DEMO_FIGURE_SPEC.md` — optional demo figure copy for meta-papers about this template only

## `paper/`
- `main.tex` — LaTeX entrypoint
- `abstract.tex` — abstract scaffold
- `sections/` — required and optional manuscript section scaffolds
- `appendix/` — appendix and supplementary hooks
- `tex/` — package setup, theorem setup, macros, and notation
- `bib/` — bibliography file
- `figures/` — figure assets derived from `PROJECT_SPEC.md`, not a separate figure-spec layer
- `tables/` — table assets and planning placeholders

## `scripts/`
- `build_paper.py` — cross-platform LaTeX build driver
- `latex_log.py` — shared LaTeX log parsing for render audit and quality gate
- `render_audit.py` — build-log and rendered-PDF review helper (`--write-full-extract` for full-document text file)
- `pdf_quality_gate.py` — pass/fail after build on critical log issues; optional `--strict-layout`
- `export_figure_pages.py` — rasterize labeled figure-bearing PDF pages as PNGs
- `figure_visual_audit.py` — build plus figure-page PNG export helper
- `check_rendered_refs.py` — rendered theorem-like cross-reference naming audit
- `map_manuscript_files.py` — generate active vs legacy manuscript file reports
- `check_placeholders.py` — unresolved placeholder audit
- `check_bib_placeholders.py` — incomplete bibliography audit
- `project_audit.py` — combined project status preview
- `clean_paper.py` — generated LaTeX artifact cleanup
