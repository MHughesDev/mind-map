## Cursor Cloud specific instructions

This repository is an **Obsidian vault** — a collection of Markdown research paper summaries and personal notes. There is no traditional application code, build system, test framework, or package manager.

### What's in the vault

- `Core Domains/` — Research paper summaries organized by topic (AI, distributed systems, programming, graph theory, etc.)
- `@Personal/` — Personal research notes and templates
- `.obsidian/` — Obsidian app configuration (do not edit manually)

### Running the application

The "application" is Obsidian (a desktop Markdown editor). To launch:

```
obsidian "obsidian://open?path=/workspace" --no-sandbox &
```

The `--no-sandbox` flag is required in the Cloud Agent VM environment.

### Lint / test / build

- **Lint**: Not applicable — this is a content-only vault with no code.
- **Tests**: Not applicable — no automated tests exist.
- **Build**: Not applicable — no build step required. Obsidian reads Markdown files directly.

### Notes for agents

- Markdown files use Obsidian-flavored syntax including `[[wikilinks]]` for internal linking and YAML frontmatter for metadata.
- Do not modify files under `.obsidian/` unless specifically asked — these are Obsidian UI configuration.
- New notes should follow the existing naming convention: `RP - <Title> (<Year>).md` for research papers.
