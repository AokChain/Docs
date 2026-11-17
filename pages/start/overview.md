---
title: What is AokChain
description: AokChain is a proof-of-stake blockchain with built-in tokens and governance commands. Its coin is AOK.
order: 10
---

AokChain is a public blockchain. Its coin is AOK. The main network started in May 2020 and has run as one chain since then.

## What the chain does

- **Proof of stake.** Blocks are made by holders of AOK whose wallets stake. The first blocks were mined with proof of work: blocks 1 to 72, and 7 of the 10 after them. Every block from 83 on is a proof-of-stake block. The target time between two blocks is 64 seconds. See [[how-staking-works]].
- **Offline staking.** You can keep your coins in your own wallet and let another node stake them for you. See [[offline-staking]].
- **Tokens.** Tokens are created and moved on the chain itself: main tokens, sub tokens, unique tokens and usernames. See [[token-basics]].
- **Governance.** Signed governance commands set the cost of creating tokens and can freeze an address. See [[how-network-rules-change]].
- **Multisig and time locks.** Coins can sit at an address that needs several signatures to spend them, or be sent with a lock so that the recipient cannot spend them before a set time.

## The software

AokChain Core is the reference software. Its code descends from Bitcoin Core and Ravencoin.

| Program | What it is |
| --- | --- |
| Desktop wallet (`aokchain-qt`) | The wallet with a window, for Windows, Linux and macOS. It runs a full node and offers staking, tokens, multisig and an explorer. |
| `aokchaind` | The node without a window, for servers. |
| `aokchain-cli` | Sends commands to a running node. |

The current release line is 4.0. It is an upgrade without a hard fork: see [[aokchain-4-0]]. Downloads are listed at [@@site_host@@/download](@@site@@/download/).

The block explorer at [@@explorer_host@@](@@explorer@@) shows blocks, transactions, addresses and tokens of the main network. See [[block-explorer]].

## Where to go next

| You want to | Read |
| --- | --- |
| Learn the words first | [[key-concepts]] and the [[glossary]] |
| Hold and send AOK | [[choose-a-wallet]], then [[desktop-wallet]] |
| Earn staking rewards | [[how-staking-works]] |
| Create a token | [[token-basics]] |
| Run a node on a server | [[install-a-node]] |
| Build on AokChain | [[developer-overview]] |
