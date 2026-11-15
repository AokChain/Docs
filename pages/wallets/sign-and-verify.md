---
title: Sign and verify messages
description: Prove that an address is yours by signing a text, and check a signature that someone sent you, in the desktop wallet or on a node.
order: 70
---

A signed message proves that the owner of an address wrote a text. Exchanges and partners ask for one to confirm that an address is yours. Signing moves no coins and sends nothing to the network.

## Prove my address

1. Open **Sign message** in the side bar. The page is called **Sign**.
2. Under **Prove my address**, click **Choose an address and sign**.
3. Under **1. My address**, click **Choose my address** and pick one of your addresses.
4. Under **2. The text to sign**, enter the text exactly as you were asked to sign it.
5. Click **Sign** and enter your passphrase if the wallet asks for it.
6. Under **3. Send this to the other side, as it is**, the address, the text and the signature appear as one block. Click **Copy all** and send the block.

The block looks like this:

```text
-----BEGIN AOKCHAIN SIGNED MESSAGE-----
I own this address
-----BEGIN SIGNATURE-----
<your address>
<the signature, 88 characters>
-----END AOKCHAIN SIGNED MESSAGE-----
```

Only ordinary addresses of your own wallet can sign. Multisig and offline staking addresses cannot.

## Check a signature

1. On the **Sign** page, under **Check a signature**, click **Paste a signature**.
2. Under **Paste what you received**, paste the whole block and click **Check**. The wallet takes the address, the text and the signature apart. If you received them separately, fill in **Address**, **Text** and **Signature** under **Or enter the three parts**.
3. The result says **Valid** or **Not valid**, with the reason.

**Valid** means that the owner of the address signed exactly this text. If one character of the text was changed, even a line break, the signature is **Not valid**.

## On a node

```bash
aokchain-cli signmessage "<address>" "I own this address"
aokchain-cli verifymessage "<address>" "<signature>" "I own this address"
```

`signmessage` returns the signature (88 characters, base64); `verifymessage` returns `true` or `false`. Signatures of the desktop wallet and of these commands are the same, so either side can check the other. For the format, see [[message-signing]].
