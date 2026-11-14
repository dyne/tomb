# Bash helpers for Bats; Tomb itself is always executed by Zsh.

setup_case() {
	export LC_ALL=C
	TOMB_TEST_BIN=${TOMB_TEST_BIN:-"$BATS_TEST_DIRNAME/../../../tomb"}
	CASE_ROOT="$BATS_TEST_TMPDIR/case"
	mkdir -p -- "$CASE_ROOT" "${TOMB_TEST_RESULTS:-$BATS_TEST_TMPDIR}/logs"
	CASE_LOG="${TOMB_TEST_RESULTS:-$BATS_TEST_TMPDIR}/logs/$(printf '%03d' "$BATS_TEST_NUMBER")-${BATS_TEST_NAME//[^a-zA-Z0-9_-]/_}.log"
	printf '%s\n' "$BATS_TEST_DESCRIPTION" >"$CASE_LOG"
	export GNUPGHOME="$CASE_ROOT/gnupg"
	mkdir -m 700 -- "$GNUPGHOME"
	CASE_NAME="bats-$BATS_TEST_NUMBER-$$"
	VOLUME="$CASE_ROOT/$CASE_NAME.tomb"
	KEY="$CASE_ROOT/key with spaces.key"
	MOUNTPOINT="$CASE_ROOT/mounted"
	TEST_PASSWORD='test password with spaces'
}

# Log commands and all output, including successful commands; use dummy secrets only.
tomb_command() {
	local status=0
	{
		printf '\n$ tomb '
		printf '%q ' "$@"
		printf '\n'
	} >>"$CASE_LOG"
	timeout --kill-after=10s "${TOMB_COMMAND_TIMEOUT:-180}s" zsh "$TOMB_TEST_BIN" --no-color "$@" \
		>"$CASE_ROOT/command.out" 2>&1 3>&- || status=$?
	cat "$CASE_ROOT/command.out" >>"$CASE_LOG"
	cat "$CASE_ROOT/command.out"
	printf 'exit=%s\n' "$status" >>"$CASE_LOG"
	return "$status"
}

require_core_tools() {
	local tool
	for tool in cryptsetup gpg mkfs.ext4 e2fsck; do
		command -v "$tool" >/dev/null || skip "missing $tool"
	done
	command -v pinentry >/dev/null || command -v pinentry-tty >/dev/null || skip 'missing pinentry'
}

require_integration() {
	[[ ${TOMB_TEST_DISPOSABLE:-0} == 1 ]] || { echo 'Integration tests require TOMB_TEST_DISPOSABLE=1 in an isolated guest.' >&2; return 1; }
	((EUID == 0)) || { echo 'Integration tests require root inside the guest.' >&2; return 1; }
	local tool
	for tool in cryptsetup gpg mkfs.ext4 e2fsck losetup findmnt mount umount; do
		command -v "$tool" >/dev/null || { echo "Missing integration dependency: $tool" >&2; return 1; }
	done
	[[ -c /dev/mapper/control ]] || { echo 'Device mapper is unavailable.' >&2; return 1; }
	[[ $(wc -l </proc/swaps) -eq 1 ]] || { echo 'Disable guest swap before integration tests.' >&2; return 1; }
}

create_volume() {
	cp -- "$BATS_FILE_TMPDIR/baseline.key" "$KEY"
	tomb_command dig -s 20 "$VOLUME"
	tomb_command lock -k "$KEY" "$VOLUME" --unsafe --tomb-pwd "$TEST_PASSWORD"
}

open_volume() {
	tomb_command open "$VOLUME" "$MOUNTPOINT" -k "$KEY" --nohook --unsafe --tomb-pwd "$TEST_PASSWORD" "$@"
}

close_volume() {
	tomb_command close "$CASE_NAME"
}

# Close only this case's mount; never invoke the legacy global `slam all` cleanup.
cleanup_case() {
	local status=0
	if [[ -d ${MOUNTPOINT:-} ]] && mountpoint -q "$MOUNTPOINT"; then
		close_volume >>"$CASE_LOG" 2>&1 || status=$?
	fi
	if [[ -f ${VOLUME:-} ]] && [[ -n $(losetup -j "$VOLUME") ]]; then
		printf 'Leaked loop device for %s\n' "$VOLUME" >>"$CASE_LOG"
		losetup -j "$VOLUME" >>"$CASE_LOG"
		status=1
	fi
	if [[ -d ${GNUPGHOME:-} ]]; then
		gpgconf --kill gpg-agent >>"$CASE_LOG" 2>&1 || status=$?
	fi
	if ((status != 0)); then
		printf 'Cleanup failed; inspect %s\n' "$CASE_LOG" >&2
		return "$status"
	fi
}
