use strict;
use warnings;

my $FILE = '../../tomb';
my $FUNCPATTERN = '_(success|warning|failure|message|print)';
my $STRINGPATTERN = '(".*?[^\\\]")';

my $date = localtime;
print '
# Tomb - The Crypto Undertaker.
# Copyright (C) 2007-2014 Dyne.org Foundation
# Denis Roio <jaromil@dyne.org>, 2013.
#
#, fuzzy
msgid ""
msgstr ""
"PO-Revision-Date: ', $date, '\n"
"Last-Translator: Denis Roio <jaromil@dyne.org>\n"
"Language: English\n"
"Language-Team: Tomb developers <crypto@lists.dyne.org>\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"

';

my @blacklist = ('"--"', '"\\\\000"', '`.*`', '$\(.*\)');

# Translatable strings that can't be automatically detected yet
my %undetectable = (
    124 => '[sudo] Enter password for user ::1 user:: to gain superuser privileges'
);

open my $handle, $FILE or die "Failed to open $FILE";
my @lines = <$handle>;
close $handle;

my %seen;
my $index = 0;
my $fold;
my $func;
my $force;
my $str;

foreach (@lines) {
    $index++;
    $force = 0;

    # It's a fold title
    if (m/^# +\{\{\{ +(.*)$/) {
        $fold = $1;
        next;
    }

    # It's a function name
    if (m/^(.*)\(\) *{$/) {
        $func = $1;
        next;
    }

    # Force if it's undetectable
    $force = 1 if exists($undetectable{$index});

    # Next if there is no print function
    next unless $force or m/$FUNCPATTERN +$STRINGPATTERN/;

    # Get string from the $undetectable hash or via regex
    if ($force) {
        $str = "\"$undetectable{$index}\"";
    }
    else {
        $str = $2;
    }

    # Next if it was seen before
    $seen{$str}++;
    next if $seen{$str} > 1;

    # Next if it's blacklisted
    next if grep {$str =~ m/$_/} @blacklist;

    print "#: tomb:$fold:$func:$index\n";
    print "msgid $str\n";
    print "msgstr \"\"\n\n";
}
