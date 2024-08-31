#!/usr/bin/env zsh

export test_description="Testing changing tomb password"

source ./setup

test_export "test" # Using already generated tomb
test_expect_success 'Testing tomb with GnuPG keys: passwd' '
    tt passwd -f -k $tomb_key --unsafe \
        --tomb-old-pwd $DUMMYPASS --tomb-pwd $DUMMYPASSNEW  &&
    tt passwd -f -k $tomb_key --unsafe \
        --tomb-old-pwd $DUMMYPASSNEW --tomb-pwd $DUMMYPASS
    '

if test_have_prereq GPGRCPT; then

test_export "recipient" # Using already generated tomb
test_expect_success 'Testing tomb with GnuPG keys: passwd' '
    tt passwd -f -k $tomb_key -g -r $KEY2
    '

fi

test_done
