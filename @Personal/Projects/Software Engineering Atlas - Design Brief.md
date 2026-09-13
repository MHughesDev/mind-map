---
title: Software Engineering Atlas - Design Brief
type: reference
status: draft
tags: [meta, atlas, knowledge-architecture, design-brief]
updated: 2026-09-13
---

# Software Engineering Atlas — Design Brief

> The problem statement, diagnosis, and design constraints for a reference library
> covering the judgment required to design, build, ship, operate, and evolve software.
> This brief defines the problem and the shape of the answer. The companion file
> `Software Engineering Atlas - Agent Brief.md` is the prompt handed to the agent
> that produces the map itself.

---

## PART 0 — WHAT ALREADY EXISTS

Before designing anything, the current state:

**`@Personal/Resources/skills/` — a v1 of this library already exists.**

| File | Lines | Genre |
|---|---|---|
| `AGENT_HARNESS_GUIDE.md` | 896 (v3.0.0) | agent-directive |
| `BACKEND_API_GUIDE.md` | 193 | agent-directive |
| `AUTH_SECURITY_GUIDE.md` | 192 | agent-directive |
| `DEPLOYMENT_OPERATIONS_GUIDE.md` | 177 | agent-directive |
| `FRONTEND_UI_GUIDE.md` | 173 | agent-directive |
| `SAAS_PRODUCT_GUIDE.md` | 163 | agent-directive |
| `DATA_LAYER_GUIDE.md` | 162 | agent-directive |
| `GUIDE_AUTHORING_GUIDE.md` | 132 | constitution |
| `_INDEX.md` | 26 | routing layer |

**`RULES.md`** — the vault constitution: two top-level sections (`Core Domains/`,
`@Personal/`), a three-tier content model (folder = subject area, file = topic,
section = module), a mandatory folder-note per folder, a frontmatter schema, and
move-never-delete.

**`Core Domains/Technology/Information Technology/`** — already contains
`Cloud Computing/`, `Networking/`, `Data Engineering/`, `DevOps/` as *learning*
material. The new library overlaps this subject space and must resolve ownership
rather than duplicate it.

---

## PART 1 — DIAGNOSIS: WHAT IS ACTUALLY BLOCKING THIS

The stated blocker is "I can't figure out what the handbooks are." That is not the
blocker. Three findings:

### 1.1 The existing constitution makes the requested library illegal

`GUIDE_AUTHORING_GUIDE.md` is a well-built set of rules — for the genre it governs.
Four of its rules directly forbid the library now being asked for:

| Current rule | Requirement it blocks |
|---|---|
| "Cap: ~1,000 lines per guide" | full-length references, explicitly not 1–2,000 line guides |
| "Never include research metadata — no citations, vendor attributions, publication dates" | research loops proposing evidence-backed updates with provenance and maturity labels |
| "Guides command; rationale rides along" | presenting alternatives, mechanisms, tradeoffs, and when each option fails |
| "Never split a guide by depth" | a volume large enough to need internal depth structure |

These are correct rules for an agent-facing rules file loaded mid-task, and wrong
rules for a reference consulted while deciding. The attempt has been to grow a rules
file into an encyclopedia, and the constitution keeps correctly stopping it. **That
is the blocker, not the topic list.**

### 1.2 Both candidate maps are the org chart in a costume

The v1 seven — Frontend / Backend-API / Data-Layer / Auth-Security /
Deployment-Ops / SaaS / Agent-Harness — is a **deployment-topology split**: where
code physically sits.

The externally-proposed 24-handbook map states it is "organized around decisions,
rather than job titles," then lists Frontend Application Architecture, Backend and
Application Service Design, API and Integration Design, Data Engineering, Security
Architecture, Testing, Build/CI-CD, Infrastructure, Observability, Performance.
Those *are* the job titles. It is a bootcamp curriculum with verb-phrase group
headers pasted on top, and its six groups ("Define / Structure / Data / Protect /
Deliver / Evolve") are waterfall phases — an ordering that contradicts the stated
use, which is consulting a reference when a decision arrives.

The diagnostic: **ask where idempotency lives.** Frontend owns retry behavior.
Backend owns handler design. API owns the contract. Distributed Systems owns
delivery guarantees. Data owns the uniqueness constraint. Five owners means zero
owners. A topology split fractures every cross-cutting concern — and the
cross-cutting concerns are where the expensive mistakes are.

### 1.3 The largest gap in both maps is the actual practice

The whole practice is *building software with an AI agent*. In the 24-map that is
a half-slot inside one handbook. In v1 it is absent — `AGENT_HARNESS_GUIDE` governs
agents *inside the shipped product*, not the agent *doing the building*.

Specifying work to an agent, structuring a repo so an agent can navigate it,
deciding what to verify versus trust in generated code, preventing context rot,
choosing when to hand over versus write by hand — that is the most repeated,
highest-leverage, least-documented decision surface in this operation. It warrants
the most developed volume in the library.

Also absent from both maps:

- **Dependency selection / build-vs-buy** — made constantly by a solo builder, reversed rarely.
- **Scope discipline** — what not to build; the dominant solo-builder failure mode.
- **Licensing, ToS, and legal constraints** as design inputs.
- **Cost** as a first-class constraint rather than a footnote to performance.
- **Time, order, and state** as one subject rather than five fragments.

---

## PART 2 — THE DESIGN

### 2.1 Two genres, one body of knowledge, joined by compilation

Do not replace the guides. Put references underneath them.

- **Reference** — long, expository, uncapped, cited, dated, maturity-labeled.
  Owns the decision space: what the decision is, what the options are, the mechanism
  that makes each work, when each fails, what evidence supports it, what is
  contested. Read when judgment is needed; retrieved when a default does not fit.

- **Guide** — the existing genre, unchanged. Capped, imperative, defaults table,
  checklist, no citations. Loaded into an agent's context to constrain execution.

**The guide is a projection of the reference.** Every default in a guide names the
reference entry that justifies it. A research loop updates the reference; a
recompile pass propagates changed defaults into the guide and bumps its version.

This resolves all four conflicts in §1.1 at once: the size cap and citation ban stay
on the guide, where they are right, and lift on the reference, where they would be
crippling. It also preserves the existing investment — the seven guides become the
first compiled outputs, and `AGENT_HARNESS_GUIDE` v3.0.0 is the existence proof
that the guide genre works.

A third element, under-weighted in both candidate maps:

- **Record** — the per-project decision log. Not reusable knowledge: the actual
  choices for one application, and what happened as a result. This is the only
  content in the system that a frontier model cannot already obtain, and it is the
  feedback edge — a recorded outcome is the evidence that revises a reference.
  Without it, the library is a worse copy of public documentation.

### 2.2 The retrieval unit is the entry, not the volume

A 400-page reference is unusable to an agent. That is precisely why the v1 files are
160 lines. Resolve the tension structurally instead of picking a side:

A reference is a sequence of **entries** plus the connective argument between them.
An entry is one decision, mechanism, pattern, or failure mode, and it is
**self-sufficient for its own assumptions**: an entry lifted out of its volume still
states its own preconditions, applicability envelope, and what it trades away.

That invariant — enforced at the entry level, not left to the retriever grabbing
enough surrounding text — is what prevents context-stripped guidance. Its
consequence is that a reference can run to 15,000 lines without becoming
unretrievable, because nothing ever loads 15,000 lines. **Depth becomes free.**

### 2.3 Organize by commitment cost, not by subject area

The first-principles question is not "what areas of software exist." It is "what
makes a decision worth a reference at all." A decision earns one when it is a
commitment, made under uncertainty, that is expensive to reverse.

So bound and order the library by **reversibility**. Volumes group decisions that
share a commitment surface:

| Commitment class | What is being committed to | Reversal cost |
|---|---|---|
| **Meaning** | what the system is about; what the words denote; what is true in the domain | trivial on day 1, ruinous on day 400 — everything downstream encodes it |
| **Shape** | where boundaries fall, what depends on what, what is contract vs. internal | determines what remains *possible* |
| **Truth & durability** | what is authoritative, what is derived, what survives, what may be deleted | highest — data outlives every rewrite |
| **Trust** | who may do what; what is assumed about a caller; what happens when that is wrong | high, and usually discovered by an incident |
| **Time, order & state** | concurrency, idempotency, clocks, state machines, retries | cross-cutting; permanently mis-filed by topology splits |
| **Change** | how code becomes running software, repeatably and reversibly | moderate, paid on every release |
| **Stress behavior** | load, failure, and cost — one subject, not three | moderate, discovered late |
| **Evidence** | how you know it works: verification, observability, analytics | compounding — absence is invisible until it is not |
| **Collaboration** | how the human and the agent divide and check work | gates the quality of every row above |
| **Continuation** | upgrade, migrate, deprecate, retire | high, and always underestimated |

This is deliberately *not* "here are your 11 volumes." Drawing boundaries against the
route test (§3.2) is the agent's job, and the research breadth required to do it well
is the reason to run an agent at all. But this is the axis, and it beats both
candidate maps because it sorts decisions by **what it costs to be wrong** — which
is exactly how a solo builder should allocate thinking time.

### 2.4 Partition by half-life, because half-life sets the maintenance obligation

| Band | Half-life | Review cadence | Evidence bar |
|---|---|---|---|
| **Principles** | decades | rarely; a revision is an event | high — revision requires argument, not a link |
| **Practices** | years | periodic | moderate — adoption evidence and stated conditions |
| **Technology facts** | months | continuous | low bar to add, hard requirement to date and version |

This is why language-specific and framework-specific practice belongs in the library
but must never be mixed into the durable volumes: it has a six-month half-life and
must be structurally quarantined, dated, and cheap to discard, so its rot cannot
contaminate the material that is still true in five years.

It also gives the research loops obvious targets: they run constantly against the
technology band, periodically against practices, and almost never against principles.

### 2.5 Scope tiers by trigger, not by "core versus extra"

- **Universal** — every project touches it.
- **Conditional** — triggered by a checkable property of the system: *it handles
  money*, *it has tenants*, *it is realtime*, *it runs models*, *it ships to
  devices*, *it touches regulated data*. State the trigger, not the domain name — a
  trigger can be evaluated against a project; a domain name cannot.
- **Technology-local** — bound to a stack and version; dated and disposable.

---

## PART 3 — WHAT THE AGENT MUST GENERATE

### 3.1 Deliverable

A design proposal containing, in order: the derivation of the organizing axis; the
volume map; per-volume specification; the routing table; the content model; the
contribution and research lifecycle; the reconciliation with what already exists;
and the build sequence. One volume specified to full depth as a worked example.

### 3.2 The route test — the primary acceptance gate

A taxonomy is good if and only if a realistic question lands in exactly one place.
The agent receives this set up front and must publish a routing table mapping each
question to exactly one owning volume and the entry within it.

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

Several are chosen to stress the seams: #3 is the five-owner idempotency problem,
#6 spans release and data, #11 spans privacy, data lifecycle, and identity, #17
spans cost and models. **A tie is a boundary defect. A gap is a coverage defect.**
Both must be fixed in the map, not explained away in prose.

### 3.3 Hard constraints on the output

1. **Derivation precedes enumeration.** State and justify the organizing axis before
   naming a single volume, and name at least two rejected axes with the reason for
   rejection. Naming what was rejected is the only evidence that a choice was made.
2. **No volume titled with a job function, an architectural layer, or a technology.**
   If a volume's honest title is "Frontend," "Backend," "DevOps," or "React," the
   boundary is a topology split and must be redrawn.
3. **Every volume names at least one decision it exclusively owns**, phrased as a
   question, that no other volume owns.
4. **Every volume names what it deliberately excludes**, and which volume owns that
   instead. Exclusions are how ownership is proven.
5. **Volume count is derived, not chosen.** No round-number targets. If the
   derivation yields 9 or 31, say so and defend it.
6. **Tier every volume** — universal / conditional (state the triggering system
   property) / technology-local (state the half-life and the expiry review interval).
7. **One volume worked to full depth**, including three sample entries in complete
   entry form. One real sample is worth twenty outlines, and it is the only way to
   check whether "substantial" means anything in the proposal.
8. **Reconcile with what exists.** Map each of the seven current guides onto the new
   structure — kept as a compiled guide, absorbed, split, or retired — and name any
   content in them the new map has no home for. Resolve placement against `RULES.md`
   (`Core Domains/` versus `@Personal/`) and the subject overlap with
   `Core Domains/Technology/Information Technology/`.
9. **Resolve the four constitution conflicts** from §1.1 explicitly, stating the
   amended rule for each of the two genres.
10. **The build sequence establishes the maintenance layer before content.** The
    first thing built is the entry schema plus one reference that proves the schema —
    not ten reference outlines.

### 3.4 Anti-requirements

- **Do not restate what a competent model already knows.** A section a frontier model
  can reproduce from memory is dead weight that costs tokens to retrieve and adds
  nothing. Concentrate substance where recall actually fails under pressure:
  tradeoffs, failure modes, applicability limits, decision procedures, and
  version-specific facts. This is the honest reading of "substantial" — density, not
  word count.
- **Do not name a storage technology, tool, or file format** before the requirements
  that would select it have been stated.
- **Do not treat volume count, word count, or update frequency as evidence of
  coverage.**
- **Do not substitute a list of desirable properties for a mechanism.** "Ensures
  consistency" is not a design; the process that *detects* an inconsistency is.

---

## PART 4 — NAMING

| Element | Name | Why |
|---|---|---|
| The collection | **Software Engineering Atlas** | an atlas is by definition a complete map collection, is revised in *editions*, and is honest about the artifact: maps of a subject space, not one narrative |
| A volume | **Reference** (`*_REFERENCE.md`) | plain, accurate, and already the value of `type:` in the vault frontmatter schema |
| The retrieval unit | **Entry** | |
| The agent-facing compiled layer | **Guide** (`*_GUIDE.md`) | unchanged; it already works |
| The per-project log | **Record** | |

Rejected: *Living Software Engineering Knowledge Base* — four abstract nouns and a
self-congratulatory adjective. "Living" is a claim about behavior, not a name, and
nothing in the name makes it true. Acceptable alternates: **Corpus** (accurate,
academic), **Compendium** (accurate, stuffy). Avoid *Codex* (precious) and *Canon*
(implies closed).

One line to remember the architecture by:

> **The Atlas maps the subject space. Each Reference owns a region. Guides are what
> you hand the agent. Records are what actually happened.**

---

## PART 5 — OPEN DECISIONS

These are not for the agent to assume. They need an answer, and the brief flags them
rather than hiding them in a default.

1. **Placement.** `@Personal/Resources/` (an engineered instrument with its own
   schema and versioning) versus `Core Domains/Technology/` (general knowledge about
   a field). `RULES.md` §10.1 splits on "studying the world" versus "producing
   something" — the Atlas is arguably both. Current lean: `@Personal/Resources/`,
   because it carries its own schema, version discipline, and agent-facing contract,
   none of which fit the strict folder-note taxonomy.
2. **Whether references live under the folder-note mandate** (`RULES.md` §4.1) or are
   exempt like `RP/` containers. A reference composed of entries is structurally
   unlike a learning topic made of modules.
3. **Whether compilation from Reference to Guide is mechanical or authored.**
   Mechanical keeps them in sync and constrains what a guide can say; authored
   produces better guides and will drift.
4. **How an outcome enters the system.** The Record is the feedback edge, and nothing
   in v1 captures what happened after a decision. Without a low-friction capture
   step, this edge will be designed and never used.
