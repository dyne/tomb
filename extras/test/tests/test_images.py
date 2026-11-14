"""Debian selection and image verification contracts, without network access."""

import contextlib
import hashlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("tomb_images", Path(__file__).parents[1] / "qemu/fetch-image.py")
IMAGES = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(IMAGES)


class ImageTests(unittest.TestCase):
    def test_each_version_fetches_its_own_verified_image(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            for version, release in [("11", "bullseye"), ("12", "bookworm"), ("13", "trixie")]:
                with self.subTest(version=version):
                    base = f"https://cloud.debian.org/images/cloud/{release}/latest/"
                    name = f"debian-{version}-generic-amd64.qcow2"
                    content = f"disk fixture {version}".encode()
                    checksum = hashlib.sha512(content).hexdigest()
                    responses = [io.BytesIO(f"{checksum}  {name}\n".encode()), io.BytesIO(content)]
                    with patch.object(IMAGES.urllib.request, "urlopen", side_effect=responses) as request:
                        with contextlib.redirect_stdout(io.StringIO()):
                            IMAGES.fetch(directory, version)
                    self.assertEqual([call.args[0] for call in request.call_args_list],
                                     [base + "SHA512SUMS", base + name])
                    self.assertEqual((directory / name).read_bytes(), content)
                    self.assertEqual((directory / (name + ".sha512")).read_text(), f"{checksum}  {name}\n")

    def test_default_remains_debian_12_and_verified_cache_is_reused(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            name = "debian-12-generic-amd64.qcow2"
            content = b"cached fixture"
            (directory / name).write_bytes(content)
            checksum = hashlib.sha512(content).hexdigest()
            response = io.BytesIO(f"{checksum}  {name}\n".encode())
            with patch.object(IMAGES.urllib.request, "urlopen", return_value=response) as request:
                with contextlib.redirect_stdout(io.StringIO()):
                    IMAGES.fetch(directory)
            request.assert_called_once_with(
                "https://cloud.debian.org/images/cloud/bookworm/latest/SHA512SUMS", timeout=60)

    def test_checksum_failure_preserves_the_existing_image(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            name = "debian-13-generic-amd64.qcow2"
            (directory / name).write_bytes(b"previous image")
            checksum = hashlib.sha512(b"expected download").hexdigest()
            responses = [io.BytesIO(f"{checksum}  {name}\n".encode()), io.BytesIO(b"corrupt download")]
            with patch.object(IMAGES.urllib.request, "urlopen", side_effect=responses):
                with self.assertRaisesRegex(ValueError, "checksum mismatch"):
                    IMAGES.fetch(directory, "13")
            self.assertEqual((directory / name).read_bytes(), b"previous image")

    def test_unsupported_version_is_rejected_before_network_access(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(IMAGES.urllib.request, "urlopen") as request:
                with self.assertRaisesRegex(ValueError, "Unsupported Debian version"):
                    IMAGES.fetch(Path(tmp), "99")
            request.assert_not_called()


if __name__ == "__main__":
    unittest.main()
