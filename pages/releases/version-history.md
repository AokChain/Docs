---
title: Version history
description: The changes of every AokChain Core version from 4.0.0 to 4.0.5, and the 3.0.x line before them.
order: 20
---

What changed in each version of AokChain Core. Every 4.0 version accepts the same blocks as every other; none of them has an activation height. Run the newest one. Downloads are being prepared at [web.aok.network/download](https://web.aok.network/download/).

| Version | Date | For whom |
|---|---|---|
| 4.0.5 | 2026-11-14 | Nodes with an address index (explorers, indexers) |
| 4.0.4 | 2026-11-14 | Programs that use the address index calls |
| 4.0.3 | 2026-11-14 | Desktop wallet users |
| 4.0.2 | 2026-11-14 | Desktop wallet users |
| 4.0.1 | 2026-11-14 | Everyone on 4.0.0 |
| 4.0.0 | 2026-11-13 | Everyone on 3.0.x |
| 3.0.5 | 2022-09-24 | The last 3.0.x version |

## 4.0.5

The address index only; the chain state does not change.

- When a block was disconnected, the coins of stakes that it had spent were not given back to the address index, so `getaddressutxos` missed them and `getaddressbalance` was too low. 4.0.5 gives them back.
- A node whose address index has been running under an older version should rebuild it once with 4.0.5: start with `-reindex` ([[indexes]]).

## 4.0.4

RPC only; the rules and the data do not change.

- The address index calls (`getaddressbalance`, `getaddresstxids`, `getaddressutxos`, `getaddressmempool`, `getaddressdeltas`) take `{"addresses": [...]}`, as their help says. One address, or a user name, as a string works as before. An address given twice counts once. `getaddresstxids` takes `start` and `end` heights in the object.
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
- The recovery words of the AOK mobile wallet, which have no BIP39 checksum, are accepted: `importmnemonic` takes `validate=false`.
- `contrib/aokchain/upgrade.sh` waits for a node that does not run under systemd, can start a new installation from the snapshot, and keeps the newest three backups.

## 4.0.0

The first 4.0 version: a new node and desktop wallet for the same chain. Everything it brings is on [[aokchain-4-0]].

## 3.0.x

| Version | Date |
|---|---|
| 3.0.5 | 2022-09-24 |
| 3.0.2 | 2022-03-31 |
| 3.0.1 | 2022-03-29 |
| 3.0.0 | 2022-03-28 |

The 3.0.x line speaks protocol version 70020. Its nodes and 4.0 nodes connect to each other and accept the same blocks, and its wallet files open in 4.0. 3.0.x does not build on current systems and has no further versions; replace it with 4.0 ([[upgrade-to-4-0]]).
