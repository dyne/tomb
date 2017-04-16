# Usage of AES128 due to shorter keysize
## 2.4

All tomb keys forged using Tomb version 2.3 or preceeding are 256 bits
large, which is insufficient to trigger usage of AES-256 encryption in
XTS mode, which is the default. Therefore all tombs locked using
smaller keys are silently encrypted using AES-128, according to the
cryptsetup manual:
> "By default a 256 bit key-size is used. Note however that XTS splits the supplied key in half, so to use AES-256 instead of AES-128 you have to set the XTS key-size to 512."

This problem has been noticed and corrected in Tomb version 2.4 where
now the 'forge' command will automatically generate 512 bits keys. To
switch to AES-256 encrypted tombs the only possibility is to create
new keys, new tombs and copy the contents across, since the LUKS
formatting occurs when the 'lock' command is issued using a new
key. Using 'setkey' to switch key does not suffice to switch to
AES-256.

This problem is minor and doesn't seem to heavily affect the security
of Tombs created before 2.4 as the cryptographic strenght of AES-128
and AES-256 is comparable; yet it is reasonable to think that larger
key sizes resist better to Quantum computing attacks.


# Vulnerability to password bruteforcing
## Issue affecting keys used in steganography

 An important part of Tomb's security model is to *make it hard for
 attackers to enter in possession of both key and data storage*: once
 that happens, bruteforcing the password can be relatively easy.

 Protection from bruteforcing is provided by the KDF module that can
 be optionally compiled in `extras/kdf-keys` and installed.

 If a key is buried in an image and then the image is stolen, the KDF
 protection does not works because *attackers can bruteforce easily
 using steghide dictionary attacks*: once found the password is the
 same for the steg crypto and the key crypto.

 Users should keep in mind these issues when planning their encryption
 scheme and, when relying on steganography, keep the image always
 mixed in the same folder with many more images since that will be the
 multiplier making it slightly harder to bruteforce their password.

 In most cases consider that *password bruteforce is a feasible attack
 vector on keys*. If there are doubts about a key being compromised is
 a good practice to change it using the `setkey` command on a secure
 machine, possibly while off-line or in single user mode.

# Ending newline in tomb keys
## 2.2

 When used to forge new keys, Tomb version 2.2 incorrectly added a new
 line ('\n', 0x0A) character at the end of each key's secret sequence
 before encoding it with GnuPG. This does not affect Tomb regression
 and compatibility with other Tomb versions as this final newline is
 ignored in any case, but third party software may have
 problems. Those writing a software that supports opening Tomb files
 should always ignore the final newline when present in the secret
 material obtained after decoding the key with the password.
 
# Versioning and stdin key
## 1.5

 Due to distraction tomb version 1.5 displays its version as 1.4.
 Also version 1.5 did not work when using -k - to pipe keys from
 stdin, plus left the encrypted keys laying around in RAM (tmpfs).
 This was a minor vulnerability fixed in 1.5.1.


# Key compatibility broken
## 1.3 and 1.3.1

 Due to an error in the creation and decoding of key files, release
 versions 1.3 and 1.3.1 cannot open older tombs, plus the tombs created
 with them will not be opened with older and newer versions of Tomb.

 This bug was fixed in commit 551a7839f500a9ba4b26cd63774019d91615cb16

 Those who have created tombs with older versions can simply upgrade
 to release 1.4 (and any other following release) to fix this issue
 and be able to operate their tombs normally.

 Those who have used Tomb 1.3 or 1.3.1 to create new tombs should use
 Tomb version 1.3.1 (available from https://files.dyne.org/tomb) to
 open them and then migrate the contents into a new tomb created using
 the latest stable Tomb version.

 This bug was due to a typo in the code which appended a GnuPG status
 string to the content of keys.  All users of Tomb 1.3.* should pay
 particular attention to this issue, however that release series was
 out as latest for less than a month.
