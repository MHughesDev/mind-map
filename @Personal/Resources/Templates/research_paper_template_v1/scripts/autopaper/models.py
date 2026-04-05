from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class SourceMaterial:
    id: str
    label: str
    raw_reference: str
    source_type: str
    exists: bool
    path: str | None = None
    url: str | None = None
    priority: int | None = None
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Claim:
    id: str
    title: str
    body: str
    evidence_hints: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class BlueprintSection:
    id: str
    title: str
    body: str
    required: bool = True
    mapped_output: str | None = None
    claim_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class FigureSpec:
    id: str
    title: str
    summary: str
    detailed_fields: dict[str, str] = field(default_factory=dict)

    def is_complete(self) -> bool:
        required = [
            "Structural Description",
            "Semantic Mapping",
            "Layout Constraints",
            "Mathematical Correspondence",
            "Rendering Instructions",
            "Caption Requirements",
            "Audit Criteria",
        ]
        return all(self.detailed_fields.get(field, "").strip() for field in required)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class TableSpec:
    id: str
    title: str
    summary: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AuditFinding:
    severity: str
    code: str
    message: str
    location: str
    recommendation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class EvidenceRecord:
    id: str
    label: str
    source_type: str
    locator: str
    exists: bool
    sha256: str | None = None
    size_bytes: int | None = None
    citation_key: str | None = None
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class RunState:
    run_id: str
    status: str
    current_stage: str
    completed_stages: list[str] = field(default_factory=list)
    findings: list[dict[str, Any]] = field(default_factory=list)
    artifacts: dict[str, str] = field(default_factory=dict)
    repairs_attempted: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class SpecData:
    spec_path: str
    raw_text: str
    headings: list[dict[str, Any]]
    numbered_sections: dict[str, str]
    project_mode: str
    draft_level: str
    autonomy_level: str
    stop_continue_rule: str
    project_identity: str
    core_objective: str
    audience_style: str
    source_materials: list[SourceMaterial] = field(default_factory=list)
    claims: list[Claim] = field(default_factory=list)
    blueprint_sections: list[BlueprintSection] = field(default_factory=list)
    figures: list[FigureSpec] = field(default_factory=list)
    tables: list[TableSpec] = field(default_factory=list)
    success_criteria: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["source_materials"] = [item.to_dict() for item in self.source_materials]
        payload["claims"] = [item.to_dict() for item in self.claims]
        payload["blueprint_sections"] = [item.to_dict() for item in self.blueprint_sections]
        payload["figures"] = [item.to_dict() for item in self.figures]
        payload["tables"] = [item.to_dict() for item in self.tables]
        return payload


def path_to_str(path: Path | None) -> str | None:
    return None if path is None else str(path)
