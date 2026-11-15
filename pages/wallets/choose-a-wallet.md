---
title: Choose a wallet
description: Which AokChain wallet to use for holding, sending, staking and tokens, and what each one needs.
order: 10
---

All AokChain wallets hold keys to the same chain, so the choice depends on how you want to use AOK.

| Wallet | Runs on | Good for |
| --- | --- | --- |
| Desktop wallet (AokChain Core) | Windows, Linux, macOS | Holding and sending AOK, staking, tokens, multisig |
| Node (`aokchaind` and `aokchain-cli`) | Linux servers, also Windows and macOS | Staking around the clock, exchanges, services |
| AOK Wallet app | Phone and web browser | In testing, see [[aok-wallet-app]] |

## Desktop wallet

The desktop wallet is AokChain Core with a window. It runs a full node on your computer: it checks every new block itself and does not depend on a server.

- It needs a computer that is online while you use it, and at least 8 GB of free disk space.
- It stakes while it runs. To stake without keeping a computer on, see [[offline-staking]].
- It can create and send tokens, sign messages, and hold coins in multisig wallets.

Start with [[desktop-wallet]].

## Node on a server

A node runs without a window and is driven with `aokchain-cli` or JSON-RPC. It is the choice for a staking server, an exchange or a service. It has the same wallet functions as the desktop wallet. See [[install-a-node]] and [[stake-with-a-full-node]].

## Keep one wallet in one place

Do not run the same wallet file on two computers at the same time, for example to stake from both: both make blocks with the same coins, and only one block of each pair can stay in the chain. To use your coins on another computer, move the wallet there: see [[back-up-and-restore]].
