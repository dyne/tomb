# Tomb ChangeLog

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
