from __future__ import annotations

import json
import subprocess
import sys
import uuid
from pathlib import Path

from .generation import (
    build_evidence_store,
    build_figure_manifest,
    build_grounding_report,
    generate_manuscript,
    update_project_status,
)
from .models import AuditFinding, RunState
from .spec import audit_spec, parse_spec, write_spec_audit_json, write_spec_audit_markdown, write_spec_json

# Initial build plus up to this many repair attempts (each attempt re-runs build-and-audit).
MAX_BUILD_REPAIR_LOOPS = 3


def _run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        errors="replace",
        check=False,
    )


def classify_build_failure(repo_root: Path) -> list[str]:
    classes: list[str] = []
    build_status = (repo_root / "docs/BUILD_STATUS.md").read_text(encoding="utf-8", errors="replace") if (repo_root / "docs/BUILD_STATUS.md").exists() else ""
    log_text = (repo_root / "paper/main.log").read_text(encoding="utf-8", errors="replace") if (repo_root / "paper/main.log").exists() else ""
    figure_audit = (repo_root / "docs/FIGURE_AUDIT.md").read_text(encoding="utf-8", errors="replace") if (repo_root / "docs/FIGURE_AUDIT.md").exists() else ""
    lower = f"{build_status}\n{log_text}".lower()
    if "file `" in lower and "not found" in lower:
        classes.append("missing-file")
    if "undefined citation" in lower or "citation `" in lower:
        classes.append("undefined-citation")
    if "undefined reference" in lower or "reference `" in lower:
        classes.append("undefined-reference")
    if "overfull \\hbox" in lower or "underfull \\hbox" in lower:
        classes.append("layout-warning")
    incomplete_match = None
    for line in figure_audit.splitlines():
        if line.startswith("- Incomplete figures:"):
            incomplete_match = line
            break
    if incomplete_match and "`0`" not in incomplete_match:
        classes.append("figure-incomplete")
    if "no latex build tool was found" in lower:
        classes.append("environment")
    if "! " in log_text:
        classes.append("latex-error")
    if not classes and "failed" in build_status.lower():
        classes.append("unknown-failure")
    return classes


def run_build_and_audits(repo_root: Path) -> list[subprocess.CompletedProcess[str]]:
    commands = [
        [sys.executable, "scripts/build_paper.py"],
        [sys.executable, "scripts/render_audit.py", "--write-full-extract"],
        [sys.executable, "scripts/check_rendered_refs.py"],
        [sys.executable, "scripts/figure_audit.py"],
        [sys.executable, "scripts/map_manuscript_files.py"],
        [sys.executable, "scripts/check_placeholders.py"],
        [sys.executable, "scripts/check_bib_placeholders.py"],
        [sys.executable, "scripts/project_audit.py"],
    ]
    results: list[subprocess.CompletedProcess[str]] = []
    for command in commands:
        results.append(_run(command, repo_root))
    return results


class AutonomousPaperRunner:
    def __init__(self, repo_root: Path, spec_path: Path | None = None) -> None:
        self.repo_root = repo_root
        self.spec_path = spec_path or repo_root / "PROJECT_SPEC.md"
        self.build_dir = repo_root / "build"
        self.docs_dir = repo_root / "docs"
        self.run_state_path = self.build_dir / "run_state.json"
        self.run_state = RunState(
            run_id=uuid.uuid4().hex[:12],
            status="initialized",
            current_stage="initialized",
        )

    def _save_state(self) -> None:
        self.run_state_path.parent.mkdir(parents=True, exist_ok=True)
        self.run_state_path.write_text(json.dumps(self.run_state.to_dict(), indent=2), encoding="utf-8")

    def _mark_stage(self, stage: str, status: str = "running") -> None:
        self.run_state.current_stage = stage
        self.run_state.status = status
        if status == "completed" and stage not in self.run_state.completed_stages:
            self.run_state.completed_stages.append(stage)
        self._save_state()

    def _record_findings(self, findings: list[AuditFinding]) -> None:
        self.run_state.findings = [item.to_dict() for item in findings]
        self._save_state()

    def _record_artifact(self, name: str, value: str) -> None:
        self.run_state.artifacts[name] = value
        self._save_state()

    def _attempt_repairs(self, failure_classes: list[str], spec, evidence) -> None:
        if any(item in failure_classes for item in ("missing-file", "undefined-citation", "latex-error")):
            if "regenerated-manuscript-and-figures" not in self.run_state.repairs_attempted:
                generate_manuscript(spec, self.repo_root, evidence)
                build_figure_manifest(spec, self.repo_root)
                self.run_state.repairs_attempted.append("regenerated-manuscript-and-figures")
        if "layout-warning" in failure_classes and "layout-warning-regeneration" not in self.run_state.repairs_attempted:
            generate_manuscript(spec, self.repo_root, evidence)
            self.run_state.repairs_attempted.append("layout-warning-regeneration")
        if "figure-incomplete" in failure_classes and "figure-manifest-refresh" not in self.run_state.repairs_attempted:
            build_figure_manifest(spec, self.repo_root)
            self.run_state.repairs_attempted.append("figure-manifest-refresh")
        self._save_state()

    def run(self, dry_run: bool = False, skip_build: bool = False) -> dict[str, object]:
        self._save_state()

        self._mark_stage("parse-spec")
        spec = parse_spec(self.spec_path, self.repo_root)
        spec_json = self.build_dir / "spec.json"
        write_spec_json(spec, spec_json)
        self._record_artifact("spec_json", str(spec_json))
        self._mark_stage("parse-spec", "completed")

        self._mark_stage("spec-audit")
        findings = audit_spec(spec)
        spec_audit_md = self.docs_dir / "SPEC_AUDIT.md"
        spec_audit_json = self.build_dir / "spec_audit.json"
        write_spec_audit_markdown(findings, spec_audit_md)
        write_spec_audit_json(findings, spec_audit_json)
        self._record_findings(findings)
        self._record_artifact("spec_audit_markdown", str(spec_audit_md))
        self._record_artifact("spec_audit_json", str(spec_audit_json))
        self._mark_stage("spec-audit", "completed")

        self._mark_stage("source-ingestion")
        evidence_path = self.build_dir / "evidence_store.json"
        evidence = build_evidence_store(spec, self.repo_root, evidence_path)
        grounding_path = self.docs_dir / "CLAIM_GROUNDING.md"
        build_grounding_report(spec, evidence, grounding_path)
        self._record_artifact("evidence_store", str(evidence_path))
        self._record_artifact("claim_grounding", str(grounding_path))
        self._mark_stage("source-ingestion", "completed")

        self._mark_stage("section-generation")
        manuscript = generate_manuscript(spec, self.repo_root, evidence)
        self._record_artifact("generated_files", json.dumps(manuscript.generated_files))
        self._mark_stage("section-generation", "completed")

        self._mark_stage("figure-generation")
        figures = build_figure_manifest(spec, self.repo_root)
        self._record_artifact("figure_manifest", figures.manifest_path)
        self._record_artifact("figure_tex", figures.tex_snippet_path)
        self._mark_stage("figure-generation", "completed")

        self._mark_stage("status-update")
        update_project_status(
            self.repo_root,
            spec,
            findings_count=len(findings),
            evidence_count=len(evidence),
            manuscript=manuscript,
            figures=figures,
        )
        self._mark_stage("status-update", "completed")

        build_results: list[dict[str, object]] = []
        failure_classes: list[str] = []
        if not dry_run and not skip_build:
            self._mark_stage("build-and-audit")
            # Loop: build/audit → classify → bounded regeneration repairs → rebuild until clean or no progress.
            max_loops = MAX_BUILD_REPAIR_LOOPS + 1
            for loop_index in range(max_loops):
                results = run_build_and_audits(self.repo_root)
                for result in results:
                    build_results.append(
                        {
                            "command": result.args,
                            "returncode": result.returncode,
                            "stdout": result.stdout[-2000:],
                            "stderr": result.stderr[-2000:],
                            "repair_loop": loop_index,
                        }
                    )
                failure_classes = classify_build_failure(self.repo_root)
                if not failure_classes:
                    break
                if loop_index == max_loops - 1:
                    break
                repairs_before = list(self.run_state.repairs_attempted)
                self._attempt_repairs(failure_classes, spec, evidence)
                if self.run_state.repairs_attempted == repairs_before:
                    break
            self._mark_stage("build-and-audit", "completed")

        self.run_state.status = "completed" if not any(item.severity == "error" for item in findings) else "blocked"
        self._save_state()
        return {
            "spec_json": str(spec_json),
            "spec_audit_markdown": str(spec_audit_md),
            "spec_audit_json": str(spec_audit_json),
            "evidence_store": str(evidence_path),
            "claim_grounding": str(grounding_path),
            "run_state": str(self.run_state_path),
            "generated_files": manuscript.generated_files,
            "bibliography_entries_written": manuscript.bibliography_entries_written,
            "figure_manifest": figures.manifest_path,
            "figure_tex": figures.tex_snippet_path,
            "figure_count": figures.figure_count,
            "unresolved_figures": figures.unresolved_figure_count,
            "findings": [item.to_dict() for item in findings],
            "failure_classes": failure_classes,
            "build_results": build_results,
        }
