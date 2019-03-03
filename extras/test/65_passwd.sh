#!/usr/bin/env zsh

export test_description="Testing changing tomb password"

source ./setup

test_export "test" # Using already generated tomb
test_expect_success 'Testing tomb with GnuPG keys: passwd' '
    tt passwd -k $tomb_key --unsafe \
        --tomb-old-pwd $DUMMYPASS --tomb-pwd $DUMMYPASSNEW  &&
    tt passwd -k $tomb_key --unsafe \
        --tomb-old-pwd $DUMMYPASSNEW --tomb-pwd $DUMMYPASS
    '

test_export "recipient" # Using already generated tomb
test_expect_success 'Testing tomb with GnuPG keys: passwd' '
    tt passwd -k $tomb_key -g -r $KEY2
    '

if test_have_prereq SPHINX ORACLE; then 
       test_export "sphinx_test" # Using already generated tomb
       test_expect_success 'Testing changing tomb password with sphinx' '
           tt passwd -k $tomb_key --unsafe \
               --tomb-old-pwd $DUMMYPASS --tomb-pwd $DUMMYPASSNEW \
               --sphx-user $DUMMYUSER --sphx-host $DUMMYHOST &&
           tt passwd -k $tomb_key --unsafe \
               --tomb-old-pwd $DUMMYPASSNEW --tomb-pwd $DUMMYPASS \
               --sphx-user $DUMMYUSER --sphx-host $DUMMYHOST
           '
fi

test_done
