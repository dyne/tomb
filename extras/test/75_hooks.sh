#!/usr/bin/env zsh

export test_description="Testing tomb bind hooks"

source ./setup

test_export "test" # Using already generated tomb
test_expect_success 'Testing bind hooks' '
    tt_open --tomb-pwd $DUMMYPASS &&
    tt_set_ownership "$MEDIA/$testname" &&
    RND="$RANDOM" &&
    bindtest="dyne-tomb-bind-test-$RND" &&
    echo "$RND" > "$MEDIA/$testname/$bindtest" &&
    rm -f "$MEDIA/$testname/bind-hooks" &&
    echo "$bindtest $bindtest" > "$MEDIA/$testname/bind-hooks" &&
    tt_close &&
    touch "/home/$USER/$bindtest" &&
    tt_open --tomb-pwd $DUMMYPASS &&
    RND2=$(cat "/home/$USER/$bindtest") &&
    [[ "$RND" = "$RND2" ]] &&
    tt list $testname &&
    tt_close
    '

test_done
