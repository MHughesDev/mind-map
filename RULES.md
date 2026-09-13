---
title: Vault Rules
type: reference
status: canonical
tags: [meta, rules, conventions]
updated: 2026-06-19
---

# Mind-Map Vault — File & Folder Rules

> The single source of truth for how every file and folder in this vault is named,
> defined, and placed. When in doubt, follow this document. When this document is
> wrong or incomplete, fix this document first, then the vault.

---

## 1. Top-Level Structure

The vault has two top-level sections:

| Folder | Purpose |
|---|---|
| **Core Domains/** | The structured knowledge base — every field a person could study, organized as a strict taxonomy of learning material. |
| **@Personal/** | Everything personal — projects, original research, and reusable resources. The `@` prefix sorts it to the top and marks it as "mine, not the knowledge tree." |

The repo root holds only meta files: `RULES.md` (this file), `MEMORY.md`, the top-level `.obsidian/` config, and `.git`.

**Rule 1.1** — Do not create new top-level folders. New content belongs inside `Core Domains/` or `@Personal/`.

---

## 2. The Three-Tier Content Model

Every piece of learning content fits one of three sizes. Getting the vocabulary right makes the folder-vs-file decision automatic.

| Tier | Is a… | Analog | Contains |
|---|---|---|---|
| **Folder** | Subject area | A *course / course sequence* | Multiple files + one folder-note |
| **Markdown file** | One coherent topic | A *chapter / unit* | Multiple learning modules (as `##` / `###` sections) |
| **Learning module** | One focused lesson | A *lecture* | Prose, math, examples — can be very long |

A single file may be long (many module-sections stacked). A folder exists **only** when one file would be the wrong container.

---

## 3. Folder vs. File — The Decision Rule

> A topic becomes a **folder** if and only if it branches into multiple distinct
> sub-topics that each deserve their own full set of learning modules.
> Otherwise it is a **single markdown file** whose modules are sections within it.

Apply three lenses, in order:

1. **Branching test (primary).** Does it fan out into 3+ parallel sub-topics studied semi-independently? → folder. Does it read as one linear progression of lessons? → file.
   - *Calculus* → folder (Limits, Derivatives, Integrals, Series, Multivariable… each its own file).
   - *Galois Theory* → file (one coherent arc of modules).
2. **Volume test (tiebreaker).** Would one file need more than ~12–15 substantial modules? → promote to folder. ~3–12 modules → keep as a file.
3. **Curriculum test (sanity check).** Whole multi-unit university course → folder. A few lectures within a course → file.

**Rule 3.1 — No over-foldering.** Never create a folder that will hold only one topic file. If a topic doesn't branch, it is a file, not a folder-with-one-file.

**Rule 3.2 — No orphan promotion.** If a folder ends up with only its folder-note and one topic file, collapse it: replace the folder with a single file at the parent level.

---

## 4. Folder-Notes (the index / glossary) — MANDATORY

**Rule 4.1** — **Every folder, at ANY depth, MUST contain exactly one folder-note: a markdown file named identically to its folder.** No exceptions other than `RP/` containers (see Exemption below). The moment a folder exists, its folder-note must exist too. Examples: `Algebra/Algebra.md`, `Calculus/Calculus.md`, `Renewable Energy/Renewable Energy.md`, `Mathematics/Mathematics.md`.

**Rule 4.1a — A topic with sub-topics is a FOLDER, not a flat file.** If a topic's content naturally divides into named sub-topics (e.g. *Renewable Energy* → Solar, Wind, Hydropower…), it becomes a **folder** whose folder-note lists those sub-topics, and each sub-topic gets its own file inside that folder. Never leave such a topic as a single flat `.md` sitting in its parent. The topic's own descriptive note lives *inside* its folder as the folder-note, never beside it in the parent.

**Rule 4.2 — Purpose of a folder-note.** It is the glossary / index / map-of-content for that folder. It must contain, in order:
1. Frontmatter with `type: moc` (see §6).
2. An `# H1` matching the folder name.
3. A short blockquote: **one paragraph defining what the topic/folder is about.**
4. A `## Topics` section listing **every learning-content file and learning sub-folder** inside it as wiki-link quick-links.

**Rule 4.3 — Links must resolve, both ways.** Every `[[link]]` in a folder-note must point to a file that exists, **and** every learning-content file/sub-folder in the folder must be listed in the folder-note. No listed topic without a file; no learning file without a listing.

**Rule 4.4** — Sub-folders are linked in the parent folder-note with a `(folder)` suffix, e.g. `- [[Linear Algebra]] (folder)`.

**Rule 4.5 — Learning content ONLY.** The folder-note indexes only files whose purpose is *learning the subject* (topic files made of learning modules) and learning sub-folders. It **MUST NOT** list research papers, the `RP/` folder, or any other non-learning resource/asset. Papers and resources still live in the folder (in `RP/` etc.) — they are simply not indexed in the folder-note.

**Rule 4.6 — Folder-note-first authoring.** When creating or expanding any folder, always:
1. Write the **folder-note first** — its description and the full `## Topics` list of intended learning topics.
2. Then create a file for **every** topic listed.
3. Use the finished folder-note as the **checklist**: a build is complete only when every link in it resolves (§4.3). This ordering is what guarantees no topic is ever listed without a file, or built without being listed.

**Exemption** — `RP/` folders (see §7) do **not** require a folder-note; they are pure containers and are never listed in a folder-note.

---

## 5. File Naming Conventions

**Rule 5.1 — Title Case with spaces.** Topic and folder names use natural Title Case: `Real Analysis.md`, `Graph Theory`, `Inner Product Spaces.md`.

**Rule 5.2 — Ampersands for compounds.** Use `&`, not "and", for paired concepts: `Probability & Statistics`, `Vectors & Vector Spaces`, `Foundations & Logic`.

**Rule 5.3 — No numeric ordering prefixes** on topic files (no `01 - …`). Ordering is conveyed by the folder-note's `## Topics` list and by Obsidian.

**Rule 5.4 — Plain names match the field.** A file's name is the topic, nothing more. No dates, no author, no version for learning topics.

**Rule 5.5 — Folder-note names mirror the folder exactly**, including `&` and casing.

**Rule 5.6 — Spelling is corrected.** Folder and file names use correct spelling even when older notes inside used a misspelling (fix by renaming/moving, never deleting — see §9).

---

## 6. Frontmatter Schema

Every **generated/structural** markdown file carries YAML frontmatter. (Hand-authored legacy notes may lack it; add it when you touch them.)

**Learning topic file:**
```yaml
---
title: <Topic Name>
type: learning-topic
domain: <Top-level domain, e.g. Mathematics>
subdomain: <Immediate parent folder>
status: stub        # stub | in-progress | complete
tags: [<domain>, <subdomain>, <topic-slug>]
---
```

**Folder-note / index (MOC):**
```yaml
---
title: <Folder Name>
type: moc
domain: <Top-level domain>
subdomain: <Immediate parent folder, or the domain itself for a domain root>
tags: [<domain>, <slug>, moc]
---
```

**Reference file** (specs, this rules file, external pointers): `type: reference`.

**Rule 6.1** — `type` is required and is the canonical way to distinguish scaffolds (`learning-topic`), indexes (`moc`), and references (`reference`) from raw papers and legacy notes.

---

## 7. Research Papers — the `RP/` Rule

**Rule 7.1 — Definition.** A "research paper" is any specific published/preprint work, in **either** form:
- A markdown summary/notes file, named `RP - <Title> (<Year>).md`.
- A raw paper file (PDF etc.), including arXiv downloads like `2506.07398v2.pdf`.

**Rule 7.2 — Placement.** Every research paper belonging to a topic lives in an `RP/` sub-folder **inside that topic's folder**. Example: `…/Graph Theory/RP/RP - A Tutorial on Spectral Clustering (2007).md`.

**Rule 7.3** — `RP/` folders are pure containers: no folder-note, no scaffolding, exempt from §4.

**Rule 7.4 — Markdown summaries are preferred** and use the `RP - <Title> (<Year>).md` name. Raw PDFs may keep their arXiv ID, but a matching `RP - <Title> (<Year>).md` summary should be created alongside when the paper is studied.

**Rule 7.5 — Papers are not topic notes.** A concept/learning note (e.g. `Spectral Graph Theory.md`, `Eigenvalues & Eigenvectors.md`) is **not** a paper and stays as a normal topic file — never moved into `RP/`.

---

## 8. Core Domains — Specific Rules

**Rule 8.1 — The 12 domains are fixed:** Mathematics, Natural Sciences, Technology, Health & Medicine, Social Sciences, Humanities, Arts & Design, Business & Economics, Law & Public Policy, Education, Applied & Professional, Interdisciplinary & Emerging. Each is a folder with a domain-root folder-note (e.g. `Mathematics/Mathematics.md`).

**Rule 8.2 — Goal: capture all of reality's domains** under a strict hierarchy, but only fold/file per §3. Breadth of topics, restraint on folder depth.

**Rule 8.3 — Typical depth is 2–3 levels** (`Domain / Subject / Topic`). Go deeper only when the branching test genuinely demands it.

**Rule 8.4 — Preserve authored notes.** Existing hand-written notes (Wikipedia-linked concept notes, learning notes, taxonomy notes) stay where their topic lives; relocate them to the correct topic folder if misplaced, but never delete.

---

## 9. Moving & Deleting

**Rule 9.1 — Move, never delete.** Existing files and folders may be **moved/renamed** to their correct place at will, but must **never be deleted**. Reorganization is encouraged; destruction is forbidden.

**Rule 9.2 — Use `git mv`** for tracked files (falls back to `mv`) to preserve history.

**Rule 9.3 — Renaming for correctness** (spelling, casing, `&`) is a move, and is allowed/expected.

---

## 10. @Personal — Specific Rules

`@Personal/` is the user's own space, split PARA-style:

| Sub-folder | Holds | Notes |
|---|---|---|
| **Projects/** | Active personal projects, idea dumps, future-projection notes (e.g. `Ideas/`, `Future Projection/`). | Working/evolving material, not reference knowledge. |
| **Research/** | The user's *original* research — both loose notes (`AI Models/`, `noval_ai_systems/`) and full paper-project repos. | See 10.2 on nested repos. |
| **Resources/** | Reusable assets: `Templates/` (AI prompts, paper templates). | Things reused across projects. |

**Rule 10.1 — Knowledge vs. personal.** Material *about a field* (learnable, general) goes in `Core Domains/`. Material that is *the user's own* (their ideas, their papers, their projects, their templates) goes in `@Personal/`. When something could go either way, ask: "Is this me studying the world, or me producing something?" Studying → Core Domains; producing → @Personal.

**Rule 10.2 — Nested git repos are sovereign.** `@Personal/Research/State-Of-Thought/` and `@Personal/Research/Supra-Hodge-Laplacians-for-Multi-View-Reasoning/` are self-contained git repositories (they have their own `.git`). **Do not** apply vault conventions inside them, do not reorganize, rename, scaffold, or add folder-notes to their contents, and do not move files in or out of them. Treat their root folder as an opaque unit. The same applies to any folder containing its own `.git` or that is clearly a code project (has `scripts/`, `tests/`, `.github/`, `pyproject`, etc.).

**Rule 10.3 — Templates stay templates.** `@Personal/Resources/Templates/` holds blueprints (e.g. `research_paper_template_v1/`). Do not treat a template's internal files as vault content; leave its structure intact.

**Rule 10.4 — Naming in @Personal is relaxed.** Title Case with spaces is preferred for new personal notes, but existing project/repo names (`noval_ai_systems`, `research_paper_template_v1`, `Supra-Hodge-Laplacians-for-Multi-View-Reasoning`) keep their original naming — these are project identities, not topics. Do not "correct" a repo or project folder name.

**Rule 10.5 — Research papers the user is *writing*** live inside their project repo under `@Personal/Research/…`, and are **not** subject to the `RP/` rule (which is only for papers being *studied* under a Core Domain topic).

---

## 11. Linking Conventions

**Rule 11.1 — Wiki-links by basename.** Use `[[Topic Name]]`; Obsidian resolves by file basename across the vault.

**Rule 11.2 — Unique basenames.** Avoid two learning-topic files sharing the same basename (it makes links ambiguous). If unavoidable, disambiguate the less-central one.

**Rule 11.3 — Every folder-note links down; topic files link across.** Folder-notes link to their children (§4). Topic files may add `## See Also` / `## Prerequisites` cross-links to related topics.

---

## 12. Quick Decision Checklist

When adding something new, ask in order:

1. **Is it the user's own work/idea/template?** → `@Personal/` (§10). Else → `Core Domains/`.
2. **Is it a published paper being studied?** → topic's `RP/` folder (§7).
3. **Does the topic branch into 3+ sub-topics each needing many modules?** → folder + folder-note (§3, §4). Else → single file (§3).
4. **Naming:** Title Case, `&` for compounds, correct spelling, no numeric prefixes (§5).
5. **Frontmatter:** set `type` correctly (§6).
6. **If you made a folder:** write its folder-note FIRST (description + full `## Topics` list of learning topics only — no papers/resources), then create a file for every listed topic, then confirm every link resolves (§4.2, §4.5, §4.6).
7. **Relocating existing files:** move/`git mv`, never delete (§9).
