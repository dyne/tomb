# Testing Tomb

Tomb's main suite uses [bats-core](https://bats-core.readthedocs.io/) to drive the
Zsh executable. Every integration case owns its volume, key, mountpoint, and GPG
home; tests can be selected without running a numbered predecessor first. Cases
run serially. The original Sharness suite remains available during migration.

## Quick commands

Run these from the repository root. Install bats-core 1.5 or later, Bash,
Python 3.9 or later, Zsh, and GNU coreutils for the host runner.

```sh
# Unprivileged checks; missing optional runtime dependencies are shown as skips.
make test-smoke

# Tests of reporting and orchestration, using fixtures instead of real volumes/VMs.
make test-harness

# Select cases and retain their evidence in a new directory.
bash extras/test/run --suite smoke --filter 'help|unknown' --output-dir .test-results/selected
```

CLI smoke checks need Tomb's runtime dependencies too: cryptsetup, GnuPG,
pinentry, e2fsprogs, file, and Linux utilities. The syntax and missing-dependency
checks can execute without those dependencies. A zero-test selection or a run
in which every test skips is a failure, rather than a green empty run.

## Integration tests inside QEMU

The host needs `qemu-system-x86_64`, `xorriso`, Python, tar, GNU coreutils, and
enough disk space for a cloud image and its temporary writes. The host does not
need root, loop devices, device mapper, SSH keys, or a local Tomb installation.
Only the guest installs Tomb's dependencies and disables its swap.

```sh
# Download a generic amd64 cloud image into an ignored local cache.
# The downloader validates SHA512 against Debian's manifest over HTTPS.
python3 extras/test/qemu/fetch-image.py .test-cache --debian 12

make test-qemu QEMU_IMAGE="$PWD/.test-cache/debian-12-generic-amd64.qcow2"

# Explicit output directory and acceleration selection:
bash extras/test/qemu/run \
  --image .test-cache/debian-12-generic-amd64.qcow2 \
  --output-dir .test-results/my-vm --accel auto --timeout 2400
```

The supplied image must be a trusted Debian/Ubuntu amd64 cloud image with
cloud-init/NoCloud, virtio block/network, and 9p filesystem support. The downloader
accepts `--debian 11`, `12`, or `13` (default `12`) and chooses Debian's **generic**
image, which includes the standard kernel. qcow2 is
the default; pass `--image-format raw` for a raw disk. The image is used in QEMU
snapshot mode, so the base image remains unchanged. Package installation needs
outbound networking; no incoming port is forwarded.

The launcher freezes the current working tree, including uncommitted changes,
into a source archive, excluding `.git`, results, and the image cache. That
archive is shared read-only. The guest copies it to its own disk, installs Bats
and dependencies, builds the PBKDF2 helpers, then runs all native Bats cases.
A separate writable share returns only the selected run's results to the host.
No writable source checkout or host home directory is shared.
Every guest installs Bats 1.11.1 from the same verified upstream commit; Debian
11's packaged Bats is too old for the suite's minimum version.
For Debian 11, the guest redirects the retired security repository to
`archive.debian.org/debian-security` before installing dependencies. This avoids
404s for packages removed from the live security mirror. Main repository URLs,
HTTP/HTTPS selection, and APT verification settings are preserved. Source changes
are recorded in `apt-sources.log`; Debian 12 and 13 keep their original sources.

Acceleration defaults to KVM when opening `/dev/kvm` and checking its API works;
otherwise it uses TCG software emulation. `--accel kvm` requires KVM and surfaces
startup failures; `--accel tcg` explicitly selects emulation. Without KVM, expect
longer boot, package-installation, and cryptographic operations. The VM has 2 GiB
RAM and two virtual CPUs. A host timeout kills a stalled emulator and marks the
run failed. The runner never treats emulator shutdown alone as success: it also
requires the guest completion marker and a passing nonempty test report.

## Reports and logs

Each invocation creates a new directory under `.test-results/`, or uses the
new directory named by `--output-dir`. Existing directories are rejected, so a
rerun does not overwrite earlier evidence. The runner prints its result path
before executing tests and a summary listing every case by name and status
afterward. Failed cases include their TAP assertion diagnostics; skipped cases
include the reason. For example:

```text
Tomb / all: FAIL (123s)
  1 passed | 1 failed | 1 skipped | 0 runner errors
  PASSED   1. contents survive close and reopen
  FAILED   2. wrong password cannot mount a volume
      expected exit 1, got 124
  SKIPPED  3. optional feature (missing tool)
```

The numbers above illustrate the format, not a recorded test run.

| Artifact | Contents |
| --- | --- |
| `results.tap` | Original Bats results, including assertion diagnostics |
| `summary.txt` | Counts, every case's name/status, failure diagnostics, and skip reasons |
| `summary.json` | Counts, exit status, duration, cases, diagnostics, and runner errors |
| `junit.xml` | CI-compatible cases, failures, skips, and infrastructure errors |
| `manifest.json` | Source hashes, Git identity when available, and suite selection |
| `logs/` | Separate command/output logs for each case and baseline key creation |
| `bats.stderr.log` | Runner-level stderr |

For QEMU runs these files live under `tests/` within the VM result directory.
The directory also contains `serial.log`, `qemu.log`, `setup.log`, `seed.log`,
`dmesg.log`, `cloud-init.log`, `kdf-build.log`, `guest-exit-code`, `vm.json`,
`vm-result.json`, `os-release`, and a host `summary.txt`, as far as execution progressed.
`vm.json` records the image hash, source archive hash, and selected acceleration;
the guest's source manifest supplies individual file hashes even though `.git`
is intentionally absent there. Failed bootstrap attempts still retain the host
console log; missing completion markers and missing reports fail the run.

All logs contain test data only. Keep real tombs and credentials out of fixtures.
`TOMB_COMMAND_TIMEOUT` (default 180 seconds) bounds each Tomb invocation;
`TOMB_SUITE_TIMEOUT` (default 1800 seconds) bounds Bats. These variables may be
increased for a slow manually run guest. The host VM timeout covers boot and
package installation too.

## Running directly in an existing disposable Linux guest

After installing the runtime dependencies and enabling loop/device-mapper
support, disable **guest** swap, build/install the PBKDF2 helpers if desired,
and run:

```sh
sudo env TOMB_TEST_DISPOSABLE=1 make test
```

The explicit environment flag and root check guard the integration suite.
Cleanup closes only a case's own mount and reports leaked loop devices; it does
not call `slam all`. Tests cover the volume lifecycle, wrong passwords,
persistence, read-only access, overwrite protection, password/key replacement,
resize, stdin keys, Argon2, PBKDF2, and steganography. Optional KDF/steganography
tools cause explicit skips. Hardware FIDO2 interactions are not exercised.

## Legacy coverage and CI

`sudo make test-legacy` retains the original Sharness suite. Its numbered files
share fixtures and must run serially. Its cleanup calls `slam all`, removes
`/tmp/tomb`, and the hooks test touches the caller's home. Its regression test
downloads and executes old releases. Use it only in a disposable environment.
Recipient tests remain disabled by default in the legacy setup.

The native Bats cases are an initial migration, not a claim of complete parity
with the old suite. Legacy coverage still includes hooks, QR output, historical
releases, and other variants. GitHub Actions retains the legacy suite alongside
Bats on `ubuntu-latest` and runs a QEMU matrix for Debian 11 (bullseye),
12 (bookworm), and 13 (trixie), also hosted on `ubuntu-latest`. Matrix jobs run
independently with fail-fast disabled and upload separate artifacts named
`tomb-qemu-debian11`, `tomb-qemu-debian12`, and `tomb-qemu-debian13`.
CI explicitly installs Bats 1.11.1 on the native runner and inside each guest,
and uploads reports/logs with
`always()` even after failures. The Actions job summary displays the text
reports. `workflow_dispatch` also allows manual execution.

When adding cases, use Bats assertions and the shared helpers; invoke Tomb as a
Zsh subprocess. Preserve independent fixtures, keep output in the case log,
and add explicit prerequisite skips for optional features. Harness regression
tests under `tests/` cover reporting failures and emulator-result extraction
without requiring root or booting a VM.
