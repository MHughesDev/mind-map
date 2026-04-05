# Paper Directory

This directory contains the LaTeX manuscript project.

## Structure
- `main.tex` — main entrypoint
- `abstract.tex` — abstract file
- `sections/` — major and optional manuscript sections
- `appendix/appendix.tex` — appendix
- `appendix/supplementary.tex` — optional supplementary hook
- `tex/` — package setup, theorem setup, macros, notation
- `bib/references.bib` — bibliography
- `figures/`, `tables/` — assets only, not conceptual spec layers

## Build
Run from repository root:
- `make build`
- `make audit`

## Rule
Do not delete placeholder markers unless the underlying content is genuinely resolved.

Do not define figure meaning in `paper/`. Figure meaning, structure, semantic mapping, and caption intent belong only in `PROJECT_SPEC.md`.

Draft every section from `PROJECT_SPEC.md`, especially:
- Section 3 for research content seeds
- Section 6 for citation policy
- Section 8 for the section blueprint
- Section 9 for theorem/proof/notation controls
- Section 12 for figure/table plans and the detailed figure-spec layer
- Section 13 for PDF style and build requirements
