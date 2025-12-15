# Tomb: The Linux Crypto Undertaker

[![Build Status](https://github.com/dyne/tomb/actions/workflows/linux.yml/badge.svg)](https://github.com/dyne/Tomb/actions)
<!-- [![Build Status](https://github.com/dyne/tomb/actions/workflows/portable.yml/badge.svg)](https://github.com/dyne/Tomb/actions) -->

Minimalistic command line tool based on Linux dm-crypt and LUKS, trusted by hackers since 2007.

You can keep your volumes secure and easily manageable with simple commands.

![tomb's logo](https://github.com/dyne/Tomb/blob/master/extras/images/monmort.png)

Create a new 120MiB `secret.tomb` folder and lock it with a new `secret.tomb.key` file.
```
 $ tomb dig   -s 120 secret.tomb
 $ tomb forge -k secret.tomb.key
 $ tomb lock  -k secret.tomb.key secret.tomb
```
To open it, do
```
 $ tomb open  -k secret.tomb.key secret.tomb
```
And after you are done
```
 $ tomb close
```
Or, if you are in a hurry, kill all processes with open files inside your tomb and close it.
```
 $ tomb slam
```

Tomb also supports two-factor unlocking with a FIDO2 passkey; see `doc/FIDO2.md` for setup details.
## 📖 [Get started on dyne.org/tomb](https://dyne.org/tomb)

<a href="https://dyne.org/tomb"><img src="https://files.dyne.org/software_by_dyne.png" width="30%"></a>

More information in `man tomb` and on [dyne.org/docs/tomb](https://dyne.org/docs/tomb).

### 💾 [Download from files.dyne.org](https://files.dyne.org/?dir=tomb)

Use only stable and signed releases in production!

Tomb's development is community-based!

## 🤏🏽 How can you help

Donations are very welcome on [dyne.org/donate](https://www.dyne.org/donate)

Translations are also welcome: see our simple [translation guide](https://github.com/dyne/Tomb/blob/master/extras/translations/README.md)

Tomb's code is short and readable: don't be afraid to inspect it! If you plan to submit a PR, please remember that this is a minimalist tool, and the code should be short and readable. Also, first, read our small intro to [Tomb's coding style](doc/HACKING.txt).

We have a [space for issues](https://github.com/dyne/Tomb/issues) open for detailed bug reports. Always include the Tomb version being used when filing a case, please.

There is also a [space for discussion](https://github.com/dyne/Tomb/discussions) of new features, desiderata and whatnot on github.

# Licensing

Tomb is Copyright (C) 2007-2025 by the Dyne.org Foundation and maintained by [Jaromil](https://github.com/jaromil). The [AUTHORS](AUTHORS.md) file contains more information on all the developers involved. The license is GNU Public License v3.

## [More info on dyne.org/tomb](https://dyne.org/tomb)
