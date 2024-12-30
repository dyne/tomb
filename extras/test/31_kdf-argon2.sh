#!/usr/bin/env zsh

export test_description="Testing tomb with argon2 KDF key"

source ./setup

if test_have_prereq ARGON; then
    test_export "argon"
    test_expect_success 'Testing argon2 KDF: tomb creation' '
        tt_dig -s 20 &&
        tt_forge --tomb-pwd $DUMMYPASS --kdf argon2 &&
        print $DUMMYPASS \
            | gpg --batch --passphrase-fd 0 --no-tty --no-options -d $tomb_key \
            | xxd &&
        tt_lock --tomb-pwd $DUMMYPASS
        '

    test_expect_success 'Testing argon2 KDF: tomb passwd' '
        tt passwd -k $tomb_key --kdf argon2 \
            --unsafe --tomb-old-pwd $DUMMYPASS --tomb-pwd $DUMMYPASSNEW &&
        tt passwd -k $tomb_key --kdf argon2 \
            --unsafe --tomb-old-pwd $DUMMYPASSNEW --tomb-pwd $DUMMYPASS
        '

    test_expect_success 'Testing argon2 KDF: tomb open & close' '
        tt_open --tomb-pwd $DUMMYPASS &&
        tt_close
        '
fi

test_done
