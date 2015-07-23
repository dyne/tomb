# TOMB INSTALLATION INSTRUCTIONS

## Install required tools

Tomb needs a few programs to be installed on a system in order to work:

 * zsh
 * sudo
 * gnupg
 * cryptsetup
 * pinentry-curses (and/or -gtk-2, -x11, -qt)

Most systems provide these tools in their package collection, for
instance on Debian/Ubuntu one can use `apt-get install` on Fedora and
CentOS one can use `yum install` and `pacman` on Arch.

## Install Tomb

To install Tomb simply download the source distribution (the tar.gz file)
from https://files.dyne.org/tomb and decompress it. From a terminal:

    cd Downloads
    tar xvfz Tomb-2.0.1.tar.gz (correct with actual file name)

Then enter its directory and run 'make install' as root, this will install
Tomb into /usr/local:

    cd Tomb-2.0.1 (correct with actual directory name)
    sudo make install

After installation one can read the commandline help or read the manual:

    tomb -h     (print a short help on the commandline)
    man tomb    (show the full usage manual)

# Basic usage

Once installed one can proceed creating a tomb, for instance:

    tomb dig -s 10 secrets.tomb       (dig a 10MB Tomb)
    tomb forge -k secrets.tomb.key    (create a new key and set its password)
    tomb lock  -k secrets.tomb.key secrets.tomb (format the tomb, lock it with key)

When this is done, the tomb can be opened with:

    tomb open -k secrets.tomb.key secrets.tomb (will ask for password)

The key can also be hidden in an image, to be used as key later

    tomb bury -k secrets.tomb.key nosferatu.jpg (hide the key in a jpeg image)
    tomb open -k nosferatu.jpg secrets.tomb (use the jpeg image to open the tomb)

Or backupped to a QRCode that can be printed on paper and hidden in
books. QRCodes can be scanned with any mobile application, resulting
into a block of text that can be used with `-k` just as a normal key.

    tomb engrave -k secrets.tomb.key  (also an image will work)

There are some more things that tomb can do for you, make sure you
have a look at the manpage and at the commandline help to find out
more.

## Basic usage notes

Here we collect notes on common issues users may or may not experience
and the commonly working solutions found.

### Pinentry issues

If pinentry has problems dealing with the password because of language
or tty settings on your system, try running `gpg-agent` by launching it
from the session initialization (~/.xsession or ~/.xinitrc) with this
command:
```
eval $(gpg-agent --daemon --write-env-file "${HOME}/.gpg-agent-info")
```


# Advanced usage

## Install optional tools

Tomb can use some optional tools to extend its functionalities:

executable | function
---------- | ---------------------------------------------------
  dcfldd   | show progress while digging tombs and keys
  steghide | bury and exhume keys inside images
  resizefs | extend the size of existing tomb volumes
  qrencode | engrave keys into printable qrcode sheets
  mlocate  | fast search of file names inside tombs
  swish++  | fast search of file contents inside tombs
  unoconv  | fast search of contents in PDF and DOC files
  lesspipe | fast search of contents in compressed archives
  haveged  | fast entropy generation for key forging

As for requirements, also optional tools may be easy to install using
the packages provided by each distribution.

Once any of the above is installed Tomb will find the tool automatically.

## Install Tomb Extras

Tomb comes with a bunch of extra tools that contribute to enhance its
functionality or integrate it into particular system environments.

### extras/gtk-tray

The Gtk tray adds a nifty tomb skull into the desktop toolbar: one can
use it to close, slam and explore the open tomb represented by it.

When using pinentry-gtk-2 it also adds a little skull on the password
input, useful to not confuse it with other password inputs.

To have it change directory `extras/gtk-tray` then

 1. make sure libnotify and gtk+-3.0 dev packages are available
 2. run `make` inside the directory to build `tomb-gtk-tray`
 3. run `sudo make install` (default PREFIX is `/usr/local`)
 4. start `tomb-gtk-tray tombname` after the tomb is open

Of cource one can include the launch of tomb-gtk-tray scripts.

### extras/kdf-keys

The KDF wrapper programs allows one to use KDF rounds on passwords in
order to obstruct dictionary based and similar brute-forcing attacks.

In case an attacker comes in possession of both a tomb and its key,
the easy to memorize password can be guessed by rapidly trying
different combinations. With KDF every try will require a significant
amount of computation that will slow down the process avoiding tight
loops and in fact making such attacks very onerous and almost
impossible.

To have it enter `extras/kdf-keys` then

 1. make sure libgcrypt dev packages are available
 2. run `make` inside the directory to build tomb-kdb-* executables
 3. run `sudo make install` (default PREFIX is `/usr/local`)
 4. use `--kdf 100` when forging a key (tune the number to your cpu)

KDF keys are recognized automatically by Tomb, which will always need
the `extras/kdf-keys` program to be installed on a machine in order to
open the Tomb.

Please note that it doesn't makes much sense to use KDF keys and
steganography, since the latter will invalidate the brute-forcing
protection. For details on the issue see [KNOWN_BUGS.md](KNOWN_BUGS).

### extras/po (translations)

There are translations available for Tomb and they are installed by
default. If you wish to update them manually navigate to extras/po
and run 'make install' as root:

    cd extras/po
    sudo make install

# Tomb support in other applications

Can Tomb be used by other applications?

Sure as Hell it can! Licensing issues aside ([GNU GPLv3+](COPYING)
terms) Tomb provides machine-readable output and interaction via some
flags:

         flag   | function
--------------- | ------------------------------------------------
 --no-color     | avoids coloring output to allow parsing
 --unsafe       | allows passwords options and cleartext key from stdin
 --tomb-pwd     | specify the key password as argument
 --tomb-old-pwd | specify the old key password as argument
 -k cleartext   | reads the unencrypted key from stdin

Yet please consider that these flags may introduce vulnerabilities and
other people logged on the same system can easily log your passwords
while such commands are executing.
We only recommend using the pinentry to input your passwords.

## Python

![](extras/images/python_for_tomb.png)

A Python wrapper is under development and already usable, but it
introduces some vulnerabilities mentioned above. Find it in
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

Happy hacking! ;^)
