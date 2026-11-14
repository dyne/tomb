"""Release-boundary, complete-report, and reproducible stamping contracts."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("tomb_release", Path(__file__).resolve().parents[3] / ".github/scripts/release.py")
RELEASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RELEASE)


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.repo = Path(self.scratch.name)
        RELEASE.git(self.repo, "init", "-q")
        RELEASE.git(self.repo, "config", "user.name", "Release Test")
        RELEASE.git(self.repo, "config", "user.email", "release@example.invalid")
        (self.repo / "doc").mkdir()
        (self.repo / "tomb").write_text('typeset VERSION="2.13.0"\ntypeset DATE="Jul/2025"\n')
        (self.repo / "doc/tomb.1").write_text('.TH tomb 1 "Jun 25, 2023" "tomb"\n')
        (self.repo / "ChangeLog.md").write_text("# Tomb ChangeLog\n## 2.13\nHistorical notes.\n")
        self.commit("Historical release")
        RELEASE.git(self.repo, "tag", "v2.13")
        RELEASE.git(self.repo, "tag", "v2.8.1")

    def commit(self, subject):
        RELEASE.git(self.repo, "add", ".")
        return RELEASE.git(self.repo, "commit", "--allow-empty", "-qm", subject)

    def plan(self):
        RELEASE.git(self.repo, "tag", "v2.13.0", "v2.13")
        self.commit("Added support using an older message style")
        self.commit("feat: a new feature")
        return RELEASE.baseline(self.repo)

    def test_legacy_tag_requires_alias_instead_of_using_an_older_release(self):
        self.commit("fix: new work")
        with self.assertRaisesRegex(ValueError, "same-commit semantic alias"):
            RELEASE.baseline(self.repo)

    def test_alias_preserves_the_historical_boundary_and_all_commits(self):
        plan = self.plan()
        self.assertEqual(plan["base_tag"], "v2.13.0")
        self.assertEqual(plan["commit_count"], 2)
        self.assertTrue(plan["legacy_bootstrap"])
        report, text, _ = RELEASE.release_report(self.repo, plan, "v2.14.0", "minor", "dyne/tomb")
        self.assertEqual(len(report["commits"]), 2)
        self.assertIn("Added support using an older message style", text)
        self.assertIn("a new feature", text)
        self.assertIn("Historical", (self.repo / "ChangeLog.md").read_text())

    def test_alias_must_not_point_at_new_work(self):
        self.commit("fix: new work")
        RELEASE.git(self.repo, "tag", "v2.13.0")
        with self.assertRaisesRegex(ValueError, "same historical release commit"):
            RELEASE.baseline(self.repo)

    def test_no_release_without_new_commits(self):
        RELEASE.git(self.repo, "tag", "v2.13.0")
        with self.assertRaisesRegex(ValueError, "No new commits"):
            RELEASE.baseline(self.repo)

    def test_report_rejects_a_version_that_does_not_increase(self):
        with self.assertRaisesRegex(ValueError, "greater than the baseline"):
            RELEASE.release_report(self.repo, self.plan(), "v2.13.0", "patch", "dyne/tomb")

    def test_initial_release_has_a_minor_version_floor(self):
        with self.assertRaisesRegex(ValueError, "at least v2.14.0"):
            RELEASE.release_report(self.repo, self.plan(), "v2.13.1", "patch", "dyne/tomb")

    def test_later_releases_use_the_latest_semantic_tag_without_the_floor(self):
        self.plan()
        RELEASE.git(self.repo, "tag", "v2.14.0")
        self.commit("fix: a later correction")
        plan = RELEASE.baseline(self.repo)
        self.assertFalse(plan["legacy_bootstrap"])
        report, _, _ = RELEASE.release_report(self.repo, plan, "v2.14.1", "patch", "dyne/tomb")
        self.assertEqual(report["next_tag"], "v2.14.1")

    def test_version_stamp_is_reproducible_and_preserves_historical_notes(self):
        plan = self.plan()
        report, _, changes = RELEASE.release_report(self.repo, plan, "v2.14.0", "minor", "dyne/tomb")
        first = RELEASE.stamp(self.repo, report, changes)
        self.assertIn('VERSION="2.14.0"', (self.repo / "tomb").read_text())
        self.assertIn("Historical notes.", (self.repo / "ChangeLog.md").read_text())
        self.assertIn("## 2.14.0", (self.repo / "ChangeLog.md").read_text())
        RELEASE.git(self.repo, "reset", "--hard", plan["source_sha"])
        self.assertEqual(RELEASE.stamp(self.repo, report, changes), first)

    def test_publication_report_preserves_the_range_and_links_validation(self):
        report, text, _ = RELEASE.release_report(self.repo, self.plan(), "v2.14.0", "minor", "dyne/tomb")
        directory = self.repo / "report"
        directory.mkdir()
        (directory / "release.json").write_text(json.dumps(report))
        (directory / "release.md").write_text(text)
        sha = "f" * 40
        run = "https://github.com/dyne/tomb/actions/runs/123"
        RELEASE.publication(directory, sha, run)
        published = json.loads((directory / "release.json").read_text())
        self.assertEqual(published["release_commit"], sha)
        self.assertEqual(published["validation_run"], run)
        self.assertEqual(published["commits"], report["commits"])
        self.assertIn(run, (directory / "release.md").read_text())


if __name__ == "__main__":
    unittest.main()
