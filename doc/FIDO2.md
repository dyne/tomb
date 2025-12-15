# FIDO2 / Passkey Support in Tomb

Tomb can protect a tomb key with a FIDO2/WebAuthn passkey instead of a traditional passphrase. The secret material that unlocks the key is derived from the authenticator, so opening the tomb requires:

- Physical presence on the passkey (touch/UV).
- The authenticator PIN (if configured).

This effectively replaces the passphrase with two‑factor authentication: you need both the hardware token and its PIN.

## How it works

- Tomb registers a discoverable credential on your authenticator using the `hmac-secret` extension.
- During forge (`tomb forge --fido2 -k …`) Tomb asks the device for an HMAC secret derived from:
  - a random challenge,
  - the relying party (`tomb.dyne.org` by default),
  - the credential id, and
  - a random salt Tomb stores in the key header.
- The returned 32‑byte secret (plus optional extra material) is used as the passphrase to encrypt the tomb key. Tomb embeds the FIDO2 metadata (`rp`, `cred`, `salt`, optional `device`) in the key header.

When opening/locking with `--fido2`, Tomb:

1) Reads the `_FIDO2 …` header from the key file.  
2) Requests a new `hmac-secret` from the authenticator with the stored RP, credential id, and salt.  
3) Uses that secret to decrypt the key and unlock the tomb.

## Usage

- Forge a FIDO2 key:
  ```
  tomb forge --fido2 -k secrets.tomb.key
  ```
- Lock/open with the passkey:
  ```
  tomb lock  --fido2 -k secrets.tomb.key secrets.tomb
  tomb open  --fido2 -k secrets.tomb.key secrets.tomb
  ```
- If you have multiple authenticators, point to one explicitly: `--fido2-device /dev/hidrawX`.

## Hardware requirements

- The authenticator must advertise the `hmac-secret` extension (`fido2-token -I` should list `extension strings: hmac-secret`).
- A PIN/UV-capable device is required; Tomb requests user verification.

### DIY option: Fidelio on Raspberry Pi Pico

If you need a compliant token and want to build it yourself, you can flash the open-source [Fidelio](https://github.com/danielinux/fidelio) firmware on a Raspberry Pi Pico to create a FIDO2 authenticator with `hmac-secret` support.

## Security notes

- The passphrase is never stored; the authenticator derives it on demand.
- Losing the registered passkey means losing access to the tomb unless you keep another copy of the key protected differently.
- The FIDO2 metadata in the key header is not secret; protect the key file itself as usual.
