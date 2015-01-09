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

open my $handle, $FILE or die "Failed to open $FILE";
my @lines = <$handle>;
close $handle;

my %seen;
my @ignored;
my $index = 0;
my $fold;
my $func;

foreach (@lines) {
    $index++;

    # It's a fold title
    if (m/^# +{{{ +(.*)$/) {
        $fold = $1;
        next;
    }

    # It's a function name
    if (m/^(.*)\(\) *{$/) {
        $func = $1;
        next;
    }

    # Next if there is no print function
    next unless m/$FUNCPATTERN +$STRINGPATTERN/;

    # Next if it was seen before
    $seen{$2}++;
    next if $seen{$2} > 1;

    # Next if it's blacklisted
    if (grep {$2 =~ m/$_/} @blacklist) {
	push @ignored, $2;
	next;
    }

    print "#. Fold: $fold\n";
    print "#. Function: $func\n";
    print "#.\n";
    print "#. Code sample:\n";

    my $sign = ' ';
    for (-7..3) {
        if($_ == -1) {
            $sign = '>';
        }
        else {
            $sign = ' ';
        }

        my $n = $index + $_;
        print "#. $sign $lines[$n]";
    }

    print "#: tomb:$index\n";
    print "msgid $2\n";
    print "msgstr \"\"\n\n";
}

print STDERR "-- IGNORED\n";
foreach (@ignored) {
    print STDERR "$_\n";
}

