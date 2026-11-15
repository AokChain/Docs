---
title: AokChain 4.0
description: What changed in the 4.0 node and wallets, and how to upgrade from 3.0.
order: 1
---

AokChain 4.0 reworks the node and the wallets without a hard fork. It connects to 3.0 nodes and opens existing wallet files.

## Highlights

- A new desktop wallet with staking, tokens, multisig and a built-in explorer
- Balance queries in milliseconds on large wallets[^1]
- Staking that uses a fraction of the CPU of 3.0

## Upgrade

1. Stop the node or the wallet.
2. Back up `wallet.dat`, see [[backup]].
3. Install 4.0 and start it. The data folder stays where it is.

> [!NOTE]
> 4.0 is not a hard fork. Nodes that stay on 3.0 keep following the same chain.

## Changes for developers

- `getstakinginfo` reports the expected time to the next stake
- ~~`listassets`~~ is `listtokens`
- New commands are in [[rpc-commands]]

[^1]: Measured on regtest, on a wallet with 30,000 transactions.
