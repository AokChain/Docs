---
title: Message signing
description: Prove control of an AokChain address by signing a text: the RPCs, the signature format, the hash, and the block of text the desktop wallet exchanges.
order: 60
---

A signed message proves that whoever made it holds the private key of an address, without moving any coins. Services use it to check that a withdrawal address belongs to a customer, or to sign in with an address. This page gives the commands and the exact format, so that other programs can make and check the same signatures.

## Sign and verify with the node

Sign with a key of the wallet:

```bash
aokchain-cli signmessage "KgF2VA2npjK7bYitFfrvoZa9FXNPieuRDF" "I control this address. 2026-11-15"
```

```text
IFH7dGp1q987L4SN0jQoHNUE/mpKl9rWz//GCw6wc7s0LCyGYWKDZGEIcf41TMB9erXvEVH2ocr8vkYzKHnMIfw=
```

Sign with a private key, without a wallet:

```bash
aokchain-cli signmessagewithprivkey "<WIF private key>" "I control this address. 2026-11-15"
```

Verify, on any node:

```bash
aokchain-cli verifymessage "KgF2VA2npjK7bYitFfrvoZa9FXNPieuRDF" \
  "IFH7dGp1q987L4SN0jQoHNUE/mpKl9rWz//GCw6wc7s0LCyGYWKDZGEIcf41TMB9erXvEVH2ocr8vkYzKHnMIfw=" \
  "I control this address. 2026-11-15"
```

The answer is `true`. With one character more or less in the text, or another address, it is `false`. This address, text and signature are a test vector: the key that made them was thrown away, so do not send coins to the address.

- Only addresses of a single key can sign: pay to public key hash, starting with `K` on mainnet. A multisig (`k`) address answers `Address does not refer to key`.
- An encrypted wallet must be unlocked for `signmessage`. A wallet unlocked for staking only answers `Error: Wallet is unlocked for staking only.`
- The text is signed byte for byte. Line breaks, trailing spaces and the character encoding (UTF-8) all count.

The desktop wallet does the same on its Sign page ("Prove my address", "Check a signature"); see [[sign-and-verify]]. The explorer API checks signatures too: `POST /api/v3/verify` ([[explorer-api]]).

## The format

| | |
|---|---|
| Message prefix | `AOK Signed Message:\n` (20 bytes, with the line feed) |
| Hash | Double SHA-256 of: the length of the prefix as a compact size (one byte, `0x14`), the prefix, the length of the message as a compact size, the message |
| Signature | 65 bytes: a header byte, then `r` and `s` (32 bytes each). The header is 27 + the recovery id, plus 4 when the key is compressed |
| Encoding | Base64, 88 characters |

The verifier recovers the public key from the signature and the hash, and compares its key hash with the address. This is the scheme of Bitcoin's `signmessage` with AokChain's prefix, so libraries for Bitcoin signed messages work when they let you set the prefix; with bitcoinjs-message, for example, the message prefix is `"\u0014AOK Signed Message:\n"`.

The hash in Python:

```bash
python3 -c '
import hashlib, sys
def cs(n):
    return bytes([n]) if n < 253 else (b"\xfd" + n.to_bytes(2, "little") if n < 0x10000 else b"\xfe" + n.to_bytes(4, "little"))
prefix = b"AOK Signed Message:\n"
msg = sys.argv[1].encode("utf-8")
data = cs(len(prefix)) + prefix + cs(len(msg)) + msg
print(hashlib.sha256(hashlib.sha256(data).digest()).hexdigest())
' "I control this address. 2026-11-15"
```

```text
d6ce418b40cee3abdb41f443bc1ee92ba8f2909c9545a43e983efea1bd70cd20
```

## The signed text of the desktop wallet

The Sign page puts the text, the address and the signature into one block, which can be pasted into a chat or a mail:

```text
-----BEGIN AOKCHAIN SIGNED MESSAGE-----
I control this address. 2026-11-15
-----BEGIN SIGNATURE-----
KgF2VA2npjK7bYitFfrvoZa9FXNPieuRDF
IFH7dGp1q987L4SN0jQoHNUE/mpKl9rWz//GCw6wc7s0LCyGYWKDZGEIcf41TMB9erXvEVH2ocr8vkYzKHnMIfw=
-----END AOKCHAIN SIGNED MESSAGE-----
```

- The text is everything between the first two markers; the line breaks right after `BEGIN AOKCHAIN SIGNED MESSAGE` and right before `BEGIN SIGNATURE` are not part of it. A text of several lines keeps its line breaks, and they must stay as they are for the signature to fit.
- After `BEGIN SIGNATURE` come the address and the signature. The wallet removes all white space there and takes the last 88 characters as the signature, so a block whose lines a messenger has joined still reads.
- Windows line ends (`\r\n`) are read as `\n`.
