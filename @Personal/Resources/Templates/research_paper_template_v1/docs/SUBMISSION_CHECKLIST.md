# Submission Checklist

## Content Integrity
- [ ] No fabricated citations remain
- [ ] No fabricated results remain
- [ ] No incomplete proof is labeled complete
- [ ] No unsupported novelty claim remains
- [ ] Limitations are stated clearly
- [ ] Section claims respect the authorization limits in `PROJECT_SPEC.md`

## Manuscript Structure
- [ ] Abstract aligned with actual paper content
- [ ] Contributions list matches body
- [ ] Notation introduced before use
- [ ] Figures/tables referenced correctly
- [ ] Figure meaning and captions match `PROJECT_SPEC.md`
- [ ] Appendix contents are intentional
- [ ] Section order and section purpose match the Section 8 blueprint

## Bibliography
- [ ] Placeholder entries removed or intentionally marked for internal draft only
- [ ] Citation style matches venue
- [ ] Must-cite works included
- [ ] Rival work treated fairly

## Formatting
- [ ] Page/word limits checked
- [ ] Blind-review requirements satisfied
- [ ] Author and affiliation formatting checked
- [ ] Build succeeds locally / in Overleaf as required
- [ ] `docs/BUILD_STATUS.md` shows a successful recent build
- [ ] `docs/PDF_REVIEW.md` has no unresolved blocking render issues
- [ ] PDF style target matches the approved typography and caption rules

## Final Audit
- [ ] `python scripts/build_paper.py`
- [ ] `python scripts/render_audit.py`
- [ ] `python scripts/check_placeholders.py`
- [ ] `python scripts/check_bib_placeholders.py`
- [ ] `python scripts/project_audit.py`
- [ ] Direct PDF review of `paper/main.pdf` completed
- [ ] Human final read completed
