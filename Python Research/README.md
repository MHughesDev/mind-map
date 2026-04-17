# Python Research

This folder tracks **Python libraries and Python-centric repositories** from GitHub or other hosts. Use it as a lightweight catalog: one row per repo, with short summaries and pointers to important APIs.

## Files

| File | Purpose |
|------|---------|
| `Python Repos.csv` | Master table of repos (see below). |
| `AGENTS.md` | Instructions for assistants updating or using this catalog. |

## `Python Repos.csv` columns

| Column | Description |
|--------|-------------|
| **ID** | Stable identifier for the row (e.g. `PR-001`, or a short slug). Use for cross-references from notes elsewhere in the vault. |
| **Title** | Human-readable repo name (often matches the GitHub `owner/repo` name). |
| **Link** | Canonical URL (HTTPS). Prefer the main project page or GitHub repo root. |
| **AI Summary** | One to three sentences: what the project does, who it is for, and anything distinctive (license, maturity, ecosystem). |
| **Important Functions or Classes** | Comma- or semicolon-separated names of key public APIs, modules, or entry points worth remembering (e.g. `pandas.DataFrame`, `fastapi.FastAPI`). |

## Conventions

- **One repo per row.** If a project spans multiple repos, use separate rows with distinct IDs.
- **Quote CSV fields** that contain commas, or avoid commas inside cells by using semicolons in the summary/API column.
- **Keep summaries factual** and refresh them when the repo’s purpose or API surface changes noticeably.

## Related tooling

The root `README.md` describes the vault’s vector pipeline; indexing includes `.csv` by default, so this table can be retrieved semantically alongside your other notes.
