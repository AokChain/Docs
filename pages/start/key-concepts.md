---
title: Key concepts
description: Keys, addresses, confirmations, fees, staking, maturity and tokens, explained in a few lines each.
order: 20
---

A short tour of the ideas that the rest of this wiki uses. The [[glossary]] has one entry for each term.

## Keys and addresses

A wallet holds private keys. Each key belongs to an address, and whoever has the key can spend what is at that address. You give your address to people who pay you; you never give out the key.

| A main network address that starts with | is |
| --- | --- |
| `K` | an ordinary address with one key |
| `k` | a script address, such as a [[multisig-wallets|multisig]] address |
| `2` | an [[offline-staking|offline staking]] address (62 characters) |

A [[usernames|username]] such as `@ALICE` is not an address, but wallets and commands accept it in place of the address that holds it.

## The wallet file

The desktop wallet keeps its keys in one file, `wallet.dat`. A passphrase encrypts the keys in that file, and a copy of the file is your backup. See [[encrypt-your-wallet]] and [[back-up-and-restore]].

## Transactions and confirmations

A transaction moves AOK or tokens from one address to another. It waits in the memory pool of the nodes until a block includes it. From then on each new block adds one confirmation. The desktop wallet shows a payment as **Unconfirmed** while it waits, then **Unconfirmed 1/6** to **Unconfirmed 5/6**, and **Confirmed** from six confirmations on.

A transaction that has been sent cannot be cancelled or reversed.

## Fees

Every transaction pays a fee in AOK. The fee depends on the size of the transaction in bytes, not on the amount, and it goes to the staker of the block that includes it. By default the desktop wallet pays about 0.01 AOK per kilobyte, so a simple payment of about 230 bytes costs about 0.0024 AOK. Nodes relay transactions that pay at least 0.0001 AOK per kilobyte.

Creating a token costs more than the fee: see [[token-names-and-costs]].

## Blocks and staking

A new block is expected every 64 seconds. To make one, a wallet stakes: it uses one of its coins to sign the block. A coin with more AOK has a proportionally better chance. The staker gets the block subsidy and the fees of the block, added to the staked coin. See [[how-staking-works]] and [[staking-rewards]].

## Maturity

Some coins have to wait before they can be used:

- A coin can stake once it has 60 confirmations, about an hour after it arrived.
- After a stake, the staked coin and its reward are **immature** for 60 blocks. During that time they can be neither spent nor staked again.

## Tokens

A token is an asset with its own name, such as `ORCHARD`, that lives on the chain next to AOK. Whoever holds the owner token `ORCHARD!` controls the token: they can issue more of it (if it is reissuable), and create sub tokens and unique tokens under it. Sending a token pays a normal fee in AOK. See [[token-basics]].

## Nodes

A node keeps a copy of the chain and checks every block and transaction against the rules. The desktop wallet runs a full node on your computer. A new installation on the main network starts from a snapshot of the chain state that the program checks against values built into it, so it is ready in minutes. See [[desktop-wallet]].

## Amounts

1 AOK is 100,000,000 of the smallest unit, so amounts have up to 8 decimals. The desktop wallet can also show amounts in mAOK (1/1,000 AOK) and µAOK (1/1,000,000 AOK): **Settings › Display › Unit to show amounts in**.
