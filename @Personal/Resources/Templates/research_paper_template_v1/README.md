# Research Paper Autonomous Kit

This repository is a reusable research-paper template built around one controlling brief: `PROJECT_SPEC.md`.

The template now assumes the spec is rich enough to drive:
- execution mode and autonomy boundaries,
- canonical naming and paper-mode locks,
- formal-commitment and variant locks,
- non-claims, done-state, and freeze policy,
- research content banks and source priorities,
- claim, citation, theorem, proof, and result controls,
- section-by-section manuscript blueprints,
- figure, table, notation, and PDF-style planning,
- figure audit criteria and rendered-page review,
- and a disciplined LaTeX build and review workflow.

## Core Rule

`PROJECT_SPEC.md` is the only authoritative execution brief for normal operation.

Figure planning, structure, semantics, and caption intent must also live only in `PROJECT_SPEC.md`. Do not create or rely on separate figure-spec files, except the optional demo copy in `docs/examples/TEMPLATE_DEMO_FIGURE_SPEC.md` for meta-papers about this template.

Legacy helpers such as `templates/paper_structure_spec_master.md` and `docs/paper_structure_spec_filled.md` are retained only as migration references. They are not co-equal sources of truth.

## Repository Layout

- `PROJECT_SPEC.md` contains the full expanded project spec.
- `AGENTS.md` and `.cursor/rules/` encode persistent agent behavior for this template.
- `.cursor/agents/` contains reusable subagent roles.
- `prompts/` contains launch and follow-up prompts for common passes.
- `docs/` contains project status, build status, PDF review, missing inputs, and decision logs.
- `paper/` contains the modular LaTeX scaffold, optional section hooks, bibliography, appendix, and visual asset folders.
- `paper/figures/` stores assets only; it is not a conceptual figure-definition layer.
- `scripts/` contains build and audit helpers.
- `templates/` contains migration helpers and a fast-fill companion, not alternate controlling specs.

## Quick Start

1. Copy this folder into a new research project.
2. Fill `PROJECT_SPEC.md`, especially the execution model, source priorities, content bank, citation policy, section blueprint, mathematical inventory, figure/table plan, and detailed figure-spec layer.
3. Add authorized source materials to the repository.
4. Open the folder in Cursor.
5. Launch the agent with `prompts/launch_cursor_agent.md` or the launch message inside `PROJECT_SPEC.md`.
6. Review `docs/PROJECT_STATUS.md`, `docs/MISSING_INPUTS.md`, and `docs/DECISIONS_LOG.md` after the first pass.
7. When the manuscript is compile-ready, run `.\verify.ps1` on Windows, `python scripts/verify.py`, or `make verify`.
8. For a strict PDF pass: `python scripts/pdf_quality_gate.py` (build + full-text extract + log gate), or after verify: `python scripts/pdf_quality_gate.py --skip-build`. Use `make verify-gate` to chain verify and the gate. Use `STRICT=1 make quality-gate` to fail on overfull boxes.
9. For figure-focused visual review: `python scripts/figure_visual_audit.py` to export figure-bearing PDF pages as PNGs, then inspect `audit/figure_visual/exports/`.
10. Repeat fixes using `prompts/pdf_convergence_loop.md` and `prompts/figure_visual_audit_loop.md` until clean.

## What The Template Supports

- fast-fill and deep-fill project intake through the expanded `PROJECT_SPEC.md`
- section-by-section drafting from explicit intent and allowed inputs
- theorem, proof, notation, and equation tracking
- section-specific citation expectations and citation integrity checks
- centralized figure definition inside the controlling spec
- figure, table, and PDF-style planning before final rendering
- rendered figure-page export for closed-loop visual auditing
- explicit blocker handling and no-invention safeguards
- modular LaTeX structure for iterative drafting and review

## Operating Rhythm

1. Human fills `PROJECT_SPEC.md` and provides authorized source materials.
2. Agent summarizes objective, constraints, blockers, and file-by-file plan.
3. Agent scaffolds or revises `paper/` from the spec.
4. Agent keeps `docs/PROJECT_STATUS.md`, `docs/MISSING_INPUTS.md`, and `docs/DECISIONS_LOG.md` current.
5. Agent builds and reviews `paper/main.pdf` when the draft level warrants it.
6. Human reviews diffs, placeholders, and unresolved blockers.

## Non-Negotiable Safety Rules

The agent may structure, scaffold, summarize, and draft.

The agent may not invent:
- citations,
- proofs,
- theorem statements unless explicitly authorized,
- experiments,
- results,
- datasets or baselines,
- authorship or submission metadata.

## Build Commands

If LaTeX is installed:

- `make build`
- `make render-audit` (refreshes `docs/PDF_REVIEW.md`)
- `make render-audit-full` (also writes `docs/PDF_TEXT_EXTRACT.md` for full-document text search; requires `pypdf` or Poppler `pdftotext`)
- `make audit`
- `make verify`
- `make verify-gate` (runs `verify` then `pdf_quality_gate.py --skip-build`)
- `make quality-gate` (full build + gate; optional `STRICT=1` for overfull boxes)
- `make clean`

Windows-friendly commands:

- `.\verify.ps1`
- `python scripts/verify.py`
- `python scripts/verify.py --all-placeholders` for the stricter repo-wide placeholder scan used by `make verify`
- `python scripts/pdf_quality_gate.py` for a single pass/fail check after build
- `python scripts/figure_visual_audit.py` for figure-page PNG export and visual inspection
- `python scripts/check_rendered_refs.py` for rendered theorem-like reference naming checks
- `python scripts/map_manuscript_files.py` to refresh active vs legacy manuscript reports

Autonomous paper-factory commands:

- `python scripts/parse_spec.py`
- `python scripts/spec_audit.py`
- `python scripts/generate_from_spec.py`
- `python scripts/figure_audit.py`
- `python scripts/run_autonomous_paper.py`
- `.\run_autonomous_paper.ps1` on Windows

Supporting docs:

- `docs/SPEC_SCHEMA.md`
- `docs/AUTONOMOUS_PAPER_FACTORY.md`
- `docs/ENVIRONMENT_SETUP.md`
- `docs/FIGURE_VISUAL_AUDIT.md`
- `docs/ACTIVE_MANUSCRIPT_FILES.md`
- `docs/LEGACY_MANUSCRIPT_FILES.md`

If `latexmk` is available, it will be used automatically by the Makefile.
