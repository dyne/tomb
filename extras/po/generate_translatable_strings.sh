#!/bin/zsh

cat <<EOF
# Tomb - The Crypto Undertaker.
# Copyright (C) 2007-2013 Dyne.org Foundation
# Denis Roio <jaromil@dyne.org>, 2013.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: Tomb $VERSION\n"
"PO-Revision-Date: `LANG=en date`\n"
"Last-Translator: Denis Roio <jaromil@dyne.org>\n"
"Language: English\n"
"Language-Team: Tomb developers <crypto@lists.dyne.org>\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"

EOF

    cat ../../tomb | awk '
/_verbose ".*"/ {
    split($0, arr, "\"");
    print "#: _verbose";
    print "msgid \"" arr[2] "\"";
    print "msgstr \"\"\n" }

/_success ".*"/ {
    split($0, arr, "\"");
    print "#: _success";
    print "msgid \"" arr[2] "\"";
    print "msgstr \"\"\n" }

/_warning ".*"/ {
    split($0, arr, "\"");
    print "#: _warning";
    print "msgid \"" arr[2] "\"";
    print "msgstr \"\"\n" }

/_failure ".*"/ {
    split($0, arr, "\"");
    print "#: _failure";
    print "msgid \"" arr[2] "\"";
    print "msgstr \"\"\n" }

/_message ".*"/ {
    split($0, arr, "\"");
    print "#: _message";
    print "msgid \"" arr[2] "\"";
    print "msgstr \"\"\n" }

/_message -n ".*"/ {
    split($0, arr, "\"");
    print "#: _message -n";
    print "msgid \"" arr[2] "\"";
    print "msgstr \"\"\n" }

/_print ".*"/ {
    split($0, arr, "\"");
    print "#: _print";
    print "msgid \"" arr[2] "\"";
    print "msgstr \"\"\n" }
'
