---
title: Encrypt your wallet
description: Protect the keys in your wallet file with a passphrase, change the passphrase, and unlock the wallet for staking only.
order: 40
---

Encryption locks the keys in your wallet file with a passphrase. Someone who copies the file, or uses your computer, cannot send your coins without it. A new desktop wallet asks for a passphrase at its first start; this page is for older wallets and for changing the passphrase.

> [!WARNING]
> Nobody can reset or recover the passphrase, not even the developers. If you forget it, the coins in the wallet are lost. Write it down and keep it where only you find it.

## Choose a passphrase

- Use ten or more random characters, or four or more words. The wallet rates what you type as **Weak.**, **Fair. Longer is better.** or **Strong.**
- Use English letters, digits and symbols. A space is allowed. The passphrase fields of the desktop wallet accept nothing else, so check that your keyboard is set to English while you type.

## Encrypt an existing wallet

If the wallet is not encrypted, a band above the pages says "This wallet is not encrypted. Anyone who copies the wallet file or uses this computer can send the coins."

1. Click **Encrypt** in that band, or go to **Settings › Wallet security › Encrypt Wallet**.
2. Type the passphrase in **New passphrase** and again in **Repeat new passphrase**.
3. Tick **I wrote the passphrase down and understand that it cannot be recovered** and click **Encrypt wallet**.
4. AokChain Core restarts to finish the encryption. After the restart it offers to save a backup: click **Save a backup...**.

Backups made before the encryption are not encrypted, and they do not hold the keys of the addresses that the wallet makes from now on. Replace them with a new backup and destroy the old copies. See [[back-up-and-restore]].

## Change the passphrase

1. Go to **Settings › Wallet security › Change Passphrase**.
2. Enter the current passphrase, then the new one twice.
3. Click **Change passphrase**.

Your backups stay valid, but they open with the passphrase that the wallet had when you made them.

## When the wallet asks for the passphrase

The wallet stays locked while it runs. It asks for the passphrase when you send AOK or tokens, sign a message, create a token or make a multisig request, and locks itself again afterwards. The side bar shows **Wallet locked** or **Wallet unlocked**.

## Unlock for staking only

Staking needs the keys, so an encrypted wallet has to be unlocked to stake. When you turn on the **Staking** switch, the wallet asks for the passphrase with **For staking only (sending coins asks for the passphrase again)** ticked. In that state the keys sign stakes and nothing else, and the side bar says **Unlocked for staking only**. See [[stake-in-the-desktop-wallet]].

## On a node

On a node, use these commands:

| Command | What it does |
| --- | --- |
| `encryptwallet "passphrase"` | Encrypts the wallet; the node stops and has to be started again |
| `walletpassphrase "passphrase" 60` | Unlocks the wallet for 60 seconds |
| `walletpassphrase "passphrase" 0 true` | Unlocks it for staking only, until it is locked or the node stops |
| `walletlock` | Locks it at once |
| `walletpassphrasechange "old" "new"` | Changes the passphrase |

A wallet whose passphrase contains characters other than English letters, digits and symbols can still be unlocked with `walletpassphrase` in **Settings › Debug window**, on the **Console** tab.

See [[stake-with-a-full-node]] for a staking server.
