from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from autopaper.spec import parse_spec


class SpecParserTests(unittest.TestCase):
    def test_parse_spec_extracts_core_fields(self) -> None:
        fixture = ROOT / "tests/fixtures/good_project_spec.md"
        spec = parse_spec(fixture, ROOT)

        self.assertEqual(spec.project_mode, "- revise existing paper")
        self.assertEqual(len(spec.claims), 1)
        self.assertGreaterEqual(len(spec.source_materials), 2)
        self.assertEqual(len(spec.figures), 1)
        self.assertIn("0.1", spec.numbered_sections)
        self.assertTrue(any(item.id == "figure-1" for item in spec.figures))
        self.assertTrue(spec.figures[0].is_complete())
        self.assertIn("Structural Description", spec.figures[0].detailed_fields)


if __name__ == "__main__":
    unittest.main()
