#!/usr/bin/env bats
load helpers

setup() { setup_case; }

@test "main executable parses as Zsh" {
	run zsh -n "$TOMB_TEST_BIN"
	[ "$status" -eq 0 ]
}

@test "missing dependencies produce an actionable error" {
	mkdir "$CASE_ROOT/bin"
	run env PATH="$CASE_ROOT/bin" /usr/bin/zsh "$TOMB_TEST_BIN" help
	[ "$status" -ne 0 ]
	[[ $output == *'Missing required dependency'* ]]
}

@test "help lists the volume lifecycle" {
	require_core_tools
	run tomb_command help
	[ "$status" -eq 0 ]
	[[ $output == *dig* && $output == *forge* && $output == *lock* && $output == *open* ]]
}

@test "unknown commands fail" {
	require_core_tools
	run tomb_command definitely-not-a-command
	[ "$status" -ne 0 ]
	[[ $output == *'no such command'* ]]
}

@test "inline passwords require the unsafe testing flag" {
	require_core_tools
	run tomb_command open "$VOLUME" -k "$KEY" --tomb-pwd dummy
	[ "$status" -ne 0 ]
	[[ $output == *'add --unsafe'* ]]
}

@test "dig rejects undersized volumes without creating a file" {
	require_core_tools
	run tomb_command dig -s 1 "$VOLUME"
	[ "$status" -ne 0 ]
	[ ! -e "$VOLUME" ]
}

@test "dig preserves an existing file" {
	require_core_tools
	printf 'preserve me\n' >"$VOLUME"
	run tomb_command dig -s 20 "$VOLUME"
	[ "$status" -ne 0 ]
	[ "$(cat "$VOLUME")" = 'preserve me' ]
}
