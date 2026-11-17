---
title: Address freezing
description: What it means when governance freezes an address, how a freeze is lifted, and how to check whether an address is frozen.
order: 10
---

Governance can freeze an address. The coins of a frozen address cannot be spent until governance unfreezes it. This page explains what a freeze covers and how to check for one.

## What a freeze does

- A freeze command carries one output script, the script of the address it freezes: pay to public key hash for an address that starts with `K`, pay to script hash for `k`. Every node refuses a transaction that spends an output with exactly that script, in the memory pool and in blocks (`bad-txns-address-frozen`).
- Payments from the address that wait in the memory pool when the freeze takes effect are dropped.
- The address can still receive. Whatever is sent to it stays there until the freeze is lifted.
- A freeze takes effect when the block with the command is added to the chain, and it lasts until an unfreeze command lifts it.

Freeze and unfreeze commands are governance commands: transactions of the network's master address, see [[how-network-rules-change]]. A transaction of any other address cannot freeze anything, and the master address cannot freeze itself.

## Check an address

- **Block explorer:** look the address up on [@@explorer_host@@](@@explorer@@). A frozen address carries a **Frozen** mark and the line "This address is frozen by governance." The **Network** page lists all frozen addresses.
- **Node:** `checkfreeze` answers `true` or `false` for the script of the address:

  ```bash
  aokchain-cli checkfreeze "<address>"
  ```

- **All at once:** `freezelist` lists every address that has a freeze entry, with `true` for frozen and `false` for one that was frozen and then unfrozen, and the `total`. On the main network it takes a while.
- **[[explorer-api|AokChain API]]:** `@@api@@/address/<address>/frozen` returns `{"address": "...", "frozen": true}` or `false`.

## Before you send

If you are not sure about an address, check it before you pay it: coins sent to a frozen address cannot be moved by its owner until the freeze is lifted.

## If your address is frozen

Only governance can lift a freeze. The coins at your other addresses are not affected, but the wallet still counts the frozen coins in your balance and may pick them for a payment, which the network then refuses. To pay from your other addresses, choose their coins with coin control: **Settings › Wallet › Enable coin control features**, then **Inputs...** on the **Send** page.
