# Environment Setup

## Required Tools

- Python 3.11 or newer
- A LaTeX toolchain available on `PATH`
- Recommended: `pypdf` for full-document text extraction (`pip install pypdf`) used by `scripts/render_audit.py --write-full-extract`
- Alternative: Poppler `pdftotext` on `PATH`

## Windows

1. Install Python.
2. Install MiKTeX or another LaTeX distribution.
3. Verify:
   - `python --version`
   - `pdflatex --version`
   - `bibtex --version`
4. Run:
   - `powershell -ExecutionPolicy Bypass -File .\\verify.ps1`
   - `python scripts/run_autonomous_paper.py --dry-run`

## Cross-Platform Validation

- `python scripts/parse_spec.py`
- `python scripts/spec_audit.py`
- `python scripts/generate_from_spec.py`
- `python scripts/figure_audit.py`
- `python scripts/run_autonomous_paper.py --dry-run`

## CI Notes

The automation tests are designed to run without a LaTeX toolchain. Full PDF builds should run in local or provisioned environments that include `pdflatex`.
