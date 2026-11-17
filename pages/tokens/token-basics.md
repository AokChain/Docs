---
title: Token basics
description: The kinds of AokChain tokens, what the owner token does, what a token's settings mean, and where tokens show up.
order: 10
---

A token is an asset with its own name that lives on the chain next to AOK. Tokens are held at ordinary addresses, sent with ordinary transactions, and shown by every wallet and by the block explorer. Creating one costs AOK; sending one costs a normal fee in AOK.

## Kinds of tokens

| Kind | Written as | What it is |
| --- | --- | --- |
| Main token | `ORCHARD` | A token with a name of its own. Also called a root token. |
| Sub token | `ORCHARD/GREEN` | A token under a main token (or under another sub token), made by the holder of the parent's owner token. |
| Unique token | `ORCHARD#tree-17` | A token that exists exactly once. The explorer calls these NFTs. See [[unique-tokens]]. |
| Username | `@ALICE` | A name that stands for the address that holds it. See [[usernames]]. |
| Owner token | `ORCHARD!` | Made automatically with every main token and sub token. |

## The owner token

When you create `ORCHARD`, you also receive one `ORCHARD!`. Whoever holds it can:

- issue more `ORCHARD`, if the token is reissuable (see [[reissue-a-token]]);
- create sub tokens such as `ORCHARD/GREEN` and unique tokens such as `ORCHARD#tree-17`.

> [!WARNING]
> The owner token can be sent like any token, and the control of the token goes with it. If it is sent to a wrong address, or the wallet that holds it is lost, nobody can issue more of the token or create tokens under it again.

Keep an owner token apart from the wallet you use every day. In the desktop wallet (4.0.7 and later), create a wallet for it, for example "Issuer", send the owner token to an address of that wallet, and create and reissue tokens from there. See [[desktop-wallet#several-wallets|Several wallets]].

## Settings of a token

| Setting | Meaning | Can it change later? |
| --- | --- | --- |
| Name | The name, unique on the chain | No |
| Quantity | How many are issued | More can be added if the token is reissuable |
| Units | Decimals, from 0 (whole units) to 8 | Can be raised, never lowered |
| Reissuable | Whether more can be issued later | Can be turned off, never on again |
| IPFS hash | A reference to a file that describes the token | Can be added or replaced at a reissue, see [[token-metadata]] |

## What tokens cannot do

- Tokens do not stake. Only AOK stakes.
- Tokens cannot be sent to an offline staking address.
- The desktop wallet sends only AOK from multisig addresses, not tokens.

## Where tokens show up

- **Desktop wallet:** the **Tokens** page lists the tokens of the wallet, with **Send** and **Receive** on each; the **Overview** page lists them too. Creating and reissuing tokens is on the pages **Create Tokens** and **Manage Tokens**, which appear in the advanced view.
- **Block explorer:** the **Tokens** page of [@@explorer_host@@](@@explorer@@) lists every token with its supply and holders.
- **Node:** `listmytokens` lists the tokens of the wallet, `gettokendata "NAME"` shows the settings of a token, and `listtokens` lists the tokens of the chain.

Next: [[create-a-token]], [[send-tokens]], [[token-names-and-costs]].
