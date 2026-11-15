---
title: Offline staking
description: Keep your coins in your own wallet and let another node stake them, with an offline staking address. Set up, check, and end it.
order: 40
---

With offline staking your coins stay under your own key while another node stakes them. The staking node holds a key that can stake the coins and nothing else; the key that spends them stays with you, on a computer that does not need to be online.

## How it works

An offline staking address is made of two addresses:

- the **staking address**, an address of the staking node;
- the **spending address**, an address of your own wallet.

Coins sent to the offline staking address can be staked with the staking key, and spent only with the spending key. When they are staked, the coins and the reward go back to the same offline staking address. Block validation in AokChain Core 4.0 checks that delegated coins and their rewards always return to that address.

- The reward belongs to you. The staking node earns nothing on the chain; any fee for the operator has to be agreed outside the chain.
- You can spend the coins at any time, staked or not.
- An offline staking address on the main network starts with `2` and has 62 characters.
- Tokens cannot be sent to an offline staking address.

## Set it up

On the staking node, which runs AokChain Core 4.0 with `staking=1` and a wallet unlocked for staking (see [[stake-with-a-full-node]]):

1. Make the staking address and give it to the owner:

   ```bash
   aokchain-cli getnewaddress "staking key"
   ```

In the owner's wallet, on a node or in the desktop wallet under **Settings › Debug window** on the **Console** tab (there without `aokchain-cli`):

2. Make the spending address:

   ```bash
   aokchain-cli getnewaddress "spending key"
   ```

3. Combine the two into the offline staking address:

   ```bash
   aokchain-cli getofflinestakingaddress "<staking address>" "<spending address>"
   ```

4. Back up the owner's wallet. The spending key is in it; without it the coins cannot be spent. See [[back-up-and-restore]].
5. Send the coins you want to delegate to the offline staking address, from any wallet.

After 60 confirmations the staking node starts to stake them.

## Check it

`validateaddress` on the offline staking address shows `isofflinestaking`, the `stakingaddress` and the `spendingaddress`. On the owner's side `ismine` is `1`; on the staking node `isstakable` is `1`.

On the staking node:

```bash
aokchain-cli getbalances
aokchain-cli getstakinginfo
```

`getbalances` lists the delegated coins under `offline_staking`, apart from the node's own balance, and they count in the `weight` of `getstakinginfo`. The staking node cannot send them.

Any node can list what is delegated to a staking address:

```bash
aokchain-cli scantxoutset start '["staking(<staking address>)"]'
```

## Spend the coins or end the delegation

The owner's wallet counts the delegated coins in its balance, but a payment does not take them on its own. With only delegated coins in the wallet, a payment fails with "Insufficient funds". To spend them, select them:

- in the desktop wallet with coin control: turn on **Settings › Wallet › Enable coin control features**, then pick the coins with **Inputs...** on the **Send** page;
- or with a raw transaction, see [[raw-transactions]].

To end the delegation, send the coins to an ordinary address of your wallet. To let payments take delegated coins like any other, start the owner's wallet with `-spendofflinestaking=1`.

## Choose the staking node

The holder of the staking key can stake your coins and refuse to stake them, nothing else. If the node stops staking, move your coins to another offline staking address or back to your wallet. The staking key is a key on a server that is online, so the operator has to keep that server safe.
