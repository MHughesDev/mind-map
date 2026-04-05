# Template demo figure specifications (optional)

Use this file **only** when the paper itself documents the **research-paper template** or autonomous tooling (meta-paper). For normal research projects, define figures in `PROJECT_SPEC.md` Section 12 and the detailed layer (11A) for **your** topic, or remove unused figure placeholders from the manuscript.

This content was previously embedded in the default `PROJECT_SPEC.md` and is kept here so new projects start with neutral figure slots.

---

## Figure plan (demo)

### Figure 1
- Purpose: provide a one-glance overview of the autonomous paper factory from spec intake to final PDF
- Must show: the ordered stages parse, audit, ingest, generate, build, audit, repair, and finalize
- Section placement: Introduction or Method overview subsection
- Data required: no experimental data; only the workflow components defined in this repository
- Style notes: clean systems diagram with consistent boxes, arrows, and minimal annotation

### Figure 2
- Purpose: illustrate claim-to-evidence grounding and how declared sources constrain generated manuscript sections
- Must show: source materials, evidence store, claim map, section generators, and bibliography outputs
- Section placement: Method or Grounding subsection
- Data required: the parsed claim map, evidence store structure, and manuscript section targets
- Style notes: left-to-right dependency diagram with evidence objects in the center and outputs on the right

### Figure 3
- Purpose: visualize the build, audit, and repair loop used to improve the manuscript automatically
- Must show: LaTeX build, render audit, figure audit, placeholder checks, failure classification, repair pass, and rerun
- Section placement: Evaluation or System operation subsection
- Data required: the build runner, audit suite, failure classes, and repair loop states
- Style notes: loop diagram with a clear success exit and a clearly marked repair cycle

---

## Detailed layer (demo)

### Figure 1: Autonomous Paper Factory Overview

- Purpose: summarize the end-to-end autonomous paper workflow implemented by this template
- Section placement: early in the paper after the introductory framing of the system

#### Structural Description
- Type (graph, layered system, pipeline, geometric, etc): pipeline diagram
- Dimensionality: 2D abstract layered layout
- Core elements (nodes, edges, layers, arrows, regions, etc): rectangular stage boxes, directed arrows, one evidence store box, one manuscript output box, one final PDF box

#### Semantic Mapping
- Nodes represent: workflow stages and persistent artifacts
- Edges represent: execution order and data flow between stages
- Layers represent: intake, generation, and verification phases
- Colors represent: phase grouping only; color is stylistic rather than semantic
- Shapes represent: boxes for processes and rounded boxes for durable artifacts

#### Layout Constraints
- Global layout (left→right, top→bottom, radial, etc): left→right
- Relative positioning rules: spec parsing and auditing must appear first, evidence store must sit between ingestion and generation, and final PDF must appear at the far right
- Alignment constraints: all process boxes should share a common baseline with consistent horizontal spacing and non-overlapping arrows

#### Mathematical Correspondence
- Related equation/operator: N/A
- Mapping from math → visual:
  - Symbol → visual element: N/A
  - Operator → transformation in figure: N/A

#### Rendering Instructions
- Style (minimal, academic, annotated, etc): minimal academic systems diagram
- Label requirements: each stage must be labeled with the exact stage name, and the final output must be labeled as the polished PDF
- Tool preference (TikZ / matplotlib / external / UNKNOWN): TikZ
- Level of detail: medium

#### Caption Requirements
- Caption must explain: that the system is driven by `PROJECT_SPEC.md`, grounded by declared evidence, and closed by build-and-repair iteration
- Caption must NOT assume: prior knowledge of the repository layout or hidden intermediate stages

### Figure 2: Claim And Evidence Grounding Flow

- Purpose: show how claims, sources, and manuscript sections are linked through the evidence store
- Section placement: Method section after the source-ingestion and grounding description

#### Structural Description
- Type (graph, layered system, pipeline, geometric, etc): bipartite dependency diagram
- Dimensionality: 2D
- Core elements (nodes, edges, layers, arrows, regions, etc): source nodes, evidence-store node, claim nodes, section nodes, bibliography node, directed edges

#### Semantic Mapping
- Nodes represent: declared sources, normalized evidence records, claims, sections, and citation outputs
- Edges represent: grounding dependencies and traceability links
- Layers represent: source layer, evidence layer, claim layer, and manuscript-output layer
- Colors represent: source-related vs claim-related vs manuscript-related groups
- Shapes represent: rounded nodes for sources, square nodes for generated artifacts, plain rectangles for reasoning stages

#### Layout Constraints
- Global layout (left→right, top→bottom, radial, etc): left→right layered
- Relative positioning rules: sources on the left, evidence in the center, claims next, manuscript sections and bibliography on the right
- Alignment constraints: claims should align vertically with their downstream sections; bibliography should sit below section outputs without crossing edges

#### Mathematical Correspondence
- Related equation/operator: N/A
- Mapping from math → visual:
  - Symbol → visual element: N/A
  - Operator → transformation in figure: N/A

#### Rendering Instructions
- Style (minimal, academic, annotated, etc): annotated academic diagram
- Label requirements: labels must name the evidence store, claim map, and bibliography generation path explicitly
- Tool preference (TikZ / matplotlib / external / UNKNOWN): TikZ
- Level of detail: medium

#### Caption Requirements
- Caption must explain: how source declarations constrain generated prose and citations through an explicit grounding path
- Caption must NOT assume: that readers know the internal filenames or implementation details without labels

### Figure 3: Build, Audit, And Repair Loop

- Purpose: depict the autonomous verification cycle that detects, classifies, and repairs manuscript problems
- Section placement: Evaluation or System operation subsection near the build-and-audit discussion

#### Structural Description
- Type (graph, layered system, pipeline, geometric, etc): looped workflow diagram
- Dimensionality: 2D
- Core elements (nodes, edges, layers, arrows, regions, etc): build box, audit box cluster, classifier box, repair box, success exit box, feedback arrow

#### Semantic Mapping
- Nodes represent: executable build and verification stages
- Edges represent: control flow and retry behavior
- Layers represent: build, audit, diagnosis, and repair phases
- Colors represent: neutral process grouping only
- Shapes represent: process rectangles with one explicit success terminal

#### Layout Constraints
- Global layout (left→right, top→bottom, radial, etc): clockwise loop with a right-side success exit
- Relative positioning rules: build feeds audits, audits feed classification, classification feeds repair, and repair returns to build
- Alignment constraints: the loop must read clearly without arrow overlap; the success exit must be visually separate from the repair loop

#### Mathematical Correspondence
- Related equation/operator: N/A
- Mapping from math → visual:
  - Symbol → visual element: N/A
  - Operator → transformation in figure: N/A

#### Rendering Instructions
- Style (minimal, academic, annotated, etc): clean annotated loop diagram
- Label requirements: audits must name build audit, render audit, figure audit, and placeholder audit; the classifier must name content, figure, layout, and environment failures
- Tool preference (TikZ / matplotlib / external / UNKNOWN): TikZ
- Level of detail: medium

#### Caption Requirements
- Caption must explain: that the system iterates until the manuscript passes quality gates or a hard blocker stops execution
- Caption must NOT assume: that every failure is automatically repairable or that the system may invent around missing evidence
