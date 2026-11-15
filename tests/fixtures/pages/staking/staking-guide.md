---
title: Staking
description: Earn block rewards with the AOK you hold, in the desktop wallet or on a node.
order: 1
aliases: [staking]
---

AokChain makes blocks by proof of stake. A wallet that holds mature AOK and stays online takes part, and every block it makes pays a reward.

## In the desktop wallet

1. Open **Receive** and create an address.
2. Send AOK to it.
3. Turn on **Staking** in the side bar.

Coins mature 60 blocks after they arrive. From then on the wallet stakes, and each stake appears in **Transactions**.

## On a node

Add `staking=1` to `aokchain.conf`, or start the node with `-staking`:

```ini
staking=1
```

Then create an address and send AOK to it:

```bash
aokchain-cli getnewaddress
```

Check that the node stakes:

```bash
aokchain-cli getstakinginfo
```

```json
{
  "enabled": true,
  "staking": true,
  "errors": "",
  "currentblocksize": 1000,
  "weight": 125000000000,
  "netstakeweight": 9800000000000,
  "expectedtime": 5120
}
```

## Without leaving a computer on

[[offline-staking]] lets a node stake for you while your coins stay in your own wallet.
