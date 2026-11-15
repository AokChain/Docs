---
title: AokChain Core 4.0
description: "What is new in AokChain Core 4.0 for wallet users, stakers, exchanges and node operators, compared with 3.0.x."
order: 10
---

AokChain Core 4.0 is a new node and desktop wallet for the same chain. It needs no hard fork and has no activation height, connects to 3.0.x nodes, and opens 3.0.x wallet files. It includes security fixes; every node, exchange and staker should upgrade ([[upgrade-to-4-0]]). The changes of each 4.0 version are on [[version-history]]; downloads are being prepared at [web.aok.network/download](https://web.aok.network/download/).

## Compatibility

| | |
|---|---|
| Chain | The same chain. The whole main network, more than three million blocks, was validated again from the first block with 4.0, and no block was rejected. |
| Activation height | None. 4.0 and 3.0.x nodes follow the same chain. |
| Protocol | Version 70021; 3.0.x (70020) and 4.0 nodes connect to each other. |
| Wallet file | Unchanged (Berkeley DB 4.8): 3.0.x wallets open in 4.0, and 3.0.x opens them again afterwards. |
| Data directory | Used as it is, with its indexes; no reindex for the upgrade. |
| RPC | Every 3.0.x command is still there, with the same arguments. |

## Security and validation

Block and transaction validation, network handling and the wallet were reviewed and strengthened. For offline staking, block validation now makes sure that delegated coins and their rewards always go back to the owner's offline staking address; the rule tightens validation without a hard fork.

Peers that break the rules are no longer written to the ban list; the node keeps a record of them in memory until it restarts. `listbanned` and `setban` show and change only the bans that you set.

## Fast first sync

A new node no longer has to fetch three million blocks from its peers ([[fast-sync]]):

- **Chain state snapshot.** A new installation can start from the chain state at block 3,031,432. The program accepts it only when its hashes match the values built into the program; it reaches the tip in minutes.
- **Block archives.** The blocks are published in 15 files at [github.com/AokChain/Mainnet-blocks](https://github.com/AokChain/Mainnet-blocks). The node imports them and validates every block as if it came from a peer.
- **assumevalid** moved to block 3,030,000, and block validation itself is faster.
- New options `bootstrapurl`, `bootstrapdir`, `bootstrap`, `bootstrapminblocks`, `snapshot`, `fetchblocks`, and RPCs `getbootstrapinfo`, `skipbootstrap`, `getsnapshotinfo`, `fetchblocks`, `getstatehashes`.

## Staking

- The staking thread no longer takes a whole processor core when there is nothing to stake, and does not repeat its search within the same 16-second slot (26.5% of a core with the 3.0.x code, 0.14% with 4.0, on a test wallet).
- `getstakinginfo` reports `staking` and `expectedtime` correctly, and adds `stakes_24h`, `orphaned_24h` and `reward_24h`; the desktop wallet shows the same in its side bar.
- `stakecombinethreshold` (default 1,000 AOK) sets the size of the staking coins: a stake gathers smaller coins of its address and splits in two at twice the threshold.
- `repaircoins` gives coins back the transaction time that a reorganization removed from the chain state, and 4.0 stakes such coins correctly.
- Stakes that lost against another block are left out of balance scans; `purgeorphanstakes` deletes them from the wallet file.
- An encrypted wallet can be unlocked for staking only, in the desktop wallet as with `walletpassphrase "<passphrase>" 0 true`. See [[stake-with-a-full-node]].

## Wallet

- A wallet with years of transactions answers quickly: it only looks at transactions with outputs that can still be spent. On a test wallet with 30,000 transactions, `getbalance` went from 67 ms to 2 ms, `sendtoaddress` from 152 ms to 18 ms and `listaddressgroupings` from more than 11 minutes to 1.4 seconds. Results are the same as before.
- `getbalances` shows the trusted, pending, immature, staked, locked and offline staking balances apart.
- `restorewallet` restores a backup into a wallet folder and loads it; `unloadwallet` unloads a second wallet; `backupwallet` backs up the right file for wallets in folders of their own.
- `aokchain-wallet` looks into a wallet file, creates one or salvages one, without a node.
- `mnemonictokeys` and `mnemonicfindaddress` derive keys from the BIP39 recovery words of another wallet; `importmnemonic` imports them.

## The desktop wallet

The Qt wallet was reorganized from the layout up ([[desktop-wallet]]):

- a side bar, a light theme, and amounts, addresses and transaction ids in a fixed-width font;
- a first start that sets a wallet passphrase and makes a backup before anything else;
- a Sign page to prove an address, check a signature, and create and use multisig wallets with signing requests ([[sign-and-verify]], [[multisig-wallets]]);
- a built-in explorer for blocks, transactions and addresses on your own node;
- back and forward buttons, and a status light on every page (from 4.0.3);
- Korean and English, chosen at the top of the settings page;
- the fast sync, with its addresses and a folder choice under Network settings.

## Commands and options for operators and developers

New RPC commands: `fetchblocks`, `getaddressinfo`, `getbalances`, `getblockstats`, `getbootstrapinfo`, `getindexinfo`, `getnodeaddresses`, `getrpcinfo`, `getsnapshotinfo`, `getstatehashes`, `importmnemonic`, `mnemonicfindaddress`, `mnemonictokeys`, `purgeorphanstakes`, `repaircoins`, `restorewallet`, `scantxoutset`, `signrawtransactionwithkey`, `signrawtransactionwithwallet`, `skipbootstrap`, `testmempoolaccept`, `unloadwallet`. `sendrawtransaction` takes a fee rate limit. See [[rpc]].

New options: `rpcwhitelist` and `rpcwhitelistdefault` (limit an RPC user to some commands, [[json-rpc]]), `daemonwait`, `startupnotify`, `shutdownnotify`, `logratelimit`, `stakecombinethreshold`, `spendofflinestaking`. The default `dbcache` is 1024 MiB on computers with 4 GB of memory or more. See [[configuration-options]].

Changed answers: since 4.0.4 the address index calls take `{"addresses": [...]}` and `getaddressutxos` returns pages; `mediantime` of `getblock` and `getblockheader` is the median time past. `getblocktemplate` serves proof-of-work templates only. Some yes-or-no fields are still printed as `1` and `0`, as in 3.0.x.

## Fixes

- `-reindex` no longer stops at a block that was stored before its parent; `-reindex-chainstate` rebuilds the token and governance databases as well.
- The balance on the send and token pages of the desktop wallet is refreshed; `getwalletinfo` no longer prints `hdmasterkeyid` without an HD seed.
- `aokchain-tx` and `libaokchainconsensus` build and link again.

## Under the hood

The code that descends from Bitcoin Core and Ravencoin was brought up to current toolchains: C++17 (GCC 13), Boost 1.83, OpenSSL 3.0.15, libevent 2.1.12, ZeroMQ 4.3.5, miniupnpc 2.2.7, Berkeley DB 4.8.30, and Qt 5.15.10 for the Windows wallet. Several commands and options were taken over from later Bitcoin Core versions.
