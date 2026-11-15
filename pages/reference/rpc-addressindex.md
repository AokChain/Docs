---
title: "RPC: Address index"
description: "RPC reference: balances, transactions and unspent outputs of addresses, read from the address index."
order: 20
generated_by: tools/rpc_reference.py
---

The help text of every command in the address index category, as AokChain Core 4.0.6 prints it with `aokchain-cli help <command>`. All categories are on [[rpc]].

> [!NOTE]
> Many examples in these help texts come from the upstream code: their addresses are often
> Bitcoin addresses, and their `curl` lines use port 8766. An AokChain node answers JSON-RPC on
> port 33440 (mainnet) or 44550 (testnet and regtest) unless `rpcport` says otherwise; see [[json-rpc]].

| Command | Summary |
|---|---|
| [getaddressbalance](#getaddressbalance) | Returns the balance for an address(es) (requires addressindex to be enabled). |
| [getaddressdeltas](#getaddressdeltas) | Returns all changes for an address (requires addressindex to be enabled). |
| [getaddresses](#getaddresses) | Print a list of all addresses in the blockchain. |
| [getaddressmempool](#getaddressmempool) | Returns all mempool deltas for an address (requires addressindex to be enabled). |
| [getaddresstxids](#getaddresstxids) | Returns the txids for an address(es) (requires addressindex to be enabled). |
| [getaddressutxos](#getaddressutxos) | Returns the unspent outputs of addresses that are not time locked any more (requires addressindex to be enabled), in the order of their block ... |
| [gettokentransactions](#gettokentransactions) | Print a list of all token transactions. |

### getaddressbalance

```text
getaddressbalance
```

Returns the balance for an address(es) (requires addressindex to be enabled).

**Arguments**

```text
"address"  (string) An address or a username, or the object:
{
  "addresses:"
    [
      "address"  (string) The base58check encoded address
      ,...
    ]
},
"includeTokens" (boolean, optional, default false)  If true this will return an expanded result which includes token balances
```

**Result**

```text
{
  "balance"  (string) The current balance in satoshis
  "received"  (string) The total number of satoshis received (including change)
}
OR
[
  {
    "tokenName"  (string) The token associated with the balance (AOK for AokChain)
    "balance"  (string) The current balance in satoshis
    "received"  (string) The total number of satoshis received (including change)
  },...

]
```

**Examples**

```text
> aokchain-cli getaddressbalance '{"addresses": ["12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX"]}'
> aokchain-cli getaddressbalance '{"addresses": ["12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX"]}', true
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getaddressbalance", "params": [{"addresses": ["12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX"]}] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getaddressbalance", "params": [{"addresses": ["12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX"]}, true] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getaddressdeltas

```text
getaddressdeltas
```

Returns all changes for an address (requires addressindex to be enabled).

**Arguments**

```text
"address"  (string) An address or a username, or the object:
{
  "addresses"
    [
      "address"  (string) The base58check encoded address
      ,...
    ]
  "start" (number) The start block height
  "end" (number) The end block height
  "chainInfo" (boolean) Include chain info in results, only applies if start and end specified
  "tokenName"   (string, optional) Get deltas for a particular token instead of AOK.
}
```

**Result**

```text
[
  {
    "tokenName"  (string) The token associated with the deltas (AOK for AokChain)
    "satoshis"  (number) The difference of satoshis
    "txid"  (string) The related txid
    "index"  (number) The related input or output index
    "height"  (number) The block height
    "address"  (string) The base58check encoded address
  }
]
```

**Examples**

```text
> aokchain-cli getaddressdeltas '{"addresses": ["12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX"]}'
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getaddressdeltas", "params": [{"addresses": ["12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX"]}] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
> aokchain-cli getaddressdeltas '{"addresses": ["12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX"],"tokenName":"MY_TOKEN"}'
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getaddressdeltas", "params": [{"addresses": ["12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX"],"tokenName":"MY_TOKEN"}] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getaddresses

```text
getaddresses "excludeZeroBalances"
```

Print a list of all addresses in the blockchain.

**Arguments**

```text
1. "excludeZeroBalances"  (bool, optional, default: true) If true, addresses with zero balance aren't included in the list. If false, they are.
```

**Examples**

```text
> aokchain-cli getaddresses true
```

### getaddressmempool

```text
getaddressmempool
```

Returns all mempool deltas for an address (requires addressindex to be enabled).

**Arguments**

```text
"address"  (string) An address or a username, or the object:
{
  "addresses"
    [
      "address"  (string) The base58check encoded address
      ,...
    ]
},
"includeTokens" (boolean, optional, default false)  If true this will return an expanded result which includes token deltas
```

**Result**

```text
[
  {
    "address"  (string) The base58check encoded address
    "tokenName"  (string) The name of the associated token (AOK for AokChain)
    "txid"  (string) The related txid
    "index"  (number) The related input or output index
    "satoshis"  (number) The difference of satoshis
    "timestamp"  (number) The time the transaction entered the mempool (seconds)
    "prevtxid"  (string) The previous txid (if spending)
    "prevout"  (string) The previous transaction output index (if spending)
  }
]
```

**Examples**

```text
> aokchain-cli getaddressmempool '{"addresses": ["12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX"]}'
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getaddressmempool", "params": [{"addresses": ["12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX"]}] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
> aokchain-cli getaddressmempool '{"addresses": ["12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX"]}', true
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getaddressmempool", "params": [{"addresses": ["12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX"]}, true] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getaddresstxids

```text
getaddresstxids
```

Returns the txids for an address(es) (requires addressindex to be enabled).

**Arguments**

```text
"address"  (string) An address or a username, or the object:
{
  "addresses"
    [
      "address"  (string) The base58check encoded address
      ,...
    ]
  "start" (number, optional) The start block height
  "end" (number, optional) The end block height
},
"includeTokens" (boolean, optional, default false)  If true this will return an expanded result which includes token transactions
```

**Result**

```text
[
  "transactionid"  (string) The transaction id
  ,...
]
```

**Examples**

```text
> aokchain-cli getaddresstxids '{"addresses": ["12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX"]}'
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getaddresstxids", "params": [{"addresses": ["12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX"]}] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
> aokchain-cli getaddresstxids '{"addresses": ["12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX"]}', true
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getaddresstxids", "params": [{"addresses": ["12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX"]}, true] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getaddressutxos

```text
getaddressutxos "address" ( amount "tokenName" )
getaddressutxos {"addresses": ["address",...], ...}
```

Returns the unspent outputs of addresses that are not time locked any more (requires addressindex to be enabled), in the order of their block height, then of their transaction id and output index.

**Arguments**

```text
1. "address"        (string) An address or a username
   or an object:
{
  "addresses": ["address",...]  (array) The addresses (or usernames)
  "tokenName": "name"   (string, optional) Outputs of this token instead of AOK ('*' for all tokens)
  "amount": n           (numeric, optional) Stop once the listed outputs add up to this amount
  "chainInfo": true|false  (boolean, optional, default false) Return an object with the hash and height of the tip as well
  "limit": n            (numeric, optional) At most n outputs: the result is an object, its "next" leads to the next page
  "after": "next"       (string, optional) Continue after this output: the "next" of the previous page
                         ("height:txid:index"), or "txid:index" of an output that is still unspent
}
2. amount           (numeric, optional) As "amount" above, after an address
3. "tokenName"      (string, optional) As "tokenName" above, after an address
```

**Result**

```text
[
  {
    "address"  (string) The address base58check encoded
    "token_name" (string) The token associated with the UTXOs (AOK for AokChain)
    "txid"  (string) The output txid
    "outputIndex"  (number) The output index
    "script"  (string) The script hex encoded
    "asm"  (string) The script
    "satoshis"  (number) The number of satoshis of the output
    "height"  (number) The block height
    "timelock"  (number) The lock time of the output (0 when it was not locked)
  }
]
With "limit" or "chainInfo":
{
  "utxos": [...]     (array) The outputs as above
  "next": "next"      (string or null) With "limit": where the next page starts, null on the last page
  "hash": "hash"      (string) With "chainInfo": the hash of the tip
  "height": n        (number) With "chainInfo": the height of the tip
}
```

**Examples**

```text
> aokchain-cli getaddressutxos "12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX"
> aokchain-cli getaddressutxos '{"addresses": ["12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX"]}'
> aokchain-cli getaddressutxos '{"addresses": ["12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX"], "limit": 1000}'
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getaddressutxos", "params": [{"addresses": ["12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX"], "limit": 1000, "after": "<next of the last page>"}] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getaddressutxos", "params": [{"addresses": ["12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX"],"tokenName":"MY_TOKEN"}] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### gettokentransactions

```text
gettokentransactions "token"
```

Print a list of all token transactions.

**Arguments**

```text
1. "token"  (str, required) Token name.
```

**Examples**

```text
> aokchain-cli gettokentransactions TOKEN
```
