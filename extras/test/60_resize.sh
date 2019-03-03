#!/usr/bin/env zsh

export test_description="Testing tomb resize feature"

source ./setup

if test_have_prereq RESIZER; then
    test_export "test" # Using already generated tomb
    test_expect_success 'Testing resize to 30 MB tomb' '
        tt resize -s 30 $tomb -k $tomb_key --unsafe --tomb-pwd $DUMMYPASS
        '

    test_export "recipient" # Using already generated tomb
    test_expect_success 'Testing resize to 30 MB tomb with GnuPG keys' '
        tt resize -s 30 $tomb -k $tomb_key -g -r $KEY2
        '
fi

if test_have_prereq RESIZER SPHINX ORACLE; then 
       test_export "sphinx_test" # Using already generated tomb
       test_expect_success 'Testing resize to 30 MB tomb (sphinx)' '
        tt resize -s 30 $tomb -k $tomb_key --unsafe --tomb-pwd $DUMMYPASS --sphx-user $DUMMYUSER --sphx-host $DUMMYHOST
        '
fi

test_done
