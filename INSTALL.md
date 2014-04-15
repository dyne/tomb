
# TOMB INSTALLATION INSTRUCTIONS

## Install required tools

Tomb needs a few programs to be installed on a system in order to work:

 * zsh
 * gnupg
 * cryptsetup
 * pinentry-curses (or -gtk or -qt as you prefer)

Most systems provide these tools in their package collection,
for instance on Debian/Ubuntu one can use 'apt-get install'
on Fedora and CentOS one can use 'yum install'

## Install Tomb

To install Tomb simply download the source distribution (the tar.gz file)
and decompress it. From a terminal:

    cd Downloads
    tar xvfz Tomb-1.5.3.tar.gz (correct with actual file name)

Then enter its directory and run 'make install' as root, this will install
Tomb into /usr/local:

    cd Tomb-1.5.3 (correct with actual directory name)
    sudo make install

After installation one can read the commandline help or read the manual:

    tomb -h     (print a short help on the commandline)
    man tomb    (show the full usage manual)

At this point one can proceed creating a tomb, for instance:

    tomb dig -s 1000 secrets.tomb       (be patient and wait a bit)
    tomb forge -k secrets.tomb.key     (be patient and follow instructions)
    tomb lock  -k secrets.tomb.key secrets.tomb

## Install optional tools

Tomb can use some optional tools to extend its functionalities:

executable | function
---------- | ---------------------------------------------------
  dcfldd   | show progress while executing long operations
  steghide | bury and exhume keys inside images
  resizefs | extend the size of existing tomb volumes
  qrencode | engrave keys into printable qrcode tags
  mlocate  | have fast search of file names inside tombs
  swish++  | have fast search of file contents inside tombs
  unoconv  | have fast search of contents in PDF and DOC files

As for requirements, also optional tools may be easy to install using
the packages provided by each distribution.

Once any of the above is installed Tomb will find the tool automatically.

## Install Tomb extras

Tomb comes with a bunch of extra tools that contribute to enhance its
functionality or integrate it into particular system environments.

