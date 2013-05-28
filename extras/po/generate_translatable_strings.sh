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
"PO-Revision-Date: `date`\n"
"Last-Translator: Denis Roio <jaromil@dyne.org>\n"
"Language-Team: Tomb developers <crypto@lists.dyne.org>\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=CHARSET\n"
"Content-Transfer-Encoding: 8bit\n"

#
#: commandline help
#

msgid ""
EOF

    ../../tomb help | awk '
{ print "\"" $0 "\"" }'
    cat <<EOF
msgstr ""

#
# tomb internal messages
#

EOF

    cat ../../tomb | awk '
/(_verbose|xxx) ".*"$/ { sub( /^(_verbose|xxx)/ , "");
		 print "#: _verbose"; shift; print "msgid " substr($0, index($0,$2)); print "msgstr \"\"\n" }

/(_success|yes) ".*"$/ { sub( /^(_success|yes)/ , "");
		 print "#: _success"; print "msgid " substr($0, index($0,$2)); print "msgstr \"\"\n" }

/(_warning|no) ".*"$/ { sub( /^(_warning|no)/ , "");
		 print "#: _warning"; print "msgid " substr($0, index($0,$2)); print "msgstr \"\"\n" }

/(_failure|die) ".*"$/ { sub( /^(_failure|die)/ , "");
		 print "#: _failure"; print "msgid " substr($0, index($0,$2)); print "msgstr \"\"\n" }

/(_message|say) ".*"$/ { sub( /^(_message|say)/ , "");
	      print "#: _message"; print "msgid " substr($0, index($0,$2)); print "msgstr \"\"\n" }

/(_message -n|act) ".*"$/ { sub( /^(_message -n|act)/ , "");
	      print "#: _message -n"; print "msgid " substr($0, index($0,$2)); print "msgstr \"\"\n" }
'

