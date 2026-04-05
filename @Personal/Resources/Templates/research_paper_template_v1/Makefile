PYTHON ?= python

.PHONY: build render-audit render-audit-full audit verify verify-gate quality-gate clean

build:
	$(PYTHON) scripts/build_paper.py

render-audit:
	$(PYTHON) scripts/render_audit.py

render-audit-full:
	$(PYTHON) scripts/render_audit.py --write-full-extract

audit:
	$(PYTHON) scripts/check_placeholders.py
	$(PYTHON) scripts/check_bib_placeholders.py
	$(PYTHON) scripts/project_audit.py

verify:
	$(PYTHON) scripts/verify.py --all-placeholders

# After verify: log gate + full-text extract refresh without rebuilding
verify-gate: verify
	$(PYTHON) scripts/pdf_quality_gate.py --skip-build

# Full build + render audit with extract + log gate (strict layout: add STRICT=1)
quality-gate:
	$(PYTHON) scripts/pdf_quality_gate.py $(if $(STRICT),--strict-layout,)

clean:
	$(PYTHON) scripts/clean_paper.py
