---
name: guide-authoring-guide
description: Use when creating, editing, splitting, or registering any guide in this skills vault. Consult before writing a new guide file, before modifying an existing guide's structure, and whenever a guide approaches the size cap. This file is the constitution — all other guides must conform to it.
version: 1.0.0
date: 2026-09-11
scope: Guide template, head requirements, size caps, splitting rules, naming, index registration, writing style for agent-executable guides.
---

# GUIDE AUTHORING GUIDE
### The constitution for every guide in this vault

---

## HOW TO APPLY THIS FILE

You (the coding agent) are creating or modifying a guide in this skills vault. Execute:

1. Confirm the topic is not already covered — read `_INDEX.md` first. Extend an existing guide before creating a new one.
2. Author the guide using the Head Template (Part 1) and Body Rules (Part 2), in that order.
3. Enforce the writing style rules (Part 3) on every line.
4. Check the size cap (Part 4). If exceeded, split by topic per Part 4 — never by depth.
5. Register the guide in `_INDEX.md` (Part 5). A guide not in the index does not exist.
6. Walk the checklist (Part 6) before declaring done.

**Prime directive:** Every guide is a monolithic, self-contained `.md` file written as directives TO a coding agent — not documentation for humans. Progressive disclosure happens at the vault level (the index) and inside the file (the head), never by fragmenting a guide into satellite files.

---

## PART 0 — MENTAL MODEL

- **One guide = one file = one topic.** A guide must remain fully usable when copied alone into any session, any tool, any runtime. No relative links to sibling files; cross-references are by guide name and part number ("see AGENT_HARNESS_GUIDE.md, Part 10").
- **The head is the load-bearing 150 lines.** An agent that reads ONLY the head must still behave correctly — just with less nuance. Everything below the head is elaboration an agent can grep into selectively.
- **The index is the routing layer.** Agents read `_INDEX.md` first, then open only matching guides. The index is the only file that must stay tiny.
- **Guides command; rationale rides along.** Directives with a one-clause "because" outperform both bare commands and essays.
- **Defaults are governed by evidence.** Every concrete number in a guide is a starting point to be overridden by measurement, and every guide must say so.

**Never (anti-patterns):**
1. Never create a references/ subfolder or split a guide by depth — split by topic into a sibling guide.
2. Never write "when to use" information anywhere except the frontmatter `description`.
3. Never include research metadata — no citations, survey names, vendor attributions, publication dates, or "studies show." Only decisions and guidelines.
4. Never bury a decision in prose when a table can carry it.
5. Never let two guides own the same decision — one guide owns it; others cross-reference it.
6. Never ship a guide without registering it in `_INDEX.md`.
7. Never use relative links between vault files.
8. Never exceed the size cap "just this once."

---

## PART 1 — HEAD TEMPLATE (required, in this exact order)

**1. YAML frontmatter** — exactly these fields:

```yaml
---
name: kebab-case-guide-name
description: Use when <trigger contexts>. Consult even if <adjacent phrasing that should still trigger>.  # pushy, 1–3 sentences, ALL when-to-use info lives here
version: MAJOR.MINOR.PATCH
date: YYYY-MM-DD
scope: Comma-separated list of the decisions this guide owns.
---
```

- `description` is the triggering mechanism. Make it slightly pushy — under-triggering is the common failure, not over-triggering.
- Bump MAJOR for restructures, MINOR for new parts/decisions, PATCH for corrections. Update `date` on every edit.

**2. Title block** — `# NAME` + one-line subtitle stating audience ("Drop-in rules file for coding agents building X").

**3. HOW TO APPLY THIS FILE** — a numbered operating procedure (4–7 steps) telling the agent the reading order, what to classify first, what to enforce, and how to verify done. Include a bolded **Prime directive** — the one sentence that survives if everything else is forgotten.

**4. PART 0 — MENTAL MODEL** — the compressed "why" (5–8 bullets) followed by a **Never** list of 8–15 anti-patterns with one-clause reasons.

**5. DEFAULTS AT A GLANCE** — one table of the concrete defaults an agent needs while working (numbers, tiers, thresholds), closing with the line: *"These defaults are starting points; override only on measured evidence, and record the evidence."*

---

## PART 2 — BODY RULES

- **Numbered parts with stable, greppable headers**: `## PART N — TOPIC` in caps. Never renumber existing parts in MINOR/PATCH edits — append.
- **Contents list** immediately after the head: one line per part. This enables partial reads (grep header → read range).
- **Decision tables** for every either-or choice: situation → choice, with an "adopt when X is measured" trigger column where applicable.
- **Phased build order** part: what to build first → last, each phase with an exit bar.
- **AI-AGENT-APP CONSIDERATIONS** part (for software-topic guides): how the topic changes when the app contains internal LLM agents; cross-reference AGENT_HARNESS_GUIDE.md by part number.
- **Final part is always the CHECKLIST**: binary, walkable items an agent states as satisfied / deferred (with reason) / N/A.

---

## PART 3 — WRITING STYLE

- Second-person imperative, addressed to the coding agent: "Use X. Enforce Y."
- One-clause rationale on non-obvious rules: "Do X because Y." Skip rationale only when self-evident.
- Concrete over abstract: numbers, header names, status codes, field names — never "appropriately sized."
- Flag contested ground honestly: "Both are defensible; default to X, switch when Z is measured."
- Mark volatile items: anything likely to change gets "verify current state before relying on this."
- No filler, no marketing tone, no hedging stacked on hedging. Density is the feature.

---

## PART 4 — SIZE CAP AND SPLITTING

- **Cap: ~1,000 lines per guide.** Approaching 900, plan a split.
- **Split by topic, never by depth**: extract a coherent sub-topic into a NEW sibling guide with its own full head, register it in the index, and leave behind a 3–5 line summary + cross-reference in the parent. (Example: an outgrown security part becomes `AGENT_SECURITY_GUIDE.md`, a peer — not `agent-harness/references/security.md`.)
- The vault stays flat. Every file self-contained. The index remains the only routing layer.

---

## PART 5 — NAMING AND INDEX REGISTRATION

- **Filenames:** `TOPIC_GUIDE.md`, SCREAMING_SNAKE_CASE, ending in `_GUIDE.md`. The index is `_INDEX.md` (leading underscore sorts it first).
- **Index entry format** (one guide per row):

```
| GUIDE_FILE.md | vX.Y.Z | Use when <one-sentence trigger>. |
```

- Registration is part of authoring, not a follow-up. Update the index row on every version bump.

---

## PART 6 — CHECKLIST

- [ ] Frontmatter has all five fields; description is pushy and owns all when-to-use info
- [ ] HOW TO APPLY procedure present with a Prime directive
- [ ] Part 0 mental model + Never list present
- [ ] Defaults-at-a-glance table present with the override sentence
- [ ] Contents list matches actual part headers
- [ ] Every either-or decision has a table with adoption triggers
- [ ] Phased build order with exit bars present
- [ ] AI-agent-app considerations part present (software guides) with harness cross-references
- [ ] Final part is a walkable checklist
- [ ] No research metadata anywhere; directives + rationale only
- [ ] Under ~1,000 lines; split planned if near cap
- [ ] Registered in `_INDEX.md` with matching version
