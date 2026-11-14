#!/usr/bin/env python3
"""Download Debian's generic amd64 cloud image and verify its published SHA512."""

import argparse
import hashlib
import os
import tempfile
import urllib.request
from pathlib import Path

BASE = "https://cloud.debian.org/images/cloud/bookworm/latest/"
NAME = "debian-12-generic-amd64.qcow2"


def sha512(path):
    digest = hashlib.sha512()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fetch(directory):
    directory.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(BASE + "SHA512SUMS", timeout=60) as response:
        checksums = response.read().decode()
    matches = [line.split()[0] for line in checksums.splitlines()
               if len(line.split()) == 2 and line.split()[1].lstrip("*") == NAME]
    if len(matches) != 1 or len(matches[0]) != 128:
        raise ValueError("No unique image checksum in Debian SHA512SUMS")
    expected = matches[0]
    image = directory / NAME
    if not image.exists() or sha512(image) != expected:
        with tempfile.TemporaryDirectory(prefix=".download-", dir=directory) as scratch:
            candidate = Path(scratch) / NAME
            with urllib.request.urlopen(BASE + NAME, timeout=60) as response, candidate.open("wb") as target:
                while block := response.read(1024 * 1024):
                    target.write(block)
            if sha512(candidate) != expected:
                raise ValueError("Image checksum mismatch; the latest image may have changed, retry")
            os.replace(candidate, image)
    (directory / (NAME + ".sha512")).write_text(f"{expected}  {NAME}\n")
    print(image.resolve())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    fetch(parser.parse_args().directory)
