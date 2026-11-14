#!/usr/bin/env python3
"""Summarize flat Bats TAP; incomplete execution must never look like a pass."""

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def parse_tap(text, exit_code):
    tests, errors, plans = [], [], []
    for line in text.splitlines():
        plan = re.fullmatch(r"1\.\.(\d+)(?:\s+#.*)?", line)
        result = re.fullmatch(r"(not ok|ok)\s+(\d+)(?:\s+(.*))?", line)
        if plan:
            plans.append(int(plan[1]))
        elif result:
            name = result[3] or "unnamed test"
            skip = re.search(r"\s+#\s*skip\b(.*)", name, re.I)
            tests.append(dict(number=int(result[2]), name=name[:skip.start()] if skip else name,
                              status="skipped" if skip else "failed" if result[1] == "not ok" else "passed",
                              reason=skip[1].strip() if skip else "", diagnostics=[]))
        elif line.startswith("Bail out!"):
            errors.append(line)
        elif line.startswith("#") and tests:
            tests[-1]["diagnostics"].append(line[1:].lstrip())
    if len(plans) != 1:
        errors.append("Expected exactly one TAP plan")
    elif plans[0] != len(tests):
        errors.append(f"Incomplete TAP: planned {plans[0]}, received {len(tests)} results")
    if [t["number"] for t in tests] != list(range(1, len(tests) + 1)):
        errors.append("TAP test numbers are not consecutive")
    if not any(t["status"] != "skipped" for t in tests):
        errors.append("No tests executed (empty selection or all skipped)")
    if exit_code and (exit_code != 1 or not any(t["status"] == "failed" for t in tests)):
        errors.append(f"Bats exited {exit_code}; inspect bats.stderr.log")
    return tests, errors


def write_reports(directory, exit_code, duration, suite):
    tests, errors = parse_tap((directory / "results.tap").read_text(errors="replace"), exit_code)
    counts = {state: sum(t["status"] == state for t in tests)
              for state in ("passed", "failed", "skipped")}
    success = not (errors or counts["failed"] or exit_code)
    result = dict(status="passed" if success else "failed", suite=suite,
                  total=len(tests), **counts, errors=errors, duration_seconds=duration,
                  exit_code=exit_code, tests=tests)
    (directory / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
    lines = [f"Tomb / {suite}: {'PASS' if success else 'FAIL'} ({duration}s)",
             f"  {counts['passed']} passed | {counts['failed']} failed | {counts['skipped']} skipped | {len(errors)} runner errors"]
    for test in tests:
        if test["status"] != "passed":
            lines.append(f"  {test['status'].upper()}: {test['name']} {test['reason']}".rstrip())
    lines.extend(f"  ERROR: {error}" for error in errors)
    lines.append(f"  Reports and per-test logs: {directory}")
    summary = "\n".join(lines) + "\n"
    (directory / "summary.txt").write_text(summary)
    print(summary, end="")

    xml = ET.Element("testsuite", name=f"tomb.{suite}", tests=str(len(tests) + len(errors)),
                     failures=str(counts["failed"]), skipped=str(counts["skipped"]),
                     errors=str(len(errors)), time=str(duration))
    for test in tests:
        case = ET.SubElement(xml, "testcase", classname=f"tomb.{suite}", name=test["name"])
        if test["status"] == "skipped":
            ET.SubElement(case, "skipped", message=test["reason"])
        elif test["status"] == "failed":
            ET.SubElement(case, "failure", message="Bats assertion failed").text = "\n".join(test["diagnostics"])
    for error in errors:
        ET.SubElement(ET.SubElement(xml, "testcase", name="runner", classname="tomb.harness"),
                      "error", message=error)
    ET.indent(xml)
    ET.ElementTree(xml).write(directory / "junit.xml", encoding="utf-8", xml_declaration=True)
    return 0 if success else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--exit-code", type=int, required=True)
    parser.add_argument("--duration", type=int, default=0)
    parser.add_argument("--suite", default="all")
    args = parser.parse_args()
    return write_reports(args.directory, args.exit_code, args.duration, args.suite)


if __name__ == "__main__":
    sys.exit(main())
