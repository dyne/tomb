#!/usr/bin/env python3
"""Use the Debian archive for bullseye's retired security package repository."""

import argparse
import re
from pathlib import Path


def configure_sources(directory, codename):
    if codename != "bullseye":
        return []
    sources = [directory / "sources.list"]
    sources += sorted((directory / "sources.list.d").glob("*.list"))
    sources += sorted((directory / "sources.list.d").glob("*.sources"))
    changed = []
    for source in sources:
        if not source.is_file():
            continue
        original = source.read_text()
        updated = re.sub(r"(https?)://(?:security|deb)\.debian\.org/debian-security(?=[/\s]|$)",
                         r"\1://archive.debian.org/debian-security", original)
        if updated != original:
            source.write_text(updated)
            changed.append(source)
    return changed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codename", required=True)
    parser.add_argument("--apt-dir", type=Path, default=Path("/etc/apt"))
    args = parser.parse_args()
    for source in configure_sources(args.apt_dir, args.codename):
        print(f"{source}: use official Debian archive for bullseye security packages")
