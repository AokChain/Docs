---
title: Use the block explorer
description: Look up blocks, transactions, addresses, tokens and usernames of the main network on v3.aokscan.com.
order: 30
---

The block explorer at [v3.aokscan.com](https://v3.aokscan.com) shows what is on the main network. Use it to check that a payment arrived, to see the balance of any address, or to look at a token. It only reads the chain: it never asks for a key or a passphrase.

## Search

Type one of these into the search box at the top of any page:

| You type | You get |
| --- | --- |
| an address | its balance, tokens and history |
| a transaction ID (64 hexadecimal characters) | the transaction |
| a block height or a block hash | the block |
| a token name, such as `ORCHARD` | the token |
| a username, such as `@NAME` | the address that holds it |

## Pages

| Menu | What it shows |
| --- | --- |
| **Home** | Total supply, block subsidy, next halving, network stake weight, the latest blocks and transactions |
| **Blocks** | All blocks, newest first |
| **Mempool** | Transactions that wait for a block |
| **Tokens** | Main tokens, sub tokens, unique tokens and usernames |
| **Rich list** | The addresses with the largest balances |
| **Charts** | Activity of the chain per day |
| **Network** | The node version, peers, minimum relay fee and the list of frozen addresses |

## Read a transaction

- **Status** is **Confirmed** once a block includes the transaction; **Confirmations** counts the blocks since then.
- **Fee** is shown in AOK and in sats/kB (a sat is 0.00000001 AOK).
- **Tx time (nTime)** is the time written into the transaction itself. **Included in block** shows when the block was made.
- **Inputs** and **Outputs** list every address with its amount, in AOK or in a token.

A transaction that is not found may not have reached the network. Check that the wallet that sent it is connected and up to date.

## Read a block

A block page shows its **Time**, **Confirmations**, **Consensus** (proof of stake for every block after block 1,440), the **Staker** address, the **Staked amount** and the **Reward**, split into subsidy and fees. Its first transaction is an empty **Coinbase**; the second, the **Coinstake**, is the stake that made the block.

## Read an address

An address page shows the **Balance** and how much of it is **Spendable**, the **Tokens** at the address (with a **Locked** column for tokens sent with a lock), and the **History** and **Unspent outputs**. A frozen address carries a **Frozen** mark and the line "This address is frozen by governance." See [[address-freezing]].

## Read a token

A token page shows the **Supply**, the number of **Holders**, the **Decimals** (the units of the token), whether it is **Reissuable**, the block where it was **Issued**, the **Issuer** and the **Owner token holder**. The **Sub** and **NFT** tabs list its sub tokens and unique tokens; the explorer calls unique tokens NFTs.

## The explorer inside the desktop wallet

The desktop wallet has an **Explorer** page of its own. It looks up transactions, blocks and addresses on the node of your computer, so nothing is sent to an outside server. For an address it says whether the address belongs to your wallet; for the balance and history of any address, use v3.aokscan.com.

## The API

Services and wallets read the same data through API v3. See [[explorer-api]].
