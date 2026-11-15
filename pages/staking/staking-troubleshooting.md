---
title: Staking troubleshooting
description: What to check when a wallet does not stake, loses stakes or keeps old stakes, and how to use repaircoins and purgeorphanstakes.
order: 60
---

Work through the checks in order. Most problems are a locked wallet, a wallet that is not synchronized, or coins that are not mature yet.

## The wallet does not stake

| You see | Cause | What to do |
| --- | --- | --- |
| **Off · the wallet is locked** | Staking is off, or the wallet was locked | Turn on the **Staking** switch and enter the passphrase with **For staking only** ticked. |
| **Off · staking is possible once synchronized**, or **On · waiting for the synchronization to finish** | The wallet is still catching up | Wait until the status light says **Up to date**. If it stays red, see [[ports-and-peers]]. |
| **On · no mature coins** | No coin has 60 confirmations | Wait about an hour after coins arrive or after a stake. |
| `"staking": 0` in `getstakinginfo` on a node | See the checks below | |

On a node, check each of these:

1. `getstakinginfo` shows `"enabled": 1`. If not, add `staking=1` to `aokchain.conf` and restart.
2. The wallet is unlocked. After every restart, run `walletpassphrase "<passphrase>" 0 true` again.
3. `getconnectioncount` shows at least 2, and `getblockchaininfo` shows a recent block. When staking starts, the node waits for two peers and a block of the last ten minutes.
4. `weight` in `getstakinginfo` is more than 0. If it is 0, the coins are not mature, or they are tokens, multisig coins or coins you locked with `lockunspent`.

For more detail, start the node with `-debug=coinstake`: it then writes each stake attempt to `debug.log`.

## Stakes are often lost

A stake is lost when another staker's block for the same height reaches the network first. A few lost stakes are normal. If you lose many:

- Keep the computer's clock exact; let the system set it automatically. Blocks carry a time, and a wrong clock makes your blocks late or refused.
- Check the connection: a node with few or slow peers hears of new blocks late and sends its own late.
- Run only one copy of a wallet. Two computers that stake the same coins compete against each other.

## After an upgrade from version 3.0

The chain state of a node that ran an older version can hold coins without the time of their transaction. Version 4.0 stakes such coins correctly, and `repaircoins` puts the missing data back. First count them:

```bash
aokchain-cli repaircoins true
```

| Field | Meaning |
| --- | --- |
| `scanned` | Unspent outputs read |
| `damaged` | Unspent outputs without a time |
| `repaired` | Of those, the ones that can be repaired (with `true`) or were repaired (without it) |
| `unreadable` | Of those, the ones whose transaction this node cannot read |

With `true` nothing is changed. Then repair them:

```bash
aokchain-cli repaircoins
```

The command reads every unspent output of the chain, which takes a while. A second `repaircoins true` should then report `"damaged": 0`. In the desktop wallet, type the commands without `aokchain-cli` in **Settings › Debug window**, on the **Console** tab.

## A staking wallet keeps growing

Every lost stake stays in the wallet file as an abandoned transaction, which makes a long-running staking wallet larger and slower to load. Balances do not include them. To delete those older than a day:

```bash
aokchain-cli purgeorphanstakes
```

It returns the number of transactions it deleted. An optional argument sets the minimum age in seconds, for example `purgeorphanstakes 3600` for one hour. If such a block ever becomes part of the chain again, its transaction is added back.
