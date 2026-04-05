from __future__ import annotations

import sys
import unittest
import uuid
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from autopaper.pipeline import AutonomousPaperRunner


class RunnerDryRunTests(unittest.TestCase):
    def test_runner_dry_run_generates_artifacts(self) -> None:
        fixture = ROOT / "tests/fixtures/good_project_spec.md"
        repo_root = ROOT / "build" / f"test_runner_{uuid.uuid4().hex[:8]}"
        if repo_root.exists():
            shutil.rmtree(repo_root)
        try:
            repo_root.mkdir(parents=True, exist_ok=True)
            (repo_root / "PROJECT_SPEC.md").write_text(fixture.read_text(encoding="utf-8"), encoding="utf-8")
            (repo_root / "sources").mkdir(parents=True, exist_ok=True)
            (repo_root / "sources/example_note.md").write_text("example note", encoding="utf-8")
            (repo_root / "docs").mkdir(parents=True, exist_ok=True)
            (repo_root / "paper/sections").mkdir(parents=True, exist_ok=True)
            (repo_root / "paper/appendix").mkdir(parents=True, exist_ok=True)
            (repo_root / "paper/bib").mkdir(parents=True, exist_ok=True)
            (repo_root / "paper/figures").mkdir(parents=True, exist_ok=True)

            runner = AutonomousPaperRunner(repo_root=repo_root, spec_path=repo_root / "PROJECT_SPEC.md")
            result = runner.run(dry_run=True)

            self.assertTrue((repo_root / "build/spec.json").exists())
            self.assertTrue((repo_root / "docs/SPEC_AUDIT.md").exists())
            self.assertTrue((repo_root / "docs/CLAIM_GROUNDING.md").exists())
            self.assertTrue((repo_root / "paper/abstract.tex").exists())
            self.assertTrue((repo_root / "paper/figures/generated_from_spec.tex").exists())
            self.assertIn("generated_files", result)
        finally:
            if repo_root.exists():
                shutil.rmtree(repo_root)


if __name__ == "__main__":
    unittest.main()
