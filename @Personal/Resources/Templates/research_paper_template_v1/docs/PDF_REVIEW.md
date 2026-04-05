# PDF Review

This file tracks rendered-PDF issues found after building the manuscript.

## Artifact Status
- `paper/main.pdf` present: no
- `paper/main.log` present: yes
- `docs/PDF_TEXT_EXTRACT.md` present: no
- PDF text preview status: `missing`

## Automated Findings Summary
- Build Errors: `2`
- Missing Files: `0`
- Undefined Citations: `0`
- Undefined References: `0`
- Overfull Boxes: `0`
- Underfull Boxes: `0`
- Package Warnings: `0`

## Automated Findings

### Build Errors
- [ ] ! Emergency stop.
- [ ] !  ==> Fatal error occurred, no output PDF file produced!

### Missing Files
- [ ] None detected.

### Undefined Citations
- [ ] None detected.

### Undefined References
- [ ] None detected.

### Overfull Boxes
- [ ] None detected.

### Underfull Boxes
- [ ] None detected.

### Package Warnings
- [ ] None detected.

## PDF Text Preview

This preview is a lightweight sanity check for the first N pages (see `scripts/render_audit.py --help`). It does not replace direct PDF inspection for layout issues. When `docs/PDF_TEXT_EXTRACT.md` exists, use it for full-document text search.

```text
PDF does not exist yet.
```

## Direct Visual Review Checklist

- [ ] No overlapping text blocks
- [ ] No figures cropped, stretched, or off-page
- [ ] No tables extending beyond page margins
- [ ] No equations overflowing into margins
- [ ] No captions colliding with figures or tables
- [ ] No unreadable axis labels, legends, or small fonts
- [ ] No broken page breaks, isolated headings, or giant whitespace gaps
- [ ] No bibliography formatting anomalies

## Recommended Fix Queue

- [ ] Resolve LaTeX build errors before any visual cleanup.
- [ ] Build the PDF successfully before attempting manual render review.

## Manual Findings

- [ ] Run `python scripts/render_audit.py`, then read `paper/main.pdf` directly and record page-level issues here.

## Recommended Fix Queue
- [ ]
