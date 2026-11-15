---
title: Staking rewards
description: What a stake earns, how the block subsidy halves, when rewards can be spent, and how to estimate your rewards.
order: 50
---

The wallet that makes a block earns the block reward: the block subsidy plus the fees of the transactions in the block.

## The block subsidy

The subsidy started at 4 AOK per block and halves every 525,960 blocks. After ten halvings, from block 5,259,600 on, there is no subsidy and stakers earn the fees only.

| From block | Subsidy per block |
| --- | --- |
| 2 | 4 AOK |
| 525,960 | 2 AOK |
| 1,051,920 | 1 AOK |
| 1,577,880 | 0.5 AOK |
| 2,103,840 | 0.25 AOK |
| 2,629,800 | 0.125 AOK |
| 3,155,760 | 0.0625 AOK |
| 3,681,720 | 0.03125 AOK |
| 4,207,680 | 0.015625 AOK |
| 4,733,640 | 0.0078125 AOK |
| 5,259,600 | 0 |

Block 1 created the initial supply of 2,100,000,000 AOK. The home page of [v3.aokscan.com](https://v3.aokscan.com) shows the current subsidy and the height of the next halving.

## Where the reward goes

The reward is added to the staked coin, at the same address. With [[offline-staking]] it goes to the offline staking address, so it belongs to the owner of the coins.

A stake and its reward are immature for 60 blocks, about an hour. After that they can be spent or staked again.

## Estimate your rewards

At the target of one block every 64 seconds the network makes about 1,350 blocks a day. Your share of them is your share of the network stake weight:

```text
your stakes per day ≈ 1,350 × your weight / network stake weight
your rewards per day ≈ your stakes per day × (subsidy + fees per block)
```

For example, with 1% of the network stake weight you can expect about 13.5 stakes a day, which at 0.125 AOK each is about 1.7 AOK a day. Real results vary from day to day by chance, and the network stake weight changes as other stakers come and go.

## See what you earned

- **Desktop wallet:** stakes are listed as **Staking reward** on the **Transactions** page (tab **Staking**). The side bar shows the stakes and the reward of the last 24 hours.
- **Node:** `getstakinginfo` reports `stakes_24h` and `reward_24h`.

A block of yours that loses against a block of another staker earns nothing. The desktop wallet counts these as lost; `getstakinginfo` reports them as `orphaned_24h`.
