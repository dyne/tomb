"""Runner contracts using controlled Bats/QEMU fixtures, without real VM boot."""

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

TEST_HOME = Path(__file__).resolve().parents[1]


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.env = os.environ.copy()
        self.env["PATH"] = str(self.bin) + os.pathsep + self.env["PATH"]
        self.output = self.root / "results with spaces"

    def executable(self, name, body):
        path = self.bin / name
        path.write_text(body)
        path.chmod(0o755)
        return path

    def runner(self, tap, exit_code=0):
        self.env["BATS"] = str(self.executable("bats", "#!/bin/bash\nprintf '%s\\n' \"$FIXTURE_TAP\"\nexit \"$FIXTURE_EXIT\"\n"))
        self.env["FIXTURE_TAP"] = tap
        self.env["FIXTURE_EXIT"] = str(exit_code)
        return subprocess.run(["bash", str(TEST_HOME / "run"), "--suite", "smoke",
                               "--output-dir", str(self.output)], env=self.env,
                              capture_output=True, text=True, timeout=30)

    def test_success_retains_tap_manifest_and_reports(self):
        run = self.runner("1..1\nok 1 fixture")
        self.assertEqual(run.returncode, 0, run.stderr + run.stdout)
        self.assertEqual(json.loads((self.output / "summary.json").read_text())["passed"], 1)
        self.assertTrue((self.output / "manifest.json").is_file())
        self.assertTrue((self.output / "junit.xml").is_file())
        self.assertIn("fixture", (self.output / "results.tap").read_text())

    def test_failed_assertion_preserves_nonzero_exit(self):
        run = self.runner("1..1\nnot ok 1 broken\n# diagnostic", 1)
        self.assertNotEqual(run.returncode, 0)
        self.assertIn("broken", (self.output / "summary.txt").read_text())

    def test_empty_filter_cannot_create_green_results(self):
        run = self.runner("1..0")
        self.assertNotEqual(run.returncode, 0)
        self.assertIn("No tests executed", run.stdout)

    def test_existing_results_are_not_overwritten(self):
        self.output.mkdir()
        marker = self.output / "preserve"
        marker.write_text("old evidence")
        run = self.runner("1..1\nok 1 fixture")
        self.assertNotEqual(run.returncode, 0)
        self.assertEqual(marker.read_text(), "old evidence")

    def qemu(self, mode):
        # Stub only the two external VM tools. Real archive creation, argument
        # handling, completion checks, summaries, and cleanup still execute.
        self.executable("xorriso", "#!/bin/bash\nexit 0\n")
        self.executable("qemu-system-x86_64", """#!/usr/bin/env python3
import json, os, sys, time
from pathlib import Path
args = sys.argv[1:]
Path(os.environ['FIXTURE_ARGS']).write_text(json.dumps(args))
mode = os.environ['FIXTURE_MODE']
if mode == 'timeout':
    time.sleep(10)
    sys.exit(0)
share = next(x for x in args if 'mount_tag=tomb-results,' in x)
output = Path(share.split('path=', 1)[1].split(',mount_tag=', 1)[0])
(output / 'serial.log').write_text('guest console')
if mode != 'missing':
    (output / 'guest-exit-code').write_text('3' if mode == 'guest-failure' else '0')
    (output / 'tests').mkdir()
    report = dict(status='failed' if mode == 'test-failure' else 'passed', passed=1, errors=[])
    (output / 'tests/summary.json').write_text(json.dumps(report))
    (output / 'tests/summary.txt').write_text('fixture test summary\\n')
sys.exit(2 if mode == 'emulator-failure' else 0)
""")
        self.env["FIXTURE_MODE"] = mode
        self.env["FIXTURE_ARGS"] = str(self.root / "qemu-args.json")
        image = self.root / "base image.qcow2"
        image.write_bytes(b"fixture disk, not a bootable image")
        run = subprocess.run(["bash", str(TEST_HOME / "qemu/run"), "--image", str(image),
                              "--output-dir", str(self.output), "--accel", "tcg",
                              "--timeout", "1" if mode == "timeout" else "10"],
                             env=self.env, capture_output=True, text=True, timeout=30)
        self.assertEqual(image.read_bytes(), b"fixture disk, not a bootable image")
        return run

    @unittest.skipUnless(shutil.which("tar") and shutil.which("timeout"), "GNU host tools required")
    def test_vm_success_requires_guest_marker_and_passing_report(self):
        run = self.qemu("pass")
        self.assertEqual(run.returncode, 0, run.stderr + run.stdout)
        args = json.loads((self.root / "qemu-args.json").read_text())
        self.assertTrue(any("snapshot=on" in arg for arg in args))
        self.assertTrue(any("mount_tag=tomb-source" in arg and "readonly=on" in arg for arg in args))
        self.assertTrue((self.output / "vm.json").is_file())
        self.assertEqual(json.loads((self.output / "vm-result.json").read_text())["status"], "passed")

    def test_emulator_shutdown_without_guest_results_fails(self):
        run = self.qemu("missing")
        self.assertNotEqual(run.returncode, 0)
        self.assertIn("completion marker missing", run.stdout)
        self.assertEqual((self.output / "serial.log").read_text(), "guest console")

    def test_guest_failure_overrides_emulator_success(self):
        run = self.qemu("guest-failure")
        self.assertNotEqual(run.returncode, 0)
        self.assertIn("Guest exited 3", run.stdout)

    def test_failed_guest_report_overrides_completion_marker(self):
        run = self.qemu("test-failure")
        self.assertNotEqual(run.returncode, 0)
        self.assertIn("not a passing execution", run.stdout)

    def test_emulator_failure_overrides_passing_guest_report(self):
        run = self.qemu("emulator-failure")
        self.assertNotEqual(run.returncode, 0)
        self.assertIn("QEMU exited 2", run.stdout)

    def test_vm_timeout_produces_failure_report(self):
        run = self.qemu("timeout")
        self.assertNotEqual(run.returncode, 0)
        self.assertIn("timeout", run.stdout)
        self.assertTrue((self.output / "vm-result.json").is_file())


if __name__ == "__main__":
    unittest.main()
