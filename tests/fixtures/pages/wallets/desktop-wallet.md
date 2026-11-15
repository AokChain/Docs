---
title: Desktop wallet
description: Install the desktop wallet, let it sync and find your way around its screens.
order: 1
aliases: [desktop]
---

The desktop wallet runs on Windows, Linux and macOS. It holds AOK and tokens, stakes, and has an explorer built in.

> [!IMPORTANT]
> Wallet download links are published on this site. Do not run installers from anywhere else.

## First start

1. Open the wallet. It shows the AOK mark while it loads the block index.
2. Let it sync. The first sync downloads every block since 2020; the side bar shows the progress and the block height.
3. Once the status light says **Up to date**, the balance and the transactions are final.

![The first sync in the desktop wallet, with the progress in the side bar](/assets/img/wallet-sync.svg)

## The screens

| Screen | What it is for |
|---|---|
| Overview | Balance (available, pending, immature), staking and recent transactions |
| Send | AOK and tokens to one or more addresses |
| Receive | Your addresses and payment requests |
| Transactions | Every transfer and stake, with filters |
| Tokens | Token balances, transfers and issuing |
| Explorer | Blocks, transactions and addresses, read from your own node |

> [!TIP]
> Press <kbd>Ctrl</kbd> + <kbd>F</kbd> on the Transactions screen to filter by address or amount.

## Where the files are

The wallet keeps its data in one folder:

| System | Folder |
|---|---|
| Windows | `%APPDATA%\AokChain` |
| Linux | `~/.aokchain` |
| macOS | `~/Library/Application Support/AokChain` |

Back up `wallet.dat` from this folder; see [[backup]].
