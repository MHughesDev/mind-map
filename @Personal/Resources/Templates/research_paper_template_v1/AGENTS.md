# AGENTS.md

This repository is a research-paper generation workspace driven by one controlling brief: `PROJECT_SPEC.md`.

## Mission

Build, revise, and maintain a modular LaTeX paper project from the expanded single-file research spec.

## Source Of Truth Order

Read these first, in this order:

1. `PROJECT_SPEC.md`
2. explicit user instructions in chat
3. source materials explicitly authorized inside `PROJECT_SPEC.md`
4. `docs/DECISIONS_LOG.md`
5. `docs/MISSING_INPUTS.md`
6. `docs/PROJECT_STATUS.md`
7. existing manuscript files under `paper/`

Legacy files such as `templates/paper_structure_spec_master.md` and `docs/paper_structure_spec_filled.md` are migration helpers only. They are non-authoritative unless the user explicitly promotes them.

If `PROJECT_SPEC.md` is missing, ask the human to create it or import the legacy material into it before proceeding.

## Operating Rules

1. Read `PROJECT_SPEC.md` first and treat it as the controlling specification.
2. Start substantial work with a plan.
3. Extract and respect the execution model in Section 0 before drafting.
4. Use the research content bank, section blueprint, theorem/proof inventory, citation policy, and detailed figure-spec layer as drafting constraints.
5. Update `docs/PROJECT_STATUS.md` for major passes.
6. Update `docs/MISSING_INPUTS.md` when blockers, missing citations, missing proofs, or missing results appear.
7. Log meaningful source conflicts, structural choices, and figure-interpretation decisions in `docs/DECISIONS_LOG.md`.
8. Prefer modular LaTeX files in `paper/`, including `tex/package_setup.tex`, `tex/theorem_setup.tex`, `tex/macros.tex`, and `tex/notation.tex`.
9. Keep unknowns explicit with the strongest available marker: `BLOCKER`, `NEEDS_CITATION`, `NEEDS_PROOF`, `NEEDS_RESULT`, `OPTIONAL_LATER`, or `PLACEHOLDER`.
10. Do not invent citations, proofs, theorem statements unless explicitly authorized, experiments, datasets, baselines, results, affiliations, venue facts, or figure structure.
11. Before calling a compile-ready pass complete, build `paper/main.pdf`, run `python scripts/render_audit.py --write-full-extract` when possible (for `docs/PDF_TEXT_EXTRACT.md`), run `python scripts/pdf_quality_gate.py --skip-build` to check `paper/main.log`, review the PDF visually, and follow `prompts/pdf_convergence_loop.md` until render-quality exit criteria are met or blockers are explicit.
12. During figure-only or final release passes, run `python scripts/figure_visual_audit.py` and inspect the exported PNG pages under `audit/figure_visual/exports/` rather than relying on figure source code alone.
13. Never claim the project is complete while critical placeholders or unresolved blockers remain.

## Default Workflow

1. Read `PROJECT_SPEC.md`.
2. Summarize objective, scope, constraints, deliverables, and blockers.
3. Create a file-by-file execution plan.
4. Update the docs status files that match the current pass.
5. Scaffold or revise `paper/` from the section blueprint, detailed figure-spec layer, and LaTeX requirements.
6. Preserve citation, proof, and result boundaries while drafting.
7. Build and render-review the manuscript when the requested draft level warrants it (include `render_audit.py --write-full-extract` and visual PDF review; use `pdf_quality_gate.py` for automated log checks).
8. Run `python scripts/check_placeholders.py`, `python scripts/check_bib_placeholders.py`, and `python scripts/project_audit.py` when available (or `python scripts/verify.py`).
9. Report changed files, remaining blockers, unresolved placeholders by severity, missing human inputs, and the next best action.

## Writing Guardrails

- If theory is incomplete, mark it incomplete.
- If proofs are partial, label them as proof sketches or unresolved proof burdens.
- If experiments are not run, never imply they were run.
- If a citation is incomplete, keep it as a marked stub and log the gap.
- If a section blueprint limits claims or tone, follow it over generic drafting instincts.
- If a style target is authorized, follow the style without copying content.

## File Targets

- Manuscript files live under `paper/`.
- Status and workflow files live under `docs/`.
- Reusable prompts live under `prompts/`.
- Subagent definitions live under `.cursor/agents/`.
- Project rules live under `.cursor/rules/`.
