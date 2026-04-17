# How to research Python repos (for agents)

Follow this when investigating a library or Python-centric repository and recording it in **`Python Repos.csv`**. The goal is **accurate, citeable rows**—not long essays.

## 1. Clarify the target

- Confirm you have a **single canonical repo** (or one row per repo if the user listed several).
- If the name is ambiguous (many projects share a title), resolve using the **exact URL** the user gave or the most official `owner/repo` match.

## 2. Gather facts from primary sources (in order)

Use tools available in your environment (browser fetch, repository APIs, local clone, etc.). Prefer reading text over guessing.

1. **Repository landing page** — README title, one-line description, and topics.
2. **Package metadata** — `pyproject.toml`, `setup.cfg`, or `setup.py` for package name, dependencies, and entry points.
3. **Documentation site** — “Getting started” or API overview *only if* the README is empty or misleading.
4. **PyPI** — Confirms package name, summary line, and link back to the repo when relevant.

Do **not** rely on forum posts, random blogs, or model memory for factual claims in the CSV.

## 3. Verify before you write

- **Purpose:** You should be able to state *what problem it solves* in one sentence using words from the README or docs.
- **APIs:** List symbols that appear in **public docs** or the package’s **top-level exports** (e.g. `__all__`, documented classes). If you cannot verify a name, **omit it** rather than guess.

## 4. Fill `Python Repos.csv` (one row)

| Column | What to write |
|--------|----------------|
| **ID** | New unique ID (see `AGENTS.md`). |
| **Title** | Repo or package name as shown on the host. |
| **Link** | HTTPS URL you used as primary (usually the repo root). |
| **AI Summary** | 1–3 sentences: purpose, typical user, one differentiator. No unverified stats (stars, downloads, “most popular”). |
| **Important Functions or Classes** | Verified symbols; use `module.Class` or `module.function` when helpful. Separate with semicolons if needed. |

If the repo is already in the table, **update the same row** (keep ID stable) unless the user wants a duplicate for a fork.

## 5. Quality bar

- **No fabrication:** If something is unclear, write a shorter summary or mark uncertainty in the summary (“Documentation emphasizes X; scope of Y not confirmed.”).
- **No scope creep:** Do not create extra Markdown reports in this folder unless the user asks.
- **CSV safety:** Quote fields that contain commas; escape `"` as `""`.

## 6. Done when

- The row is complete, consistent with sources, and saved.
- You can name **which sources** informed the summary and API column (README, docs page, `pyproject.toml`, etc.) if asked.
