---
title: What AokChain is
description: A proof-of-stake blockchain with tokens, user names and governance built into the chain.
order: 1
aliases: [overview]
---

AokChain is a proof-of-stake blockchain that has run as one chain since May 2020. Tokens, unique tokens, user names and governance are part of the chain itself, not contracts on top of it.

## Coins and tokens

AOK is the coin of the chain. It pays network fees and it is what you stake. Tokens are issued on the same chain and move with the same transactions:

- **Tokens** have a name such as `ROOT`, an amount and a number of decimals.
- **Sub tokens** sit under a root token: `ROOT/SUB`.
- **Unique tokens** exist once: `ROOT#TAG`.

See [[create-a-token]] and [[token-metadata]] for the details.

## Staking

Blocks come from staking, not mining. Any wallet that holds mature coins can stake, and [[offline-staking]] lets another node stake for you while the coins stay in your wallet.

> [!NOTE]
> A block target is 64 seconds. Rewards arrive as stakes in your transaction list.

## Where to go next

| You want to | Start with |
|---|---|
| Hold and send AOK | [[desktop-wallet]] |
| Earn rewards | [[staking-guide]] |
| Run a node | [[run-a-node]] |
| Build on AokChain | [[json-rpc]] |
