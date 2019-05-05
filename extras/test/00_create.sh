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

if test_have_prereq SPHINX ORACLE; then
	test_export "sphinx_test"
	test_expect_success 'Testing tomb creation: dig, forge and lock (sphinx password handling)' '
    tt_dig -s 20 &&
    tt_forge --tomb-pwd $DUMMYPASS --sphx-user $DUMMYUSER --sphx-host $DUMMYHOST &&
    print $(echo $DUMMYPASS | sphinx get $DUMMYUSER $DUMMYHOST) \
        | gpg --batch --passphrase-fd 0 --no-tty --no-options -d $tomb_key \
        | hexdump -C &&
    tt_lock --tomb-pwd $DUMMYPASS --sphx-user $DUMMYUSER --sphx-host $DUMMYHOST
    '
fi

test_done
