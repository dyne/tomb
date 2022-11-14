
# Portable Tomb :: the crypto undertaker runs everywhere

 [![continuous integration tests badge](https://github.com/dyne/tomb/actions/workflows/portable.yml/badge.svg)](https://github.com/dyne/Tomb/actions) test coverage status for portability between Ubuntu-20 and FreeBSD-13.
 
## ⚠️ WORK IN PROGRESS 🛠️

This is the portable version of [Tomb](https://github.com/dyne/tomb) using [Veracrypt](https://www.veracrypt.fr) in place of cryptsetup.

[![software by Dyne.org](https://files.dyne.org/software_by_dyne.png)](http://www.dyne.org)

# Purpose

Portable tomb achieves direct **interoperable access to tomb volumes** between:

- GNU and Busybox Linux
- MS/Windows using WSL2
- Apple/OSX using [MacFUSE](https://osxfuse.github.io/)
- FreeBSD

Portable tomb reduces dependencies and in particular uses only the **POSIX sh interpreter**.

# Status

Portable tomb development is in progress and tracked via issues and the [portable milestone](https://github.com/dyne/Tomb/milestone/9).

## Features

The following features will be implemented where possible:

- mount bind (Linux only)
- ps / slam
- resize (pending investigation)
- index & search ([recoll based](https://github.com/dyne/Tomb/issues/211))
- bury / exhume

## Dependencies

- FreeBSD: `fusefs-libs3 fusefs-lkl e2fsprogs util-linux`
- Linux: `fuse3 util-linux`
- crossplatform [Veracrypt binaries](https://files.dyne.org/tomb3/third-party) console-only

## Note on Veracrypt

The way upstream developers distribute Veracrypt is far from meeting our minimalist needs, but the console-only binary once installed has a few library dependencies and is all what we need.

I setup [my own build](https://github.com/jaromil/veracrypt) and provide binary builds of Veracrypt v1.25.9 for download on Tomb's file repository for testing purposes.

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
