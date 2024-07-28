#!/usr/bin/env zsh

export test_description="Testing tomb with pbkdf2 KDF key"

source ./setup

if test_have_prereq KDF; then
    test_export "kdf"
    test_expect_success 'Testing pbkdf2 KDF: tomb creation' '
        tt_dig -s 20 &&
        tt_forge --tomb-pwd $DUMMYPASS --kdf &&
        print $DUMMYPASS \
            | gpg --batch --passphrase-fd 0 --no-tty --no-options -d $tomb_key \
            | xxd &&
        tt_lock --tomb-pwd $DUMMYPASS
        '

    test_expect_success 'Testing pbkdf2 KDF: tomb passwd' '
        tt passwd -k $tomb_key \
            --unsafe --tomb-old-pwd $DUMMYPASS --tomb-pwd $DUMMYPASSNEW &&
        tt passwd -k $tomb_key \
            --unsafe --tomb-old-pwd $DUMMYPASSNEW --tomb-pwd $DUMMYPASS
        '

    test_expect_success 'Testing pbkdf2 KDF: tomb open & close' '
        tt_open --tomb-pwd $DUMMYPASS &&
        tt_close
        '
fi

test_done
