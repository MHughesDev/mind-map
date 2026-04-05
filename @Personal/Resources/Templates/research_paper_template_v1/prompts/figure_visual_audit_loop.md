# Figure visual audit loop

Use this when the paper builds but figures may still have visual defects.

## Goal

Eliminate visible figure-quality issues by repeating:

`build -> export figure pages -> inspect PNGs -> edit figure files -> rebuild -> re-export`

## Required inputs

- `PROJECT_SPEC.md`
- `paper/main.pdf`
- `paper/main.aux`
- `audit/figure_visual/manifest.json`
- figure audit criteria from Section 12 of `PROJECT_SPEC.md`

## Loop

1. Run `python scripts/figure_visual_audit.py`.
2. Open all PNGs under `audit/figure_visual/exports/`.
3. For each figure, check:
   - title/label collisions
   - arrow/text overlap
   - node/text overlap
   - dashed boxes striking through labels
   - crowded legends
   - caption/figure semantic mismatch
   - whether the intended distinctions are actually visible
4. Use `audit/figure_visual/manifest.json` to map the figure label to its source file.
5. Edit only the relevant files under `paper/figures/` or nearby caption/manuscript references if required.
6. Rebuild and re-export.
7. Stop only when all figure blocker conditions in `PROJECT_SPEC.md` are cleared or a real blocker is explicit.

## Scope discipline

In a figure-only pass:
- allowed: TikZ/layout/legend/caption alignment fixes
- not allowed: opportunistic manuscript restructuring, claim changes, citation changes, or reopening frozen sections
