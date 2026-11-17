---
title: Stake in the desktop wallet
description: Turn on staking in the AokChain Core desktop wallet with a staking-only unlock, and read what the side bar shows.
order: 20
---

The desktop wallet stakes while it runs. You turn staking on with the **Staking** switch at the bottom of the side bar.

## Start staking

1. Receive the AOK you want to stake into the wallet. See [[send-and-receive]].
2. Wait until the status light says **Up to date** and the coins have 60 confirmations, about an hour.
3. Turn on the **Staking** switch.
4. The wallet asks for your passphrase. Keep **For staking only (sending coins asks for the passphrase again)** ticked, enter the passphrase and click **Start staking**.

The side bar now shows **Staking only** under the name of the wallet (**Unlocked for staking only** in versions before 4.0.7) and a line such as "On · a reward about every 3 hours". Point at the staking line to see your weight, the network weight and the expected time.

Keep the computer on and awake: a wallet that sleeps does not stake.

## While it stakes

- Each stake appears on the **Transactions** page as **Staking reward**; the **Staking** tab lists only stakes.
- After a stake, the coin and its reward show under **Immature (staking rewards)** on the **Overview** page for 60 blocks.
- The side bar adds a line for the last 24 hours, such as "24 h: 2 rewards · 0.25 AOK". If some of your blocks lost against a block of another staker, it adds "· 1 lost"; those earn nothing.
- To send coins while staking, use **Send** as usual. The wallet asks for the passphrase and returns to staking only after the payment.

## Stop staking

Turn off the **Staking** switch. A wallet that was unlocked for staking only is locked again.

After a restart the switch is off. Turn it on again to stake.

## Several wallets

Each wallet stakes on its own, with its own coins. The **Staking** switch is that of the wallet shown, so turn it on in every wallet that should stake. When other open wallets stake, the side bar adds a line such as "1 other wallet staking". Closing a wallet stops its staking. See [[desktop-wallet#several-wallets|Several wallets]].

## What the side bar says

| Side bar | Meaning |
| --- | --- |
| On · a reward about every ... | The wallet stakes. |
| Off · staking is possible once synchronized | The wallet is still catching up with the network. |
| On · waiting for the synchronization to finish | Staking is on and starts when the wallet has caught up. |
| Off · the wallet is locked | The switch is off, or the wallet was locked from elsewhere. Turn the switch on. |
| On · no mature coins | No coin has 60 confirmations yet, or all coins are immature after a stake. |

If staking still does not start, see [[staking-troubleshooting]].

## A wallet without encryption

If your wallet is not encrypted, the switch starts staking without asking for a passphrase. Anyone who gets a copy of the wallet file can then spend the coins: see [[encrypt-your-wallet]].
