import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from latex_log import critical_failure, parse_log  # noqa: E402


class TestLatexLog(unittest.TestCase):
    def test_parse_undefined_citation(self) -> None:
        log = r"Package natbib Warning: Citation `foo` on page 1 undefined."
        f = parse_log(log)
        self.assertEqual(len(f["undefined_citations"]), 1)
        self.assertTrue(critical_failure(f))

    def test_parse_overfull_not_critical(self) -> None:
        log = r"Overfull \hbox (1.2pt too wide) in paragraph at lines 10--12"
        f = parse_log(log)
        self.assertEqual(len(f["overfull_boxes"]), 1)
        self.assertFalse(critical_failure(f))

    def test_parse_latex_error_critical(self) -> None:
        log = "! Undefined control sequence.\nl.1 \\foo"
        f = parse_log(log)
        self.assertGreaterEqual(len(f["errors"]), 1)
        self.assertTrue(critical_failure(f))


if __name__ == "__main__":
    unittest.main()
