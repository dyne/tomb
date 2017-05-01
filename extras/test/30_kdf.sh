#!/usr/bin/env zsh

export test_description="Testing tomb with KDF key"

source ./setup

if test_have_prereq KDF; then
    test_export "kdf"
    test_expect_success 'Testing KDF: tomb creation' '
        tt_dig -s 20 &&
        tt_forge --tomb-pwd $DUMMYPASS --kdf 1 &&
        print $DUMMYPASS \
            | gpg --batch --passphrase-fd 0 --no-tty --no-options -d $tomb_key \
            | hexdump -C &&
        tt_lock --tomb-pwd $DUMMYPASS --kdf 1
        '

    test_expect_success 'Testing KDF: tomb passwd' '
        tt passwd -k $tomb_key --kdf 1 \
            --unsafe --tomb-old-pwd $DUMMYPASS --tomb-pwd $DUMMYPASSNEW &&
        tt passwd -k $tomb_key --kdf 1 \
            --unsafe --tomb-old-pwd $DUMMYPASSNEW --tomb-pwd $DUMMYPASS
        '

    test_expect_success 'Testing KDF: tomb open & close' '
        tt_open --tomb-pwd $DUMMYPASS --kdf 1 &&
        tt_close
        '
fi

test_done
