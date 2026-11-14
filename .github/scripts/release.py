#!/usr/bin/env python3
"""Prepare release evidence and version stamps; version arithmetic belongs to semver-action."""

import argparse
import datetime as dt
import html
import json
import os
import re
import subprocess
from pathlib import Path

TAG = re.compile(r"v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")


def git(repo, *args, env=None):
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True, text=True, env=env).stdout.strip()


def version(tag):
    match = TAG.fullmatch(tag)
    if not match:
        raise ValueError(f"Expected a stable vMAJOR.MINOR.PATCH tag, got {tag!r}")
    return tuple(map(int, match.groups()))


def baseline(repo, ref="HEAD"):
    source = git(repo, "rev-parse", f"{ref}^{{commit}}")
    tags = git(repo, "tag", "--merged", source).splitlines()
    stable = [tag for tag in tags if TAG.fullmatch(tag)]
    if not stable:
        raise ValueError("No reachable semantic tag: first alias v2.13 as v2.13.0 at the same commit")
    previous = max(stable, key=version)
    legacy = [tag for tag in tags if re.fullmatch(r"v[0-9]+\.[0-9]+", tag)]
    if any(tuple(map(int, tag[1:].split('.'))) + (0,) > version(previous) for tag in legacy):
        raise ValueError("A newer two-component tag needs a same-commit semantic alias before releasing")
    bootstrap = previous == "v2.13.0" and "v2.13" in tags
    if bootstrap and git(repo, "rev-parse", "v2.13^{commit}") != git(repo, "rev-parse", "v2.13.0^{commit}"):
        raise ValueError("v2.13 and v2.13.0 must identify the same historical release commit")
    count = int(git(repo, "rev-list", "--count", f"{previous}..{source}"))
    if not count:
        raise ValueError("No new commits since the last release")
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    return dict(base_tag=previous, source_sha=source, commit_count=count,
                legacy_bootstrap=bootstrap, timestamp=now.isoformat(), date=now.date().isoformat())


def commits_since(repo, previous, source):
    raw = git(repo, "log", "--reverse", "--format=%H%x00%an%x00%aI%x00%B%x00", f"{previous}..{source}")
    fields = raw.split("\0")
    commits = []
    for offset in range(0, len(fields) - 1, 4):
        sha, author, date, message = fields[offset:offset + 4]
        subject = next((line for line in message.splitlines() if line.strip()), "(no commit message)")
        commits.append(dict(sha=sha.strip(), author=author, date=date,
                            subject=subject, message=message.strip()))
    return commits


def markdown(text):
    return re.sub(r"([\\`*_\[\]])", r"\\\1", html.escape(text, quote=False))


def release_report(repo, plan, next_tag, bump, repository, rationale=""):
    version(next_tag)
    if version(next_tag) <= version(plan["base_tag"]):
        raise ValueError("The next version must be greater than the baseline")
    if plan["legacy_bootstrap"] and version(next_tag) < (2, 14, 0):
        raise ValueError("The first semantic release must be at least v2.14.0")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        raise ValueError("Invalid GitHub repository name")
    commits = commits_since(repo, plan["base_tag"], plan["source_sha"])
    if len(commits) != plan["commit_count"]:
        raise ValueError("Commit count changed since version planning")
    url = f"https://github.com/{repository}"
    groups = {name: [] for name in ("Breaking changes", "Features", "Fixes", "Other changes")}
    for commit in commits:
        subject = commit["subject"]
        if re.search(r"BREAKING[ -]CHANGE:|^[\w-]+(?:\([^\n]*\))?!:", commit["message"], re.M):
            category = "Breaking changes"
        elif re.match(r"(?:feat|feature)(?:\([^)]*\))?:", subject, re.I):
            category = "Features"
        elif re.match(r"(?:fix|bugfix)(?:\([^)]*\))?:|^fix(?:ed)?\b", subject, re.I):
            category = "Fixes"
        else:
            category = "Other changes"
        groups[category].append(f"- {markdown(subject)} ([{commit['sha'][:8]}]({url}/commit/{commit['sha']})) — {markdown(commit['author'])}")
    changes = []
    for category, entries in groups.items():
        if entries:
            changes.extend([f"### {category}", "", *entries, ""])
    lines = [f"# Tomb {next_tag}", "", f"- Release date: {plan['date']}",
             f"- Previous release: `{plan['base_tag']}`", f"- Version increment: `{bump}`",
             f"- Commits since the previous release: {len(commits)}",
             f"- Source candidate: `{plan['source_sha']}`",
             f"- [Full comparison]({url}/compare/{plan['base_tag']}...{plan['source_sha']})", ""]
    if plan["legacy_bootstrap"]:
        lines.extend(["`v2.13.0` is an alias of the historical `v2.13` release, not a new release.", ""])
    if rationale:
        lines.extend([markdown(rationale), ""])
    lines.extend(changes)
    report = dict(**plan, next_tag=next_tag, next_version=next_tag[1:], bump=bump,
                  rationale=rationale, commits=commits)
    return report, "\n".join(lines), "\n".join(changes)


def publication(directory, release_commit, run_url):
    if not re.fullmatch(r"[0-9a-f]{40}", release_commit):
        raise ValueError("Invalid release commit")
    if not re.fullmatch(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/actions/runs/[0-9]+", run_url):
        raise ValueError("Invalid validation run URL")
    path = directory / "release.json"
    report = json.loads(path.read_text())
    report.update(release_commit=release_commit, validation_run=run_url,
                  validation="Native Bats, legacy suite, and Debian 11/12/13 QEMU jobs succeeded")
    path.write_text(json.dumps(report, indent=2) + "\n")
    with (directory / "release.md").open("a") as notes:
        notes.write(f"\n## Publication\n\n- Release commit: `{release_commit}`\n"
                    f"- [Validation run]({run_url}): native Bats, legacy, and Debian 11/12/13 QEMU jobs succeeded.\n"
                    "- See the validation artifacts for individual results and skipped cases.\n"
                    "- Source archive and SHA256SUMS are attached to this release.\n")


def stamp(repo, report, changes):
    """Stamp only release metadata, then make a reproducible version commit."""
    if git(repo, "rev-parse", "HEAD") != report["source_sha"]:
        raise ValueError("Checkout differs from the planned source commit")
    if git(repo, "status", "--porcelain", "--untracked-files=no"):
        raise ValueError("Tracked files must be clean before release preparation")
    date = dt.date.fromisoformat(report["date"])
    path = repo / "tomb"
    source = path.read_text()
    source, versions = re.subn(r'^typeset VERSION="[^"]*"$',
                               f'typeset VERSION="{report["next_version"]}"', source, flags=re.M)
    source, dates = re.subn(r'^typeset DATE="[^"]*"$',
                            f'typeset DATE="{date.strftime("%b/%Y")}"', source, flags=re.M)
    if (versions, dates) != (1, 1):
        raise ValueError("Expected one VERSION and one DATE declaration")
    path.write_text(source)
    manual = repo / "doc/tomb.1"
    text, count = re.subn(r'^\.TH tomb 1 "[^"]*"',
                          f'.TH tomb 1 "{date.strftime("%b %d, %Y")}"', manual.read_text(), count=1)
    if count != 1:
        raise ValueError("Cannot locate the manual's release date")
    manual.write_text(text)
    changelog = repo / "ChangeLog.md"
    existing = changelog.read_text()
    heading = "# Tomb ChangeLog\n"
    if not existing.startswith(heading):
        raise ValueError("Unexpected changelog heading")
    entry = f"## {report['next_version']}\n### {date.strftime('%B %Y')}\n\n{changes}\n"
    changelog.write_text(heading + entry + existing[len(heading):])
    git(repo, "add", "tomb", "doc/tomb.1", "ChangeLog.md")
    env = dict(os.environ, GIT_AUTHOR_DATE=report["timestamp"], GIT_COMMITTER_DATE=report["timestamp"])
    git(repo, "-c", "user.name=github-actions[bot]", "-c", "user.email=41898282+github-actions[bot]@users.noreply.github.com",
        "-c", "commit.gpgsign=false", "commit", "-m", f"chore(release): {report['next_tag']}", env=env)
    return git(repo, "rev-parse", "HEAD")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    sub = parser.add_subparsers(dest="operation", required=True)
    plan = sub.add_parser("baseline")
    plan.add_argument("--ref", default="HEAD")
    plan.add_argument("--output", type=Path, required=True)
    plan.add_argument("--github-output", type=Path)
    notes = sub.add_parser("report")
    notes.add_argument("--plan", type=Path, required=True)
    notes.add_argument("--next-tag", required=True)
    notes.add_argument("--bump", choices=("major", "minor", "patch"), required=True)
    notes.add_argument("--repository", required=True)
    notes.add_argument("--rationale", default="")
    notes.add_argument("--output-dir", type=Path, required=True)
    prepare = sub.add_parser("stamp")
    prepare.add_argument("--report-dir", type=Path, required=True)
    published = sub.add_parser("publication")
    published.add_argument("--report-dir", type=Path, required=True)
    published.add_argument("--release-commit", required=True)
    published.add_argument("--run-url", required=True)
    args = parser.parse_args()
    if args.operation == "baseline":
        data = baseline(args.repo, args.ref)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(data, indent=2) + "\n")
        if args.github_output:
            with args.github_output.open("a") as target:
                for key in ("base_tag", "source_sha", "timestamp", "legacy_bootstrap"):
                    value = str(data[key]).lower() if isinstance(data[key], bool) else data[key]
                    target.write(f"{key}={value}\n")
    elif args.operation == "report":
        data, text, changes = release_report(args.repo, json.loads(args.plan.read_text()),
            args.next_tag, args.bump, args.repository, args.rationale)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / "release.json").write_text(json.dumps(data, indent=2) + "\n")
        (args.output_dir / "release.md").write_text(text + "\n")
        (args.output_dir / "changes.md").write_text(changes + "\n")
    elif args.operation == "stamp":
        report = json.loads((args.report_dir / "release.json").read_text())
        print(stamp(args.repo, report, (args.report_dir / "changes.md").read_text()))
    else:
        publication(args.report_dir, args.release_commit, args.run_url)


if __name__ == "__main__":
    main()
