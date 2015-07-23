        .....                                                ..
     .H8888888h.  ~-.                                  . uW8"
     888888888888x  `>        u.      ..    .     :    `t888
    X~     `?888888hx~  ...ue888b   .888: x888  x888.   8888   .
    '      x8.^"*88*"   888R Y888r ~`8888~'888X`?888f`  9888.z88N
     `-:- X8888x        888R I888>   X888  888X '888>   9888  888E
          488888>       888R I888>   X888  888X '888>   9888  888E
        .. `"88*        888R I888>   X888  888X '888>   9888  888E
      x88888nX"      . u8888cJ888    X888  888X '888>   9888  888E
     !"*8888888n..  :   "*888*P"    "*88%""*88" '888!` .8888  888"
    '    "*88888888*      'Y"         `~    "    `"`    `%888*%"
            ^"***"`                                        "`

*A minimalistic commandline tool to manage encrypted volumes* aka **The Crypto Undertaker**

![](https://github.com/dyne/Tomb/blob/master/extras/images/monmort.png)

Updates on website: https://www.dyne.org/software/tomb

Get the stable .tar.gz signed release for production use!

Download it from https://files.dyne.org/tomb

# What is Tomb, the crypto undertaker?

Tomb aims to be a free and open source system for easy encryption and
backup of personal files, written in code that is easy to review and
links shared GNU/Linux components.

At present, Tomb consists of a simple shell script (Zsh) using
standard filesystem tools (GNU) and the cryptographic API of the Linux
kernel (cryptsetup and LUKS). Tomb can also produce machine parsable
output to facilitate its use inside graphical applications.

# How does it work?

To create a Tomb, do:
```
 $ tomb dig -s 100 secret.tomb
 $ tomb forge secret.tomb.key
 $ tomb lock secret.tomb -k secret.tomb.key
```
To open it, do
```
 $ tomb open secret.tomb -k secret.tomb.key
```
and after you are done
```
 $ tomb close
```
or if you are in a hurry
```
 $ tomb slam all
```

For the instructions on how to get started using Tomb, see [INSTALL](INSTALL.md).

```
  Syntax: tomb [options] command [arguments]

  Commands:

   // Creation:
   dig     create a new empty TOMB file of size -s in MB
   forge   create a new KEY file and set its password
   lock    installs a lock on a TOMB to use it with KEY

   // Operations on tombs:
   open    open an existing TOMB
   index   update the search indexes of tombs
   search  looks for filenames matching text patterns
   list    list of open TOMBs and information on them
   close   close a specific TOMB (or 'all')
   slam    slam a TOMB killing all programs using it
   resize  resize a TOMB to a new size -s (can only grow)

   // Operations on keys:
   passwd  change the password of a KEY (needs old pass)
   setkey  change the KEY locking a TOMB (needs old key and pass)

   // Backup on paper:
   engrave makes a QR code of a KEY to be saved on paper

   // Steganography:
   bury    hide a KEY inside a JPEG image (for use with -k)
   exhume  extract a KEY from a JPEG image (prints to stout)

  Options:

   -s     size of the tomb file when creating/resizing one (in MB)
   -k     path to the key to be used ('-k -' to read from stdin)
   -n     don't process the hooks found in tomb
   -o     mount options used to open (default: rw,noatime,nodev)
   -f     force operation (i.e. even if swap is active)
   --kdf  generate passwords armored against dictionary attacks

   -h     print this help
   -v     print version, license and list of available ciphers
   -q     run quietly without printing informations
   -D     print debugging information at runtime
```

# What is this for, exactly?

This tool can be used to dig .tomb files (LUKS volumes), forge keys
protected by a password (GnuPG symmetric encryption) and use the keys
to lock the tombs. Tombs are like single files whose contents are
inaccessible in the absence of the key they were locked with and its
password.

Once open, the tombs are just like normal folders and can contain
different files, plus they offer advanced functionalities like bind
and execution hooks and fast search, or they can be slammed close even
if busy. Keys can be stored on separate media like USB sticks, NFC, or
bluetooth devices to make the transport of data safer: one always
needs both the tomb and the key, plus its password, to access it.

The tomb script takes care of several details to improve user's
behaviour and the security of tombs in everyday usage: secures the
typing of passwords from keyloggers, facilitates hiding keys inside
images, indexes and search a tomb's contents, lists open tombs and
selectively closes them, warns the user about free space and last time
usage, etc.

# How secure is this?

Death is the only sure thing in life. That said, Tomb is a pretty
secure tool especially because it is kept minimal, its source is
always open to review (even when installed) and its code is easy to
read with a bit of shell script knowledge.

All encryption tools being used in Tomb are included as default in
many GNU/Linux operating systems and therefore are regularly peer
reviewed: we don't add anything else to them really, just a layer of
usability.

The file [KNOWN_BUGS.md](KNOWN_BUGS.md) contains some notes on known
vulnerabilities and threat model analysis.

In absence or malfunction of the Tomb script it is always possible to
access the contents of a Tomb only using a dm-crypt enabled Linux
kernel, cryptsetup, GnuPG and any shell interpreter issuing the
following commands as root:
```
lo=$(losetup -f)
losetup -f secret.tomb
pass="$(gpg -d secret.key)"
echo -n -e "$pass" | cryptsetup --key-file - luksOpen $lo secret
mount /dev/mapper/secret /mnt
```
One can change the last argument `/mnt` to where the Tomb has to be
mounted and made accessible. To close the tomb then use:
```
umount /mnt
cryptsetup luksClose /dev/mapper/secret
```

# Stage of development

Tomb is an evolution of the 'mknest' tool developed for the
[dyne:bolic](http://www.dynebolic.org) 100% Free GNU/Linux
distribution in 2001: its 'nesting' mechanism allowed the liveCD users
to encrypt and make persistent home directories. Since then the same
shell routines kept being maintained and used for dyne:bolic until
2007, when they were ported to work on more GNU/Linux distributions.

As of today, Tomb is a very stable tool also used in mission critical
situations by a number of activists in dangerous zones. It has been
reviewed by forensics analysts and it can be considered to be safe for
military grade use where the integrity of information stored depends
on the user's behaviour and the strength of a standard AES-256 (XTS
plain) encryption algorithm.

# Use stable releases in production!

Anyone planning to use Tomb to store and access secrets should not use
the latest development version in Git, but use instead the .tar.gz
release on https://files.dyne.org/tomb . The stable version will
always ensure backward compatibility with older tombs: we make sure it
creates sane tombs and keys by running various tests before releasing
it. The development version in Git might introduce sudden bugs and is
not guaranteed to produce backward- or forward-compatible tombs and keys.
The development version in Git should be used to report bugs, test new
features and develop patches.

So be warned: do not use the latest Git version in production
environments, but use a stable release versioned and packed as
tarball on https://files.dyne.org/tomb

# How can you help

Donations are very welcome, please go to https://www.dyne.org/donate

Translations are also needed: they can be contributed via this website
https://poeditor.com/join/project?hash=33bdefea2e46b26f512a0caae55fbbb5
or simply sending the .po file. Start from `extras/po/tomb.pot`.

The code is pretty short and readable: start looking around and the
materials found in `doc/` which are good pointers at security measures
to be further implemented.

For the bleeding edge visit https://github.com/dyne/Tomb

If you plan to commit code into Tomb, please keep in mind this is a
minimalist tool and its code should be readable. Guidelines on the
coding style are illustrated in [doc/HACKING.txt](doc/HACKING.txt).

Tomb's developers can be contacted using the issues on GitHub or over
IRC on https://irc.dyne.org channel **#dyne** (or direct port 9999 SSL)

# Licensing

Tomb is Copyright (C) 2007-2015 by the Dyne.org Foundation

Tomb is designed, written and maintained by Denis Roio <jaromil@dyne.org>

More information on all the developers involved is found in the
[AUTHORS](AUTHORS.md) file.

This source code is free software; you can redistribute it and/or
modify it under the terms of the GNU Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This source code is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  Please refer
to the GNU Public License for more details.

You should have received a copy of the GNU Public License along with
this source code; if not, write to: Free Software Foundation, Inc.,
675 Mass Ave, Cambridge, MA 02139, USA.
