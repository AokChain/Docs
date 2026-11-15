---
title: Back up and restore
description: Keep a copy of your wallet file or recovery words, and bring a wallet back from it.
order: 3
---

## Back up the desktop wallet

Use **File › Backup wallet** and save the copy somewhere other than the computer it runs on.

- [x] Encrypt the wallet with a passphrase first
- [x] Save the backup to a USB stick or another computer
- [ ] Test the backup: open it on another computer with a fresh wallet

> [!CAUTION]
> Anyone with the wallet file and its passphrase can spend your coins. Keep the two apart.

## Restore

Stop the wallet, put the backup in place of `wallet.dat` in the data folder (see [[desktop-wallet#where-the-files-are|where the files are]]) and start the wallet again. It rescans the chain for your transactions.

```bash
aokchain-qt -rescan
```

## Check the passphrase

Unlock the wallet for a minute from the console to check that you remember the passphrase:

```text
walletpassphrase "your passphrase" 60
```
