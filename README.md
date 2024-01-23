# Tomb: The Linux Crypto Undertaker

[![Build Status](https://github.com/dyne/tomb/actions/workflows/linux.yml/badge.svg)](https://github.com/dyne/Tomb/actions)
<!-- [![Build Status](https://github.com/dyne/tomb/actions/workflows/portable.yml/badge.svg)](https://github.com/dyne/Tomb/actions) -->

Minimalistic command line tool based on Linux dm-crypt and LUKS, trusted by hackers since 2007.

You can keep your volumes secure and easily manageable with simple commands.

![tomb's logo](https://github.com/dyne/Tomb/blob/master/extras/images/monmort.png)

```
 $ tomb dig -s 100 secret.tomb
 $ tomb forge secret.tomb.key
 $ tomb lock secret.tomb -k secret.tomb.key
```
To open it, do
```
 $ tomb open secret.tomb -k secret.tomb.key
```
And after you are done
```
 $ tomb close
```
Or, if you are in a hurry, kill all processes with open files inside your tomb and close it.
```
 $ tomb slam
```
## [Get started on dyne.org/software/tomb](https://dyne.org/software/tomb)

<a href="https://dyne.org/software/tomb"><img src="https://files.dyne.org/software_by_dyne.png" width="30%"></a>

All information is found on our website.

Use only stable and signed releases in production!

### 💾 [Download from files.dyne.org/tomb](https://files.dyne.org/tomb/)

Tomb's development is community-based!

## How can you help

Donations are very welcome on [dyne.org/donate](https://www.dyne.org/donate)

Translations are also welcome: see our simple [translation guide](https://github.com/dyne/Tomb/blob/master/extras/translations/README.md)

Tomb's code is short and readable: don't be afraid to inspect it! If you plan to submit a PR, please remember that this is a minimalist tool, and the code should be short and readable. Also, first, read our small intro to [Tomb's coding style](doc/HACKING.txt).

We have a [space for issues](https://github.com/dyne/Tomb/issues) open for detailed bug reports. Always include the Tomb version being used when filing a case, please.

There is also a [space for discussion](https://github.com/dyne/Tomb/discussions) of new features, desiderata and whatnot on github.

# Licensing

Tomb is Copyright (C) 2007-2023 by the Dyne.org Foundation and maintained by [Jaromil](https://github.com/jaromil). The [AUTHORS](AUTHORS.md) file contains more information on all the developers involved. The license is GNU Public License v3.

## [More info on dyne.org/software/tomb](https://dyne.org/software/tomb)

