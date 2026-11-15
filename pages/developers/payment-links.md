---
title: Payment links
description: "The aokchain: URI that the desktop wallet reads from links and QR codes: address, amount, label and message, encoding rules and examples."
order: 50
---

A payment link opens the desktop wallet with a payment filled in: the recipient, the amount and a note. Shops and invoices use it as a link or a QR code. This page describes the `aokchain:` URI exactly as the desktop wallet reads and writes it.

## Format

```text
aokchain:<address>[?amount=<AOK>][&label=<text>][&message=<text>]
```

```text
aokchain:KacWDE2Fyqywwr6YDKt1FYthycv3Ee7dqv?amount=12.5&label=Order%201042&message=Thank%20you
```

| Part | Meaning |
|---|---|
| `aokchain:` | The scheme. `aokchain://` is read the same way. |
| `<address>` | The AokChain address to pay. A slash after it is ignored. |
| `amount` | The amount in AOK: digits with a `.` as the decimal point and at most 8 decimals, for example `12.5` or `0.00010000`. No thousands separators, no unit. |
| `label` | A name for the recipient, filled in as the label of the payment in the send form. |
| `message` | A note for the payer, shown in the send form. The payer's wallet keeps it with the payment in its own records; it is not written into the transaction. |

- `label` and `message` are percent-encoded (UTF-8): a space is `%20`, `&` is `%26`.
- Parameters that the wallet does not know are ignored, unless their name starts with `req-`. A `req-` parameter means "required": the wallet refuses a link with a `req-` parameter it does not understand, instead of paying without it.
- A link with an amount that does not parse (a comma, more than 8 decimals) is refused as a whole.
- The link names AOK only. There is no parameter for tokens.

## How the wallet uses it

- **Opening a link.** The Windows installer script, the macOS application bundle and the Linux desktop file of the source declare the `aokchain:` scheme, so a wallet installed through one of them opens such links with the send form filled in. A wallet that was only unpacked from an archive registers nothing; use File, Open URI then. The payer checks and confirms the payment; a link never sends anything by itself.
- **File, Open URI** in the wallet takes a pasted link, and a link dropped onto the window works the same way.
- **Receiving.** The Receive page makes such a link and its QR code from the address, amount, label and message you enter, and copies either. The QR code holds the link text; a link longer than 255 characters gets no QR code.
- An address that is not valid for the network the wallet runs on gives `Invalid payment address`; a malformed link gives `URI cannot be parsed!`.

The wallet also has code for the old BIP70 payment protocol, which a link with an `r=` parameter starts. Do not build new payment flows on it.

## Make a link in code

Percent-encode the label and the message, and write the amount with a dot and no more than 8 decimals:

```bash
python3 -c 'from urllib.parse import quote; print("aokchain:%s?amount=%s&label=%s" % ("KacWDE2Fyqywwr6YDKt1FYthycv3Ee7dqv", "12.5", quote("Order 1042", safe="")))'
```

```text
aokchain:KacWDE2Fyqywwr6YDKt1FYthycv3Ee7dqv?amount=12.5&label=Order%201042
```

Give every order its own address (`getnewaddress`), so that the payment can be matched without relying on the label or the message, which the payer can change. Then watch the address as [[exchange-integration]] describes.
