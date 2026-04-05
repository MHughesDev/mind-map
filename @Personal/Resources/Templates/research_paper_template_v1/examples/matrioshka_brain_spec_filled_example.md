# Filled Example — Matrioshka Brain Paper

This file is a legacy example project. For new work, use `PROJECT_SPEC.md` as the controlling brief and treat this file as an illustrative content sample only.

## 1. Project Identity
- Working title: The Matrioshka Brain: A Layered Cognitive State Architecture for Persistent Agentic Reasoning
- Short title / running title: Matrioshka Brain
- Paper type: theoretical / systems / methods hybrid
- Primary contribution type: new formal framework
- Secondary contribution types: operator family, cognitive-state architecture, consistency functional
- Primary field: AI systems
- Subfield: agentic reasoning architectures, mathematical foundations of cognitive state
- Keywords: agentic systems, cognitive state, multilayer graphs, spectral methods, persistent reasoning, thought structures

## 2. Deliverables
- full LaTeX manuscript
- appendix scaffold
- bibliography scaffold
- figure placeholders
- README
- build instructions

## 3. Reader Model
- Primary audience: AI systems researchers, mathematical ML researchers, agent-architecture researchers
- Secondary audience: graph learning / topology / formal methods researchers
- Must explain from scratch: exact ontology of external/session/global state, open vs closed thought distinction, operator family, consistency functional

## 4. Core Purpose
- Main objective: define a formal cognitive-state architecture in which explicit thought objects live across abstraction layers and evolve under operator-based state transitions
- Core research question: how can agentic reasoning be organized as a persistent layered internal state rather than transient prompt-only computation?
- Main thesis: a layered thought-state system with explicit open/closed state separation, vector-addressable thought objects, directed cross-layer relations, and a consistency energy can serve as a principled substrate for persistent agentic reasoning
- Why it matters: current agentic systems are often prompt-fragmented, memory-shallow, and weakly structured; this paper proposes a more principled internal state model

## 5. Problem Statement
- Informal problem: current agents lack a durable, structured internal cognitive state
- Formal problem: define an internal mathematical object MB_t with state spaces, relations, operators, and coherence diagnostics
- Non-goals: this paper does not empirically prove superiority over all existing architectures; it introduces the formal framework first

## 6. Claim Map
- Claim 1: the external/session/global split yields a cleaner ontology for agentic state
- Claim 2: open-thought/session and closed-thought/global separation supports more disciplined persistence
- Claim 3: a layered directed graph with vector-labeled thoughts and a consistency energy yields useful diagnostics for contradiction, cyclicity, and fragmentation
- Claim 4: offline consolidation is a necessary architectural component for long-term coherence

## 7. Formal Setup
- Core mathematical objects: time-indexed external state E_t, session state S_t, global state G_t, thought set X_t, relation graph M_t, layer set Lambda, vector space V, consistency functional E_MB
- Sets: time, agents, layers, relation types, statuses
- Operators: ingest, retrieve, interpret, abstract, decompose, revise, close, reopen, consolidate, merge, split, rewire, relevel, summarize, repair
- Relations: supports, contradicts, depends_on, implies, elaborates, abstracts_to, decomposes_to, revises, summarizes
- Assumptions: open and closed states are disjoint; session and global state are disjoint; every thought has a layer and vector

## 8. System Details
- Method/system name: Matrioshka Brain
- Plain summary: a persistent thought-based cognitive architecture for agents
- Technical summary: a dynamic multilayer directed signed weighted vector-labeled cognitive graph with separate open and closed state spaces and operator-driven transitions
- Online/offline modes: yes
- Multi-agent behavior: yes, via shared and optionally private session regions
- Memory/state model: session stores open thoughts; global stores closed persistent thoughts

## 9. Evidence Plan
- Main evidence types: formal definitions, operator system, consistency functional, theoretical argumentation, synthetic examples
- Empirical evaluation: UNKNOWN
- Baselines: UNKNOWN
- Metrics: conceptual and structural only unless later experiments are added

## 10. Results Requirements
- Since this is theory-first, main results are formal clarity, operator completeness, architectural coherence, and a path to future higher-order extensions
- Do not claim empirical superiority without experiments

## 11. Literature Policy
- Must discuss: memory architectures, agentic systems, graph-based reasoning, spectral methods, higher-order/topological reasoning where relevant
- Citation rule: every technical comparison or literature claim should be cited
- No fabrication rule: strict

## 12. Style
- Tone: formal, precise, mathematically serious
- Style: intuition followed by formalism
- Voice: use “we”
- Jargon: moderate to high, but define terms carefully

## 13. Structure
Required sections:
- Abstract
- Introduction
- Related Work
- Preliminaries / Background
- Problem Setup
- Method / Theory
- Discussion
- Limitations
- Conclusion
- Appendix

## 14. Figures
- Figure 1: conceptual diagram of external/session/global state
- Figure 2: layer structure and directed edges
- Figure 3: operator lifecycle for a thought from ingestion to closure/reopening/consolidation

## 15. LaTeX / Build
- One-column preferred for preprint
- article class acceptable
- Use amsmath, amsthm, mathtools, graphicx, booktabs, hyperref, cleveref, enumitem
- Use BibTeX unless venue requires otherwise

## 16. Transparency
- Unknown experiments must remain explicit
- Incomplete proofs must be labeled as sketches or placeholders
- Missing citations must be recorded in docs/MISSING_INPUTS.md

## 17. AI Rules
- AI may draft prose and LaTeX
- AI must not invent literature or results
- Unknown handling: continue with placeholders and explicit TODO markers
