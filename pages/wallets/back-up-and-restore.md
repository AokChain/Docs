---
title: Back up and restore
description: Save a copy of your wallet file, keep it safe, and restore it in the desktop wallet or on a node.
order: 50
---

Your coins are in the wallet file on your computer. If the disk fails or the computer is lost, only a backup of that file brings them back. The desktop wallet does not use recovery words: the backup is the wallet file, and it opens with your passphrase.

## Make a backup

1. Go to **Settings › Wallet security › Backup Wallet**.
2. Choose a place and a file name and save. A message confirms that the wallet data was saved.
3. Copy the file to a USB drive or another computer. A backup that stays on the same disk does not help when that disk fails.

The backup is encrypted with the same passphrase as the wallet. Keep the passphrase written down in a different place from the backup.

## When to make a new one

Make a new backup:

- after you encrypt the wallet, because older backups are not encrypted and lack the keys the wallet makes from then on;
- after you import a key or add a multisig wallet;
- from time to time, so that labels and recent addresses are in it.

A multisig wallet is also described by its multisig information file. Keep that file with the backup. See [[multisig-wallets]].

## Restore in the desktop wallet

1. Close AokChain Core and wait until it has ended.
2. Open the data folder. The wallet file is `wallets/wallet.dat` (or `wallet.dat` in data folders of older versions). See [[desktop-wallet#where-the-files-are|Where the files are]].
3. Rename the current `wallet.dat`, for example to `wallet-old.dat`, so that nothing is lost.
4. Copy your backup into the same folder and name it `wallet.dat`.
5. Start AokChain Core. It reads the blocks since the backup was made and adds the transactions it finds; the status light shows **Rescanning** meanwhile.

A new installation starts from a snapshot of the chain state and has no blocks from before it. If the restored wallet needs them to find its earlier transactions, the wallet asks to download the past blocks. Click **Download**; the side bar shows the progress, and you can keep using the wallet.

## Restore on a node

On a node that runs, load the backup as a wallet of its own:

```bash
aokchain-cli restorewallet "restored" "/home/user/backup.dat"
```

The backup is copied to the folder `restored` in the wallet directory and loaded; the backup file itself is not changed. Address that wallet with `-rpcwallet=restored`, for example:

```bash
aokchain-cli -rpcwallet=restored getbalance
```

To make a backup on a node, use `backupwallet`:

```bash
aokchain-cli backupwallet "/home/user/backup.dat"
```

## Move the wallet to another computer

1. On the old computer, make a backup and close AokChain Core.
2. Install AokChain Core on the new computer and start it. Choose the data folder, then click **Quit** at the **Wallet passphrase** step: your backup already has a passphrase.
3. Put the backup in the data folder as `wallets/wallet.dat`, replacing the empty wallet that the first start made, and start AokChain Core again.
4. When the coins show on the new computer, stop using the old one.
