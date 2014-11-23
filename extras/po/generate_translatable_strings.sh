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

# This is how we get the strings to be translated:
#
# 1. sed filters the tomb file and only shows the lines containing a print
#    function, e.g. warning. It outputs two columns separated by a tab.
#    The first column contains the function that is called, and the second one
#    contains the message.
#
# 2. cat adds the line number as a new first column.
#
# 3. sort orders the lines using the third column and removes contiguous 
#    duplicate lines. The third column is the string to be translated, removing
#    duplicates even if they are printed by different functions.
#
# 4. sort reorders the lines numerically using the first column.
#
# 5. awk reads the column-formatted input and outputs valid pot lines.

PRINTFUNC="_\(success\|warning\|failure\|message\|print\)"

sed -n -e "s/^.*$PRINTFUNC \(\".*\"\).*$/\1\t\2/p" ../../tomb \
    | cat -n | sort -uk3 | sort -nk1 | cut -f2- | awk \
'BEGIN { FS = "\t" }
{ print "#:", $1;
  print "msgid", $2;
  print "msgstr \"\"\n"
}'
