---
title: "RPC: Blockchain"
description: "RPC reference: blocks, the chain state, the mempool, governance, the snapshot and the block archives."
order: 21
generated_by: tools/rpc_reference.py
---

The help text of every command in the blockchain category, as AokChain Core 4.0.7 prints it with `aokchain-cli help <command>`. All categories are on [[rpc]].

> [!NOTE]
> Many examples in these help texts come from the upstream code: their addresses are often
> Bitcoin addresses, and their `curl` lines use port 8766. An AokChain node answers JSON-RPC on
> port 33440 (mainnet) or 44550 (testnet and regtest) unless `rpcport` says otherwise; see [[json-rpc]].

| Command | Summary |
|---|---|
| [checkfreeze](#checkfreeze) | Returns freze status for address. |
| [fetchblocks](#fetchblocks) | Download the past blocks of a node that started from a chain state snapshot, in the background. |
| [freezelist](#freezelist) | Returns list of frozen addresses. |
| [getbestblockhash](#getbestblockhash) | Returns the hash of the best (tip) block in the longest blockchain. |
| [getblock](#getblock) | If verbosity is 0, returns a string that is serialized, hex-encoded data for block 'hash'. |
| [getblockchaininfo](#getblockchaininfo) | Returns an object containing various state info regarding blockchain processing. |
| [getblockcount](#getblockcount) | Returns the number of blocks in the longest blockchain. |
| [getblockhash](#getblockhash) | Returns hash of block in best-block-chain at height provided. |
| [getblockhashes](#getblockhashes) | Returns array of hashes of blocks within the timestamp range provided. |
| [getblockheader](#getblockheader) | If verbose is false, returns a string that is serialized, hex-encoded data for blockheader 'hash'. |
| [getblockstats](#getblockstats) | Computes statistics of one block of the active chain. |
| [getbootstrapinfo](#getbootstrapinfo) | State of the block bootstrap (-bootstrapurl): block archives that are fetched over HTTP and imported. |
| [getchaintips](#getchaintips) | Return information about all known tips in the block tree, including the main chain as well as orphaned branches. |
| [getchaintxstats](#getchaintxstats) | Compute statistics about the total number and rate of transactions in the chain. |
| [getdifficulty](#getdifficulty) | Returns the proof-of-work difficulty as a multiple of the minimum difficulty. |
| [getindexinfo](#getindexinfo) | Returns the indexes that this node keeps. |
| [getmempoolancestors](#getmempoolancestors) | If txid is in the mempool, returns all in-mempool ancestors. |
| [getmempooldescendants](#getmempooldescendants) | If txid is in the mempool, returns all in-mempool descendants. |
| [getmempoolentry](#getmempoolentry) | Returns mempool data for given transaction |
| [getmempoolinfo](#getmempoolinfo) | Returns details on the active state of the TX memory pool. |
| [getrawmempool](#getrawmempool) | Returns all transaction ids in memory pool as a json array of string transaction ids. |
| [getsnapshotinfo](#getsnapshotinfo) | The chain state snapshot that this program accepts, whether this node started from one, and the state of the past blocks (the blocks up to the ... |
| [getspentinfo](#getspentinfo) | Returns the txid and index where an output is spent. |
| [getstatehashes](#getstatehashes) | Compute the hashes that identify the chain state of this node at its tip: the values that a program must have compiled in to accept a chain state ... |
| [gettxout](#gettxout) | Returns details about an unspent transaction output. |
| [gettxoutproof](#gettxoutproof) | Returns a hex-encoded proof that "txid" was included in a block. |
| [gettxoutsetinfo](#gettxoutsetinfo) | Returns statistics about the unspent transaction output set. |
| [issuanceinfo](#issuanceinfo) | Returns issuance cost for tokens. |
| [preciousblock](#preciousblock) | Treats a block as if it were received before others with the same work. |
| [pruneblockchain](#pruneblockchain) |  |
| [repaircoins](#repaircoins) | Look for unspent outputs that have no transaction time in the chain state of this node, and give them the time and the coinstake mark of their ... |
| [savemempool](#savemempool) | Dumps the mempool to disk. |
| [scantxoutset](#scantxoutset) | Scans the unspent transaction outputs of the chain for outputs that pay to the given addresses or scripts. |
| [skipbootstrap](#skipbootstrap) | Give the block bootstrap up and get the blocks from the peers. |
| [verifychain](#verifychain) | Verifies blockchain database. |
| [verifytxoutproof](#verifytxoutproof) | Verifies that a proof points to a transaction in a block, returning the transaction it commits to and throwing an RPC error if the block is not in ... |

### checkfreeze

```text
checkfreeze "address"
```

Returns freze status for address.

### fetchblocks

```text
fetchblocks
```

Download the past blocks of a node that started from a chain state snapshot, in the background. The blocks come from the block archives (-bootstrapurl, -bootstrapdir or the built-in address); every block is checked against the block index and stored. Nothing is validated again. getsnapshotinfo shows the progress. Wallets that wait for these blocks are scanned at the end.

**Result**

```text
true|false    (boolean) true: the download was started; false: the past blocks are there
```

**Examples**

```text
> aokchain-cli fetchblocks
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "fetchblocks", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### freezelist

```text
freezelist
```

Returns list of frozen addresses.

### getbestblockhash

```text
getbestblockhash
```

Returns the hash of the best (tip) block in the longest blockchain.

**Result**

```text
"hex"      (string) the block hash hex encoded
```

**Examples**

```text
> aokchain-cli getbestblockhash
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getbestblockhash", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getblock

```text
getblock "blockhash" ( verbosity )
```

If verbosity is 0, returns a string that is serialized, hex-encoded data for block 'hash'. If verbosity is 1, returns an Object with information about block &lt;hash&gt;. If verbosity is 2, returns an Object with information about block &lt;hash&gt; and information about each transaction.

**Arguments**

```text
1. "blockhash"          (string, required) The block hash
2. verbosity              (numeric, optional, default=1) 0 for hex encoded data, 1 for a json object, and 2 for json object with transaction data
```

**Result (for verbosity = 0)**

```text
"data"             (string) A string that is serialized, hex-encoded data for block 'hash'.
```

**Result (for verbosity = 1)**

```text
{
  "hash" : "hash",     (string) the block hash (same as provided)
  "confirmations" : n,   (numeric) The number of confirmations, or -1 if the block is not on the main chain
  "size" : n,            (numeric) The block size
  "strippedsize" : n,    (numeric) The block size excluding witness data
  "weight" : n           (numeric) The block weight as defined in BIP 141
  "height" : n,          (numeric) The block height or index
  "version" : n,         (numeric) The block version
  "versionHex" : "00000000", (string) The block version formatted in hexadecimal
  "merkleroot" : "xxxx", (string) The merkle root
  "tx" : [               (array of string) The transaction ids
     "transactionid"     (string) The transaction id
     ,...
  ],
  "time" : ttt,          (numeric) The block time in seconds since epoch (Jan 1 1970 GMT)
  "mediantime" : ttt,    (numeric) The median block time in seconds since epoch (Jan 1 1970 GMT)
  "nonce" : n,           (numeric) The nonce
  "bits" : "1d00ffff", (string) The bits
  "difficulty" : x.xxx,  (numeric) The difficulty
  "chainwork" : "xxxx",  (string) Expected number of hashes required to produce the chain up to this block (in hex)
  "previousblockhash" : "hash",  (string) The hash of the previous block
  "nextblockhash" : "hash"       (string) The hash of the next block
}
```

**Result (for verbosity = 2)**

```text
{
  ...,                     Same output as verbosity = 1.
  "tx" : [               (array of Objects) The transactions in the format of the getrawtransaction RPC. Different from verbosity = 1 "tx" result.
         ,...
  ],
  ,...                     Same output as verbosity = 1.
}
```

**Examples**

```text
> aokchain-cli getblock "00000000c937983704a73af28acdec37b049d214adbda81d7e2a3dd146f6ed09"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getblock", "params": ["00000000c937983704a73af28acdec37b049d214adbda81d7e2a3dd146f6ed09"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getblockchaininfo

```text
getblockchaininfo
```

Returns an object containing various state info regarding blockchain processing.

**Result**

```text
{
  "chain": "xxxx",        (string) current network name as defined in BIP70 (main, test, regtest)
  "blocks": xxxxxx,         (numeric) the current number of blocks processed in the server
  "headers": xxxxxx,        (numeric) the current number of headers we have validated
  "bestblockhash": "...", (string) the hash of the currently best block
  "difficulty": xxxxxx,     (numeric) the current difficulty
  "mediantime": xxxxxx,     (numeric) median time for the current best block
  "verificationprogress": xxxx, (numeric) estimate of verification progress [0..1]
  "chainwork": "xxxx"     (string) total amount of work in active chain, in hexadecimal
  "size_on_disk": xxxxxx,   (numeric) the estimated size of the block and undo files on disk
  "pruned": xx,             (boolean) if the blocks are subject to pruning
  "pruneheight": xxxxxx,    (numeric) lowest-height complete block stored (only present if pruning is enabled)
  "automatic_pruning": xx,  (boolean) whether automatic pruning is enabled (only present if pruning is enabled)
  "prune_target_size": xxxxxx,  (numeric) the target size used by pruning (only present if automatic pruning is enabled)
  "softforks": [            (array) status of softforks in progress
     {
        "id": "xxxx",        (string) name of softfork
        "version": xx,         (numeric) block version
        "reject": {            (object) progress toward rejecting pre-softfork blocks
           "status": xx,       (boolean) true if threshold reached
        },
     }, ...
  ],
  "bip9_softforks": {          (object) status of BIP9 softforks in progress
     "xxxx" : {                (string) name of the softfork
        "status": "xxxx",    (string) one of "defined", "started", "locked_in", "active", "failed"
        "bit": xx,             (numeric) the bit (0-28) in the block version field used to signal this softfork (only for "started" status)
        "startTime": xx,       (numeric) the minimum median time past of a block at which the bit gains its meaning
        "timeout": xx,         (numeric) the median time past of a block at which the deployment is considered failed if not yet locked in
        "since": xx,           (numeric) height of the first block to which the status applies
        "statistics": {        (object) numeric statistics about BIP9 signalling for a softfork (only for "started" status)
           "period": xx,       (numeric) the length in blocks of the BIP9 signalling period
           "threshold": xx,    (numeric) the number of blocks with the version bit set required to activate the feature
           "elapsed": xx,      (numeric) the number of blocks elapsed since the beginning of the current period
           "count": xx,        (numeric) the number of blocks with the version bit set in the current period
           "possible": xx      (boolean) returns false if there are not enough blocks left in this period to pass activation threshold
        }
     }
  }
  "warnings" : "...",         (string) any network and blockchain warnings.
}
```

**Examples**

```text
> aokchain-cli getblockchaininfo
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockchaininfo", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getblockcount

```text
getblockcount
```

Returns the number of blocks in the longest blockchain.

**Result**

```text
n    (numeric) The current block count
```

**Examples**

```text
> aokchain-cli getblockcount
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockcount", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getblockhash

```text
getblockhash height
```

Returns hash of block in best-block-chain at height provided.

**Arguments**

```text
1. height         (numeric, required) The height index
```

**Result**

```text
"hash"         (string) The block hash
```

**Examples**

```text
> aokchain-cli getblockhash 1000
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockhash", "params": [1000] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getblockhashes

```text
getblockhashes timestamp
```

Returns array of hashes of blocks within the timestamp range provided.

**Arguments**

```text
1. high         (numeric, required) The newer block timestamp
2. low          (numeric, required) The older block timestamp
3. options      (string, required) A json object
    {
      "noOrphans":true   (boolean) will only include blocks on the main chain
      "logicalTimes":true   (boolean) will include logical timestamps with hashes
    }
```

**Result**

```text
[
  "hash"         (string) The block hash
]
[
  {
    "blockhash": (string) The block hash
    "logicalts": (numeric) The logical timestamp
  }
]
```

**Examples**

```text
> aokchain-cli getblockhashes 1231614698 1231024505
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockhashes", "params": [1231614698, 1231024505] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
> aokchain-cli getblockhashes 1231614698 1231024505 '{"noOrphans":false, "logicalTimes":true}'
```

### getblockheader

```text
getblockheader "hash" ( verbose )
```

If verbose is false, returns a string that is serialized, hex-encoded data for blockheader 'hash'. If verbose is true, returns an Object with information about blockheader &lt;hash&gt;.

**Arguments**

```text
1. "hash"          (string, required) The block hash
2. verbose           (boolean, optional, default=true) true for a json object, false for the hex encoded data
```

**Result (for verbose = true)**

```text
{
  "hash" : "hash",     (string) the block hash (same as provided)
  "confirmations" : n,   (numeric) The number of confirmations, or -1 if the block is not on the main chain
  "height" : n,          (numeric) The block height or index
  "version" : n,         (numeric) The block version
  "versionHex" : "00000000", (string) The block version formatted in hexadecimal
  "merkleroot" : "xxxx", (string) The merkle root
  "time" : ttt,          (numeric) The block time in seconds since epoch (Jan 1 1970 GMT)
  "mediantime" : ttt,    (numeric) The median block time in seconds since epoch (Jan 1 1970 GMT)
  "nonce" : n,           (numeric) The nonce
  "bits" : "1d00ffff", (string) The bits
  "difficulty" : x.xxx,  (numeric) The difficulty
  "chainwork" : "0000...1f3"     (string) Expected number of hashes required to produce the current chain (in hex)
  "previousblockhash" : "hash",  (string) The hash of the previous block
  "nextblockhash" : "hash",      (string) The hash of the next block
}
```

**Result (for verbose=false)**

```text
"data"             (string) A string that is serialized, hex-encoded data for block 'hash'.
```

**Examples**

```text
> aokchain-cli getblockheader "00000000c937983704a73af28acdec37b049d214adbda81d7e2a3dd146f6ed09"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockheader", "params": ["00000000c937983704a73af28acdec37b049d214adbda81d7e2a3dd146f6ed09"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getblockstats

```text
getblockstats hash_or_height ( stats )
```

Computes statistics of one block of the active chain. Amounts are in satoshis. The coinbase and the stake transaction count as transactions, inputs and outputs, and not for the fees.

**Arguments**

```text
1. hash_or_height   (string or numeric, required) The block hash or the height of the block
2. stats            (array, optional) The values to return (all of them by default)
```

**Result**

```text
{
  "avgfee": n, "avgfeerate": n (satoshis per byte), "avgtxsize": n,
  "blockhash": "hex", "height": n, "time": n, "mediantime": n,
  "ins": n, "outs": n, "txs": n, "utxo_increase": n,
  "maxfee": n, "maxfeerate": n, "maxtxsize": n, "minfee": n, "minfeerate": n, "mintxsize": n,
  "total_out": n, "total_size": n, "totalfee": n,
  "proof_of_stake": true|false,
  "stake_reward": n     (numeric) outputs minus inputs of the stake transaction (the reward with the fees)
}
```

**Examples**

```text
> aokchain-cli getblockstats 1000 '["txs","totalfee"]'
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockstats", "params": [1000, ["txs","totalfee"]] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getbootstrapinfo

```text
getbootstrapinfo
```

State of the block bootstrap (-bootstrapurl): block archives that are fetched over HTTP and imported.

**Result**

```text
{
  "configured": true|false,   (boolean) -bootstrapurl is set and -bootstrap is not 0
  "url": "...",             (string) where the archives come from
  "state": "...",           (string) off, starting, manifest, running, done, notneeded, failed or skipped
  "active": true|false,       (boolean) blocks are not requested from peers meanwhile
  "chunks": n,                (numeric) archives that this node needs
  "chunks_downloaded": n,     (numeric)
  "chunks_imported": n,       (numeric)
  "bytes_total": n,           (numeric) bytes to download
  "bytes_downloaded": n,      (numeric)
  "start_height": n,          (numeric) height when the bootstrap began
  "target_height": n,         (numeric) last height of the archives
  "height": n,                (numeric) current height
  "seconds_download": n,      (numeric) time spent downloading
  "seconds_import": n,        (numeric) time spent decompressing and validating
  "seconds_total": n,         (numeric)
  "message": "..."          (string) what it is doing, or why it failed
}
```

**Examples**

```text
> aokchain-cli getbootstrapinfo
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getbootstrapinfo", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getchaintips

```text
getchaintips
```

Return information about all known tips in the block tree, including the main chain as well as orphaned branches.

**Result**

```text
[
  {
    "height": xxxx,         (numeric) height of the chain tip
    "hash": "xxxx",         (string) block hash of the tip
    "branchlen": 0          (numeric) zero for main chain
    "status": "active"      (string) "active" for the main chain
  },
  {
    "height": xxxx,
    "hash": "xxxx",
    "branchlen": 1          (numeric) length of branch connecting the tip to the main chain
    "status": "xxxx"        (string) status of the chain (active, valid-fork, valid-headers, headers-only, invalid)
  }
]
Possible values for status:
1.  "invalid"               This branch contains at least one invalid block
2.  "headers-only"          Not all blocks for this branch are available, but the headers are valid
3.  "valid-headers"         All blocks are available for this branch, but they were never fully validated
4.  "valid-fork"            This branch is not part of the active chain, but is fully validated
5.  "active"                This is the tip of the active main chain, which is certainly valid
```

**Examples**

```text
> aokchain-cli getchaintips
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getchaintips", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getchaintxstats

```text
getchaintxstats ( nblocks blockhash )
```

Compute statistics about the total number and rate of transactions in the chain.

**Arguments**

```text
1. nblocks      (numeric, optional) Size of the window in number of blocks (default: one month).
2. "blockhash"  (string, optional) The hash of the block that ends the window.
```

**Result**

```text
{
  "time": xxxxx,                (numeric) The timestamp for the final block in the window in UNIX format.
  "txcount": xxxxx,             (numeric) The total number of transactions in the chain up to that point.
  "window_block_count": xxxxx,  (numeric) Size of the window in number of blocks.
  "window_tx_count": xxxxx,     (numeric) The number of transactions in the window. Only returned if "window_block_count" is > 0.
  "window_interval": xxxxx,     (numeric) The elapsed time in the window in seconds. Only returned if "window_block_count" is > 0.
  "txrate": x.xx,               (numeric) The average rate of transactions per second in the window. Only returned if "window_interval" is > 0.
}
```

**Examples**

```text
> aokchain-cli getchaintxstats
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getchaintxstats", "params": [2016] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getdifficulty

```text
getdifficulty
```

Returns the proof-of-work difficulty as a multiple of the minimum difficulty.

**Result**

```text
n.nnn       (numeric) the proof-of-work difficulty as a multiple of the minimum difficulty.
```

**Examples**

```text
> aokchain-cli getdifficulty
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getdifficulty", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getindexinfo

```text
getindexinfo ( "index_name" )
```

Returns the indexes that this node keeps. They are written with every block, so an index that is listed is complete up to the tip.

**Arguments**

```text
1. "index_name"   (string, optional) Only this index: txindex, tokenindex, addressindex, spentindex, timestampindex
```

**Result**

```text
{
  "name": {
    "synced": true,
    "best_block_height": n
  }, ...
}
```

**Examples**

```text
> aokchain-cli getindexinfo
> aokchain-cli getindexinfo txindex
```

### getmempoolancestors

```text
getmempoolancestors txid (verbose)
```

If txid is in the mempool, returns all in-mempool ancestors.

**Arguments**

```text
1. "txid"                 (string, required) The transaction id (must be in mempool)
2. verbose                  (boolean, optional, default=false) True for a json object, false for array of transaction ids
```

**Result (for verbose=false)**

```text
[                       (json array of strings)
  "transactionid"           (string) The transaction id of an in-mempool ancestor transaction
  ,...
]
```

**Result (for verbose=true)**

```text
{                           (json object)
  "transactionid" : {       (json object)
    "size" : n,             (numeric) virtual transaction size as defined in BIP 141. This is different from actual serialized size for witness transactions as witness data is discounted.
    "fee" : n,              (numeric) transaction fee in AOK
    "modifiedfee" : n,      (numeric) transaction fee with fee deltas used for mining priority
    "time" : n,             (numeric) local time transaction entered pool in seconds since 1 Jan 1970 GMT
    "height" : n,           (numeric) block height when transaction entered pool
    "descendantcount" : n,  (numeric) number of in-mempool descendant transactions (including this one)
    "descendantsize" : n,   (numeric) virtual transaction size of in-mempool descendants (including this one)
    "descendantfees" : n,   (numeric) modified fees (see above) of in-mempool descendants (including this one)
    "ancestorcount" : n,    (numeric) number of in-mempool ancestor transactions (including this one)
    "ancestorsize" : n,     (numeric) virtual transaction size of in-mempool ancestors (including this one)
    "ancestorfees" : n,     (numeric) modified fees (see above) of in-mempool ancestors (including this one)
    "wtxid" : hash,         (string) hash of serialized transaction, including witness data
    "depends" : [           (array) unconfirmed transactions used as inputs for this transaction
        "transactionid",    (string) parent transaction id
       ... ]
  }, ...
}
```

**Examples**

```text
> aokchain-cli getmempoolancestors "mytxid"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getmempoolancestors", "params": ["mytxid"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getmempooldescendants

```text
getmempooldescendants txid (verbose)
```

If txid is in the mempool, returns all in-mempool descendants.

**Arguments**

```text
1. "txid"                 (string, required) The transaction id (must be in mempool)
2. verbose                  (boolean, optional, default=false) True for a json object, false for array of transaction ids
```

**Result (for verbose=false)**

```text
[                       (json array of strings)
  "transactionid"           (string) The transaction id of an in-mempool descendant transaction
  ,...
]
```

**Result (for verbose=true)**

```text
{                           (json object)
  "transactionid" : {       (json object)
    "size" : n,             (numeric) virtual transaction size as defined in BIP 141. This is different from actual serialized size for witness transactions as witness data is discounted.
    "fee" : n,              (numeric) transaction fee in AOK
    "modifiedfee" : n,      (numeric) transaction fee with fee deltas used for mining priority
    "time" : n,             (numeric) local time transaction entered pool in seconds since 1 Jan 1970 GMT
    "height" : n,           (numeric) block height when transaction entered pool
    "descendantcount" : n,  (numeric) number of in-mempool descendant transactions (including this one)
    "descendantsize" : n,   (numeric) virtual transaction size of in-mempool descendants (including this one)
    "descendantfees" : n,   (numeric) modified fees (see above) of in-mempool descendants (including this one)
    "ancestorcount" : n,    (numeric) number of in-mempool ancestor transactions (including this one)
    "ancestorsize" : n,     (numeric) virtual transaction size of in-mempool ancestors (including this one)
    "ancestorfees" : n,     (numeric) modified fees (see above) of in-mempool ancestors (including this one)
    "wtxid" : hash,         (string) hash of serialized transaction, including witness data
    "depends" : [           (array) unconfirmed transactions used as inputs for this transaction
        "transactionid",    (string) parent transaction id
       ... ]
  }, ...
}
```

**Examples**

```text
> aokchain-cli getmempooldescendants "mytxid"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getmempooldescendants", "params": ["mytxid"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getmempoolentry

```text
getmempoolentry txid
```

Returns mempool data for given transaction

**Arguments**

```text
1. "txid"                   (string, required) The transaction id (must be in mempool)
```

**Result**

```text
{                           (json object)
    "size" : n,             (numeric) virtual transaction size as defined in BIP 141. This is different from actual serialized size for witness transactions as witness data is discounted.
    "fee" : n,              (numeric) transaction fee in AOK
    "modifiedfee" : n,      (numeric) transaction fee with fee deltas used for mining priority
    "time" : n,             (numeric) local time transaction entered pool in seconds since 1 Jan 1970 GMT
    "height" : n,           (numeric) block height when transaction entered pool
    "descendantcount" : n,  (numeric) number of in-mempool descendant transactions (including this one)
    "descendantsize" : n,   (numeric) virtual transaction size of in-mempool descendants (including this one)
    "descendantfees" : n,   (numeric) modified fees (see above) of in-mempool descendants (including this one)
    "ancestorcount" : n,    (numeric) number of in-mempool ancestor transactions (including this one)
    "ancestorsize" : n,     (numeric) virtual transaction size of in-mempool ancestors (including this one)
    "ancestorfees" : n,     (numeric) modified fees (see above) of in-mempool ancestors (including this one)
    "wtxid" : hash,         (string) hash of serialized transaction, including witness data
    "depends" : [           (array) unconfirmed transactions used as inputs for this transaction
        "transactionid",    (string) parent transaction id
       ... ]
}
```

**Examples**

```text
> aokchain-cli getmempoolentry "mytxid"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getmempoolentry", "params": ["mytxid"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getmempoolinfo

```text
getmempoolinfo
```

Returns details on the active state of the TX memory pool.

**Result**

```text
{
  "size": xxxxx,               (numeric) Current tx count
  "bytes": xxxxx,              (numeric) Sum of all virtual transaction sizes as defined in BIP 141. Differs from actual serialized size because witness data is discounted
  "usage": xxxxx,              (numeric) Total memory usage for the mempool
  "maxmempool": xxxxx,         (numeric) Maximum memory usage for the mempool
  "mempoolminfee": xxxxx       (numeric) Minimum fee rate in AOK/kB for tx to be accepted
}
```

**Examples**

```text
> aokchain-cli getmempoolinfo
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getmempoolinfo", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getrawmempool

```text
getrawmempool ( verbose )
```

Returns all transaction ids in memory pool as a json array of string transaction ids.

Hint: use getmempoolentry to fetch a specific transaction from the mempool.

**Arguments**

```text
1. verbose (boolean, optional, default=false) True for a json object, false for array of transaction ids

Result: (for verbose = false):
[                     (json array of string)
  "transactionid"     (string) The transaction id
  ,...
]

Result: (for verbose = true):
{                           (json object)
  "transactionid" : {       (json object)
    "size" : n,             (numeric) virtual transaction size as defined in BIP 141. This is different from actual serialized size for witness transactions as witness data is discounted.
    "fee" : n,              (numeric) transaction fee in AOK
    "modifiedfee" : n,      (numeric) transaction fee with fee deltas used for mining priority
    "time" : n,             (numeric) local time transaction entered pool in seconds since 1 Jan 1970 GMT
    "height" : n,           (numeric) block height when transaction entered pool
    "descendantcount" : n,  (numeric) number of in-mempool descendant transactions (including this one)
    "descendantsize" : n,   (numeric) virtual transaction size of in-mempool descendants (including this one)
    "descendantfees" : n,   (numeric) modified fees (see above) of in-mempool descendants (including this one)
    "ancestorcount" : n,    (numeric) number of in-mempool ancestor transactions (including this one)
    "ancestorsize" : n,     (numeric) virtual transaction size of in-mempool ancestors (including this one)
    "ancestorfees" : n,     (numeric) modified fees (see above) of in-mempool ancestors (including this one)
    "wtxid" : hash,         (string) hash of serialized transaction, including witness data
    "depends" : [           (array) unconfirmed transactions used as inputs for this transaction
        "transactionid",    (string) parent transaction id
       ... ]
  }, ...
}
```

**Examples**

```text
> aokchain-cli getrawmempool true
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getrawmempool", "params": [true] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getsnapshotinfo

```text
getsnapshotinfo
```

The chain state snapshot that this program accepts, whether this node started from one, and the state of the past blocks (the blocks up to the snapshot height, which such a node does not have until they are downloaded with fetchblocks).

**Result**

```text
{
  "accepted_height": n,       (numeric) height of the snapshot that this program accepts, 0: none
  "accepted_block": "hash",  (string) the block at that height
  "snapshot_height": n,       (numeric) height of the snapshot that this node started from, -1: it did not
  "past_blocks": "...",      (string) "present", "missing" or "downloading"
  "bytes_total": n,           (numeric) size of the block archives of the download
  "bytes_done": n,            (numeric) bytes of them that are downloaded and stored
  "blocks_stored": n,         (numeric) blocks stored by the download
  "wallet_waits": true|false, (boolean) a wallet has not been scanned for transactions in the past blocks
  "error": "..."            (string) why the last download stopped
}
```

**Examples**

```text
> aokchain-cli getsnapshotinfo
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getsnapshotinfo", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getspentinfo

```text
getspentinfo
```

Returns the txid and index where an output is spent.

**Arguments**

```text
{
  "txid" (string) The hex string of the txid
  "index" (number) The start block height
}
```

**Result**

```text
{
  "txid"  (string) The transaction id
  "index"  (number) The spending input index
  ,...
}
```

**Examples**

```text
> aokchain-cli getspentinfo '{"txid": "0437cd7f8525ceed2324359c2d0ba26006d92d856a9c20fa0241106ee5a597c9", "index": 0}'
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getspentinfo", "params": [{"txid": "0437cd7f8525ceed2324359c2d0ba26006d92d856a9c20fa0241106ee5a597c9", "index": 0}] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getstatehashes

```text
getstatehashes
```

Compute the hashes that identify the chain state of this node at its tip: the values that a program must have compiled in to accept a chain state snapshot of that height. Reads every unspent output and every token and governance record; this takes a while.

**Result**

```text
{
  "height": n,              (numeric) height of the tip
  "block": "hash",         (string) hash of the tip
  "utxo": "hash",          (string) hash over every unspent output with all the fields that the chainstate stores
  "utxo_legacy": "hash",   (string) hash_serialized_2 of gettxoutsetinfo, for comparison with other versions
  "tokens": "hash",        (string) hash over the token database (without the undo records of blocks)
  "governance": "hash",    (string) hash over the governance database
  "index": "hash",         (string) hash over the block index of the active chain
  "coins": n,               (numeric) number of unspent outputs
  "snapshotparams": "..."  (string) height:block:utxo:tokens:governance:index
}
```

**Examples**

```text
> aokchain-cli getstatehashes
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getstatehashes", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### gettxout

```text
gettxout "txid" n ( include_mempool )
```

Returns details about an unspent transaction output.

**Arguments**

```text
1. "txid"             (string, required) The transaction id
2. "n"                (numeric, required) vout number
3. "include_mempool"  (boolean, optional) Whether to include the mempool. Default: true.     Note that an unspent output that is spent in the mempool won't appear.
```

**Result**

```text
{
  "bestblock" : "hash",    (string) the block hash
  "confirmations" : n,       (numeric) The number of confirmations
  "value" : x.xxx,           (numeric) The transaction value in AOK
  "scriptPubKey" : {         (json object)
     "asm" : "code",       (string)
     "hex" : "hex",        (string)
     "reqSigs" : n,          (numeric) Number of required signatures
     "type" : "pubkeyhash", (string) The type, eg pubkeyhash
     "addresses" : [          (array of string) array of aokchain addresses
        "address"     (string) aokchain address
        ,...
     ]
  },
  "coinbase" : true|false   (boolean) Coinbase or not
}
```

**Examples**

```text
Get unspent transactions
> aokchain-cli listunspent

View the details
> aokchain-cli gettxout "txid" 1

As a json rpc call
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "gettxout", "params": ["txid", 1] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### gettxoutproof

```text
gettxoutproof ["txid",...] ( blockhash )
```

Returns a hex-encoded proof that "txid" was included in a block.

NOTE: By default this function only works sometimes. This is when there is an unspent output in the utxo for this transaction. To make it always work, you need to maintain a transaction index, using the -txindex command line option or specify the block in which the transaction is included manually (by blockhash).

**Arguments**

```text
1. "txids"       (string) A json array of txids to filter
    [
      "txid"     (string) A transaction hash
      ,...
    ]
2. "blockhash"   (string, optional) If specified, looks for txid in the block with this hash
```

**Result**

```text
"data"           (string) A string that is a serialized, hex-encoded data for the proof.
```

### gettxoutsetinfo

```text
gettxoutsetinfo
```

Returns statistics about the unspent transaction output set. Note this call may take some time.

**Result**

```text
{
  "height":n,     (numeric) The current block height (index)
  "bestblock": "hex",   (string) the best block hash hex
  "transactions": n,      (numeric) The number of transactions
  "txouts": n,            (numeric) The number of output transactions
  "bogosize": n,          (numeric) A meaningless metric for UTXO set size
  "hash_serialized_2": "hash", (string) The serialized hash
  "disk_size": n,         (numeric) The estimated size of the chainstate on disk
  "total_amount": x.xxx          (numeric) The total amount
}
```

**Examples**

```text
> aokchain-cli gettxoutsetinfo
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "gettxoutsetinfo", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### issuanceinfo

```text
issuanceinfo
```

Returns issuance cost for tokens.

### preciousblock

```text
preciousblock "blockhash"
```

Treats a block as if it were received before others with the same work.

A later preciousblock call can override the effect of an earlier one.

The effects of preciousblock are not retained across restarts.

**Arguments**

```text
1. "blockhash"   (string, required) the hash of the block to mark as precious
```

**Result**

**Examples**

```text
> aokchain-cli preciousblock "blockhash"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "preciousblock", "params": ["blockhash"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### pruneblockchain

```text
pruneblockchain
```

**Arguments**

```text
1. "height"       (numeric, required) The block height to prune up to. May be set to a discrete height, or a unix timestamp
                  to prune blocks whose block time is at least 2 hours older than the provided timestamp.
```

**Result**

```text
n    (numeric) Height of the last block pruned.
```

**Examples**

```text
> aokchain-cli pruneblockchain 1000
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "pruneblockchain", "params": [1000] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### repaircoins

```text
repaircoins ( checkonly )
```

Look for unspent outputs that have no transaction time in the chain state of this node, and give them the time and the coinstake mark of their transaction again. Versions before 4.0 lost both when a block was disconnected in a reorganization. A wallet then staked such a coin with a wrong kernel: its blocks were rejected by every node (bad-cs-proofhash) and the coin never staked again. Reads every unspent output; this takes a while.

**Arguments**

```text
1. checkonly    (boolean, optional, default=false) only count, change nothing
```

**Result**

```text
{
  "scanned": n,      (numeric) unspent outputs read
  "damaged": n,      (numeric) unspent outputs without a time
  "repaired": n,     (numeric) of those, the ones that were repaired (with checkonly: that can be repaired)
  "unreadable": n    (numeric) of those, the ones whose transaction cannot be read on this node
}
```

**Examples**

```text
> aokchain-cli repaircoins true
> aokchain-cli repaircoins
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "repaircoins", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### savemempool

```text
savemempool
```

Dumps the mempool to disk.

**Examples**

```text
> aokchain-cli savemempool
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "savemempool", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### scantxoutset

```text
scantxoutset "start" [scanobjects,...]
```

Scans the unspent transaction outputs of the chain for outputs that pay to the given addresses or scripts. Nothing is added to a wallet, and no rescan and no past blocks are needed: this is the balance of an address as the chain has it now.

**Arguments**

```text
1. "action"       (string, required) "start" (the scan runs in this call)
2. "scanobjects"  (array, required) What to look for. Each item is a string or {"desc": "string"}:
      "address" or "addr(address)"   outputs that pay to the address (also to its public key, as stakes do), with or without token data
      "raw(hex script)"              outputs with exactly this script
      "staking(address)"             offline staking outputs whose staking key is this address: what
                                       was delegated to a staker; "staking(*)" finds all of them
```

**Result**

```text
{
  "success": true,
  "txouts": n,             (numeric) unspent outputs read
  "height": n,             (numeric) height of the chain at the scan
  "bestblock": "hex",
  "unspents": [
    {
      "txid": "hex",
      "vout": n,
      "scriptPubKey": "hex",
      "address": "xxx",    (string) the scan object that it matched
      "amount": x.xxx,      (numeric) in AOK
      "height": n,          (numeric) height of the block of the output
      "coinstake": true,    (boolean) only for outputs of a stake
      "token": true         (boolean) only for outputs that carry a token; listtokenbalancesbyaddress has the amounts
    }, ...
  ],
  "total_amount": x.xxx    (numeric) sum of the amounts, in AOK
}
```

**Examples**

```text
> aokchain-cli scantxoutset start '["address"]'
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "scantxoutset", "params": ["start", ["address"]] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### skipbootstrap

```text
skipbootstrap
```

Give the block bootstrap up and get the blocks from the peers.

**Result**

```text
true|false    (boolean) whether a bootstrap was running
```

**Examples**

```text
> aokchain-cli skipbootstrap
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "skipbootstrap", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### verifychain

```text
verifychain ( checklevel nblocks )
```

Verifies blockchain database.

**Arguments**

```text
1. checklevel   (numeric, optional, 0-4, default=4) How thorough the block verification is.
2. nblocks      (numeric, optional, default=30, 0=all) The number of blocks to check.
```

**Result**

```text
true|false       (boolean) Verified or not
```

**Examples**

```text
> aokchain-cli verifychain
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "verifychain", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### verifytxoutproof

```text
verifytxoutproof "proof"
```

Verifies that a proof points to a transaction in a block, returning the transaction it commits to and throwing an RPC error if the block is not in our best chain

**Arguments**

```text
1. "proof"    (string, required) The hex-encoded proof generated by gettxoutproof
```

**Result**

```text
["txid"]      (array, strings) The txid(s) which the proof commits to, or empty array if the proof is invalid
```
