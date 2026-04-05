# Spec Schema

This document describes the structured artifacts produced from `PROJECT_SPEC.md`.

## Output Artifact

- `build/spec.json`

## Top-Level Fields

- `spec_path`: absolute path of the parsed spec file
- `raw_text`: original markdown source
- `headings`: heading records with level, title, numbering, and body content
- `numbered_sections`: map of numbered section identifiers such as `0.1`, `5`, `11A`
- `project_mode`: normalized content from section `0.1`
- `draft_level`: normalized content from section `0.2`
- `autonomy_level`: normalized content from section `0.3`
- `stop_continue_rule`: normalized content from section `0.4`
- `project_identity`: content from section `1`
- `core_objective`: content from section `2`
- `audience_style`: content from section `7`
- `source_materials`: parsed records from section `4`
- `claims`: structured claim records from section `5`
- `blueprint_sections`: per-section blueprint records from section `8.3`
- `figures`: figure plan and detailed figure-spec records from sections `12` and `11A`
- `tables`: parsed table records from section `12.2`
- `success_criteria`: normalized list from section `17`

## Source Material Record

- `id`
- `label`
- `raw_reference`
- `source_type`
- `exists`
- `path`
- `url`
- `priority`
- `notes`

## Claim Record

- `id`
- `title`
- `body`
- `evidence_hints`

## Blueprint Section Record

- `id`
- `title`
- `body`
- `required`
- `mapped_output`
- `claim_ids`

## Figure Record

- `id`
- `title`
- `summary`
- `detailed_fields`

## Audit Outputs

- `docs/SPEC_AUDIT.md`
- `build/spec_audit.json`

These outputs are produced by `python scripts/spec_audit.py` and should block autonomous execution when they contain unresolved errors.
