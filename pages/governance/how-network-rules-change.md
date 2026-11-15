---
title: How network rules change
description: The two ways AokChain's rules change, signed governance commands and new versions of AokChain Core, and how to see the current values.
order: 20
---

Some values of AokChain are set on the chain by governance commands; everything else is a rule in the node software and changes only with a new version.

## Governance commands

Governance commands are transactions of the network's master address, which is written into AokChain Core. On the main network it is `kp5eNwMzDfDgHXMG3XZw73c6rTA6WzFJEx`, and commands count from block 871,500 on. A command is a data output in a transaction that spends a coin of the master address, so it needs the master key's signature; the same data from any other address does nothing.

| Command | What it changes |
| --- | --- |
| Freeze | The outputs with the script of an address can no longer be spent. See [[address-freezing]]. |
| Unfreeze | Lifts a freeze. |
| Cost | The cost of creating a main token, a sub token, a unique token, a username, or of a reissue. See [[token-names-and-costs]]. |
| Cost address | The address that receives these costs. |

A command takes effect when its block is added to the chain. If that block is replaced in a reorganization, the command is undone with it.

To see the current values:

| Value | Node | Explorer |
| --- | --- | --- |
| Costs and the cost address | `issuanceinfo` | [/api/v3/tokens/issuance](https://v3.aokscan.com/api/v3/tokens/issuance) |
| Frozen addresses | `freezelist`, `checkfreeze "<address>"` | The **Network** page, [/api/v3/governance](https://v3.aokscan.com/api/v3/governance) |

## New versions of AokChain Core

The rules that decide whether a block or a transaction is valid, such as the block reward, the maturity of stakes or the token name rules, are part of the node software. They change only when node operators install a new version.

- A change that only makes the rules stricter can come with a new version without a hard fork: nodes that have not upgraded still accept the blocks of upgraded nodes. Version 4.0 is an upgrade of this kind; it has no activation height.
- A change that allows something the old rules refuse is a hard fork. It needs an activation height that is announced in advance, and every node, staker and exchange has to upgrade before that height.

Version 4.0 speaks protocol version 70021 and connects to older nodes as before. It also carries a switch that stops peering with old, incompatible nodes from a block height. The switch is off; such a height would be announced in advance, once an upgrade schedule is set.

## Keep up to date

4.0 includes security fixes; upgrade your node and your desktop wallet. See [[upgrade-to-4-0]]. What each version changed is in [[version-history]], and 4.0 is described in [[aokchain-4-0]].
