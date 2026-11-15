---
title: Glossary
description: The words of AokChain and its wallets, one short entry each, from address to weight.
order: 50
---

Every entry has its own anchor, so other pages can link to it, for example `[[glossary#owner-token]]`.

### Address

The place you receive AOK and tokens at. Ordinary main network addresses start with `K`, script addresses such as multisig addresses with `k`, and offline staking addresses with `2`. See [[key-concepts#keys-and-addresses|Keys and addresses]].

### AOK

The coin of AokChain. 1 AOK is 100,000,000 of the smallest unit (often called a sat).

### AokChain Core

The reference software: the desktop wallet `aokchain-qt`, the node `aokchaind` and the command-line client `aokchain-cli`.

### Block

A batch of transactions added to the chain. A new block is expected every 64 seconds.

### Block reward

What the staker of a block earns: the block subsidy plus the fees of the transactions in the block. See [[staking-rewards]].

### Coin control

A setting of the desktop wallet that lets you choose which coins a payment spends: **Settings › Wallet › Enable coin control features**, then **Inputs...** on the **Send** page.

### Coinstake

The transaction in a proof-of-stake block that spends the staked coin and pays it back with the reward.

### Confirmation

A block that includes a transaction, or comes after the one that does. A transaction with six confirmations is shown as **Confirmed** in the desktop wallet.

### Fee

The amount of AOK a transaction pays to the staker of its block. It depends on the size of the transaction. See [[key-concepts#fees|Fees]].

### Frozen address

An address that governance has frozen. Outputs with its script cannot be spent until it is unfrozen. See [[address-freezing]].

### Governance

Signed commands of the network's master address. They set the cost of creating tokens, set the address that receives that cost, and freeze or unfreeze addresses. See [[how-network-rules-change]].

### Halving

Every 525,960 blocks the block subsidy is cut in half. See [[staking-rewards]].

### Immature

Coins that have to wait before they can be used: a new stake and its reward for 60 blocks. The desktop wallet shows them under **Immature (staking rewards)**.

### IPFS hash

A reference (starting with `Qm`, 46 characters) to a file on IPFS that describes a token. See [[token-metadata]].

### Main token

A token with a name of its own, such as `ORCHARD`. Also called a root token. See [[token-basics]].

### Memory pool

The transactions that a node has received and that wait for a block. Also called the mempool.

### Multisig

An address that needs M of N signatures to spend its coins, for example 2 of 3. See [[multisig-wallets]].

### Network stake weight

An estimate of all the coins that stake on the network at the moment. Your share of it decides how often you stake.

### Node

A program that keeps the chain and checks every block. The desktop wallet runs one. See [[install-a-node]].

### Offline staking

Coins that stay in the owner's wallet and are staked by another node. See [[offline-staking]].

### Orphaned stake

A block of yours that lost against a block of another staker that arrived first. It earns nothing; the staked coin is free again. The desktop wallet counts these as lost.

### Owner token

The token `NAME!` that is created with the token `NAME`. Its holder can reissue the token and create sub tokens and unique tokens under it. See [[token-basics]].

### Passphrase

The password that encrypts the keys in the wallet file. It cannot be recovered. See [[encrypt-your-wallet]].

### Proof of stake

The way AokChain makes blocks: holders of coins sign blocks with them instead of mining. See [[how-staking-works]].

### Reissue

Issuing more of an existing token, or changing its settings, by the holder of its owner token. See [[reissue-a-token]].

### Signing request

A multisig payment that is passed from participant to participant until enough of them have signed it. See [[multisig-wallets]].

### Snapshot

A copy of the chain state at a fixed block. A new installation starts from it and checks it against values built into the program.

### Stake

A coin of your wallet used to make a block, or the act of making one.

### Staking-only unlock

A state of an encrypted wallet in which the keys sign stakes and nothing else. Sending still asks for the passphrase. See [[stake-in-the-desktop-wallet]].

### Sub token

A token under a main token, written `MAIN/SUB`. See [[token-basics]].

### Time lock

A lock that keeps the recipient of coins or tokens from spending them before a block height or a time. The desktop wallet calls it **Send with a lock**.

### Token

An asset with its own name that lives on the chain next to AOK. See [[token-basics]].

### Transaction

A transfer of AOK or tokens, signed by the keys of its inputs.

### Transaction time

Every AokChain transaction carries the time it was made (nTime). The explorer shows it as **Tx time (nTime)**.

### Unique token

A token that exists exactly once, written `MAIN#tag`. The explorer calls unique tokens NFTs. See [[unique-tokens]].

### Units

The number of decimals of a token, from 0 to 8. See [[token-names-and-costs]].

### Username

A name such as `@ALICE` that stands for the address that holds it. See [[usernames]].

### Wallet file

The file `wallet.dat` that holds the keys of a desktop wallet or a node. See [[back-up-and-restore]].

### Watch-only

An address the wallet follows without having its key, such as a multisig address. Its coins are shown apart from your own balance.

### Weight

The amount of your coins that can stake at the moment. `getstakinginfo` shows it in sats.
