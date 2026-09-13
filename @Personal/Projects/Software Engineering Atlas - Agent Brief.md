---
title: Software Engineering Atlas - Agent Brief
type: reference
status: draft
tags: [meta, atlas, prompt, agent-brief]
updated: 2026-09-13
---

# Agent Brief — Design the Software Engineering Atlas

> Copy everything below the rule into the agent. It is self-contained: it assumes no
> prior conversation. Rationale for these constraints is in
> `Software Engineering Atlas - Design Brief.md`.

---

## TASK

Design the **Software Engineering Atlas**: a reference library covering the knowledge
and judgment required to design, build, verify, ship, operate, and evolve software
systems. Design the map and the architecture. **Do not write the references.**

Your output is a design proposal I will implement. It must be concrete enough to
build from, and it must pass the route test below.

## CONTEXT

I am a solo builder. I develop applications with Claude as my engineering partner;
together we cover the responsibilities of an entire technical organization. I need
references I consult when making decisions across the whole lifecycle — product,
design, architecture, data, delivery, operation, evolution.

The subject is judgment, not syntax: what the decision is, what the options are, why
each works, when each fails, how to tell which case I am in. Language- and
framework-specific practice belongs in the library, but as a separate, dated,
disposable class of content — not mixed into the durable material.

I already built a v1 and it is the wrong shape. It is seven agent-directive rules
files (~160–900 lines each) split by deployment topology: Frontend, Backend/API,
Data Layer, Auth/Security, Deployment/Operations, SaaS, Agent Harness. Their
governing constitution caps files at ~1,000 lines, forbids citations and publication
dates, and requires imperative voice. Those are correct rules for a rules file loaded
into an agent's context mid-task. They are the wrong rules for a reference consulted
while deciding, which is what I now need. Part of your job is to resolve that
conflict rather than inherit it.

## THE ORGANIZING PROBLEM

Do not organize by job function, architectural layer, or lifecycle phase. Every such
split fractures the cross-cutting concerns, and the cross-cutting concerns are where
the expensive mistakes live.

The test case: **where does idempotency live?** In a topology split, the frontend owns
retry behavior, the backend owns handler design, the API owns the contract, the
distributed-systems volume owns delivery guarantees, and the data volume owns the
uniqueness constraint. Five owners is zero owners. Your organization must not have
this property, for idempotency or for anything else.

Derive the axis from first principles. A candidate worth considering, which you may
adopt, refine, or reject with reasons: a decision earns a reference when it is a
**commitment, made under uncertainty, that is expensive to reverse** — so group
decisions by the commitment surface they share, and order them by reversal cost.
Commitments about *meaning* (what the domain words denote) are trivial to change on
day one and ruinous on day four hundred. Commitments about *truth and durability*
(what is authoritative, what is derived, what survives) are the most expensive class,
because data outlives every rewrite.

Whatever axis you choose, justify it, and name at least two axes you rejected and why.

## DELIVERABLE

In this order:

**1. Derivation.** The organizing axis, its justification, and the rejected
alternatives. Before any volume is named.

**2. Volume map.** The volumes, each with: title; the decisions it owns; what it
deliberately excludes and which volume owns that instead; and its major internal
subject areas.

**3. Per-volume tiering.** Each volume marked:
- **Universal** — every project touches it.
- **Conditional** — triggered by a checkable property of the system (*handles money*,
  *has tenants*, *is realtime*, *runs models*, *ships to devices*, *touches regulated
  data*). State the trigger, not the domain name.
- **Technology-local** — bound to a stack and version. State its half-life and review
  interval.

**4. Routing table.** Per the route test below. Mandatory.

**5. Content model.** How knowledge is represented. Address specifically:
- The unit of authorship versus the unit of retrieval. I need references deep enough
  to study and precise enough for an agent to retrieve from without losing the
  assumptions that make the guidance valid. Resolve this structurally — not by
  choosing one and hoping.
- The content types you introduce (concept, mechanism, decision procedure, pattern,
  failure mode, procedure, evidence, …) and why each distinction earns its keep.
- Stable identity when content is renamed, moved, split, or merged.
- How applicability is expressed: language, version, platform, workload, scale.
- How maturity and evidence are expressed: established principle, conditional
  recommendation, emerging technique, disputed claim, superseded guidance.
- Where reusable knowledge ends and per-project decisions begin.

**6. Content half-life partition.** Principles (decades), practices (years),
technology facts (months) have different review cadences and different evidence bars.
Show how the architecture keeps fast-rotting content from contaminating durable
content.

**7. Contribution lifecycle.** How I or an agent adds, corrects, expands, splits,
merges, supersedes, or retires content. Specify: what must accompany a change; how
dependent content is found; how duplication and contradiction are *detected*; what
validation runs; what can be accepted without review and what cannot, and the basis
for that line; how concurrent edits reconcile; how a change is reversed; how
superseded guidance stays traceable without reading as current. Review must be
practical for one person.

**8. Research loop.** I will run agents on recurring research loops against this
library. Specify how they choose topics, evaluate source authority and independence,
distinguish new evidence from a repeated claim, handle disagreement between sources,
separate established practice from emerging technique, decide whether a finding
materially changes existing guidance, and avoid treating agent-generated text as
independent evidence. Specify when a topic is done and when it is revisited.
Recency is not authority.

**9. Reconciliation with what exists.** Map each of the seven v1 guides onto the new
structure — kept as a compiled artifact, absorbed, split, or retired — and name any
content in them your map has no home for. Then state the amended rule, for each
genre, on: the size cap, the citation ban, the imperative-voice requirement, and the
prohibition on splitting by depth.

**10. Quality and coverage criteria.** How I detect a substantive gap, weak guidance,
stale content, or a degraded entry. Do not use file count, word count, or update
frequency as a proxy for quality. Include the failure modes of the knowledge system
itself and the mechanism that catches each.

**11. Build sequence.** What gets built first. The maintenance layer and the entry
schema precede content production; the first content is one reference that proves the
schema, not ten outlines.

**12. One volume worked to full depth** — the complete specification for a single
volume, including three sample entries in full entry form. This is how I judge
whether "substantial" means anything in your proposal.

**13. Three worked traces.** Show the system behaving: adding a new subject; revising
guidance after new evidence contradicts it; and correcting a bad change that has
already propagated into several references.

## ROUTE TEST — the primary acceptance gate

A taxonomy is good if and only if a realistic question lands in exactly one place.
Publish a table mapping every question below to **exactly one** owning volume and the
entry within it.

1. Should this be one service or two?
2. Should this field be nullable?
3. A retried webhook double-charged a customer. Where is the guidance?
4. Postgres or SQLite for this application?
5. Should the agent write this module, or should I?
6. How do I roll back a deploy that included a destructive migration?
7. Should "cancelled" be a status column or a separate table?
8. Is this library safe to depend on?
9. A page is slow. Where do I start?
10. Should this run as a background job or inline?
11. How do users delete their account such that the data is actually gone?
12. Two users edited the same record. What should happen?
13. Should I add a cache here?
14. What must be in the spec before Claude starts this feature?
15. Is this API change breaking?
16. Should tenants share a database?
17. An LLM feature costs too much per request.
18. A subsystem needs replacing. How, without a feature freeze?

**A question with two plausible owners is a boundary defect. A question with none is
a coverage defect.** Fix both in the map. Do not resolve them in prose.

## HARD CONSTRAINTS

1. No volume titled with a job function, an architectural layer, or a technology. If
   a volume's honest title is "Frontend," "Backend," "DevOps," or "React," the
   boundary is a topology split — redraw it.
2. Every volume names at least one decision it **exclusively** owns, phrased as a
   question.
3. Every volume names its exclusions and where they live instead.
4. Volume count is derived, never chosen. No round-number targets. If the derivation
   yields 9 or 31, say so and defend it.
5. Name no storage technology, tool, or file format before stating the requirement
   that selects it. Separate essential capabilities from implementation choices.
6. **Do not restate what a competent frontier model already knows.** A section a model
   can reproduce from memory is dead weight that costs tokens to retrieve and adds
   nothing. Concentrate substance where recall fails under pressure: tradeoffs,
   failure modes, applicability limits, decision procedures, and version-specific
   facts. "Substantial" means dense, not long.
7. Never substitute a list of desirable properties for a mechanism. "Ensures
   consistency" is not a design — the process that *detects* an inconsistency is.
8. State every consequential choice as a choice, with its alternative and what it
   costs. Flag unresolved decisions explicitly instead of defaulting past them.
9. Distinguish the library's intended scope from the order in which it gets
   populated. A staged plan must preserve the full scope.

## WHAT I AM JUDGING

Whether the boundaries hold under the route test. Whether a volume's exclusions prove
its ownership. Whether the retrieval unit carries its own assumptions. Whether the
maintenance design specifies mechanisms rather than intentions. Whether the worked
volume is deep enough to be worth consulting twice.

Not length, not volume count, and not how many desirable properties you can name.
