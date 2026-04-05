from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

from .models import BlueprintSection, EvidenceRecord, FigureSpec, SpecData
from .spec import extract_bullets, is_placeholder_text, normalize_block


PAPER_SECTION_MAP = {
    "introduction": "paper/sections/01_introduction.tex",
    "related work": "paper/sections/02_related_work.tex",
    "background": "paper/sections/03_background.tex",
    "problem setup": "paper/sections/04_problem_setup.tex",
    "method": "paper/sections/05_method.tex",
    "framework": "paper/sections/05_method.tex",
    "theory": "paper/sections/06_theory.tex",
    "algorithm": "paper/sections/06a_algorithms.tex",
    "experiments": "paper/sections/07_experiments.tex",
    "results": "paper/sections/08_results.tex",
    "discussion": "paper/sections/09_discussion.tex",
    "limitations": "paper/sections/10_limitations.tex",
    "broader impact": "paper/sections/10a_broader_impact_ethics.tex",
    "ethics": "paper/sections/10a_broader_impact_ethics.tex",
    "conclusion": "paper/sections/11_conclusion.tex",
    "acknowledgments": "paper/sections/11a_acknowledgments.tex",
    "appendix": "paper/appendix/appendix.tex",
    "supplementary": "paper/appendix/supplementary.tex",
}

SECTION_TITLES = {
    "paper/sections/01_introduction.tex": "Introduction",
    "paper/sections/02_related_work.tex": "Related Work",
    "paper/sections/03_background.tex": "Background / Preliminaries",
    "paper/sections/04_problem_setup.tex": "Problem Setup",
    "paper/sections/05_method.tex": "Method / Framework",
    "paper/sections/06_theory.tex": "Theory",
    "paper/sections/06a_algorithms.tex": "Algorithms",
    "paper/sections/07_experiments.tex": "Experiments",
    "paper/sections/08_results.tex": "Results",
    "paper/sections/09_discussion.tex": "Discussion",
    "paper/sections/10_limitations.tex": "Limitations",
    "paper/sections/10a_broader_impact_ethics.tex": "Broader Impact / Ethics",
    "paper/sections/11_conclusion.tex": "Conclusion",
    "paper/sections/11a_acknowledgments.tex": "Acknowledgments",
    "paper/appendix/appendix.tex": "Appendix",
    "paper/appendix/supplementary.tex": "Supplementary Material",
}


@dataclass
class ManuscriptGenerationResult:
    generated_files: list[str]
    bibliography_entries_written: int


@dataclass
class FigureGenerationResult:
    manifest_path: str
    tex_snippet_path: str
    figure_count: int
    unresolved_figure_count: int


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "item"


def sha256_for_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_evidence_store(spec: SpecData, repo_root: Path, output_path: Path) -> list[EvidenceRecord]:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    evidence: list[EvidenceRecord] = []
    for index, source in enumerate(spec.source_materials, start=1):
        citation_key = slugify(source.label)
        if source.url:
            evidence.append(
                EvidenceRecord(
                    id=f"evidence-{index}",
                    label=source.label,
                    source_type=source.source_type,
                    locator=source.url,
                    exists=True,
                    citation_key=citation_key,
                    notes=["Remote source declared in spec; retrieval policy should verify metadata before final citation use."],
                )
            )
            continue

        path = Path(source.path or "")
        exists = path.exists()
        evidence.append(
            EvidenceRecord(
                id=f"evidence-{index}",
                label=source.label,
                source_type=source.source_type,
                locator=str(path),
                exists=exists,
                sha256=sha256_for_path(path) if exists and path.is_file() else None,
                size_bytes=path.stat().st_size if exists and path.is_file() else None,
                citation_key=citation_key,
                notes=list(source.notes),
            )
        )
    output_path.write_text(json.dumps([item.to_dict() for item in evidence], indent=2), encoding="utf-8")
    return evidence


def build_grounding_report(spec: SpecData, evidence: list[EvidenceRecord], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    usable_evidence = [item for item in evidence if item.exists]
    lines = [
        "# Claim Grounding Report",
        "",
        "This file maps spec claims to the currently available evidence store.",
        "",
    ]
    if not spec.claims:
        lines.extend(["- No claims were parsed from the spec.", ""])
    for claim in spec.claims:
        lines.extend([f"## {claim.id}", "", claim.body or "_No claim body found._", ""])
        if usable_evidence:
            lines.append("### Available evidence candidates")
            lines.extend(f"- `{item.id}`: `{item.label}` ({item.locator})" for item in usable_evidence[:5])
        else:
            lines.append("### Available evidence candidates")
            lines.append("- None.")
        if claim.evidence_hints:
            lines.extend(["", "### Evidence hints from the spec"])
            lines.extend(f"- {hint}" for hint in claim.evidence_hints)
        lines.append("")
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def map_blueprint_outputs(blueprint_sections: list[BlueprintSection]) -> dict[str, BlueprintSection]:
    mapping: dict[str, BlueprintSection] = {}
    for blueprint in blueprint_sections:
        body_lower = blueprint.body.lower()
        title_lower = blueprint.title.lower()
        for key, output_path in PAPER_SECTION_MAP.items():
            if key in body_lower or key in title_lower:
                blueprint.mapped_output = output_path
                mapping.setdefault(output_path, blueprint)
                break
    return mapping


def render_paragraphs(text: str) -> str:
    def usable(line: str) -> bool:
        stripped = line.strip()
        if not stripped:
            return False
        if is_placeholder_text(stripped):
            return False
        if stripped.endswith(":"):
            return False
        if re.fullmatch(r"[-_*`#=]{3,}", stripped):
            return False
        if not re.search(r"[A-Za-z0-9]", stripped):
            return False
        return True

    items = [
        item
        for item in extract_bullets(text)
        if usable(item)
    ]
    if items:
        return "\n\n".join(items[:4])
    lines = [
        line
        for line in normalize_block(text).splitlines()
        if usable(line)
    ]
    if not lines:
        return "Add project-specific content here."
    return "\n\n".join(lines[:4])


def claim_ids_for_section(section_path: str, spec: SpecData) -> list[str]:
    keywords = {
        "paper/sections/01_introduction.tex": {"claim-1", "claim-2"},
        "paper/sections/05_method.tex": {"claim-1"},
        "paper/sections/06_theory.tex": {"claim-2", "claim-3"},
        "paper/sections/07_experiments.tex": {"claim-1", "claim-3"},
        "paper/sections/08_results.tex": {"claim-1", "claim-2", "claim-3"},
        "paper/sections/11_conclusion.tex": {claim.id for claim in spec.claims},
    }
    selected = list(keywords.get(section_path, set()) & {claim.id for claim in spec.claims})
    return sorted(selected)


def section_body_for_path(section_path: str, spec: SpecData, mapping: dict[str, BlueprintSection]) -> str:
    blueprint = mapping.get(section_path)
    core = render_paragraphs(blueprint.body if blueprint else spec.core_objective)
    safe_intro = "Generated from the project specification."
    lines = [safe_intro, "", core]

    if "related_work" in section_path or "related work" in section_path:
        lines.extend(["", "Use only authorized sources here."])
    elif "experiments" in section_path:
        lines.extend(["", "Keep experiments aligned with authorized evidence."])
    elif "results" in section_path:
        lines.extend(["", "Keep result statements evidence-backed."])
    elif "acknowledgments" in section_path:
        lines = ["Acknowledgments may be added here only when the project specification and submission state allow them."]

    claim_ids = claim_ids_for_section(section_path, spec)
    comment = f"% Claims: {', '.join(claim_ids)}" if claim_ids else "% Claims: none mapped yet"
    return comment + "\n" + "\n".join(lines).strip() + "\n"


def abstract_body(spec: SpecData) -> str:
    objective = render_paragraphs(spec.core_objective)
    controls = render_paragraphs(spec.numbered_sections.get("8.4", ""))
    return (
        "\\begin{abstract}\n"
        "Generated from PROJECT_SPEC.md.\n\n"
        f"{objective}\n\n"
        f"{controls}\n"
        "\\end{abstract}\n"
    )


def paper_title(spec: SpecData) -> str:
    identity = render_paragraphs(spec.project_identity)
    if identity.startswith("This section should"):
        return "Spec-Driven Research Draft"
    first_line = identity.splitlines()[0].strip()
    return first_line[:100]


def paper_author(spec: SpecData) -> str:
    author_block = render_paragraphs(spec.numbered_sections.get("14", ""))
    if author_block.startswith("This section should"):
        return ""
    first_line = author_block.splitlines()[0].strip()
    return first_line[:100]


def update_main_tex(repo_root: Path, spec: SpecData) -> None:
    main_tex = repo_root / "paper/main.tex"
    if not main_tex.exists():
        return
    text = main_tex.read_text(encoding="utf-8")
    text = re.sub(r"\\title\{.*?\}", lambda _match: f"\\title{{{paper_title(spec)}}}", text, count=1)
    text = re.sub(r"\\author\{.*?\}", lambda _match: f"\\author{{{paper_author(spec)}}}", text, count=1)
    main_tex.write_text(text, encoding="utf-8")


def write_bibliography_from_evidence(evidence: list[EvidenceRecord], output_path: Path) -> int:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    entries: list[str] = [
        "% Bibliography generated from the evidence store.",
        "% Replace or enrich these entries only with verified metadata.",
        "",
    ]
    written = 0
    for item in evidence:
        if item.source_type == "url":
            entries.extend(
                [
                    f"@misc{{{item.citation_key},",
                    f"  title = {{{item.label}}},",
                    f"  howpublished = {{\\url{{{item.locator}}}}},",
                    "  note = {Source declared in PROJECT_SPEC.md and pending metadata hardening}",
                    "}",
                    "",
                ]
            )
            written += 1
        elif item.exists and item.locator.lower().endswith(".pdf"):
            entries.extend(
                [
                    f"@misc{{{item.citation_key},",
                    f"  title = {{{item.label}}},",
                    f"  note = {{Local PDF source at `{item.locator}`; metadata should be completed from the source itself}}",
                    "}",
                    "",
                ]
            )
            written += 1
    if written == 0:
        entries.append("% No evidence records were eligible for automatic bibliography generation.")
    output_path.write_text("\n".join(entries).rstrip() + "\n", encoding="utf-8")
    return written


def generate_manuscript(spec: SpecData, repo_root: Path, evidence: list[EvidenceRecord]) -> ManuscriptGenerationResult:
    generated_files: list[str] = []
    mapping = map_blueprint_outputs(spec.blueprint_sections)

    update_main_tex(repo_root, spec)
    generated_files.append("paper/main.tex")

    abstract_path = repo_root / "paper/abstract.tex"
    abstract_path.write_text(abstract_body(spec), encoding="utf-8")
    generated_files.append(str(abstract_path.relative_to(repo_root)))

    for relative_path in SECTION_TITLES:
        file_path = repo_root / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        title = SECTION_TITLES[relative_path]
        heading = "\\section*{Acknowledgments}" if "Acknowledgments" in title else f"\\section{{{title}}}"
        if relative_path.endswith("supplementary.tex"):
            heading = "\\section{Supplementary Material}"
        content = section_body_for_path(relative_path, spec, mapping)
        file_path.write_text(f"{heading}\n{content}", encoding="utf-8")
        generated_files.append(str(file_path.relative_to(repo_root)))

    bib_path = repo_root / "paper/bib/references.bib"
    entries_written = write_bibliography_from_evidence(evidence, bib_path)
    generated_files.append(str(bib_path.relative_to(repo_root)))

    return ManuscriptGenerationResult(generated_files=generated_files, bibliography_entries_written=entries_written)


def build_figure_manifest(spec: SpecData, repo_root: Path) -> FigureGenerationResult:
    build_dir = repo_root / "build"
    figure_json = build_dir / "figure_specs.json"
    figure_tex = repo_root / "paper/figures/generated_from_spec.tex"
    build_dir.mkdir(parents=True, exist_ok=True)
    figure_tex.parent.mkdir(parents=True, exist_ok=True)

    figure_json.write_text(json.dumps([figure.to_dict() for figure in spec.figures], indent=2), encoding="utf-8")

    tex_lines = [
        "% Auto-generated from PROJECT_SPEC.md detailed figure definitions.",
        "% Include this file explicitly only after reviewing figure readiness and placement.",
        "",
    ]
    unresolved = 0
    for figure in spec.figures:
        if figure.is_complete() and not is_placeholder_text(figure.summary):
            tex_lines.extend(
                [
                    "\\begin{figure}[t]",
                    "\\centering",
                    "\\fbox{\\parbox{0.9\\linewidth}{\\centering Figure asset should be rendered from the structured figure specification.}}",
                    f"\\caption{{{figure.detailed_fields.get('Caption Requirements', figure.summary).replace('{', '').replace('}', '')}}}",
                    f"\\label{{fig:{slugify(figure.id)}}}",
                    "\\end{figure}",
                    "",
                ]
            )
        else:
            unresolved += 1
            tex_lines.extend(
                [
                    f"% {figure.id} remains unresolved because its detailed specification is incomplete.",
                    "",
                ]
            )
    figure_tex.write_text("\n".join(tex_lines).rstrip() + "\n", encoding="utf-8")
    return FigureGenerationResult(
        manifest_path=str(figure_json),
        tex_snippet_path=str(figure_tex),
        figure_count=len(spec.figures),
        unresolved_figure_count=unresolved,
    )


def update_project_status(
    repo_root: Path,
    spec: SpecData,
    findings_count: int,
    evidence_count: int,
    manuscript: ManuscriptGenerationResult,
    figures: FigureGenerationResult,
) -> None:
    status_path = repo_root / "docs/PROJECT_STATUS.md"
    status_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Project Status",
        "",
        "## Current Objective",
        render_paragraphs(spec.core_objective),
        "",
        "## Project Mode",
        f"- {normalize_block(spec.project_mode) or 'unspecified'}",
        "",
        "## Requested Draft Level",
        f"- {normalize_block(spec.draft_level) or 'unspecified'}",
        "",
        "## Current Phase",
        "- drafting",
        "- build review",
        "- auditing",
        "",
        "## Latest Agent Summary",
        f"Generated `{len(manuscript.generated_files)}` manuscript outputs from the parsed spec, recorded `{evidence_count}` evidence items, and found `{findings_count}` spec-audit findings.",
        "",
        "## Source-Of-Truth Check",
        "- `PROJECT_SPEC.md` read this pass?: yes",
        f"- Highest-priority external materials consulted?: {evidence_count} evidence item(s) declared by the spec",
        "- Any source conflicts logged in `docs/DECISIONS_LOG.md`?: not yet",
        "",
        "## Files Most Recently Changed",
    ]
    lines.extend(f"- `{item}`" for item in manuscript.generated_files[:12])
    lines.extend(
        [
            "",
            "## Figure Status",
            f"- Figures defined in `PROJECT_SPEC.md`: {len(spec.figures)}",
            f"- Figures with detailed entries in `11A`: {sum(1 for item in spec.figures if item.detailed_fields)}",
            "- Figures implemented in `paper/`: generated manifest only",
            f"- Figures still placeholders: {figures.unresolved_figure_count}",
            "",
            "## Recommended Next Action",
            "Review the generated manuscript against the evidence store, then run the autonomous build-and-audit loop.",
            "",
            "## Last Updated By",
            "- human / agent: agent",
            "- date: auto-generated during autonomous paper run",
        ]
    )
    status_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
