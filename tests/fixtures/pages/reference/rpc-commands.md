---
title: RPC commands
description: Every JSON-RPC command of the node, grouped as in the help output.
order: 1
generated_by: tools/rpc_reference.py
---

Commands from `aokchain-cli help`, grouped as the node groups them.

## Blockchain

### getblockchaininfo

Returns the state of the chain: network, height, headers and sync progress.

```text
getblockchaininfo
```

### getblock

Returns a block by its hash. With `verbosity` 0 the block is hex, with 1 it is JSON.

```text
getblock "blockhash" ( verbosity )
```

| Argument | Type | Description |
|---|---|---|
| `blockhash` | string | The block hash |
| `verbosity` | number | 0 hex, 1 JSON, 2 JSON with transactions |

### getblockhash

Returns the hash of the block at a height.

```text
getblockhash height
```

## Raw transactions

### createrawtransaction

Creates a transaction from inputs and outputs without signing it.

```text
createrawtransaction [{"txid":"id","vout":n},...] {"address":amount,...}
```

### signrawtransaction

Signs the inputs of a raw transaction that the wallet holds keys for.

```text
signrawtransaction "hexstring"
```

### sendrawtransaction

Sends a signed transaction to the network.

```text
sendrawtransaction "hexstring"
```

## Wallet

### getnewaddress

Returns a new receiving address.

```text
getnewaddress ( "label" )
```

### getbalance

Returns the available balance.

```text
getbalance
```

### walletpassphrase

Unlocks the wallet for a number of seconds.

```text
walletpassphrase "passphrase" timeout
```
