---
title: Desktop wallet
description: Install the AokChain Core desktop wallet, go through the first start, and find your way around its window.
order: 20
aliases: [desktop]
---

The desktop wallet is AokChain Core with a window (`aokchain-qt`). It runs on Windows, Linux and macOS and keeps a full node on your computer. This page takes you from the download to a synchronized wallet.

## Download

Get the desktop wallet from [web.aok.network/download](https://web.aok.network/download/). Official downloads and their SHA256 checksums are listed on that page only. Compare the checksum of the file you downloaded with the one on the page before you install it.

## First start

The first start goes through the steps **Start**, **Wallet passphrase** and **Backup**, with the download of the chain state in between.

1. **Welcome.** Choose a language under **Language**. Under **Data folder**, keep **Use the default data directory** or pick **Use a custom data directory:**. The folder needs at least 8 GB of free space. Click **Continue**.
2. **Fast start.** On the main network, a new installation now downloads a snapshot of the chain state at block 3,031,432 (about 1 GB) and checks it against values built into the program. The start screen shows the progress ("Fast start: downloading the snapshot"); this takes a few minutes. The blocks before the snapshot are downloaded later, and only if you need them, for example to find the earlier transactions of a restored wallet.
3. **Protect the wallet.** Type a passphrase in **New passphrase** and again in **Repeat new passphrase**. Use English letters, digits and symbols; a space is allowed. Tick **I wrote the passphrase down and understand that it cannot be recovered** and click **Encrypt wallet**. The program restarts to finish the encryption.
4. **Keep a backup.** Click **Save a backup...** and save the copy of the wallet file on a USB drive or another computer. **Later** skips this step; you can make a backup at any time from **Settings**.

> [!WARNING]
> Nobody can reset or recover the passphrase. If you forget it, the coins in the wallet are lost.

After the snapshot, the wallet follows the chain from block 3,031,432 to the newest block.

## While it synchronizes

Until the wallet has caught up with the network, a window shows the blocks left and the progress, and the page header says "Balances may differ from the real ones while synchronizing". Click **Hide** to use the wallet in the meantime. The side bar keeps showing the progress.

If you have downloaded block archives yourself, **Choose a folder with block archives...** imports them; every block is checked as usual. See [[fast-sync]].

## The window

The side bar on the left opens the pages:

| Page | Keys | What you do there |
| --- | --- | --- |
| **Overview** | Alt+1 | Balance, tokens, recent transactions and a search box |
| **Send** | Alt+2 | Send AOK or tokens, see [[send-and-receive]] and [[send-tokens]] |
| **Receive** | Alt+3 | Get an address and a QR code to be paid |
| **Transactions** | Alt+4 | The history of the wallet, with filters and **Export to CSV** |
| **Tokens** | Alt+5 | The tokens of the wallet |
| **Explorer** | Alt+8 | Look up blocks, transactions and addresses on your own node |
| **Address book** | Alt+9 | Your receiving addresses and the addresses you send to, see [[address-book]] |
| **Sign message** | | Prove an address, check a signature, multisig, see [[sign-and-verify]] |
| **Settings** | Alt+0 | Options, wallet security and information |

At the bottom of the side bar are the **Staking** switch, the synchronization state, the number of peers and the network, the state of the wallet (for example **Wallet locked**) and the version.

Next to every page title is a status light:

- **Up to date** (green): the node has peers and a recent block.
- **Synchronizing**, **Importing blocks**, **Reindexing** or **Rescanning** (amber): the node is busy; balances may be incomplete until it is done.
- **No connection** or **Network off** (red): no peers, or the network activity is turned off.

Click the light, or press F5 (Cmd+R on a Mac), to read the page again. The back and forward buttons in the header go through the pages you have opened; Alt+Left and Alt+Right (Cmd+[ and Cmd+] on a Mac) do the same.

## Coming from version 3.0

A wallet file of version 3.0.x opens in 4.0 as before.

1. Close the old wallet and make a copy of its `wallet.dat`.
2. Install 4.0 and start it. It uses the same data folder.
3. If the wallet is not encrypted yet, a band above the pages says "This wallet is not encrypted." Click **Encrypt** and follow [[encrypt-your-wallet]].

For nodes on servers, see [[upgrade-to-4-0]].

## Where the files are

| System | Default data folder |
| --- | --- |
| Windows | `%APPDATA%\AokChain` |
| macOS | `~/.aokchain` |
| Linux | `~/.aokchain` |

The wallet file is `wallets/wallet.dat` in the data folder. Data folders made by older versions may keep it directly in the data folder as `wallet.dat`. **Settings › Open Configuration File** opens `aokchain.conf`, the configuration file in the data folder.

## Change the language

At the top of **Settings**, pick a language in **Language**, then click **Restart now**.

## Network options

Most people never need them. **Settings › Network settings** has port mapping (UPnP), incoming connections, a SOCKS5 proxy, Tor and the addresses of the block archives for a fast first synchronization. See [[ports-and-peers]].
