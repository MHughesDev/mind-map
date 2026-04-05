# Research Project Spec - Autonomy-Oriented Master Template

This file is the single controlling brief for a research-paper project.

It is designed so an autonomous agent can, from one master file:
- scaffold the repository,
- draft or revise the manuscript,
- preserve scope and non-claims,
- distinguish mainline formalism from optional variants,
- manage citations, figures, proofs, and release packaging,
- and iterate on the compiled PDF until defined quality gates are met.

If a detail is not in this file or in explicitly authorized source materials, the agent must not invent it.

---

# How To Use

1. Copy this template into a new project as `PROJECT_SPEC.md`.
2. Fill every required field with either a real value, `UNKNOWN`, or `N/A`.
3. Do not leave silent ambiguity.
4. If a choice is intentionally deferred, mark that explicitly.
5. Treat this file as the canonical source of truth for the paper.
6. If legacy planning files exist, migrate anything still relevant into this file.

Recommended launch message:

`Read PROJECT_SPEC.md and execute this repository autonomously. Treat it as the controlling specification. Preserve all unknowns explicitly, do not fabricate citations, proofs, results, or experiments, and follow the PDF convergence loop until the declared done-state is reached or a blocker is explicit.`

---

# Global Rules

- If evidence is missing, preserve the gap.
- If citations are missing, do not fake them.
- If proofs are missing, do not claim them complete.
- If results are missing, do not imply they exist.
- All manuscript prose must be reader-facing, not repo-facing.
- Status markers belong in docs, not in reader-facing manuscript prose.
- Appendix material is still reader-facing scholarship, not a storage dump.
- If the main thesis is too unclear to draft responsibly, stop and ask for clarification.
- If noncritical information is missing, continue with explicit placeholders.

Use these unresolved markers in docs and planning artifacts:
- `[BLOCKER: ...]`
- `[NEEDS_CITATION: ...]`
- `[NEEDS_PROOF: ...]`
- `[NEEDS_RESULT: ...]`
- `[OPTIONAL_LATER: ...]`
- `[PLACEHOLDER: ...]`
- `[UNVERIFIED: ...]`

Do not leave repo-style markers in final manuscript prose unless transformed into proper scholarly language.

---

# Agent Execution Contract

The agent must:
- read this file first,
- summarize the objective, scope, constraints, deliverables, and blockers,
- extract the allowed pass taxonomy before editing,
- create a file-by-file execution plan,
- scaffold or revise the LaTeX project under `paper/`,
- create or update:
  - `docs/PROJECT_STATUS.md`
  - `docs/BUILD_STATUS.md`
  - `docs/PDF_REVIEW.md`
  - `docs/MISSING_INPUTS.md`
  - `docs/DECISIONS_LOG.md`
  - `docs/FIGURE_AUDIT.md`
- preserve all unknowns explicitly,
- keep theorem/proof/result status honest,
- run local audit/build scripts when available,
- use rendered PDF inspection, including figure-page raster export, during convergence passes,
- report changed files, remaining placeholders, blockers, and the next best action.

The agent must not:
- invent citations,
- invent theorem statements unless explicitly authorized,
- invent proofs,
- invent experiments,
- invent quantitative results,
- invent datasets or baselines,
- invent submission facts,
- invent author affiliations,
- claim completion while critical placeholders remain,
- perform opportunistic edits outside the current pass scope.

---

# 0. Fill Strategy

## 0.1 Project mode
- Project mode:
  - scaffold only
  - outline only
  - draft from notes
  - revise existing paper
  - citation hardening
  - theory formalization
  - experiment write-up
  - reviewer-defense pass
  - release-readiness pass
  - mixed mode

## 0.2 Desired draft level
- Desired draft level:
  - outline only
  - structured draft
  - polished draft
  - preprint-ready
  - submission-style draft

## 0.3 Allowed autonomy level
- Allowed autonomy level:
  - high for structure, low for claims
  - high for prose, low for math
  - high for theory, low for citations
  - high until explicit blocker
  - custom:

## 0.4 Stop/continue rule
- Continue with placeholders unless blocked?:
- Items that must block execution:
- Items that should never block execution:
- Checkpoint cadence, if any:

## 0.5 Pass taxonomy
- Allowed pass types:
  - formalization pass
  - theory-hardening pass
  - style-convergence pass
  - build-resolution pass
  - citation pass
  - figure-only pass
  - proof-boundary pass
  - metadata insertion pass
  - release-readiness pass
  - freeze confirmation pass
- For each allowed pass, what it may change:
- For each allowed pass, what it may not change:

## 0.6 Done-state target
- Target done-state:
  - scaffold-complete
  - formal-core-complete
  - literature-grounded
  - build-verified
  - preprint-ready
  - release-ready
  - venue-submission-ready
- Stop when target done-state is reached?:

## 0.7 Freeze policy
- Freeze begins when:
- After freeze, allowed changes:
- After freeze, forbidden changes:
- Figure-only fixes allowed after freeze?:
- Metadata-only edits allowed after freeze?:
- What counts as a release blocker after freeze:

---

# 1. Project Identity

## 1.1 Basic identity
- Final paper title:
- Short title / running title:
- Subtitle, if any:
- Internal codename:
- Preferred folder name:
- Preferred LaTeX main file name:
- Preferred bibliography file name:
- Primary field:
- Subfield:
- Secondary fields:
- Keywords:
- Paper category:
  - pure theory
  - theory + method
  - empirical
  - systems
  - hybrid
- Current stage:
- Target venue or outlet:
- Blind review expected?:
- arXiv intended?:
- Journal extension expected?:

## 1.2 Canonical naming and terminology
- Canonical object name:
- Terms allowed in the paper:
- Terms allowed only internally:
- Deprecated names to avoid:
- Search keywords that must not bleed into manuscript terminology:
- Canonical names for:
  - global state:
  - session slice:
  - external state or interface:
  - open thought / provisional object:
  - closed thought / accepted object:
  - belief:
  - closure operator:
  - admissibility:
  - merge:
  - conflict policy:
  - provenance policy:

## 1.3 Reader-facing identity constraints
- Terms or framings to avoid:
- Informal metaphors allowed in manuscript?:
- Informal metaphors allowed only internally?:
- Internal codename may appear in manuscript?:

---

# 2. Core Objective, Scope, And Non-Claims

## 2.1 Core objective
- Main objective:
- Core research question:
- Main thesis / key insight:
- Why this matters:
- Gap in the literature or practice:
- Reader takeaway:
- Primary contribution type:
- Secondary contribution types:

## 2.2 Novelty framing
- Absolute novelty claims forbidden?:
- Preferred novelty language:
  - synthesis
  - formalization
  - architecture
  - decomposition
  - reference framework
  - custom:
- Specific bounded novelty statement:
- Novelty language to avoid:

## 2.3 Paper mode and prohibited content
- Explicitly prohibited sections:
  - experiments
  - results
  - implementation
  - ablations
  - benchmarks
  - case studies
  - deployment
  - user study
  - other:
- Allowed evidence types:
  - definitions
  - propositions
  - theorems
  - conjectures
  - proofs
  - proof sketches
  - worked symbolic examples
  - empirical results
  - other:
- Forbidden claim types:
  - runtime claims
  - benchmark claims
  - implementation claims
  - deployment claims
  - broad generality claims beyond stated results
  - other:

## 2.4 Non-claims
- This paper does not claim:
- This paper does not compare:
- This paper does not prove:
- This paper does not implement:
- This paper does not measure:
- What must not be overclaimed:

---

# 3. Research Content Bank

This section is for the actual research content seeds the agent may use to shape the manuscript.

## 3.1 Core concepts and topics
- Core concepts that must appear:
- Supporting concepts that should appear:
- Optional concepts that may appear:
- Concepts to exclude:
- Terms that must be defined explicitly:
- Terms that should not be used:

## 3.2 Content seeds / idea fragments
- Seed 1:
- Seed 2:
- Seed 3:
- Seed 4:
- Seed 5:

## 3.3 Canonical examples or motivating cases
- Example 1:
- Example 2:
- Example 3:
- Counterexample or failure case to mention:

## 3.4 Interpretation policy
- The agent may paraphrase seeds into prose?:
- The agent may reorganize seeds?:
- The agent may compress repetitive seeds?:
- The agent must preserve any seed verbatim?:
- Verbatim passages to preserve:

---

# 4. Source Materials And Priority

## 4.1 Priority order
1. `PROJECT_SPEC.md`
2. explicit user instructions
3. `AGENTS.md` and `README.md`
4. workflow documentation under `docs/`
5. executable automation under `scripts/`
6. active manuscript and build artifacts under `paper/` and `build/`
7. legacy files only when explicitly promoted

## 4.2 Available materials
- `PROJECT_SPEC.md`
- `AGENTS.md`
- `README.md`
- `docs/FRONT_TO_END_WORKFLOW.md`
- `docs/FILE_MAP.md`
- `docs/REVIEW_RUBRIC.md`
- `docs/SUBMISSION_CHECKLIST.md`
- `docs/FIGURE_VISUAL_AUDIT.md`
- `prompts/pdf_convergence_loop.md`
- `prompts/figure_visual_audit_loop.md`
- `scripts/build_paper.py`
- `scripts/render_audit.py`
- `scripts/pdf_quality_gate.py`
- `scripts/spec_audit.py`
- `scripts/run_autonomous_paper.py`
- `scripts/export_figure_pages.py`
- `scripts/figure_visual_audit.py`
- `paper/main.tex`
- `paper/tex/package_setup.tex`
- `paper/tex/theorem_setup.tex`
- `paper/bib/references.bib`

## 4.3 Source usage rules
- Highest-authority source for scientific content: `PROJECT_SPEC.md`
- Highest-authority source for style/formatting: `README.md`, `AGENTS.md`, and `docs/REVIEW_RUBRIC.md`
- Highest-authority source for theorem statements: `PROJECT_SPEC.md`
- Highest-authority source for active manuscript state: active files under `paper/`, then built PDF, then logs
- Highest-authority source for citation metadata: `paper/bib/references.bib` plus explicitly authorized sources
- Highest-authority source for figure semantics: detailed figure specs in this file
- What the agent may use style-only, not content-wise:
- What the agent must not use at all:

## 4.4 Source conflict policy
- If sources conflict, prioritize:
  1. `PROJECT_SPEC.md`
  2. active manuscript files
  3. built PDF
  4. build and audit logs
  5. summary docs
- Must log conflicts in `docs/DECISIONS_LOG.md`?:
- Must stop on core scientific conflicts?:

---

# 5. Claim And Evidence Map

## Claim 1
- Statement:
- Strength:
- Evidence available:
- Citations required:
- Proof required?:
- Result required?:
- Caveats:
- What would weaken it:
- Scope of validity:
- Scope limits:

## Claim 2
- Statement:
- Strength:
- Evidence available:
- Citations required:
- Proof required?:
- Result required?:
- Caveats:
- What would weaken it:
- Scope of validity:
- Scope limits:

## Claim 3
- Statement:
- Strength:
- Evidence available:
- Citations required:
- Proof required?:
- Result required?:
- Caveats:
- What would weaken it:
- Scope of validity:
- Scope limits:

## Claim guardrails
- Claims to soften:
- Claims that must not appear:
- Claims requiring explicit caveats:
- Known uncertainty boundaries:
- Claims that are allowed only with proof:
- Claims that are allowed only with citations:
- Claims that are allowed only with results:

---

# 6. Literature, Related Work, And Citation Policy

## 6.1 Citation and literature strategy
- Citation pass timing:
  - first draft
  - second pass
  - late-stage only
  - custom:
- Must-cite families:
- Forbidden citation sources:
- Preprints allowed?:
- Websites allowed?:
- Style references may influence citation density?:
- Novelty language policy before citations are verified:
- Unsupported claims should be softened or left marked:

## 6.2 Related-work families
- Adjacent family 1:
  - How this paper differs:
  - What this paper does not claim relative to it:
- Adjacent family 2:
  - How this paper differs:
  - What this paper does not claim relative to it:
- Adjacent family 3:
  - How this paper differs:
  - What this paper does not claim relative to it:
- Adjacent family 4:
  - How this paper differs:
  - What this paper does not claim relative to it:
- Bounded novelty statement:
- Non-claims relative to adjacent literature:

## 6.3 Citation quality policy
- Citation density target:
- Minimum source quality:
- Books allowed?:
- Reports allowed?:
- Must every non-obvious claim be cited?:
- Must citations be verified before inclusion?:
- The agent may add new verified citations beyond the listed ones?:
- The agent must not add citations unless explicitly listed?:
- The agent should mark uncited claims as `[NEEDS_CITATION]`?:

## 6.4 Citation formatting and reference behavior
- Citation style preference:
- In-text citation behavior:
  - parenthetical only
  - textual when natural
  - mixed
- Preferred reference granularity:
  - one citation per paragraph when enough
  - cite every claim cluster
  - cite nearly every nontrivial claim
- When multiple sources support one point, prefer:
  - one strongest source
  - two diverse sources
  - foundational + recent pair
- DOI preference:
- URL policy:
- arXiv formatting preference:
- Author initials vs full names:
- Conference/journal formatting preference:

---

# 7. Audience And Writing Style

## 7.1 Audience
- Primary audience:
- Secondary audience:
- Assumed background:
- Concepts requiring gentle introduction:
- Terms to define explicitly:

## 7.2 Style reference section
- Primary reference manuscript for style:
- What may be imitated:
  - section rhythm
  - tone
  - notation placement
  - intro structure
  - conclusion structure
  - discussion style
  - figure caption style
  - theorem pacing
  - custom:
- What may not be copied:
  - content
  - claims
  - citations
  - formulas
  - terminology unless authorized

## 7.3 Writing controls
- Preferred terminology:
- Terms to avoid:
- Tone:
- Assertiveness level:
- Paragraph density:
- Jargon level:
- Voice preference:
- Sentence complexity preference:
- Include intuition paragraphs?:
- Include roadmap paragraphs?:
- Include takeaway paragraphs?:
- Include example-driven exposition?:
- Reader-facing prose required?:

---

# 8. Section-by-Section Blueprint

## 8.1 Required major sections
- [ ] Abstract
- [ ] Introduction
- [ ] Related Work
- [ ] Background / Preliminaries
- [ ] Problem Setup
- [ ] Method / Theory
- [ ] Algorithms
- [ ] Experiments
- [ ] Results
- [ ] Discussion
- [ ] Limitations
- [ ] Broader Impact / Ethics
- [ ] Conclusion
- [ ] Appendix
- [ ] Supplementary Material
- [ ] Acknowledgments
- [ ] Other:

## 8.2 Preferred section order
1.
2.
3.
4.
5.
6.
7.
8.
9.
10.

## 8.3 Section-by-section content plan

### Section 1
- Section name:
- Purpose:
- Must include:
- Must not include:
- Inputs or notes to use:
- Claims allowed here:
- Citations expected here:
- Tone or pacing notes:
- Ideal ending of the section:

### Section 2
- Section name:
- Purpose:
- Must include:
- Must not include:
- Inputs or notes to use:
- Claims allowed here:
- Citations expected here:
- Tone or pacing notes:
- Ideal ending of the section:

### Section 3
- Section name:
- Purpose:
- Must include:
- Must not include:
- Inputs or notes to use:
- Claims allowed here:
- Citations expected here:
- Tone or pacing notes:
- Ideal ending of the section:

### Section 4
- Section name:
- Purpose:
- Must include:
- Must not include:
- Inputs or notes to use:
- Claims allowed here:
- Citations expected here:
- Tone or pacing notes:
- Ideal ending of the section:

### Section 5
- Section name:
- Purpose:
- Must include:
- Must not include:
- Inputs or notes to use:
- Claims allowed here:
- Citations expected here:
- Tone or pacing notes:
- Ideal ending of the section:

## 8.4 Epistemic status policy
- What may appear as a definition:
- What may appear as a proposition:
- What may appear as a theorem:
- What must remain a conjecture:
- What must move to appendix:
- What should be an open question:
- Whether proof obligations may appear in main text:
- Acceptable wording for unresolved results:

## 8.5 Abstract / intro / conclusion controls
- Abstract must include:
- Abstract must exclude:
- Introduction must emphasize:
- Introduction must not overclaim:
- Conclusion must restate:
- Conclusion must not imply:

---

# 9. Mathematical Content And Theory Control

## 9.1 Core mathematical objects
- Core mathematical objects:
- Sets:
- Variables:
- Functions:
- Operators:
- Relations:
- Constraints:
- Assumptions:
- Boundary conditions:
- Edge cases:

## 9.2 Formal commitments and variant lock
- Core mathematical object:
  - Main choice:
  - Rejected alternatives:
  - Optional future variants:
  - Main text / appendix / omit:
- Layer semantics:
  - Main choice:
  - Rejected alternatives:
  - Optional future variants:
  - Main text / appendix / omit:
- Layer 0 policy:
  - Main choice:
  - Rejected alternatives:
  - Optional future variants:
  - Main text / appendix / omit:
- Support-edge directionality:
  - Main choice:
  - Rejected alternatives:
  - Optional future variants:
  - Main text / appendix / omit:
- Cross-layer dependency rule:
  - Main choice:
  - Rejected alternatives:
  - Optional future variants:
  - Main text / appendix / omit:
- Conflict coexistence rule:
  - Main choice:
  - Rejected alternatives:
  - Optional future variants:
  - Main text / appendix / omit:
- Admissibility regime:
  - Main choice:
  - Rejected alternatives:
  - Optional future variants:
  - Main text / appendix / omit:
- Closure semantics:
  - Main choice:
  - Rejected alternatives:
  - Optional future variants:
  - Main text / appendix / omit:
- Merge semantics:
  - Main choice:
  - Rejected alternatives:
  - Optional future variants:
  - Main text / appendix / omit:
- Provenance semantics:
  - Main choice:
  - Rejected alternatives:
  - Optional future variants:
  - Main text / appendix / omit:
- Belief definition:
  - Main choice:
  - Rejected alternatives:
  - Optional future variants:
  - Main text / appendix / omit:
- Recursive admissibility mainline or optional:
- Higher-order topology core or future work:

## 9.3 Mainline vs optional variants
- Variant 1:
  - Mainline in paper?:
  - Appendix only?:
  - Future work only?:
  - Reference policy?:
  - Must be implemented in figures?:
- Variant 2:
  - Mainline in paper?:
  - Appendix only?:
  - Future work only?:
  - Reference policy?:
  - Must be implemented in figures?:

## 9.4 Formal statement policy
- Allowed environments:
- Disallowed environments:
- Maximum number of conjectures in main text:
- When to use remark vs proposition:
- Whether axioms are allowed:
- Whether algorithm environments are allowed:

## 9.5 Definitions that must appear early
1.
2.
3.
4.
5.

## 9.6 Mathematical equations and formulas inventory
- Equation / formula 1:
  - Role in paper:
  - Must be exact or can be provisional?:
  - Section where it belongs:
- Equation / formula 2:
  - Role in paper:
  - Must be exact or can be provisional?:
  - Section where it belongs:
- Equation / formula 3:
  - Role in paper:
  - Must be exact or can be provisional?:
  - Section where it belongs:
- Equation / formula 4:
  - Role in paper:
  - Must be exact or can be provisional?:
  - Section where it belongs:

## 9.7 Formal statement inventory

### Statement 1
- Type: proposition / lemma / theorem / corollary / definition / conjecture / remark / axiom
- Draft statement:
- Why it matters:
- Proof status:
- Required assumptions:
- Section placement:

### Statement 2
- Type:
- Draft statement:
- Why it matters:
- Proof status:
- Required assumptions:
- Section placement:

### Statement 3
- Type:
- Draft statement:
- Why it matters:
- Proof status:
- Required assumptions:
- Section placement:

### Statement 4
- Type:
- Draft statement:
- Why it matters:
- Proof status:
- Required assumptions:
- Section placement:

## 9.8 Proof policy
- Need theorems?:
- Need lemmas?:
- Need proofs?:
- Need proof sketches in main text?:
- Need full proofs in appendix?:
- Proof rigor level:
- The agent may draft proof skeletons when full proofs are missing?:
- The agent must mark unresolved proof burdens as `[NEEDS_PROOF]`?:

## 9.9 Notation presentation
- Notation summary required?:
- Placement:
  - after abstract
  - in preliminaries
  - appendix only
  - custom:
- Table vs prose list:
- Whether notation should reappear later:
- Whether local symbol reminders are expected:
- Symbols already reserved:
- Symbols to avoid:
- Indexing conventions:
- Bold vector preference:
- Matrix notation preference:
- Equation numbering preference:
- Theorem numbering preference:

---

# 10. Method / System / Architecture Blueprint

- Main method / system / theorem name:
- Plain-English summary:
- Technical summary:
- Major components:
- Inputs:
- Outputs:
- Pipeline or logical order:
- Online mode description:
- Offline mode description:
- Multi-agent behavior:
- Memory/state model:
- Failure modes:
- Safety considerations:
- Need pseudocode?:
- Need formal algorithms?:
- Need architecture / system description?:
- Need design rationale section?:
- Need complexity analysis?:

---

# 11. Experiments, Results, And Evaluation

- Evidence sources:
- Datasets:
- Baselines:
- Metrics:
- Statistical reporting requirements:
- Hardware / software requirements:
- Reproducibility constraints:
- Main results to highlight:
- Negative results to include:
- Required ablations:
- Required robustness checks:
- Required error analysis:
- Required limitations discussion:
- Results that are not yet verified:

## 11.1 Evidence authorization by section
- Sections allowed to make empirical claims:
- Sections allowed to make only conceptual claims:
- Sections where `[NEEDS_RESULT]` must appear if evidence is missing:

## 11A. Worked Example And Reference Policy Layer
- If the framework is policy-parameterized, require a reference policy family?:
- Reference policy family:
- Why it was chosen:
- What it is not claiming:
- Conservative or permissive:
- Pedagogical or normative:
- Worked symbolic example required?:
- Location:
  - main text
  - appendix
- Worked example must include:
  - at least one evidence node
  - at least one open candidate
  - session slice
  - merge step or merge-ready condition
  - closure
  - belief vs closed distinction
  - contradiction case yes/no

---

# 12. Figures, Tables, And Visuals

All conceptual figure definitions belong in this file. Do not create separate conceptual figure-spec files.

## 12.1 Figure plan

### Figure 1
- Purpose:
- Must show:
- Section placement:
- Data required:
- Style notes:

### Figure 2
- Purpose:
- Must show:
- Section placement:
- Data required:
- Style notes:

### Figure 3
- Purpose:
- Must show:
- Section placement:
- Data required:
- Style notes:

## 12.2 Table plan

### Table 1
- Purpose:
- Required columns:
- Required rows:
- Section placement:
- Data required:

### Table 2
- Purpose:
- Required columns:
- Required rows:
- Section placement:
- Data required:

## 12.3 Figure specification layer (detailed)

### Figure 1: `[PLACEHOLDER: short name]`
- Purpose:
- Section placement:

#### Structural Description
- Type (graph, layered system, pipeline, geometric, etc):
- Dimensionality:
- Formal object being depicted:
- Core elements (nodes, edges, layers, arrows, regions, etc):

#### Semantic Mapping
- Nodes represent:
- Edges represent:
- Layers represent:
- Colors represent:
- Shapes represent:

#### Layout Constraints
- Global layout (left-to-right, top-to-bottom, radial, etc):
- Relative positioning rules:
- Alignment constraints:
- Required nodes/edges/layers/regions:
- Forbidden visual semantics:

#### Mathematical Correspondence
- Related equation/operator:
- Mapping from math to visual:
  - Symbol to visual element:
  - Operator to transformation in figure:

#### Rendering Instructions
- Style (minimal, academic, annotated, didactic, structural only):
- Label requirements:
- Legend policy:
- Tool preference (TikZ / matplotlib / external / UNKNOWN):
- Level of detail:
- Intended visual hierarchy:
- What must be visually distinguished:
- What must not be shown:
- What can be deferred to the caption:

#### Caption Requirements
- Caption must explain:
- Caption must NOT assume:
- Caption may mention concepts not shown?:

#### Audit Criteria
- Release-quality criteria:
- Minimum readability requirements:
- What counts as too crowded:
- Acceptable label density:
- Must survive grayscale?:
- Must read standalone?:
- Blocker conditions:

### Figure 2: `[PLACEHOLDER: short name or delete this block]`
- Purpose:
- Section placement:

#### Structural Description
- Type (graph, layered system, pipeline, geometric, etc):
- Dimensionality:
- Formal object being depicted:
- Core elements (nodes, edges, layers, arrows, regions, etc):

#### Semantic Mapping
- Nodes represent:
- Edges represent:
- Layers represent:
- Colors represent:
- Shapes represent:

#### Layout Constraints
- Global layout (left-to-right, top-to-bottom, radial, etc):
- Relative positioning rules:
- Alignment constraints:
- Required nodes/edges/layers/regions:
- Forbidden visual semantics:

#### Mathematical Correspondence
- Related equation/operator:
- Mapping from math to visual:
  - Symbol to visual element:
  - Operator to transformation in figure:

#### Rendering Instructions
- Style (minimal, academic, annotated, didactic, structural only):
- Label requirements:
- Legend policy:
- Tool preference (TikZ / matplotlib / external / UNKNOWN):
- Level of detail:
- Intended visual hierarchy:
- What must be visually distinguished:
- What must not be shown:
- What can be deferred to the caption:

#### Caption Requirements
- Caption must explain:
- Caption must NOT assume:
- Caption may mention concepts not shown?:

#### Audit Criteria
- Release-quality criteria:
- Minimum readability requirements:
- What counts as too crowded:
- Acceptable label density:
- Must survive grayscale?:
- Must read standalone?:
- Blocker conditions:

### Figure 3: `[PLACEHOLDER: short name or delete this block]`
- Purpose:
- Section placement:

#### Structural Description
- Type (graph, layered system, pipeline, geometric, etc):
- Dimensionality:
- Formal object being depicted:
- Core elements (nodes, edges, layers, arrows, regions, etc):

#### Semantic Mapping
- Nodes represent:
- Edges represent:
- Layers represent:
- Colors represent:
- Shapes represent:

#### Layout Constraints
- Global layout (left-to-right, top-to-bottom, radial, etc):
- Relative positioning rules:
- Alignment constraints:
- Required nodes/edges/layers/regions:
- Forbidden visual semantics:

#### Mathematical Correspondence
- Related equation/operator:
- Mapping from math to visual:
  - Symbol to visual element:
  - Operator to transformation in figure:

#### Rendering Instructions
- Style (minimal, academic, annotated, didactic, structural only):
- Label requirements:
- Legend policy:
- Tool preference (TikZ / matplotlib / external / UNKNOWN):
- Level of detail:
- Intended visual hierarchy:
- What must be visually distinguished:
- What must not be shown:
- What can be deferred to the caption:

#### Caption Requirements
- Caption must explain:
- Caption must NOT assume:
- Caption may mention concepts not shown?:

#### Audit Criteria
- Release-quality criteria:
- Minimum readability requirements:
- What counts as too crowded:
- Acceptable label density:
- Must survive grayscale?:
- Must read standalone?:
- Blocker conditions:

Figure strictness rule:
- Figures must be derivable from the mathematical definitions.
- No figure may introduce structure not present in the formalism.
- If a figure simplifies reality, it must state the simplification explicitly.
- A figure is not complete unless the intended visual hierarchy is specified.

## 12.4 Visual standards
- Color allowed?:
- Grayscale-safe required?:
- Colorblind-safe required?:
- Preferred plotting/table style:
- Caption style preference:
- Notation summary table required?:
- Symbol glossary required?:
- Should visuals favor explanatory diagrams over data-heavy charts?:

## 12.5 PDF style / typography targets
- Style source files authorized for format only:
- One-column or two-column preference:
- Typography notes:
- Title block style:
- TOC preference:
- Section heading style:
- Theorem styling preference:
- Notation-summary placement:
- Figure caption tone:
- Table style preference:
- Hyperlink/color styling:
- Margin density / whitespace preference:

---

# 13. LaTeX, Build, And Audit Requirements

## 13.1 LaTeX project requirements
- Manuscript must be LaTeX?:
- Preferred document class:
- Preferred compiler:
- Preferred bibliography system:
- Overleaf-compatible required?:
- Local build required?:
- Avoid shell-escape?:
- Avoid external dependencies?:
- One-column or two-column?:
- Page or word limit:
- Required packages:
- Forbidden packages:
- Single-file or multi-file LaTeX project?:
- Preferred section file naming:
- Separate macros file?:
- Separate notation file?:
- Separate appendix file?:
- Separate theorem setup file?:
- Separate package setup file?:

## 13.2 Build environment assumptions
- OS:
- Expected TeX distribution:
- Whether `latexmk` is required or optional:
- Whether build scripts may patch PATH:
- Whether strict-layout is required:
- Whether PyMuPDF-based figure raster export is expected:
- Whether Poppler `pdftotext` is expected:

## 13.3 Theorem and cross-reference policy
- Allowed theorem-like environments:
- Disallowed theorem-like environments:
- `cleveref` naming must be validated?:
- Theorem-reference misnaming is a release blocker?:

## 13.4 PDF convergence and audit requirements
- Build log must be checked every compile-ready pass?:
- Direct PDF reading required before release claims?:
- Figure-page raster export required for figure passes?:
- Placeholder/scaffold-language scan required?:
- Overfull boxes block release?:
- Which PDF issues are blockers:
- Which PDF issues are warnings only:

---

# 14. Front Matter, Authorship, And Release Metadata

## 14.1 Authorship metadata
- Author list in order:
- Affiliations:
- Corresponding author:
- Blind review handling:
- Acknowledgments allowed in draft?:
- Funding statement:
- Conflict statement:
- Ethics / safety statement:
- Data / code availability statement:
- Camera-ready only fields to omit for now:

## 14.2 Release metadata
- Date policy:
- PDF author string:
- PDF title string:
- PDF keywords:
- arXiv-ready abstract version:
- Venue-neutral vs venue-specific release target:
- README release pointers needed?:
- Release notes needed?:

---

# 15. Explicit Unknowns And Stop Conditions

- Unknown theorem statements:
- Unknown proofs:
- Unknown experiments:
- Unknown baselines:
- Unknown metrics:
- Unknown citations:
- Unknown venue requirements:
- Unknown figures/tables:
- Missing source materials:
- Items that require human approval before drafting:
- Items the agent should not block on:
- Items that must block execution:

---

# 16. Agent Autonomy Preferences

- The agent should start by:
- The agent may create these folders/files without asking:
- The agent should preserve these files verbatim:
- The agent should prefer modularity vs speed:
- The agent should optimize for:
- The agent should avoid:
- The ideal first-pass outcome is:
- The ideal final outcome is:

---

# 17. Success Criteria

## 17.1 Done-state ladder
- Scaffold-complete requires:
- Formal-core-complete requires:
- Literature-grounded requires:
- Build-verified requires:
- Preprint-ready requires:
- Release-ready requires:
- Venue-submission-ready requires:

## 17.2 Success criteria
- Definition of a good first draft:
- Definition of an excellent draft:
- Top priorities:
  1.
  2.
  3.
- Main failure modes to avoid:
- Likely reviewer attacks to preempt:
- Strongest section(s) that must land well:

---

# 18. Fillable Quick-Start Appendix (Optional)

## 18.1 Five-sentence project summary
1.
2.
3.
4.
5.

## 18.2 Five must-mention bullets
- 
- 
- 
- 
- 

## 18.3 Five must-avoid bullets
- 
- 
- 
- 
- 

## 18.4 Drop-in theorem/proposition notes
- Note 1:
- Note 2:
- Note 3:

## 18.5 Drop-in citation notes
- Source 1:
- Source 2:
- Source 3:

---

# 19. Final Pre-Execution Checklist

- [ ] Topic clearly defined
- [ ] Canonical terminology locked
- [ ] Paper mode selected
- [ ] Prohibited content declared
- [ ] Main contribution stated
- [ ] Claims bounded
- [ ] Non-claims explicit
- [ ] Formal commitments locked
- [ ] Mainline vs optional variants specified
- [ ] Epistemic status policy specified
- [ ] Structure specified
- [ ] Citation policy specified
- [ ] Related-work families specified
- [ ] Figure specs and audit criteria specified
- [ ] Build assumptions specified
- [ ] Release metadata block filled
- [ ] Done-state target selected
- [ ] Freeze policy explicit
- [ ] Unknowns explicitly marked
- [ ] AI constraints explicit

---

# Final Control Instruction

When this file is filled, the AI must be able to use it as the primary execution brief for the project.

If legacy helpers such as `templates/paper_structure_spec_master.md` or `docs/paper_structure_spec_filled.md` also exist, this file takes precedence unless the user explicitly says otherwise.

If this file leaves a detail unspecified, the agent may choose a reversible low-risk default for structure and formatting, but not for scientific claims, citations, proofs, results, authorship metadata, or figure semantics.
