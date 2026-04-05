# Optional Cursor Setup

This file describes optional enhancements you may enable in Cursor for stronger autonomy.

## 1. Project Rules
This repository already includes `.cursor/rules/` files. Keep them version controlled.

## 2. AGENTS.md
The repository root includes `AGENTS.md` for project-wide instructions.

## 3. Subagents
The repository includes reusable subagents in `.cursor/agents/`.

Suggested uses:
- `paper-builder` for generation
- `reviewer` for critique
- `citation-auditor` for bibliography and evidence checks

## 4. Cloud Agents
If you use cloud agents:
- ensure the repo contains all required instructions,
- document environment assumptions,
- keep external secrets outside the repo,
- prefer reproducible build commands.

## 5. Hooks and Skills
This kit does not require hooks to function, but hooks/skills can be added later if you want automatic linting or post-edit audits.
