# Agents: Python Research folder

Use this file when reading or editing anything under `Python Research/`.

## Scope

- **In scope:** Libraries, frameworks, tools, and applications where **Python is the primary language** or the main integration surface (e.g. a CLI or Python SDK), regardless of host (GitHub, GitLab, Gitea, PyPI project pages linked from docs, etc.).
- **Out of scope:** Repos that only vendor Python or mention it in passing; put those elsewhere unless the user asks to include them.

## Primary artifact

- **`Python Repos.csv`** is the source of truth. Do not duplicate the full catalog in Markdown; link to the CSV or summarize a **small** subset when answering questions.

## When adding or updating a row

1. **ID** — Use a new unique ID. Prefer a simple pattern: `PR-001`, `PR-002`, … or a short slug (`numpy-core`) if the user prefers names over numbers.
2. **Title** — Match the repo’s display name or `owner/repo` for GitHub.
3. **Link** — Use HTTPS. Prefer the repository URL; use the official docs URL only if there is no public repo or the user specifies it.
4. **AI Summary** — 1–3 sentences: purpose, typical use, and one differentiator if obvious. Do not invent maintainers, stars, or features; if unsure, say what is uncertain or leave the summary minimal.
5. **Important Functions or Classes** — List symbols that a developer would actually import or subclass (module paths welcome). Omit noise (`__init__`) unless it is the documented entry point.

## CSV safety

- If a field contains commas, **wrap the field in double quotes** and escape internal double quotes as `""`.
- Prefer semicolons to separate multiple API names in the last column when commas would force heavy quoting.

## When the user asks for “research” on Python repos

- Prefer **adding or updating rows** in `Python Repos.csv` over creating long standalone notes, unless they ask for a separate write-up.
- After substantive edits, remind them the table is suitable for vault indexing (see root `README.md`).
