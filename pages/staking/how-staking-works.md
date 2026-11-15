---
title: How staking works
description: How AokChain wallets make blocks with their coins, what you need to stake, how often you can expect a reward, and the ways to stake.
order: 10
aliases: [staking]
---

AokChain uses proof of stake. Instead of miners, wallets that hold AOK make the blocks, and the wallet that makes a block earns its reward. This page explains the mechanism; the pages after it show how to stake.

## How a block is made

Every 16 seconds a staking wallet tries each of its coins once. Each try is like a lottery ticket: a coin wins if a hash of the coin and the time falls below the current target. A coin with more AOK has a proportionally better chance, and how long you have held it plays no part. When a coin wins, the wallet makes a block, signs it with the key of that coin and sends it to the network.

The difficulty adjusts so that the whole network makes a block about every 64 seconds.

## What you need

- **Mature coins.** A coin can stake once it has 60 confirmations, about an hour after it arrived.
- **A running, connected wallet.** The wallet has to be synchronized and have peers. When staking starts it waits for at least two peers and a recent block.
- **An unlocked wallet.** An encrypted wallet has to be unlocked for staking; the staking-only unlock signs stakes and nothing else.
- **Staking switched on.** In the desktop wallet with the **Staking** switch, on a node with `staking=1`.

There is no minimum amount.

## How often you stake

Your chance per block is your share of all coins that stake at the moment:

```text
expected time between your stakes = 64 seconds × network stake weight / your weight
```

For example, if your weight is 1% of the network stake weight, expect a stake about every 6,400 seconds, a little under two hours. This is an average; single stakes come earlier or later by chance. The desktop wallet shows the estimate in the side bar ("On · a reward about every ..."); a node reports it as `expectedtime` in `getstakinginfo`.

## What happens to your coins

- The staked coin is spent by the stake and paid back in the same block, together with the reward. It stays with the same key, so the explorer shows it at the same address.
- After the stake, the coin and its reward are immature for 60 blocks. During that time they can be neither spent nor staked again.
- A stake gathers the small coins of the same address, those under 1,000 AOK, and splits a coin of 2,000 AOK or more into two. Over time the coins of a staking wallet end up between 1,000 and 2,000 AOK each. A node sets this size with `-stakecombinethreshold`.
- Sometimes another staker's block for the same height arrives first. Your block then loses: it earns nothing and the staked coin is free again. The desktop wallet counts these as lost.

## What does not stake

- Tokens, and AOK at multisig addresses.
- Coins that you locked with coin control.

## Ways to stake

| Way | For | Page |
| --- | --- | --- |
| Desktop wallet | Staking on your own computer while it runs | [[stake-in-the-desktop-wallet]] |
| Full node | A server that stakes around the clock | [[stake-with-a-full-node]] |
| Offline staking | Keep the coins in your wallet and let another node stake them | [[offline-staking]] |

What a stake earns is on [[staking-rewards]]. If nothing happens, see [[staking-troubleshooting]].
