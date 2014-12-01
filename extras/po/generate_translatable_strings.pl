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

foreach (@lines) {
    $index++;
    # Ignore if there is no print function on this line
    next unless m/$FUNCPATTERN +$STRINGPATTERN/;

    # Ignore if the string was seen before
    $seen{$2}++;
    next if $seen{$2} > 1;

    # Ignore if this string is blacklisted
    if (grep {$2 =~ m/$_/} @blacklist) {
	push @ignored, $2;
	next;
    }

    for (-7..3) {
        my $n = $index + $_;
        print "#. $lines[$n]";
    }
    print "#: tomb:$index\n";
    print "msgid $2\n";
    print "msgstr \"\"\n\n";
}

print STDERR "-- IGNORED\n";
foreach (@ignored) {
    print STDERR "$_\n";
}

