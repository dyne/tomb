#!/usr/bin/env zsh

export test_description="Testing common operations on tomb"

source ./setup

test_export "test" # Using already generated tomb
test_expect_success 'Testing open with wrong password ' '
    test_must_fail tt_open --tomb-pwd wrongpassword
    '

test_expect_success 'Testing open with good password ' '
    tt_open --tomb-pwd $DUMMYPASS &&
    tt_close
    '

test_expect_success 'Testing open in read only mode' '
    chmod -w $tomb &&
    tt_open --tomb-pwd $DUMMYPASS -o ro,noatime,nodev &&
    tt_close &&
    chmod +w $tomb
    '

test_done
