---
title: Version history
description: "The changes of every AokChain Core version from 4.0.0 to 4.0.8, and the 3.0.x line before them."
order: 20
---

What changed in each version of AokChain Core. Every 4.0 version accepts the same blocks as every other; none of them has an activation height. Run the newest one. Downloads are listed at [@@site_host@@/download](@@site@@/download/).

| Version | Date | For whom |
|---|---|---|
| 4.0.8 | 2026-11-17 | Everyone on 4.0: nodes with an address index, nodes that open several wallets, desktop wallet users on Linux |
| 4.0.7 | 2026-11-17 | Desktop wallet users; nodes that load wallets while they run |
| 4.0.6 | 2026-11-16 | Everyone on 4.0: programs that call the wallet and token commands, operators who change indexes, desktop wallet users |
| 4.0.5 | 2026-11-14 | Nodes with an address index (explorers, indexers) |
| 4.0.4 | 2026-11-14 | Programs that use the address index calls |
| 4.0.3 | 2026-11-14 | Desktop wallet users |
| 4.0.2 | 2026-11-14 | Desktop wallet users |
| 4.0.1 | 2026-11-14 | Everyone on 4.0.0 |
| 4.0.0 | 2026-11-13 | Everyone on 3.0.x |
| 3.0.5 | 2022-09-24 | The last 3.0.x version |

## 4.0.8

A maintenance release. The rules do not change: 4.0.8 accepts the same blocks as 4.0.0 to 4.0.7, and the chain state is not touched. Upgrade every node.

- Token queries: the commands that read token data are coordinated with block processing, and listing tokens is a little faster.
- Reorganizations and re-indexing: disconnecting blocks and reading blocks back from disk (`-reindex`, `-reindex-chainstate`) are exact for every kind of token transaction: issues, reissues, transfers, sub tokens, unique tokens, usernames and owner tokens.
- Address index: token outputs other than transfers are stored without a lock time. A node that runs with `-addressindex` should be started once with `-reindex` after the upgrade, which corrects the records of earlier blocks; new blocks are right without it, and `getaddressutxos` was not affected. Other nodes need nothing ([[upgrade-to-4-0#explorers-and-indexers|Explorers and indexers]]).
- Staking wallets: `-stakingwallet=<name>` names the wallets that `-staking` stakes with. It may be given several times, and without it every wallet stakes, as before. A node that stakes with one wallet and opens others for a service names its staking wallet; the others then do not stake, whether they are opened at the start or later ([[stake-with-a-full-node#several-wallets|Several wallets]]).
- Desktop wallet for Linux: the Linux release has the desktop wallet again, as 3.0.5 had: `aokchain-qt` in an archive of its own, with Qt linked in. It uses the X and font libraries that an Ubuntu 22.04 or 24.04 desktop installs, and types other scripts through IBus ([[desktop-wallet#on-linux|On Linux]]).
- Desktop wallet: the **Staking** switch shows "on" only once staking has started, not while the passphrase is being asked for. The steps of the multisig wizard have a row of their own, so its title fits a window of 1280 px. The units are named AOK, Milli-AOK and Micro-AOK, "username" is one word everywhere, and the passphrase hint names no keyboard key.
- Help texts: every example uses AokChain's ports and example addresses that belong to nobody, and amounts are in AOK. A token name that is too short or reserved is refused with that reason; the error codes are unchanged. `-staking` and `-advancedui` are in the help ([[configuration-options]]).
- Version text: the release programs report the plain version, `v4.0.8`. A build from a source archive names its own commit.

## 4.0.7

The desktop wallet runs several wallets in one window; the rules and the chain state do not change, and a node with one wallet behaves as before.

- Desktop wallet: the wallet that is shown is chosen at the top of the side bar, with **Create Wallet**, **Open Wallet**, **Restore Wallet** and **Close Wallet**. Every page follows the wallet shown, and each wallet has its own keys, tokens, multisig wallets, passphrase and **Staking** switch ([[desktop-wallet#several-wallets|Several wallets]]).
- A new wallet can be encrypted right away, and encrypting a wallet that is not the first one needs no restart. The wallets that were open are opened again at the next start; with `-wallet` exactly the named wallets are loaded.
- With several wallets open, the window title, the notifications and the console name the wallet. The console has a wallet selector. A wallet that a command loads or unloads while the window is open appears in the window or leaves it within a few seconds.
- A wallet that is created or loaded while the node runs (`createwallet`, `loadwallet`, `restorewallet`) stakes when the node runs with `-staking`; before, only the wallets of the start staked.
- `unloadwallet` waits for a running stake search of that wallet (at most a minute) before the wallet file is closed. The answers and error codes of the wallet commands are unchanged.
- Desktop wallet texts: "1 kind" and "2 kinds" of tokens and "24 h: 1 reward" instead of "(s)", **Staking only** under the name of a wallet that is unlocked for staking only.

## 4.0.6

Small fixes of the node, the commands and the desktop wallet; the rules and the chain state do not change.

- `sendtoaddress` and `sendfrom` refuse a `lock_time` from 1 to 255 or below 0 with error `-8`. Such a value made an output without a lock; 0 is still no lock, and 256 or more locks as before.
- `conf_target` and `estimate_mode` of `sendtoaddress` and `sendmany` work; they always failed. The help of `sendtoaddress` says that the message is written into the transaction.
- Every token command and `createrawtransaction` refuse an offline staking address with error `-5`, `Tokens cannot be sent to an offline staking address`. A transfer there failed with `Transaction amount too small`, an issue or a reissue only when it was sent.
- `registerusername` answers a name that is not a username with `Invalid username: <name>` and the rule.
- `issueunique` takes a sub token as the parent: `issueunique "ORCHARD/GREEN" '["tree-17"]'`.
- `aokchain-cli` without a running node says `couldn't connect to server`, and `-rpcwait` waits while a starting node has not written its cookie yet.
- A start with `-reindex-chainstate` and a changed index stops with the `-reindex` message and no longer deletes the token database first ([[indexes]]).
- `removeaddress` does not rescan on a pruned node, and its help is its own.
- Desktop wallet: typos on the token pages, the quantity limits of **Create Tokens** and **Manage Tokens** follow the 25,000,000,000 of the rules, large quantities stay exact, the multisig backup help names **Wallet security**, and the token send page says when an address cannot hold tokens.

## 4.0.5

The address index only; the chain state does not change.

- When a block is disconnected, the address index now gets back the coins that the stakes of the block had spent, so that `getaddressutxos` and `getaddressbalance` include them.
- A node whose address index has been running under an older version should rebuild it once with 4.0.5: start with `-reindex` ([[indexes]]).

## 4.0.4

RPC only; the rules and the data do not change.

- The address index calls (`getaddressbalance`, `getaddresstxids`, `getaddressutxos`, `getaddressmempool`, `getaddressdeltas`) take `{"addresses": [...]}`, as their help says. One address, or a username, as a string works as before. An address given twice counts once. `getaddresstxids` takes `start` and `end` heights in the object.
- `getaddressutxos` returns pages: with `{"limit": n}` it answers `{"utxos": [...], "next": "..."}`, and `after` continues from `next`. The outputs come in the order of block height, transaction id and output index. The object also takes `chainInfo`, `amount` and `tokenName`.
- `mediantime` of `getblock` and `getblockheader` is the median time past of the block; before, it was the block's own time.

## 4.0.3

The desktop wallet only; `aokchaind` and `aokchain-cli` are the same as in 4.0.1.

- Back and forward buttons on every page header, through the pages, the explorer's lookups and the Sign pages. Alt+Left and Alt+Right (Cmd+[ and Cmd+] on a Mac) and the mouse buttons do the same.
- A status light next to every page title: green when the node has peers and a recent block, amber while it syncs or reads, red without a connection. A click on it, or F5 (Cmd+R), reads the page again.

## 4.0.2

The desktop wallet only; `aokchaind` is the same as in 4.0.1.

- The settings page no longer offers to restore from the recovery words of another wallet. The RPCs `importmnemonic`, `mnemonicfindaddress` and `mnemonictokeys` stay.
- Passphrase fields take English letters, digits and symbols only, and say so when another character is typed. A wallet whose passphrase has other characters is unlocked with `walletpassphrase` in the console.

## 4.0.1

- Security fixes. Every 4.0.0 node should upgrade.
- `getblocktemplate` serves proof-of-work templates only; when the next block has to be a proof-of-stake block it returns an error.
- `-debug=coinstake` works, and the duration of the first stake search after a start is logged.
- `importmnemonic` takes `validate=false`, which skips the BIP39 checksum of the recovery words.

## 4.0.0

The first 4.0 version: a new node and desktop wallet for the same chain. Everything it brings is on [[aokchain-4-0]].

## 3.0.x

| Version | Date |
|---|---|
| 3.0.5 | 2022-09-24 |
| 3.0.2 | 2022-03-31 |
| 3.0.1 | 2022-03-29 |
| 3.0.0 | 2022-03-28 |

The 3.0.x line speaks protocol version 70020. Its nodes and 4.0 nodes connect to each other and follow the same chain, and its wallet files open in 4.0. 3.0.x does not build on current systems and has no further versions; replace it with 4.0 ([[upgrade-to-4-0]]).
