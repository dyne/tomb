#!/usr/bin/env zsh

export test_description="Tomb regression tests"

source ./setup
autoload -U is-at-least

TOMB_VERSION=("2.4" "2.3" "2.2" "2.0.1" "2.1")
zshversion=$(zsh --version | awk 'NR==1 {print $2}')
{ is-at-least "5.3" $zshversion } && TOMB_VERSION=("2.3")

for version in "${TOMB_VERSION[@]}"; do
    URL="https://files.dyne.org/tomb/old-releases/Tomb-$version.tar.gz"

    curl "$URL" > "$TMP/tomb-regression.tar.gz"
    mkdir -p "$TMP/tomb-regression"
    tar xfz "$TMP/tomb-regression.tar.gz" \
        --strip-components 1 -C "$TMP/tomb-regression"
    T="$TMP/tomb-regression/tomb"
    [[ "$version" == "$(${T} -v |& awk 'NR==1 {print $3}')" ]] || continue

    test_export "regression_$version"
    test_expect_success "Regression tests: opening old tomb ($version) with Tomb" "
        tt_dig -s 20 &&
        tt_forge --tomb-pwd $DUMMYPASS &&
        tt_lock --tomb-pwd $DUMMYPASS &&
        T='$TOMB_BIN' &&
        tt_open --tomb-pwd $DUMMYPASS &&
        tt_close
        "

    test_export "test" # Using already generated tomb
    test_expect_success "Regression tests: opening new tomb with Tomb $version" "
        export T='$TMP/tomb-regression/tomb' &&
        tt_open --tomb-pwd $DUMMYPASS &&
        tt_close
        "
done

test_done
