#!/usr/bin/env zsh

export test_description="Testing common operations on tomb"

source ./setup

_getaccess() { stat --format=%X "$1"; }
_getmodif() { stat --format=%Y "$1"; }

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

test_expect_success 'Testing tomb files stat restoration' '
    access=$(_getaccess $tomb_key) &&
    modif=$(_getmodif $tomb_key) &&
    tt_open --tomb-pwd $DUMMYPASS &&
    tt_close &&
    [[ "$access" == "$(_getaccess $tomb_key)" ]] &&
    [[ "$modif" == "$(_getmodif $tomb_key)" ]]
    '

if test_have_prereq LSOF; then
    gcc -Wall -o $TMP/close_block $TEST_HOME/close_block.c
    test_expect_success 'Testing functionality of the slam operation (use of lsof)' '
        mkdir $TMP/testmount &&
        tt_open $TMP/testmount --tomb-pwd $DUMMYPASS &&
        tt_set_ownership $TMP/testmount &&
        $TMP/close_block $TMP/testmount/occupied 20 &
        tt slam
        '
fi

if test_have_prereq DOAS; then
    test_export "doas_test" # Using already generated tomb
    test_expect_success 'Testing open with good password (using doas instead of sudo)' '
        tt_open --sudo doas --tomb-pwd $DUMMYPASS &&
        tt_close --sudo doas
        '
fi

test_done
