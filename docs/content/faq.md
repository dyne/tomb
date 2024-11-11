---
title: Frequently Asked Questions
description_markdown: "Everything you need to know about Tomb, but were too afraid to ask"
image: 'images/dowse-dataprevention-campaign-1024x576.jpg'
sections:
- title: "Development?"
  content_markdown: "Tomb is on GitHub, where most of the community activity goes.\n\n

Developers can interact with us via a discussion area, issues, or pull requests. The README is also a brief introduction for developers willing to engage.\n\n

The [short tomb tester howto](https://github.com/dyne/Tomb/wiki/TesterHowTo) provides a guide to troubleshooting problems. Anyone planning to write code in Tomb should first look at the [short tomb developer howto](https://github.com/dyne/Tomb/wiki/DeveloperHowto). \n\n

To get in touch with us in person please plan to participate in one of the yearly [italian hackmeeting](http://hackmeeting.org), usually held during summer on the peninsula."
  image: "images/tomb_crew_hkm11.webp"
  button:
    URL: "https://github.com/dyne/Tomb/discussions"
    label: Get in touch
layout: about
---

## How secure is Tomb?

**Death is the only sure thing in life**. That said, Tomb is a pretty secure tool mainly because it is kept minimal, its source is always open to review (even when installed), and its code is easy to read with some shell script knowledge. Plus, **no cloud or network connection is needed: Tomb works offline**.

GNU/Linux distributions include all encryption tools we use in Tomb and therefore, they are regularly peer-reviewed: we don't add anything else to them, just a layer of usability.

If needed, **it is always possible to access the contents of a tomb without the tomb script**, only using a few commands typed into any shell interpreter:

```
lo=$(losetup -f)
losetup -f secret.tomb
gpg -d secret.key | head -c -1 | cryptsetup --key-file - luksOpen $lo secret
mount /dev/mapper/secret /mnt
```

One can change the last argument `/mnt` to where the Tomb has to be mounted and made accessible. To close the tomb, use:

```
umount /mnt
cryptsetup luksClose /dev/mapper/secret
```


## Who needs Tomb?

> Democracy requires privacy as much as Freedom of Expression. — Anonymous

The world is full of prevarication and political imprisonments, war rages in several places, and media is mainly used for propaganda by the powers in charge. Some of us face the dangers of being tracked by oppressors opposing our self-definition, independent thinking and resistance to homologation.

Our target community are GNU/Linux users with no time to click around, sometimes using old or borrowed computers, operating in places endangered by conflict where **a leak of personal data can be a threat**.

Even if one can't own a laptop, Tomb makes it possible to go around with a USB stick and borrow computers, leaving no trace and keeping data safe during transport.


> The distinction between public and private is becoming increasingly blurred with the increasing intrusiveness of the media and advances in electronic technology. While this distinction is always the outcome of continuous cultural negotiation, it continues to be critical, for where nothing is private, democracy becomes impossible.

The Internet offers plenty of free services; in most cases, **corporate or state monopolies host all private information**. Server-hosted services and web-integrated technologies gather all data into huge information pools made available to established economic and cultural regimes.

**Tomb is ethical software that empowers everyone to protect their privacy**.

## Aren't there enough encryption tools?

The current situation in personal desktop encryption is far from optimal.

The encrypted home mechanism of most operating systems doesn’t make it easy to transport around, and they do not separate the keys from the storage: only the password is needed to open them, which is prone to brute-forcing attacks.

[TrueCrypt](http://en.wikipedia.org/wiki/TrueCrypt) makes use of statically linked libraries with code is hard to audit. Furthermore, it is [not considered free](http://lists.freedesktop.org/archives/distributions/2008-October/000276.html) by operating system distributors because of its liability reasons. (see [Debian](http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=364034), [Ubuntu](https://bugs.edge.launchpad.net/ubuntu/+bug/109701), [Suse](http://lists.opensuse.org/opensuse-buildservice/2008-10/msg00055.html), [Gentoo](http://bugs.gentoo.org/show_bug.cgi?id=241650) and [Fedora](https://fedoraproject.org/wiki/ForbiddenItems#TrueCrypt)).

[Veracrypt](https://veracrypt.org) is a very portable rewrite of TrueCrypt (works also on Mac OSX) but it is very slow and has some interaction patterns that are not secure. Its way of encrypting is comparable to Tomb.

[EncFS](http://www.arg0.net/encfs) doesn’t need root access. But it has drawbacks: it implements weaker encryption, doesn't promote the separated storage of keys and exposes the size of each single file rather than hiding the structure of a folder.


Watch Tomb's development history in this infographic based on git commits.
<iframe title="dyne/Tomb - Gource visualisation" width="100%" height="315" src="https://tv.dyne.org/videos/embed/54255dae-4bc5-4538-9c61-c5d2d69779da" frameborder="0" allowfullscreen="" sandbox="allow-same-origin allow-scripts allow-popups allow-forms"></iframe>

## Compliancy

Tomb qualifies as sound for use with information rated as "top secret" when used on an underlying stack of carefully reviewed hardware (random number generator and other components) and software (Linux kernel build, crypto modules, device manager, compiler used to built, shell interpreter and packaged dependencies).

Tomb volumes are fully compliant with the FIPS 197 advanced encryption standard published by NIST and with the following industry standards:

- Information technology -- Security techniques -- Encryption algorithms
	- [ISO/IEC 18033-1:2015](http://www.iso.org/iso/home/store/catalogue_tc/catalogue_detail.htm?csnumber=54530)  -- Part 1: General
	- [ISO/IEC 18033-3:2010](http://www.iso.org/iso/home/store/catalogue_ics/catalogue_detail_ics.htm?csnumber=54531) -- Part 3: Block ciphers

Tomb implementation is known to at least partially address issues raised in:

- Information technology -- Security techniques -- Key management
	- [ISO/IEC 11770-1:2010](http://www.iso.org/iso/home/store/catalogue_tc/catalogue_detail.htm?csnumber=53456)  -- Part 1: Framework
	- [ISO/IEC 11770-2:2008](http://www.iso.org/iso/home/store/catalogue_tc/catalogue_detail.htm?csnumber=46370)  -- Part 2: Mechanisms using symmetric techniques
- [ISO/IEC 27005:2011](http://www.iso.org/iso/home/store/catalogue_tc/catalogue_detail.htm?csnumber=56742) Information technology -- Security techniques -- Information security risk management
- [ISO/IEC 24759:2014](http://www.iso.org/iso/home/store/catalogue_tc/catalogue_detail.htm?csnumber=59142) Information technology -- Security techniques -- Test requirements for cryptographic modules

Any help on further verification of compliance is very welcome, as our access to ISO/IEC documents is limited.


> All I know is what the words know, and dead things, and that makes a handsome little sum, with a beginning and a middle and an end, as in the well-built phrase and the long sonata of the dead. — Samuel Beckett
