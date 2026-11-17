---
title: Network parameters
description: "Ports, message start bytes, address and key prefixes, block timing, maturity, reward schedule and activation heights of mainnet, testnet and regtest."
order: 12
---

The constants of the three AokChain networks, as AokChain Core 4.0 defines them (`src/chainparams.cpp`, `src/chainparamsbase.cpp`, `src/consensus/consensus.h`, `src/amount.h`, `src/validation.cpp`). Use them when you write software that speaks to the network or parses its data.

## Networks

| | Mainnet | Testnet | Regtest |
|---|---|---|---|
| Name in RPC (`chain`) | `main` | `test` | `regtest` |
| Select with | (default) | `-testnet` | `-regtest` |
| P2P port | 33441 | 44551 | 18444 |
| RPC port | 33440 | 44550 | 44550 |
| Message start (magic) | `3b ee e0 02` | `44 4b 52 04` | `43 52 4f 57` |
| Data subdirectory | (none) | `testnet1` | `regtest` |
| DNS seed | `dns.aok.network` | none | none |
| Genesis block | `000c513d39b0e3657b7b0ca79b2d4b9b18c1f03dacb394acf0e71f49064b3306` | `0027badb24c5a6f882e1151a47ab22e974491f7247888f5e5f330899589ed17d` | `79f23c0228fcd0c7c1e4f5c32ad3f4f390165a0f618659d627186719212a7e64` |
| Genesis time | 1589879227 (2020-05-19 UTC) | 1630926558 | 1296688602 |

The genesis block of mainnet carries the text `Trump Threatens WHO With Permanent Cutoff of U.S. Funds | May 19, 2020 Bloomberg`. Its output pays nothing and cannot be spent.

## Protocol

| | Value |
|---|---|
| Protocol version of 4.0 | 70021 |
| Oldest peer version accepted | 60018 |
| Block hash | BLAKE2b-256 of the 80-byte header |
| Transaction id, merkle root | Double SHA-256, as in Bitcoin |
| Transaction format | Version, time, inputs, outputs, lock time; a message string when the version is 2 or higher ([[raw-transactions]]) |
| Block format | Header, transactions, then the block signature: a byte vector, empty in proof-of-work blocks |
| Message signing prefix | `AOK Signed Message:\n` ([[message-signing]]) |
| SegWit | Off on mainnet and testnet, on in regtest |
| BIP34, BIP65 (CLTV), BIP66, CSV | On, on every network |

## Addresses and keys

| Base58 version | Mainnet | Testnet | Regtest |
|---|---|---|---|
| Pay to public key hash | 46: addresses start with `K` | 66: `T` | 111: `m` or `n` |
| Pay to script hash | 108: `k` | 128: `t` | 196: `2` |
| Offline staking (two key hashes, 62 characters) | 63: `2` | 125: `4` | 115: `3` |
| Private key (WIF) | 255: compressed keys start with `e` | 143: `N` | 239: `c` |
| Extended public key | `0488B21E` (`xpub`) | `043587CF` (`tpub`) | `043587CF` (`tpub`) |
| Extended private key | `0488ADE4` (`xprv`) | `04358394` (`tprv`) | `04358394` (`tprv`) |

There are no bech32 addresses. An address with a valid checksum for one network is not valid on another; `validateaddress` checks it.

## Blocks and time

| | Mainnet | Testnet | Regtest |
|---|---|---|---|
| Target block interval | 64 s | 64 s | 60 s |
| Difficulty | Adjusted after every block toward the interval, over a 16-minute window | Not adjusted | Not adjusted |
| Last height open to proof of work | 1,440 (the last mined block is 82) | 1,440,000 | 1,440,000 |
| Stake search | In 16-second steps of the block time | same | same |
| Block time ahead of the node's clock, at most | 10 minutes | 10 minutes | 10 minutes |
| Deepest reorganization accepted | 499 blocks (`maxreorg` is 500) | 499 blocks | 59 blocks (`maxreorg` is 60) |
| Largest block | 2,000,000 bytes (weight 8,000,000) | same | weight 8,000,000; 2,000,000 bytes without witness data |

On mainnet, blocks 1 to 72 were mined with proof of work. Block 73 is the first proof-of-stake block and block 82 the last mined one, 79 proof-of-work blocks in all; every block from 83 on is a proof-of-stake block. A block is refused when its size without witness data, times four, is above the weight limit, so without SegWit a block has at most 2,000,000 bytes. The difficulty rule moves the target after each block by `((N - 1) * T + 2 * actual) / ((N + 1) * T)`, where `T` is the interval, `N` is 15 (16 minutes over 64 seconds) and `actual` is the time between the two previous blocks of the same kind, at most `10 * T`.

## Maturity

| | Blocks |
|---|---|
| Outputs of a proof-of-work block (coinbase) can be spent after | 10 |
| Outputs of a stake (coinstake) can be spent after | 60 (10 for stakes before block 159,500 on mainnet) |
| A coin can be staked when it is at least | 60 blocks deep |

The wallet shows its own staked coins and rewards as immature until one block later than these limits.

## Reward

| Height | Reward per block |
|---|---|
| 0 (genesis) | 0 |
| 1 | 2,100,000,000 AOK |
| 2 to 525,959 | 4 AOK |
| 525,960 to 1,051,919 | 2 AOK |
| 1,051,920 to 1,577,879 | 1 AOK |
| 1,577,880 to 2,103,839 | 0.5 AOK |
| 2,103,840 to 2,629,799 | 0.25 AOK |
| 2,629,800 to 3,155,759 | 0.125 AOK |
| 3,155,760 to 3,681,719 | 0.0625 AOK |
| 3,681,720 to 4,207,679 | 0.03125 AOK |
| 4,207,680 to 4,733,639 | 0.015625 AOK |
| 4,733,640 to 5,259,599 | 0.0078125 AOK |
| 5,259,600 and later | 0 |

- The reward halves every 525,960 blocks; after the tenth halving there is none, and stakers earn the fees only.
- A block may claim at most the reward of its height plus the fees of its transactions. A stake claims it as the difference between what the coinstake pays out and what it takes in.
- If every block claims its full reward, the issuance ends at 2,104,203,562.9375 AOK. The [[explorer-api|AokChain API]] serves the supply at the tip (`/supply`).
- The same schedule applies on testnet and regtest.

1 AOK is 100,000,000 satoshis. No single amount may exceed 25,000,000,000 AOK; this bound is a range check, not the supply.

## Activation heights

| Rule | Mainnet | Testnet | Regtest |
|---|---|---|---|
| Tokens | 159,500 | 10 | 10 |
| Tokens at pay-to-script-hash addresses | 450,000 | 15 | 10 |
| IPFS data in tokens | 622,000 | 20 | not set |
| A transaction's time no longer has to be at least the time of its inputs | 695,000 | 0 | 0 |
| Governance, offline staking and transaction version 2 | 871,500 | never | 10 |

## Fixed points

| | Mainnet |
|---|---|
| Last checkpoint | 3,030,000 `27a0660bf43381e7d367472a74d696873ff69bb36582031f9c2ed2ae1c58bdf1` |
| `assumevalid` block (scripts below it are not checked during the first sync) | the same block |
| Chain state snapshot that the program accepts | 3,031,432 `58a07d1f4dbe68b7fa66d864272ca6351a60de13a409c132b034c9da03af909a` ([[fast-sync]]) |

Testnet and regtest have no checkpoints and no snapshot.

## Governance and token costs

| | Mainnet | Testnet | Regtest |
|---|---|---|---|
| Governance master address | `kp5eNwMzDfDgHXMG3XZw73c6rTA6WzFJEx` | none | `2NDM6PPx2FNYvgqvDdE8qnopCCD6kcGt14v` |
| Token fee address, as built in | `KdZFAFeKV8C5JzdEdgcPYDZku92KkD3fHy` | `TufvYmro3vSfDerUAjvjXMjYqUsFw6iWS7` | `n3XzBy9gndByXLeAgz5qG5xJkNNw31ULXy` |
| Built-in costs: root, reissue, sub, unique, username | 10,000, 10,000, 100, 100, 1 AOK | 1 AOK each | 10,000, 10,000, 100, 100, 1 AOK |

Governance can change the fee address and the costs, and has done so on mainnet. `issuanceinfo` returns the values in force; see [[token-names-and-costs]] and [[address-freezing]].
