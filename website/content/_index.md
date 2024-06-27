---
title: Dowse
description: 'Tomb is a system to make strong encryption easy for everyday use. A tomb is like a locked folder that can be safely transported and hidden in a filesystem.'
image: "images/tombanim.webp"
sections:
- title: The missing On-OFF button in IOT
  description_markdown: "Connected things like home appliances should have a clear behaviour humans
    can understand and react upon. This includes a simple switch to turn them off. Dowse gives an ON/OFF
    switch back to any device in your LAN."
  image: "images/20160705_082209.jpg"
  button:
    label: "Read more"
    URL: "about/"
- title: "Dowse is fun"
  description_markdown: "Dowse talks back to your devices. In open standards: MQTT, Websockets,
    Open Sound Control. Many types of Internet connected things can treasure the messages that
    Dowse publishes, to turn them into action. Is a good start for artists, hobbyists and
    makers to create amazing network-aware effects, visualisations and interfaces. We try to
    help a community of dowsers to explore this possibility. Share your dowse projects with us."
  image: "images/h10-1024x683.jpg"
  button:
    label: "Community"
    URL: "community/"
- title: "...and More"
  description_markdown: "Dowse keeps your private network private and lets you understand what
    is trying to talk about what and be aware of misbehaviours. If necessary Dowse can mute
    things as well: it switches their access to internet off. \n\nDowse is a open source project.
    Experts can look at is code. It is built to last and to be used by anyone because is a
    community project. **If you are interested in us giving workshops...**"
  image: "images/hd6.jpg"
  button:
    label: Get in touch
    URL: "mailto:info+dowse@dyne.org"
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
