#!/usr/bin/env zsh

export test_description="Testing rendering QR Code key"

source ./setup

if test_have_prereq QRENCODE; then
    test_export "test"
    test_expect_success 'Testing rendering a QR printable key backup' '
        tt engrave -k $tomb_key
        '
fi

test_done
