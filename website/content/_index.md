---
title: Dowse
description: 'Tomb is a system to make strong encryption easy for everyday use. A tomb is like a locked folder that can be safely transported and hidden in a filesystem.'
image: "images/tomb-horizontal.webp"
sections:
- title: "Get Started"
  description_markdown: "Tombs are operated from a terminal command line and require root access to the machine (or just sudo access to the script)."
  image: "images/tombanim.webp"
  button:
    label: "Entomb your secrets"
    URL: "https://dyne.org/docs/tomb/get-started"
- title: "Advanced usage"
  description_markdown: "The tomb script takes care of several details to improve a user’s behaviour and the security of tombs in everyday usage"
  image: "images/tomb_songs.webp"
  button:
    label: "protect your data"
    URL: "https://dyne.org/docs/tomb/advanced"
- title: "External applications"
  description_markdown: "pass-tomb, Secrets, Mausoleum, zuluCrypt... Tomb has an ecosystem of third party apps ready to help you secure your digital life"
  image: "images/foster_privacy.webp"
  button:
    label: Enhance your privacy
    URL: "https://dyne.org/docs/tomb/3rd-party-apps"
---

Tomb is a 100% free and open source tool that facilitates managing secret files in volumes protected by strong encryption.

Tomb’s ambition is to improve safety by way of:

- a minimalist design consisting of small and readable code
- the facilitation of good practices, i.e.: key/storage physical separation
- the adoption of a few standards and battle-tested components

### How it works

We design Tomb’s hidden file encryption to generate encrypted storage folders to be opened and closed using associated key files, which are also protected with a password chosen by the user.

A tomb is a file whose contents are kept secret and indistinguishable; it can be safely renamed, transported and hidden in filesystems; its keys should be kept separate, for instance, keeping the tomb file on your computer’s hard disk and the key files on a USB stick. Once open, the tomb looks like a folder.

Tomb derives from scripts used in the dyne:bolic 100% Free GNU/Linux distribution and a shell script (Zsh) using standard filesystem tools (GNU) and the cryptographic API of the Linux kernel (dm-crypt and LUKS via cryptsetup). Tomb’s status and error messages are translated into many human languages and have multiple graphical applications to operate.
