# AGENTS.md

## Cursor Cloud specific instructions

### Codebase overview
This repository is an **Obsidian knowledge vault** (not a traditional software project). It contains ~53 Markdown research paper summaries and concept notes organized under `Core Domains/` and `@Personal/`. The `.obsidian/` directory holds editor configuration.

There is **no build system, no package manager, no dependencies, and no automated tests** — the content is purely Markdown files.

### Running Obsidian
- Obsidian is installed as an extracted AppImage at `/opt/squashfs-root/obsidian`.
- Launch with: `DISPLAY=:1 /opt/squashfs-root/obsidian --no-sandbox --disable-gpu-sandbox &`
- The vault config at `~/.config/obsidian/obsidian.json` is pre-configured to auto-open `/workspace`.
- DBus errors on startup are expected in this container environment and do not affect functionality.

### Working with the vault
- Notes use Obsidian's wiki-link syntax: `[[Note Title]]` for internal links.
- Research paper notes are prefixed with `RP -` followed by the paper title and year.
- The vault structure: `Core Domains/` (organized by academic discipline) and `@Personal/` (personal research, templates).

### Linting / testing
- No linters or test suites exist for this repository.
- Validation is visual: open the vault in Obsidian and verify notes render correctly and links resolve.
