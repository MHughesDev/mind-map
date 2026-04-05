# Autonomous Paper Factory

This document describes the end-to-end automation stack for spec-driven paper production.

## Entry Points

- `python scripts/parse_spec.py`
- `python scripts/spec_audit.py`
- `python scripts/generate_from_spec.py`
- `python scripts/figure_audit.py`
- `python scripts/run_autonomous_paper.py`

## Execution Stages

1. Parse `PROJECT_SPEC.md` into `build/spec.json`
2. Audit the parsed spec and write `docs/SPEC_AUDIT.md`
3. Build an evidence store from declared source materials
4. Generate a claim-grounding report
5. Generate manuscript section files and bibliography scaffolds
6. Generate figure manifests and LaTeX snippets
7. Run build and audit scripts
8. Classify failures and record attempted repairs (up to three repair rounds: rebuild/regenerate after each round while failures remain and new repair strategies apply)
9. Persist run state in `build/run_state.json`

## Render artifacts

- Each build-and-audit pass runs `scripts/render_audit.py --write-full-extract` so `docs/PDF_TEXT_EXTRACT.md` can be refreshed locally (gitignored) for agent text search.

## Key Artifacts

- `build/spec.json`
- `build/spec_audit.json`
- `build/evidence_store.json`
- `build/figure_specs.json`
- `build/run_state.json`
- `build/autonomous_run_summary.json`
- `docs/SPEC_AUDIT.md`
- `docs/CLAIM_GROUNDING.md`
- `docs/FIGURE_AUDIT.md`

## Safety Model

- Spec placeholders and missing required sections block execution readiness.
- Source materials are ingested only from what the spec declares.
- Generated bibliography entries are scaffolded from declared evidence and should be enriched with verified metadata.
- Build failures are classified before any repair attempt is recorded.
- Human override files remain `docs/MISSING_INPUTS.md` and `docs/DECISIONS_LOG.md`.
