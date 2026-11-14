"""Reporting contracts: preserve failed/skipped cases and reject incomplete TAP."""

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("tomb_report", Path(__file__).parents[1] / "report.py")
REPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REPORT)


class ReportingTests(unittest.TestCase):
    def test_successful_run_with_optional_skip(self):
        tests, errors = REPORT.parse_tap("1..2\nok 1 lifecycle\nok 2 optional # skip missing tool\n", 0)
        self.assertEqual(errors, [])
        self.assertEqual([t["status"] for t in tests], ["passed", "skipped"])
        self.assertEqual(tests[1]["name"], "optional")
        self.assertEqual(tests[1]["reason"], "missing tool")

    def test_failure_keeps_assertion_diagnostics(self):
        tests, errors = REPORT.parse_tap("1..1\nnot ok 1 wrong password\n# expected nonzero\n", 1)
        self.assertEqual(errors, [])
        self.assertEqual(tests[0]["status"], "failed")
        self.assertEqual(tests[0]["diagnostics"], ["expected nonzero"])

    def test_empty_selection_is_not_success(self):
        _, errors = REPORT.parse_tap("1..0\n", 0)
        self.assertTrue(any("No tests executed" in error for error in errors))

    def test_all_skipped_is_not_success(self):
        _, errors = REPORT.parse_tap("1..1\nok 1 optional # skip no dependency\n", 0)
        self.assertTrue(any("No tests executed" in error for error in errors))

    def test_truncated_output_is_not_success(self):
        _, errors = REPORT.parse_tap("1..2\nok 1 completed\n", 0)
        self.assertTrue(any("Incomplete TAP" in error for error in errors))

    def test_missing_plan_and_duplicate_numbers_are_errors(self):
        _, errors = REPORT.parse_tap("ok 1 first\nok 1 duplicate\n", 0)
        self.assertEqual(len(errors), 2)

    def test_bailout_is_an_error_even_after_a_success(self):
        _, errors = REPORT.parse_tap("1..1\nok 1 first\nBail out! setup failed\n", 0)
        self.assertIn("Bail out! setup failed", errors)

    def test_nonzero_runner_exit_cannot_be_hidden_by_passing_tap(self):
        _, errors = REPORT.parse_tap("1..1\nok 1 first\n", 124)
        self.assertTrue(any("exited 124" in error for error in errors))

    def test_reports_agree_and_escape_xml(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            (output / "results.tap").write_text("1..2\nok 1 success\nnot ok 2 <invalid> & quoted\n# reason & details\n")
            with contextlib.redirect_stdout(io.StringIO()):
                status = REPORT.write_reports(output, 1, 9, "integration")
            self.assertEqual(status, 1)
            summary = json.loads((output / "summary.json").read_text())
            self.assertEqual((summary["passed"], summary["failed"], summary["duration_seconds"]), (1, 1, 9))
            xml = ET.parse(output / "junit.xml").getroot()
            self.assertEqual(xml.attrib["failures"], "1")
            self.assertEqual(xml.findall("testcase")[1].attrib["name"], "<invalid> & quoted")
            self.assertEqual(xml.find("testcase/failure").text, "reason & details")
            self.assertIn("FAIL", (output / "summary.txt").read_text())


if __name__ == "__main__":
    unittest.main()
