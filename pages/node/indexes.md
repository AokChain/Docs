---
title: Indexes
description: "The optional indexes of an AokChain node (transactions, tokens, addresses, spent outputs, timestamps), what needs them and how to turn them on."
order: 70
---

A node can keep indexes beyond what it needs to validate blocks. They answer questions such as "which transactions touched this address" without a wallet. This page lists them, the commands that need them, and how to change them.

## The indexes

| Option | Default | What it adds | Commands that need it |
|---|---|---|---|
| `txindex` | 1 | Every transaction of the chain by its id. | `getrawtransaction` for transactions with no unspent output left; `gettxoutproof` without a block hash. |
| `tokenindex` | 1 | Token balances by address. | `listaddressesbytoken`, `listtokenbalancesbyaddress`, `listuniquetokenholders`. |
| `addressindex` | 0 | Every output and input by address, and the address side of the mempool. | `getaddressbalance`, `getaddressdeltas`, `getaddresstxids`, `getaddressutxos`, `getaddressmempool`. |
| `spentindex` | 0 | For every spent output, the transaction and input that spent it. | `getspentinfo`. With it, `getrawtransaction` with verbose output also shows the address and value of each input and `spentTxId`, `spentIndex` and `spentHeight` of each spent output. |
| `timestampindex` | 0 | Block hashes by time. | `getblockhashes`. |

`tokenindex` is not listed by `aokchaind -help`, but the node reads it. `getindexinfo` lists the indexes that a node keeps; each one is written with every block, so a listed index is complete up to the tip:

```bash
aokchain-cli getindexinfo
```

The full help of the address index calls is on [[rpc-addressindex]], the others on [[rpc-blockchain]] and [[rpc-tokens]].

## Turn an index on or off

An index is built from the blocks, so a change needs a rebuild.

1. Set the option in `aokchain.conf`, for example:

   ```ini
   addressindex=1
   spentindex=1
   timestampindex=1
   ```

2. Start the node once with `-reindex`:

   ```bash
   aokchaind -daemon -reindex
   ```

   The node reads all blocks from its own block files again and validates them; that takes about as long as a first sync from the block archives. Do not set `reindex=1` in the file, or it rebuilds at every start.

If you change an index and start without `-reindex`, the node stops with a message such as `You need to rebuild the database using -reindex to change -txindex` and "Please restart with -reindex to recover." `-reindex-chainstate` does not help: it keeps the old index settings and gives the same message again. Nothing is changed by such a start; put the old setting back, or rebuild with `-reindex`.

> [!WARNING]
> Versions before 4.0.6 name `-reindex-chainstate` in the message for `addressindex`, `spentindex` and `timestampindex`, and a start with `-reindex-chainstate` and a changed index deletes the token database before it stops. The next start then reports `Corrupted block database detected`, and only `-reindex` repairs the node. With those versions, never combine `-reindex-chainstate` with a changed index.

## A new node with indexes

Set the indexes before the first start. A new data directory with any index other than the defaults does not start from the chain state snapshot, because the snapshot carries no indexes; it validates every block, from the block archives if it has them (see [[fast-sync]]):

```bash
aokchaind -daemon -bootstrapdir=$HOME/aok-mainnet-files -addressindex=1 -spentindex=1 -timestampindex=1
```

A node that started from the snapshot cannot rebuild with `-reindex` until it has fetched the past blocks (`fetchblocks`). To add indexes to such a node, fetch the past blocks first, or start again with an empty data directory.

## Address index calls

Since 4.0.4 the address index calls take one address as a string or several in an object:

```bash
aokchain-cli getaddressbalance "KacWDE2Fyqywwr6YDKt1FYthycv3Ee7dqv"
aokchain-cli getaddressbalance '{"addresses": ["KacWDE2Fyqywwr6YDKt1FYthycv3Ee7dqv", "Krp9Fwe7rEZm6Y6YxnngFc9to7y1Q4QX9W"]}'
```

`aokchain-cli` reads an argument as JSON only when it starts with `{` or `[`. An address given twice counts once, and a username (`@NAME`) can stand for its address. `getaddresstxids` and `getaddressdeltas` also take `start` and `end` heights in the object.

`getaddressutxos` returns the unspent outputs that are no longer time locked, in the order of block height, transaction id and output index. With `limit` it returns pages:

```bash
aokchain-cli getaddressutxos '{"addresses": ["KacWDE2Fyqywwr6YDKt1FYthycv3Ee7dqv"], "limit": 1000}'
```

The answer is then an object `{"utxos": [...], "next": "..."}`. Pass `next` back as `after` for the following page; `next` is `null` on the last page. `chainInfo: true` adds the hash and height of the tip, `tokenName` lists the outputs of a token instead of AOK (`"*"` for all tokens).

Amounts in these answers are in satoshis (1 AOK = 100,000,000).

> [!IMPORTANT]
> A node that kept an address index under 3.0.x or under 4.0 before 4.0.5 should rebuild it once with 4.0.5 or later (`-reindex`), so that every unspent output is in it.

## Pruning

`prune` deletes old block files to save space. It cannot be combined with `txindex`, which is on by default, so a pruned node needs `txindex=0`; it cannot rescan old wallet transactions or serve old blocks. Pruning was not tested with AokChain Core 4.0, nor with the other indexes; a node that serves others or keeps a wallet should keep all blocks.
