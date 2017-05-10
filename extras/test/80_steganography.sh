#!/usr/bin/env zsh

export test_description="Testing steganography features"

source ./setup

if test_have_prereq STEGHIDE; then
    test_export "test" # Using already generated tomb
    cp -f "$TEST_HOME/arditi.jpg" "$tomb_img"
    test_expect_success 'Testing tomb and steganographic: bury' '
        tt bury -k $tomb_key $tomb_img \
            --unsafe --tomb-pwd $DUMMYPASS
        '

    test_expect_success 'Testing tomb and steganographic: exhume' '
        tt exhume -k $tomb_key_steg $tomb_img \
            --unsafe --tomb-pwd $DUMMYPASS
        '

    test_expect_success 'Testing tomb and steganographic: open' '
        tt open -k $tomb_key_steg $tomb --unsafe --tomb-pwd $DUMMYPASS &&
        tt_close
        '

    test_expect_success 'Testing tomb and steganographic: piping keys using -k -' '
        tkey=`tt exhume $tomb_img --unsafe --tomb-pwd $DUMMYPASS` &&
        print "$tkey" | tt open -k - $tomb --unsafe --tomb-pwd $DUMMYPASS &&
        tt_close
        '

    test_expect_success 'Testing tomb and steganographic: open image.jpeg' '
        tt open -k $tomb_img $tomb --unsafe --tomb-pwd $DUMMYPASS &&
        tt_close
        '

    test_export "recipient" # Using already generated tomb
    cp -f "$TEST_HOME/arditi.jpg" "$tomb_img"
    test_expect_success 'Testing tomb with GnuPG keys and steganographic: bury' '
        tt bury -k $tomb_key $tomb_img -g -r $KEY1 \
            --unsafe --tomb-pwd $DUMMYPASS
        '

    test_expect_success 'Testing tomb with GnuPG keys and steganographic: exhume' '
        tt exhume -k $tomb_key_steg $tomb_img \
            --unsafe --tomb-pwd $DUMMYPASS
        '

    test_expect_success 'Testing tomb with GnuPG keys and steganographic: open' '
        tt open -k $tomb_key_steg $tomb -g &&
        tt_close
        '

    test_expect_success 'Testing tomb with GnuPG keys and steganographic: piping keys using -k -' '
        tkey=`tt exhume $tomb_img --unsafe --tomb-pwd $DUMMYPASS` &&
        print "$tkey" | tt open -k - $tomb -g &&
        tt_close
        '

    test_expect_success 'Testing tomb with GnuPG keys and steganographic: open image.jpeg' '
        tt open -k $tomb_img $tomb -g --unsafe --tomb-pwd $DUMMYPASS &&
        tt_close
        '
fi

test_done
