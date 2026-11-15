---
title: Offline staking
description: Let another node stake your AOK while the coins and the spending key stay in your wallet.
order: 2
---

Offline staking splits one address into two keys. The **staking key** goes to a node that is always online and stakes. The **spending key** stays in your wallet, so only you can move the coins.

![Your wallet keeps the coins and the spending key, a staking node holds the staking key](/assets/img/offline-staking.svg)

## Set it up

1. On the staking node, create a staking address:

   ```bash
   aokchain-cli getnewaddress
   ```

2. In your wallet, make the offline staking address from the staking node's address and one of your own:

   ```bash
   aokchain-cli getofflinestakingaddress "<staking address>" "<spending address>"
   ```

3. Send the AOK you want staked to the new address.

> [!NOTE]
> Rewards go to your address. The staking node never holds coins it can spend.

## Stop

Send the coins from the offline staking address to an ordinary address. The staking node stops staking them with the next block.

## Questions

**Can the staking node spend my coins?** No. It only has the staking key.

**What happens when the staking node is offline?** Nothing is lost; the coins wait. See [[staking-guide#on-a-node|staking on a node]] to run your own.
