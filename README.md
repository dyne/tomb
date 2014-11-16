
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

Latest stable version: **2.0**

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

For the instructions on how to get started using Tomb, see [INSTALL](INSTALL.md).

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

The tomb script takes care of several details to improve the security
of tombs in everyday usage: adopting PIN entry for passwords,
facilitating the storage of backup keys using image steganography,
listing open tombs and selectively closing them, warning the user
about their size and last time they were used, etc.

# How secure is this?

Death is the only sure thing in life. That said, Tomb is a pretty
secure tool especially because it is kept minimal, its source is always
open, and its code is easy to review with a bit of shell script
knowledge.

All encryption tools being used in Tomb are included as default in
many GNU/Linux operating systems and therefore are regularly peer
reviewed: we don't add anything else to them really, just a layer of
usability.

The code of Tomb can be read in a literate programming style on
http://tomb.dyne.org/literate

# Stage of development

Tomb is an evolution of the 'mknest' tool developed for the dyne:bolic
GNU/Linux distribution, which is used by its 'nesting' mechanism to
encrypt the Home directory of users, a system implemented already in
2001. Since then, the same shell routines kept being maintained and in
2007, they were adapted to work on various other GNU/Linux distributions.

As of today, Tomb is a very stable tool also used in mission critical
situations by a number of activists in dangerous zones. It has been
reviewed by forensics analysts and it can be considered to be safe for
military grade use where the integrity of information stored depends on 
the user's behaviour and the strength of a standard AES-256
(XTS plain) encryption algorithm.

# Use stable releases in production

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

Donations are always welcome, see https://www.dyne.org/donate

Translations are also needed: they can be contributed via this website
https://poeditor.com/join/project?hash=33bdefea2e46b26f512a0caae55fbbb5
or simply sending the .po file. Start from `extras/po/tomb.pot`.

The code is pretty short and readable: start looking around and the
materials found in `doc/` which are good pointers at security measures
to be further implemented.

For the bleeding edge visit https://github.com/dyne/Tomb

Tomb's developers can be contacted using the issues on GitHub or over
IRC on https://irc.dyne.org channel **#dyne**

Some enthusiastic ideas are in the [TODO](doc/TODO.org) file.

Information on developers involved is found in the [AUTHORS](AUTHORS.md) file.
