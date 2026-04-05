from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from autopaper.spec import audit_spec, parse_spec


class SpecAuditTests(unittest.TestCase):
    def test_good_spec_avoids_errors(self) -> None:
        fixture = ROOT / "tests/fixtures/good_project_spec.md"
        spec = parse_spec(fixture, ROOT)
        findings = audit_spec(spec)

        error_codes = {item.code for item in findings if item.severity == "error"}
        self.assertEqual(set(), error_codes)

    def test_incomplete_spec_emits_errors(self) -> None:
        fixture = ROOT / "tests/fixtures/incomplete_project_spec.md"
        spec = parse_spec(fixture, ROOT)
        findings = audit_spec(spec)

        error_codes = {item.code for item in findings if item.severity == "error"}
        self.assertIn("project-mode-missing", error_codes)
        self.assertIn("claims-missing", error_codes)
        self.assertIn("blueprint-missing", error_codes)
        self.assertIn("done-state-target-missing", error_codes)
        self.assertIn("formal-commitments-missing", error_codes)


if __name__ == "__main__":
    unittest.main()
