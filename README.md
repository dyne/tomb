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

# What is it for, exactly?

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

# Can Tomb be used inside other applications?

Sure as Hell it can! Licensing issues aside ([GNU GPLv3+](COPYING)
terms) Tomb provides machine-readable output and interaction via some flags:

              flag   | function
-------------------- | ------------------------------------------------
 --no-color          | avoids coloring output to allow parsing
 --unsecure-dev-mode | allows giving passwords as argument
 --tomb-pwd          | specify the key password as argument
 --tomb-old-pwd      | specify the old key password as argument
 --sudo-pwd          | specify the sudo password as argument

Yet please consider that these flags may introduce vulnerabilities as
process table scanning can reveal passwords while such commands are
executing. For passwords in particular the best is always let Tomb
gather them via pinentry.

## Python

![](extras/images/python_for_tomb.png)

A Python wrapper is under developed and already usable, but it
introduces the vulnerabilities mentioned above. Find it in
`extras/tomber`. For more information see [PYTHON](extras/PYTHON.md).

## Graphical applications

So far the only graphical application supporting Tomb volumes is
[ZuluCrypt](https://github.com/mhogomchungu/zuluCrypt). One needs to
activate the Tomb plugin included in its source and will be able to
create, open and close tombs. It might still miss advanced Tomb
functionalities that are only available from the command-line.

## Let us know!

If you plan to develop any kind of wrapper for Tomb you are welcome to
let us know. Tomb is really meant to be maintained as a minimal tool
for long-term compatibility when handling something so delicate as our
secrets. For anything else we rely on your own initiative.

Happy hacking! :&^)
