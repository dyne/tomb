load bats_setup

@test "Find the tomb" {
	assert_file_exists "$TOMB"
	>&3 echo "Found: $TOMB"
}

@test "Open tomb with key" {
	mkdir -p "$TOMB".mnt
    ./tomb open -k "$TOMB".key "$TOMB" "$TOMB".mnt
}

@test "Check integrity of random data" {
	sha512sum "$TOMB".mnt/random.data | awk '{print $1}'
	cat "$TOMB".hash
	>&2 echo $newhash
	>&2 echo $oldhash
	assert_equal "$newhash" "$oldhash"
	if [ -r "$TOMB".uname ]; then
		>&3 cat "$TOMB".uname
	fi
}

@test "Close tomb" {
    ./tomb close "$TOMB"
}
