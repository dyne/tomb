#!/usr/bin/env bats
load helpers

setup_file() {
	require_integration
	local base_home="$BATS_FILE_TMPDIR/gnupg"
	mkdir -m 700 "$base_home"
	GNUPGHOME="$base_home" timeout --kill-after=10s "${TOMB_COMMAND_TIMEOUT:-180}s" zsh "$TOMB_TEST_BIN" forge \
		-k "$BATS_FILE_TMPDIR/baseline.key" --unsafe --tomb-pwd 'test password with spaces' \
		>"$TOMB_TEST_RESULTS/logs/baseline-forge.log" 2>&1 3>&-
}

teardown_file() {
	GNUPGHOME="$BATS_FILE_TMPDIR/gnupg" gpgconf --kill gpg-agent
}

setup() { setup_case; }
teardown() { cleanup_case; }

@test "dig forge lock creates a LUKS volume and private key" {
	create_volume
	run cryptsetup isLuks "$VOLUME"
	[ "$status" -eq 0 ]
	[ "$(stat -c %a "$KEY")" = 600 ]
}

@test "wrong password cannot mount a volume" {
	create_volume
	run tomb_command open "$VOLUME" "$MOUNTPOINT" -k "$KEY" --nohook --unsafe --tomb-pwd wrong
	[ "$status" -eq 1 ]
	! mountpoint -q "$MOUNTPOINT"
}

@test "contents survive close and reopen" {
	create_volume
	open_volume
	printf 'persistent contents\n' >"$MOUNTPOINT/contents.txt"
	close_volume
	open_volume
	[ "$(cat "$MOUNTPOINT/contents.txt")" = 'persistent contents' ]
	close_volume
}

@test "read-only mount rejects writes" {
	create_volume
	open_volume -o ro,noatime,nodev
	run bash -c 'printf forbidden >"$1/forbidden"' _ "$MOUNTPOINT"
	[ "$status" -ne 0 ]
	[ ! -e "$MOUNTPOINT/forbidden" ]
	close_volume
}

@test "locking an already locked volume preserves its header" {
	create_volume
	local before
	before=$(sha256sum "$VOLUME")
	run tomb_command lock "$VOLUME" -k "$KEY" --unsafe --tomb-pwd "$TEST_PASSWORD"
	[ "$status" -eq 1 ]
	[ "$(sha256sum "$VOLUME")" = "$before" ]
}

@test "password change rejects the old password and accepts the new one" {
	create_volume
	tomb_command passwd -k "$KEY" --unsafe --tomb-old-pwd "$TEST_PASSWORD" --tomb-pwd changed
	run open_volume
	[ "$status" -eq 1 ]
	TEST_PASSWORD=changed
	open_volume
	close_volume
}

@test "setkey accepts the replacement and rejects the original key" {
	create_volume
	tomb_command forge -k "$CASE_ROOT/new.key" --unsafe --tomb-pwd "$TEST_PASSWORD"
	tomb_command setkey "$KEY" "$VOLUME" -k "$CASE_ROOT/new.key" --unsafe \
		--tomb-pwd "$TEST_PASSWORD" --tomb-old-pwd "$TEST_PASSWORD"
	run open_volume
	[ "$status" -eq 1 ]
	KEY="$CASE_ROOT/new.key"
	open_volume
	close_volume
}

@test "resize grows the filesystem while preserving contents" {
	create_volume
	open_volume
	printf retained >"$MOUNTPOINT/retained"
	close_volume
	tomb_command resize "$VOLUME" -s 180 -k "$KEY" --unsafe --tomb-pwd "$TEST_PASSWORD"
	[ "$(stat -c %s "$VOLUME")" -eq $((180 * 1024 * 1024)) ]
	open_volume
	[ "$(cat "$MOUNTPOINT/retained")" = retained ]
	close_volume
}

@test "encrypted keys can be read from stdin" {
	create_volume
	tomb_command open "$VOLUME" "$MOUNTPOINT" -k - --nohook --unsafe --tomb-pwd "$TEST_PASSWORD" <"$KEY"
	mountpoint -q "$MOUNTPOINT"
	close_volume
}

@test "Argon2 key headers round trip through lock and open" {
	command -v argon2 >/dev/null || skip 'argon2 not installed'
	tomb_command forge -k "$KEY" --unsafe --tomb-pwd "$TEST_PASSWORD" \
		--kdf argon2 --kdfiter 1 --kdfmem 10 --kdfpar 1
	grep -q '^_KDF_argon2_' "$KEY"
	tomb_command dig -s 20 "$VOLUME"
	tomb_command lock "$VOLUME" -k "$KEY" --unsafe --tomb-pwd "$TEST_PASSWORD"
	open_volume
	close_volume
}

@test "steganographic keys can be recovered and used" {
	command -v steghide >/dev/null || skip 'steghide not installed'
	create_volume
	cp "$BATS_TEST_DIRNAME/../arditi.jpg" "$CASE_ROOT/carrier.jpg"
	tomb_command bury -k "$KEY" "$CASE_ROOT/carrier.jpg" --unsafe --tomb-pwd "$TEST_PASSWORD"
	tomb_command exhume -k "$CASE_ROOT/recovered.key" "$CASE_ROOT/carrier.jpg" --unsafe --tomb-pwd "$TEST_PASSWORD"
	KEY="$CASE_ROOT/recovered.key"
	open_volume
	close_volume
}

@test "PBKDF2 key headers round trip through lock and open" {
	command -v tomb-kdb-pbkdf2 >/dev/null || skip 'PBKDF2 helpers not installed'
	tomb_command forge -k "$KEY" --unsafe --tomb-pwd "$TEST_PASSWORD" --kdf pbkdf2 --kdfiter 1
	grep -q '^_KDF_pbkdf2sha1_' "$KEY"
	tomb_command dig -s 20 "$VOLUME"
	tomb_command lock "$VOLUME" -k "$KEY" --unsafe --tomb-pwd "$TEST_PASSWORD"
	open_volume
	close_volume
}
