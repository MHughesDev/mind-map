# Agentic procedures — from top-tier sources to something new

Personal playbook for **multi-step agent workflows** that treat papers and files as **evidence**, not authority. The outcome is a **new composite**: a design, a method, a product direction, or a falsifiable plan—not a book report.

Use this as a **brainstorming session structure**: phases build on each other; you can assign each phase to a different agent or rerun phases with stricter constraints.

---

## Principles (non-negotiable)

1. **Separation of duties:** Ingestion ≠ extraction ≠ synthesis ≠ evaluation. Mixing them invites hallucinated citations and premature “answers.”
2. **Claims over summaries:** Every nontrivial statement should trace to a **claim ID** tied to a source location when possible.
3. **Explicit uncertainty:** Mark inference vs quotation; mark **A** (directly supported), **B** (reasonable extension), **C** (speculative).
4. **Adversarial pass:** Assume a reviewer wants to reject your synthesis; collect **falsifiers** early.

---

## Phase 0 — Charter (5–15 minutes of human time; agent can draft)

**Inputs:** Rough goal, audience, constraints (time, compute, regulation), and “what would count as new.”

**Agent output:**

- One-sentence **north star**.
- **Non-goals** (at least three).
- **Success criteria** (what artifact exists at the end; what would make you discard the run).

**Stop if:** The goal is “understand the paper” only—then use a lighter extractive template, not full synthesis.

---

## Phase 1 — Source intake & normalization

**Objective:** Make every downstream step **mechanical**.

**Steps:**

1. **Inventory** each source with: type, version, date, access constraints, and why it is in scope.
2. **Normalize** into a working format the agent can chunk (plain text with headings preserved; PDFs via OCR/text layer check).
3. **Segment** long documents: abstract, intro, methods, results, discussion, limitations—**even if** the agent later reads full text.

**Agent checklist:**

- [ ] Bibliography entries are consistent (title, authors, year, venue, identifier).
- [ ] Figures/tables referenced are listed (even if not reproduced).
- [ ] Known limitations section captured (many papers hide caveats there).

**Failure mode:** Starting synthesis on a **misidentified** version (wrong arXiv revision). Mitigation: record version IDs in the ledger.

---

## Phase 2 — High-fidelity extraction (claim mining)

**Objective:** Build a **claims ledger**: small, testable statements, each tied to evidence.

**Per source, repeat:**

1. **Extract claims** in atomic form (one mechanism, one result, one assumption per row).
2. Tag each claim: **Empirical** (data shown), **Theoretical** (proof/derivation), **Heuristic** (intuition or engineering rule).
3. Record **support**: section/figure/equation/table; quote or tight paraphrase **with location**.
4. Record **scope**: dataset, domain, scale, distribution shift caveats.

**Agent prompt pattern (conceptual):**

- “Do not synthesize across sources in this phase.”
- “If the paper does not justify a step, label it **gap**, not **fact**.”
- “Prefer the authors’ **limitations** over your extrapolation.”

**Output artifact:** Tables like in `session-template.md` (Claims ledger).

---

## Phase 3 — Cross-source reasoning (still not “creative” yet)

**Objective:** Map the **landscape** before inventing.

**Build:**

1. **Agreement graph:** clusters of claims that reinforce each other.
2. **Conflict list:** contradictions with hypothesized cause (different task, metric, population, or error).
3. **Dependency graph:** what must be true for claim X to matter for our goal?

**Agent tasks:**

- **Reconcile** conflicts only when evidence allows; otherwise keep **open tension**.
- **Flag overfitting to benchmarks**: impressive numbers that may not transfer.

**Output artifact:** Short “state of evidence” memo **without** your new idea yet—only structure.

---

## Phase 4 — Directed synthesis (“something new”)

**Objective:** Generate **hooks**: candidate new artifacts grounded in Phase 2–3.

**Rules:**

1. Each hook must cite **at least two claim IDs** *or* one claim plus an explicit **new assumption** labeled **C**.
2. Prefer **composable** ideas (modules, interfaces) over monolithic genius.
3. Produce **alternatives**: minimum three hooks with different tradeoffs (speed vs rigor, generality vs performance).

**Agent output formats (pick one primary):**

- **Architecture sketch:** components, data flows, failure containment.
- **Method sketch:** algorithmic steps, inputs/outputs, where learning enters.
- **Narrative sketch:** story arc for teaching or persuasion, with evidence anchors.

**Anti-pattern:** “Buzzword fusion” without a mechanism. Mitigation: require a **mechanism paragraph** per hook.

---

## Phase 5 — Red team / falsification

**Objective:** Try to break every hook **before** you fall in love with it.

**Per hook, answer:**

1. **Falsifiers:** What observation kills it?
2. **Baselines:** What simpler thing gets 80% of the benefit?
3. **Leakage / evaluation traps:** data snooping, trivial shortcuts, metric gaming.
4. **Operational hazards:** cost, latency, maintenance, human oversight boundaries.

**Optional agent role-play:** Skeptical reviewer, safety reviewer, “budget owner,” “junior maintainer.”

**Output artifact:** Ranked hooks with **risk tags** (technical, ethical, organizational).

---

## Phase 6 — Consolidation & next artifact

**Objective:** One coherent **deliverable** and a **minimal next experiment**.

**Deliverable options:**

| Artifact | Best when… |
|----------|------------|
| One-pager | You need alignment with others fast |
| Spec + interfaces | You will implement or delegate implementation |
| Experiment plan | Evidence is thin and you must de-risk |
| Public writeup | Goal is clarity, teaching, or critique |

**Must include:**

- **Decisions** (locked vs tentative).
- **Open questions** ranked by information value.
- **Stop rule**: when to archive vs iterate.

---

## Multi-agent choreography (patterns)

**Pattern A — Pipeline:** Agent 1 intake → Agent 2 claims → Agent 3 cross-map → Agent 4 synthesis → Agent 5 red team. Best for **traceability**.

**Pattern B — Ensemble:** Two independent syntheses from the same ledger → **merge** with a third agent judging conflicts. Best when **creativity** matters and you can afford duplication.

**Pattern C — Specialist swarm:** Parallel Phase 2 per source, then single **integrator** for Phase 3–4. Best for **many long papers**.

**Pattern D — Human gate:** Human approves ledger before synthesis; human approves hooks before red team depth. Best for **high-stakes** or regulated domains.

---

## Quality bar (quick self-score before you ship the brainstorm)

| Check | Question |
|-------|----------|
| Traceability | Can a reader see which source supports each important sentence? |
| Falsifiability | Is there a clear way you could be wrong? |
| Scope honesty | Are limitations of sources repeated in *your* proposal? |
| Novelty clarity | What is genuinely new vs rearrangement? |
| Next step | Is there one concrete next action beyond “more reading”? |

---

## When *not* to use this full stack

- Single short blog post → Phase 2 lite + Phase 6 memo only.
- Pure literature review with no new proposal → Phase 2–3, stop.
- Time-sensitive decision with no sources → charter + risk log; do not fake citations.

---

## Related file

Use **[session-template.md](./session-template.md)** as the blank worksheet for each run.
