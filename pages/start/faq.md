---
title: FAQ
description: Short answers to the questions people ask first about wallets, staking, fees, tokens and the 4.0 upgrade.
order: 40
---

## Wallets

### Where do I download the wallet?

From [@@site_host@@/download](@@site@@/download/). Official downloads and their SHA256 checksums are listed on that page only.

### Does my wallet file from version 3.0 work with 4.0?

Yes. A 3.0.x `wallet.dat` opens in 4.0 as before. Make a copy of it before you upgrade. See [[upgrade-to-4-0]].

### How long does the first start take?

A new installation of the desktop wallet downloads a snapshot of the chain state (about 1 GB), checks it against values built into the program, and then follows the chain from there. This takes a few minutes on a normal connection. See [[desktop-wallet]].

### Does the desktop wallet have recovery words?

No. The desktop wallet keeps its keys in the wallet file. Your backup is a copy of that file, together with your passphrase. See [[back-up-and-restore]].

### I forgot my wallet passphrase. Can it be reset?

No. Nobody can reset or recover it. Without the passphrase the coins in an encrypted wallet cannot be spent. If you still have a backup that was made before you encrypted the wallet, it holds the keys of the addresses that existed at that time.

### What happened to the mobile wallet?

The AOK Wallet runs on phones and in the web browser. See [[aok-wallet-app]].

## Payments

### Can I cancel a payment?

No. A transaction that has been sent cannot be cancelled or reversed. Check the address before you click **Send**.

### What does a payment cost?

A fee that depends on the size of the transaction. With the default settings of the desktop wallet a simple payment costs about 0.0024 AOK. See [[key-concepts#fees|Fees]].

### My payment stays unconfirmed. What can I do?

Make sure your wallet is connected: the light next to the page title should say **Up to date**. If the transaction never gets into a block, right-click it on the **Transactions** page and choose **Abandon transaction**. This frees its coins in your wallet so that you can send again. The item is available only when the transaction is no longer waiting in the memory pool of your node.

### Who can see my transactions?

Everyone. All transactions and balances are public on the chain. They are linked to addresses, not to names. The desktop wallet gives you a new address for every payment request, which keeps your payments apart.

## Staking

### How much AOK do I need to stake?

There is no minimum. Your chance to make the next block grows with the amount you stake, and the wallet shows how often you can expect a reward. Coins can stake once they have 60 confirmations. See [[how-staking-works]].

### Why is part of my balance immature?

After a stake, the staked coin and its reward wait 60 blocks, about an hour, before they can be spent or staked again. See [[staking-rewards]].

### Do I have to keep my computer on to stake?

Yes, the wallet has to run and be connected. If you do not want to keep a computer on, you can delegate your coins to a node that stakes them: see [[offline-staking]].

## Tokens

### What does it cost to create a token?

Creating a token costs a fixed amount of AOK on top of the fee. The amounts are set by governance. See [[token-names-and-costs]].

### Why can I not find Create Tokens in the desktop wallet?

The pages **Create Tokens** and **Manage Tokens** appear when the wallet runs with the advanced view. See [[create-a-token]].

## The network

### My wallet says No connection.

The wallet has no peers. Check that the computer is online and that a firewall does not block AokChain Core. See [[ports-and-peers]].

### Is my address frozen?

Look the address up on [@@explorer_host@@](@@explorer@@): a frozen address carries a **Frozen** mark. See [[address-freezing]].
