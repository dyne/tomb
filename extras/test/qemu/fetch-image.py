#!/usr/bin/env python3
"""Download Debian's generic amd64 cloud image and verify its published SHA512."""

import argparse
import hashlib
import os
import tempfile
import urllib.request
from pathlib import Path

RELEASES = {"11": "bullseye", "12": "bookworm", "13": "trixie"}


def image_spec(version):
    if version not in RELEASES:
        raise ValueError(f"Unsupported Debian version: {version}")
    return (f"https://cloud.debian.org/images/cloud/{RELEASES[version]}/latest/",
            f"debian-{version}-generic-amd64.qcow2")


def sha512(path):
    digest = hashlib.sha512()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fetch(directory, version="12"):
    base, name = image_spec(version)
    directory.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(base + "SHA512SUMS", timeout=60) as response:
        checksums = response.read().decode()
    matches = [line.split()[0] for line in checksums.splitlines()
               if len(line.split()) == 2 and line.split()[1].lstrip("*") == name]
    if len(matches) != 1 or len(matches[0]) != 128:
        raise ValueError("No unique image checksum in Debian SHA512SUMS")
    expected = matches[0]
    image = directory / name
    if not image.exists() or sha512(image) != expected:
        with tempfile.TemporaryDirectory(prefix=".download-", dir=directory) as scratch:
            candidate = Path(scratch) / name
            with urllib.request.urlopen(base + name, timeout=60) as response, candidate.open("wb") as target:
                while block := response.read(1024 * 1024):
                    target.write(block)
            if sha512(candidate) != expected:
                raise ValueError("Image checksum mismatch; the latest image may have changed, retry")
            os.replace(candidate, image)
    (directory / (name + ".sha512")).write_text(f"{expected}  {name}\n")
    print(image.resolve())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--debian", choices=sorted(RELEASES), default="12")
    args = parser.parse_args()
    fetch(args.directory, args.debian)
