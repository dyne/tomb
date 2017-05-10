#!/usr/bin/env zsh

export test_description="Testing tomb creation"

source ./setup
test_cleanup

test_export "test"
test_expect_success 'Testing tomb creation: dig, forge and lock' '
    tt_dig -s 20 &&
    tt_forge --tomb-pwd $DUMMYPASS &&
    print $DUMMYPASS \
        | gpg --batch --passphrase-fd 0 --no-tty --no-options -d $tomb_key \
        | hexdump -C &&
    tt_lock --tomb-pwd $DUMMYPASS
    '

test_done
