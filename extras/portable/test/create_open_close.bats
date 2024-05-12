load bats_setup

@test "Dig tomb" {
	rm -f "$TOMB"
	>&3 echo "$TOMB"
	./tomb dig -s 20 "$TOMB"
}

@test "Forge key" {
	rm -f "$TOMB".key
	./tomb forge "$TOMB".key
}

@test "Lock tomb with key" {
	./tomb lock -k "$TOMB".key "$TOMB"
}

@test "Open tomb with key" {
	mkdir -p "$TOMB".mnt
    ./tomb open -k "$TOMB".key "$TOMB" "$TOMB".mnt
}

@test "Create random.data inside the tomb" {
	dd if=/dev/urandom of="$TOMB".mnt/random.data bs=1024 count=10000
	>&3 ls -l "$TOMB".mnt/random.data
	sha512sum "$TOMB".mnt/random.data | awk '{print $1}' | >&3 tee "$TOMB".hash
	uname -a > "$TOMB".uname
}

@test "Close tomb" {
    ./tomb close "$TOMB"
}

@test "Re-open tomb with key" {
    ./tomb open -k "$TOMB".key "$TOMB" "$TOMB".mnt
}

@test "Check integrity of random data" {
	newhash=`sha512sum "$TOMB".mnt/random.data | awk '{print $1}'`
	oldhash=`cat "$TOMB".hash`
	>&2 echo $newhash
	>&2 echo $oldhash
	assert_equal "$newhash" "$oldhash"
	if [ -r "$TOMB".uname ]; then
		>&3 cat "$TOMB".uname
	fi
}

@test "Close the tomb again" {
    ./tomb close "$TOMB"
}
