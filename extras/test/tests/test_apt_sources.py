"""Guest APT configuration contracts, using fixtures instead of system files."""

import importlib.util
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("tomb_apt", Path(__file__).parents[1] / "qemu/apt-sources.py")
APT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(APT)


class AptSourceTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        (self.root / "sources.list.d").mkdir()

    def test_bullseye_rewrites_security_only_and_preserves_verification(self):
        source = self.root / "sources.list"
        main = "deb http://deb.debian.org/debian bullseye main\n"
        updates = "deb http://deb.debian.org/debian bullseye-updates main\n"
        security = "deb [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] http://security.debian.org/debian-security bullseye-security main\n"
        source.write_text(main + updates + security)
        self.assertEqual(APT.configure_sources(self.root, "bullseye"), [source])
        expected = main + updates + security.replace("security.debian.org", "archive.debian.org")
        self.assertEqual(source.read_text(), expected)
        self.assertEqual(APT.configure_sources(self.root, "bullseye"), [])

    def test_deb822_and_extra_list_files_accept_either_live_security_host(self):
        deb822 = self.root / "sources.list.d/debian.sources"
        original = ("Types: deb\nURIs: https://deb.debian.org/debian-security/\n"
                    "Suites: bullseye-security\nComponents: main\n"
                    "Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg\n")
        deb822.write_text(original)
        extra = self.root / "sources.list.d/security.list"
        extra.write_text("deb https://security.debian.org/debian-security bullseye-security main\n")
        self.assertCountEqual(APT.configure_sources(self.root, "bullseye"), [deb822, extra])
        self.assertEqual(deb822.read_text(), original.replace(
            "https://deb.debian.org/debian-security", "https://archive.debian.org/debian-security"))
        self.assertIn("https://archive.debian.org/debian-security", extra.read_text())

    def test_supported_releases_leave_sources_unchanged(self):
        source = self.root / "sources.list"
        original = "deb http://security.debian.org/debian-security bookworm-security main\n"
        for codename in ("bookworm", "trixie", ""):
            with self.subTest(codename=codename):
                source.write_text(original)
                self.assertEqual(APT.configure_sources(self.root, codename), [])
                self.assertEqual(source.read_text(), original)


if __name__ == "__main__":
    unittest.main()
