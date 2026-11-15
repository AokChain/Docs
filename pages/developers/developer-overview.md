---
title: Developer overview
description: "Where to start when you build on AokChain: the interfaces of a node, the differences from Bitcoin that break code, and how to test on regtest."
order: 10
---

AokChain Core descends from Bitcoin Core and Ravencoin, so most tools and habits carry over. This page lists the ways to talk to a node, the places where AokChain differs in ways that break code written for Bitcoin, and how to test without real coins.

## Ways in

| Interface | Use it for | Page |
|---|---|---|
| JSON-RPC | Everything: wallets, payments, chain data, tokens. | [[json-rpc]], [[rpc]] |
| `aokchain-cli` | The same commands from a shell. | [[json-rpc]] |
| ZeroMQ | Push notifications of new blocks and transactions. | [[zmq]] |
| `walletnotify`, `blocknotify` | Run a command on wallet and chain events. | [[exchange-integration]] |
| REST | Read-only blocks, transactions, headers and mempool over plain HTTP, without authentication. | below |
| `aokchain-tx` | Build and sign transactions offline. | [[raw-transactions]] |
| `aokchain-wallet` | Inspect, create or salvage a wallet file without a node. | [[configuration-options#aokchain-wallet]] |
| Explorer API v3 | Chain data over HTTPS without your own node. | [[explorer-api]] |

### REST

With `rest=1` the node answers `GET` requests on its RPC port, without authentication, so keep that port local:

```bash
curl -s http://127.0.0.1:33440/rest/chaininfo.json
curl -s http://127.0.0.1:33440/rest/tx/<txid>.json
curl -s http://127.0.0.1:33440/rest/block/<hash>.json
```

The paths are `/rest/tx/`, `/rest/block/`, `/rest/block/notxdetails/`, `/rest/headers/<count>/<hash>` and `/rest/getutxos`, each with `.json`, `.hex` or `.bin`, and `/rest/chaininfo`, `/rest/mempool/info` and `/rest/mempool/contents`, with `.json` only.

## What differs from Bitcoin

| Area | AokChain | Consequence for your code |
|---|---|---|
| Consensus | Proof-of-work blocks ended at block 1,440; every later block is proof of stake, with a target of 64 seconds between blocks. | No mining. `getblocktemplate` serves only proof-of-work templates, so on mainnet it returns an error. See [[how-staking-works]]. |
| Transaction format | A 4-byte time after the version; version 2 adds a message string at the end. | Bitcoin parsers and test vectors fail. See [[raw-transactions]]. |
| Block hash | BLAKE2b-256 of the 80-byte header. Every block ends with a signature field after the transactions, empty in proof-of-work blocks. | Do not compute block hashes with SHA-256; parse the signature field. |
| SegWit | Not active on mainnet and testnet. | Only legacy and P2SH scripts; no bech32 addresses. |
| Addresses | `K` (P2PKH), `k` (P2SH), `2` (offline staking, 62 characters) on mainnet; WIF keys start with `e`. | Use the version bytes of [[network-parameters]]. |
| Tokens | Token data rides in the script of an output with 0 AOK. | Wallet lists mix AOK and token entries; check `token_name`. See [[exchange-integration]]. |
| Time-locked outputs | `sendtoaddress` takes a lock time that makes a `CHECKLOCKTIMEVERIFY` output; `transfer` takes one that locks the token output. | The third positional argument of `sendtoaddress` is `lock_time`. |
| Governance | A master key can freeze addresses and set the costs of token issuance. | Check `checkfreeze` before paying out. See [[address-freezing]]. |
| Offline staking | An output that one key spends and another key stakes. | `scantxoutset` with `staking(<address>)` finds delegated coins. See [[offline-staking]]. |
| RPC values | Some yes-or-no fields are `1` and `0`. | Accept both forms. See [[json-rpc]]. |
| Wallet accounts | Labels are also legacy accounts; `sendmany` spends from one account's balance. | Use `sendtoaddress` or raw transactions. See [[exchange-integration]]. |

## Test on regtest

Regtest is a private chain on your computer, where you make blocks on demand:

```bash
aokchaind -regtest -daemon
aokchain-cli -regtest getnewaddress
aokchain-cli -regtest generatetoaddress 101 <that address>
aokchain-cli -regtest getbalance
```

| Regtest fact | Value |
|---|---|
| Data directory | `regtest` under the data directory |
| P2P and RPC ports | 18444 and 44550 (the RPC port is the same as testnet's) |
| Block 1 | Pays 2,100,000,000 AOK, as on mainnet |
| Blocks after it | 4 AOK each, spendable after 10 confirmations |
| Proof of stake | Not before height 1,440,000; `-lastpowblock=<height>` starts it earlier, for tests |
| Tokens, governance | Active from height 10 |
| Addresses | Start with `m` or `n` (P2PKH) and `2` (P2SH); WIF keys with `c` |

Token issuing on regtest costs the built-in amounts (10,000 AOK for a root token) and pays them to the built-in regtest address; `issuanceinfo` shows both.

The test network (`-testnet`, port 44551) has no DNS seed; connect to nodes you know with `addnode`.

## Source and builds

The source of AokChain Core 4.0 is published at [github.com/AokChain/AokChain](https://github.com/AokChain/AokChain) with the release. [[install-a-node]] builds it on Linux.
