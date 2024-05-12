load bats_setup

# f_create=""
# f_format=""
# f_map=""
# f_mount=""
# f_close=""

@test "Create a new tomb" {
	# >&3 echo $PW
	>&3 echo $TOMB
	echo -n "$PW" | $f_create "$TOMB" 20M ${PIM}
}

@test "Map the tomb" {
	echo -n "$PW" | $f_map "$TOMB" ${PIM}
}

@test "Format the tomb" {
    $f_format "/tmp/.veracrypt_aux_mnt1" || {
		$f_close "$TOMB"
		return false
	}
}

@test "Mount the tomb" {
	mkdir -p "$MNT"
	$f_mount "$TOMB" "$MNT" || {
		$f_close "$TOMB"
		return false
	}
}

@test "Create random.data inside the tomb" {
	dd if=/dev/urandom of="$MNT"/random.data bs=1024 count=10000 || {
		# sudo umount testmnt
		$f_close "$TOMB"
		return false
	}
	>&3 ls -l "$MNT"/random.data
	sha512sum "$MNT"/random.data | awk '{print $1}' | >&3 tee "$TOMB".hash
	uname -a > "$TOMB".uname
}

@test "Close the test.tomb" {
	>&3 veracrypt -l
	# sudo umount "$TMP"/testmnt
	$f_close "$TOMB"
}


@test "Re-Map the test.tomb" {
	echo -n "$PW" | $f_map "$TOMB" ${PIM}
}

@test "Re-Mount the test.tomb" {
	mkdir -p "$MNT"
	$f_mount "$TOMB" "$MNT" || {
		$f_close "$TOMB"
		return false
	}
}

@test "Re-Check integrity of random data" {
	newhash=`sha512sum "$MNT"/random.data | awk '{print $1}'`
	oldhash=`cat "$TOMB".hash`
	>&2 echo $newhash
	>&2 echo $oldhash
	assert_equal "$newhash" "$oldhash"
	if [ -r "$TOMB".uname ]; then
		>&3 cat "$TOMB".uname
	fi
}


@test "Re-Close the test.tomb" {
	>&3 veracrypt -l
	$f_close "$TOMB"
}
