#!/usr/bin/env zsh

export test_description="Testing tomb resize feature"

source ./setup

if test_have_prereq RESIZER; then
  test_export "test" # Using already generated tomb
  test_expect_success 'Testing resize to 30 MB tomb' '
        tt resize -s 30 $tomb -k $tomb_key --unsafe --tomb-pwd $DUMMYPASS
        '
  if test_have_prereq GPGRCPT; then
    test_export "recipient" # Using already generated tomb
    test_expect_success 'Testing resize to 30 MB tomb with GnuPG keys' '
        tt resize -s 30 $tomb -k $tomb_key -g -r $KEY2
        '
  fi

fi # RESIZER

if test_have_prereq BTRFS; then
    test_export "btrfs"
    test_expect_success 'Testing resize using BTRFS filesystem' '
        tt resize -s 150 $tomb -k $tomb_key --unsafe --tomb-pwd $DUMMYPASS
        '

    test_export "btrfsmixed"
    test_expect_success 'Testing resize using BTRFS filesystem' '
        tt resize -s 30 $tomb -k $tomb_key --unsafe --tomb-pwd $DUMMYPASS
        '
fi

test_done
