# Tomb ChangeLog

## 2.8.1
### Nov 2020

This is a minor bugfix release. It fixes two bugs introduced by the
previous release: the release of loopback devices and a typo affecting
password insertion in text-only mode. It also provides a cosmetic fix
for the output of 'tomb list' that now displays correct sizes. At
last, the docker wrapper has been included in extras/ to be shipped in
Tomb. The span of CVE-2020-28638 has been assessed with more precision
and KNOWN_BUGS updated accordingly.

## 2.8
### Nov 2020

This new release updates the documentation, improves usability and
fixes two bugs. A bug has been found (CVE-2020-28638) to corrupt
passwords entered using pinentry-curses on desktops using a X11
DISPLAY, the documentation in KNOWN_BUGS outlines how to fix
regressions. Another bug has been fixed to prevent mounting tombs that
are already opened, a situation leading to potential data loss.
Changes mentioned lead to a small internal refactoring and cleanup,
leading to a change in the way volumes appear in /dev/mapper. Along
the usability improvements are the support of GNUPGHOME environment
variable to support non-standard GnuPG home locations as well updated
translations and the fact that debug messages are now written to
stderr, making it easier to parse stdout.

## 2.7
### Oct 2019

Fixed getent parsing of passwd and notation of conditionals
normalised.  A few other minor fixes and documentation improvements.


## 2.6
### May 2019

This release adds new features and provides an important fix for usage
of Tomb with cryptsetup 2.1 and future versions; it also fixes a
whitespace bug in KDF passwords, all fixes are documented in
KNOWN_BUGS. A notable new feature is the libsphinx integration for
password-authenticated key agreement (PAKE). Another feature is the
integration of cloakify to support new cloak/uncloak commands that
hide keys inside long text files. Also support for gpg sub-keys has
been added and overall gpg asymmetric key protection is improved.



## 2.5
### January 2018

This is mostly a bugfix release, including two internal
refactorings. An important change is the re-introduction (since v2.3)
of ownership change of all files inside tombs, to facilitate single
user usage, which is now default and can be prevented using the '-p'
flag on 'open' commands. The first refactoring concerns the test
units, now using the 'sharness' framework. The other refactoring
concerns 'post-hooks' now renamed to 'exec-hooks' and launched on
'open' and 'close' commands with a defined set of arguments. Another
internal change concerns the use of 'findmnt' instead of parsing the
output of 'mount -l', which grants compatibility with more recent
versions of util-linux. A fix was made to the 'slam' command for a
better process detection and the introduction of a new 'ps' command to
just list processes using tombs. Another fix was made to support tomb
hidden filenames (starting with a dot) without any extension. Some
more minor fixes were made to messaging and translations, plus all the
documentation is updated.


## 2.4
### April 2017

This release introduces a major new feature with support for
asymmetric encryption of Tomb keys using public/private GPG key
pairs. It is now possible to protect a Tomb key using a GPG key (which
can also be password-less for automations) as well encrypt a Tomb key
for multiple recipients (list of GPG ids). Other improvements include:
a fix to the 'slam' command with better detection of running programs
using 'lsof' (new optional dependency); a fix to 'forge' key creation
to really use 512 bits long keys to really trigger usage of AES256;
correct support for opening tombs in read-only mode; update of the
Tomber python wrapper in extras. Documentation has been updated.

## 2.3
### January 2017

Fix to bug occurring when using ZSh version 5.3 or higher. Fix to
inclusion of final newline in keys generated with 2.2, only affecting
third-party software. Removed chmod/chown of tombs when open. Enhanced
continuous integration script with regression tests with usage of old
stable versions of Tomb and shellcheck linting.  Improved parser and
post-hooks to avoid usage of external binaries (grep and cat) also
improving security when decrypting keys. Fix for clean execution via
sudo nopasswd. Updated extras/gtomb to latest stable version.  Various
documentation updates about kdf, using images as keys, deniability and
gpg-agent usage. New experimental port to Android platforms in extras.

## 2.2
### December 2015

New Qt5 desktop tray in extras/qt-tray.
New Zenity based Gtk interface in extras/gtomb (experimental).
Better resizing procedure recovers from failure without starting over
with a new dig.  Fixes for correct handling of bind-hooks mountpoints
containing whitespaces, implying a refactoring of how the mtab is
parsed, along with workaround for Debian bugs. Updated all strings to
report MiB sizes. Fix to correctly show last time opened. Fix to EUID
detection and to installed manpage permissions.

## 2.1.1
### August 2015

Added translations to Italian and Swedish.
Minor documentation updates.


## 2.1
### July 2015

All users updating should close their tombs first, then update and
reopen them with this new version. However, lacking to do so will not
cause any data loss, just an unclean umount of tombs.

This new stable release including several bugfixes to smooth the user
experience in various situations. Documentation is reviewed and
extended and translations are updated.

More in detail, fixes to: mountpoint removal, language localization,
gtk-2 pinentry themeing, udisk2 compatibility (/run/media/$USER
mountpoint support), handling of key failures, kdf documentation,
swish-e file contents search and encrypted swap detection.

Deniability is improved by allowing any filename to be used for tombs
(also without .tomb extension). Code has been overall cleaned up.


## 2.0.1
### December 2014

Fix for usage with GnuPG 1.4.11, a problem affecting long term
GNU/Linux distribution releases like Ubuntu 12.04 and Mint 13.
Minor messaging fixes.

## 2.0
### November 2014

Tomb goes international: now translated to Russian, French, Spanish
and German.

The usability has improved: steganographed images can now be used
directly as keys using `-k`. Tomb now works also across ssh
connections: it is possible to pipe cleartext secrets from stdin using
`-k cleartext` but that requires the --unsafe flag.

The security is also improved by avoiding most uses of temporary
files. The privilege escalation model has been simplified and sudo is
called only when needed. All code has been refactored for readability
and integration with zsh features. Signal handlers are now in place,
global arrays are used to keep track of temp files. Namespace has been
revisioned and corrected, described in [HACKING](docs/HACKING.txt).

## 1.5.3
### June 2014

Various usability fixes and documentation updates. Password changing
and key changing procedures have been refactored and dev-mode
operation from scripts has been tested against a few new wrappers
being developed. A strings file is made available for translators.

## 1.5.2
### February 2014

Removed automatic guessing of key file besides tomb to encourage
users to keep tomb and key separated, but also to simplify the
code in key retrieval and avoid a bug occurring in the previous
version.

## 1.5.1
### February 2014

Fix to stdin piping of keys, which were not correctly processed
nor were deleted from volatile memory (tmpfs).

Version is now updated accordingly.

## 1.5
### January 2014

Minor bugfixes to documentation, error handling, support for
multiple and encrypted swap partitions and qr code engraving.

This release also includes some minor code refactoring of
load_key() and loop mount checks. Also the tray app is updated
to gtk-3 and works simply with a tomb name as argument.

Documentation was updated accordingly.

## 1.4
### June 2013

This release fixes an important bug affecting Tomb 1.3.* which
breaks backward compatibility with older tombs and invalidates
keys created using 1.3 or 1.3.1. For more information about it
read the file KNOWN_BUGS.

New features are also included:
indexing and search of file contents, engraving of keys into paper
printable QRCodes for backup purposes and improvements in key
encryption. A setkey command is added to change the key file that
is locking a Tomb.

This release restores backward compatibility
with tombs created before the 1.3 release series.

## 1.3.1 (DEPRECATED, see [KNOWN_BUGS](KNOWN_BUGS.md))
### June 2013

Major bugfixes following the recent refactoring.

This release fixes various advanced commands as search/index, KDF key
protection against dictionary attacks and steganographic hiding of
keys. It provides compatibility across GnuPG 1.4.11 and .12 which
broke the decoding of keys. Usage of commandline option is made
consistent and full paths are honored.

A new test suite is included and documentation is updated accordingly.

## 1.3 (DEPRECATED, see [KNOWN_BUGS](KNOWN_BUGS.md))
### May 2013

A refactoring of Tomb's main script internals was made, including
a new messaging system, machine parsable output, cleaner code and
updated compatibility to Debian 7. A new search feature lets users
index and run fast filename searches in their open tombs. Creation
of tombs is broken out in three steps (dig, forge and lock).

Source distribution includes experimental add-ons for a python
GUI, KDF key encryption and a key "undertaker". Documentation was
updated.


## 1.2
### Nov 2011

Includes an Important fix to password parsing for spaces and
extended chars, plus a new 'passwd' command to change a key's
password. Tomb now checks for swap to avoid its usage (see SWAP
section in manpage) and warns the user when the tomb is almost
full.

## 1.1
### May 2011

Fixes to mime types, icons and desktop integration.

A new 'list' command provides an overview on all tombs currently open.

Now a tomb cannot be mounted multiple times, the message console has
colors and better messages.

Different mount options (like read-only) can also be specified by hand on the commandline.

## 1.0
### March 2011

Clean and stable. Now passwords are handled exclusively using
pinentry. Also support for steganography of keys (bury and exhume)
was added to the commandline.

Commandline and desktop operations are well separated so that tomb can be used via remote terminal.

A new command 'slam' immediately closes a tomb killing all processes that keep it busy.

## 0.9.2
### February 2011

The tomb-open wizard now correctly guides you through the creation
of new tombs and helps when saving the keys on external USB
storage devices. The status tray now reliably closes its tomb.

## 0.9.1
### February 2011

Sourcecode cleanup, debugging and testing.

Integrated some feedback after filing Debian's ITP and RFS.

## 0.9
### January 2011

Tomb is now a desktop application following freedesktop standards:
it provides a status tray and integrates with file managers.

The main program has been thoroughly tested and many bugs were fixed.

## August 2010

The first usable version of Tomb goes public among hacker friends

## During the year 2009

Tomb has been extensively tested, perfectioned and documented
after being used by its author.

## Sometime in 2007

[MKNest](http://code.dyne.org/dynebolic/tree/dyneII/startup/bin/mknest)
was refactored to work on the Debian distribution and since
then renamed to Tomb. [dyne:bolic](http://www.dynebolic.org) specific dependencies where
removed, keeping Zsh as the shell script it is written with.

## Back in 2005

The "nesting" feature of [dyne:bolic](http://www.dynebolic.org)
GNU/Linux lets users encrypt their home in a file, using a shell script and a graphical
interface called Taschino.

Taschino included a shell script wrapping cryptsetup to encrypt
loopback mounted partitions with the algo AES-256 (cbc-essiv
mode): this script was called 'mkNest' and its the ancestor of
Tomb.
