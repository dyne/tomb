# Releasing Tomb

Only the **Release Tomb** workflow calculates and publishes releases. It has a
`workflow_dispatch` trigger: pushes, tags, PRs, and merges never launch release
calculation or publication automatically. Ordinary test CI continues to run.

## Tag migration

The historical `v2.13` tag is preserved. `v2.13.0` is a second tag at that exact
historical release commit, not at the current development HEAD. It does not
represent another release. Older tags are not renamed or moved.

New release tags use `vMAJOR.MINOR.PATCH`. The first new semantic release is at
least `v2.14.0`, accounting for unreleased FIDO2 functionality whose original
commit messages predate Conventional Commits. This one-time minor floor is
provided to the semver action as an additional feature message and recorded in
the report. A detected breaking change may select a higher version.

## Request a release

After this workflow is merged into `master`:

1. Open **Actions → Release Tomb → Run workflow**.
2. Select the `master` branch.
3. Leave **preview** unchecked to publish. Check it to calculate the version and
   download the report without tests, version commits, tags, or publication.
4. Start the workflow.

Publication is the default when a maintainer manually starts the workflow. The
workflow does not dispatch itself. It rejects other branches and serializes
release runs rather than cancelling a release in progress.

## Version calculation and coverage

The workflow checks out the exact dispatched commit with full tag/history
coverage and selects the highest reachable stable semantic tag. A newer legacy
two-component tag without a corresponding semantic baseline is an error; it
does not silently fall back to an older release.

[`ietf-tools/semver-action`](https://github.com/ietf-tools/semver-action) is pinned
to a reviewed commit. It compares the selected tag with the exact source SHA
and paginates across the entire commit range. No commit limit or first-parent
filter is applied. Conventional Commit prefixes determine the increment:

- `feat:` / `feature:` select a minor increment.
- A `BREAKING CHANGE:` note selects a major increment.
- Other parsed commit types count as patch changes. If none of the historical
  messages can select a bump, the fallback is patch.
- No new commits means no new release.

The generated report lists **every commit** in the range, including older
message styles and merge commits, independently of which messages the action
can classify. It contains grouped changes, author/commit links, the comparison,
baseline, source SHA, chosen increment, date, and migration rationale. JSON is
provided alongside Markdown.

## Validation and publication

A production run reuses the ordinary Linux CI workflow, including native Bats,
the legacy suite, and the Debian 11/12/13 QEMU matrix. Publication requires all
those jobs to succeed for the dispatched source. Preview runs stop at planning.

After validation the workflow stamps the calculated version and date in `tomb`,
updates the manual date, prepends generated notes to `ChangeLog.md`, and creates
a `chore(release): vX.Y.Z` metadata commit. Historical changelog entries remain.
Zsh syntax is checked after stamping; the functional test gate covered the
source candidate before these release-metadata changes.

The metadata commit and tag are pushed atomically. If `master` changed during
validation, publication stops; request a new manual run so those new commits
are included. The workflow never force-pushes branches or tags. Repository
policy must permit the workflow token to push release metadata to `master`.

The published GitHub Release contains:

- `Tomb-X.Y.Z.tar.gz`, built from the tagged metadata commit with the correct
  runtime version, manual, and changelog;
- `release.md` and `release.json`, including the release commit and validation
  run link;
- `SHA256SUMS` covering the archive and both reports.

The Actions summary displays the generated report. Planning and publication
artifacts are retained for 30 days, including partial results after failure.
Checksums describe integrity; this workflow does not generate maintainer GPG
signatures for distribution outside GitHub.

## Recovering a publication failure

If tests fail, no new release commit or tag is pushed. Fix the problem and start
a new manual release run.

If publication fails after the atomic push, use **Re-run failed jobs** on that
same Actions run. The successful planning/test outputs and frozen report are
reused. Metadata commits are reproducible from that report; an existing tag
must identify the same commit. A matching release that already exists is left
unchanged. Do not delete or move a release tag to retry publication.
