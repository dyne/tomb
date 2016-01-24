This is an experimental port of Tomb to Android platform

REQUIRES ROOT - see on-line docs on how to root Android.

This includes a static binary of cryptsetup to interact with the
dm-crypt Linux API for filesystem cryptography (ELF for ARMv6)

Tombs can be created and opened correctly 

Only aes-cbc-essiv:sha254 crypto algo is supported.

At the moment tombs cannot be closed.
One has to reboot the device for that.

Other functions have not been tested.

More than ever, this is provided WITHOUT ANY WARRANTY

