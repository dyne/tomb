![Tomb's skull icon](docs/monmort.jpg)

# Portable Tomb :: the crypto undertaker runs everywhere

 <!-- [![continuous integration tests badge](https://github.com/dyne/tomb3/actions/workflows/ci.yml/badge.svg)](https://github.com/dyne/Tomb3/actions) test coverage status for Ubuntu-20, FreeBSD-13 and Mac/OSX. -->
## ⚠️ WORK IN PROGRESS 🛠️

This is the portable version of [Tomb](https://github.com/dyne/tomb) using [Veracrypt](https://www.veracrypt.fr) in place of cryptsetup.

[![software by Dyne.org](https://files.dyne.org/software_by_dyne.png)](http://www.dyne.org)

# Purpose

Portable tomb achieves direct **interoperable access to tomb volumes** between:

- GNU/Linux
- MS/Windows using WSL2
- Apple/OSX using [MacFUSE](https://osxfuse.github.io/)
- FreeBSD

as well reduce dependencies and in particular use only the **POSIX sh interpreter**.

## References:
- [Milestone on v2 repo](https://github.com/dyne/Tomb/milestone/8)
- [Feature poll](https://github.com/dyne/Tomb/issues/409)

## Features

The following v2 features will be ported:

[ ] mount bind
[ ] ps / slam
[ ] resize
[ ] index & search
[ ] bury / exhume

## Dependencies

- FreeBSD: `fusefs-libs3 fusefs-lkl e2fsprogs util-linux`
- Linux: `fuse3 util-linux`
- crossplatform [Veracrypt binaries](https://files.dyne.org/tomb3/third-party) console-only

### Note on Veracrypt

The way upstream developers distribute Veracrypt is far from meeting our minimalist needs, but the console-only binary once installed has a few library dependencies and is all what we need. We will likely setup our own build (and eventually need to [fork veracrypt's commandline-client interface](https://github.com/dyne/Tomb3/issues/2)) meanwhile binary builds of Veracrypt v1.25.9 are provided for download on our own file repository for testing purposes: **use at your own risk**.

# Disclaimer

Tomb is Copyright (C) 2007-2022 by the Dyne.org Foundation and
developed by [Jaromil](https://github.com/jaromil).

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
