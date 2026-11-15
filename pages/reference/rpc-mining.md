---
title: "RPC: Mining"
description: "RPC reference: block templates, mining and staking information, and block submission."
order: 24
generated_by: tools/rpc_reference.py
---

The help text of every command in the mining category, as AokChain Core 4.0.6 prints it with `aokchain-cli help <command>`. All categories are on [[rpc]].

> [!NOTE]
> Many examples in these help texts come from the upstream code: their addresses are often
> Bitcoin addresses, and their `curl` lines use port 8766. An AokChain node answers JSON-RPC on
> port 33440 (mainnet) or 44550 (testnet and regtest) unless `rpcport` says otherwise; see [[json-rpc]].

| Command | Summary |
|---|---|
| [getblocktemplate](#getblocktemplate) | If the request parameters include a 'mode' key, that is used to explicitly select between the default 'template' request or a 'proposal'. |
| [getmininginfo](#getmininginfo) | Returns a json object containing mining-related information. |
| [getnetworkhashps](#getnetworkhashps) | Returns the estimated network hashes per second based on the last n blocks. |
| [getstakinginfo](#getstakinginfo) | Returns an object containing staking-related information. |
| [prioritisetransaction](#prioritisetransaction) | Accepts the transaction into mined blocks at a higher (or lower) priority |
| [setgenerate](#setgenerate) | Set 'generate' true or false to turn generation on or off. |
| [submitblock](#submitblock) | Attempts to submit new block to network. |

### getblocktemplate

```text
getblocktemplate ( TemplateRequest )
```

If the request parameters include a 'mode' key, that is used to explicitly select between the default 'template' request or a 'proposal'. It returns data needed to construct a block to work on. For full specification, see BIPs 22, 23, 9, and 145:

```text
    https://github.com/aokchain/bips/blob/master/bip-0022.mediawiki
    https://github.com/aokchain/bips/blob/master/bip-0023.mediawiki
    https://github.com/aokchain/bips/blob/master/bip-0009.mediawiki#getblocktemplate_changes
    https://github.com/aokchain/bips/blob/master/bip-0145.mediawiki
```

**Arguments**

```text
1. template_request         (json object, optional) A json object in the following spec
     {
       "mode":"template"    (string, optional) This must be set to "template", "proposal" (see BIP 23), or omitted
       "capabilities":[     (array, optional) A list of strings
           "support"          (string) client side supported feature, 'longpoll', 'coinbasetxn', 'coinbasevalue', 'proposal', 'serverlist', 'workid'
           ,...
       ],
       "rules":[            (array, optional) A list of strings
           "support"          (string) client side supported softfork deployment
           ,...
       ]
     }
```

**Result**

```text
{
  "version" : n,                    (numeric) The preferred block version
  "rules" : [ "rulename", ... ],    (array of strings) specific block rules that are to be enforced
  "vbavailable" : {                 (json object) set of pending, supported versionbit (BIP 9) softfork deployments
      "rulename" : bitnumber          (numeric) identifies the bit number as indicating acceptance and readiness for the named softfork rule
      ,...
  },
  "vbrequired" : n,                 (numeric) bit mask of versionbits the server requires set in submissions
  "previousblockhash" : "xxxx",     (string) The hash of current highest block
  "transactions" : [                (array) contents of non-coinbase transactions that should be included in the next block
      {
         "data" : "xxxx",             (string) transaction data encoded in hexadecimal (byte-for-byte)
         "txid" : "xxxx",             (string) transaction id encoded in little-endian hexadecimal
         "hash" : "xxxx",             (string) hash encoded in little-endian hexadecimal (including witness data)
         "depends" : [                (array) array of numbers
             n                          (numeric) transactions before this one (by 1-based index in 'transactions' list) that must be present in the final block if this one is
             ,...
         ],
         "fee": n,                    (numeric) difference in value between transaction inputs and outputs (in satoshis); for coinbase transactions, this is a negative Number of the total collected block fees (ie, not including the block subsidy); if key is not present, fee is unknown and clients MUST NOT assume there isn't one
         "sigops" : n,                (numeric) total SigOps cost, as counted for purposes of block limits; if key is not present, sigop cost is unknown and clients MUST NOT assume it is zero
         "weight" : n,                (numeric) total transaction weight, as counted for purposes of block limits
         "required" : true|false      (boolean) if provided and true, this transaction must be in the final block
      }
      ,...
  ],
  "coinbaseaux" : {                 (json object) data that should be included in the coinbase's scriptSig content
      "flags" : "xx"                  (string) key name is to be ignored, and value included in scriptSig
  },
  "coinbasevalue" : n,              (numeric) maximum allowable input to coinbase transaction, including the generation award and transaction fees (in satoshis)
  "coinbasetxn" : { ... },          (json object) information for coinbase transaction
  "target" : "xxxx",                (string) The hash target
  "mintime" : xxx,                  (numeric) The minimum timestamp appropriate for next block time in seconds since epoch (Jan 1 1970 GMT)
  "mutable" : [                     (array of string) list of ways the block template may be changed
     "value"                          (string) A way the block template may be changed, e.g. 'time', 'transactions', 'prevblock'
     ,...
  ],
  "noncerange" : "00000000ffffffff",(string) A range of valid nonces
  "sigoplimit" : n,                 (numeric) limit of sigops in blocks
  "sizelimit" : n,                  (numeric) limit of block size
  "weightlimit" : n,                (numeric) limit of block weight
  "curtime" : ttt,                  (numeric) current timestamp in seconds since epoch (Jan 1 1970 GMT)
  "bits" : "xxxxxxxx",              (string) compressed target of next block
  "height" : n                      (numeric) The height of the next block
}
```

**Examples**

```text
> aokchain-cli getblocktemplate
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getblocktemplate", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getmininginfo

```text
getmininginfo
```

Returns a json object containing mining-related information.

**Result**

```text
{
  "blocks": nnn,             (numeric) The current block
  "currentblockweight": nnn, (numeric) The last block weight
  "currentblocktx": nnn,     (numeric) The last block transaction
  "difficulty": xxx.xxxxx    (numeric) The current difficulty
  "networkhashps": nnn,      (numeric) The network hashes per second
  "hashespersec": nnn,       (numeric) The hashes per second of built-in miner
  "pooledtx": n              (numeric) The size of the mempool
  "chain": "xxxx",           (string) current network name as defined in BIP70 (main, test, regtest)
  "warnings": "..."          (string) any network and blockchain warnings
  "errors": "..."            (string) DEPRECATED. Same as warnings. Only shown when aokchaind is started with -deprecatedrpc=getmininginfo
}
```

**Examples**

```text
> aokchain-cli getmininginfo
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getmininginfo", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getnetworkhashps

```text
getnetworkhashps ( nblocks height )
```

Returns the estimated network hashes per second based on the last n blocks. Pass in \[blocks\] to override # of blocks, -1 specifies since last difficulty change. Pass in \[height\] to estimate the network speed at the time when a certain block was found.

**Arguments**

```text
1. nblocks     (numeric, optional, default=120) The number of blocks, or -1 for blocks since last difficulty change.
2. height      (numeric, optional, default=-1) To estimate at the time of the given height.
```

**Result**

```text
x             (numeric) Hashes per second estimated
```

**Examples**

```text
> aokchain-cli getnetworkhashps
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getnetworkhashps", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getstakinginfo

```text
getstakinginfo
```

Returns an object containing staking-related information.

**Result (the fields about the wallet are there when a wallet is loaded)**

```text
{
  "enabled": true|false,     (boolean) staking is switched on (-staking)
  "staking": true|false,     (boolean) the wallet is looking for stakes now
  "weight": n,               (numeric) the coins of the wallet that can stake, in satoshis
  "netstakeweight": n,       (numeric) estimate of the coins that stake in the network, in satoshis
  "expectedtime": n,         (numeric) expected seconds between two stakes of this wallet
  "stakes_24h": n,           (numeric) stakes of this wallet in the chain in the last 24 hours
  "orphaned_24h": n,         (numeric) stakes of the last 24 hours that lost against another block; they earn nothing
  "reward_24h": x.xxx,       (numeric) what the stakes of the last 24 hours brought, in AOK
  ...
}
```

### prioritisetransaction

```text
prioritisetransaction <txid> <dummy value> <fee delta>
```

Accepts the transaction into mined blocks at a higher (or lower) priority

**Arguments**

```text
1. "txid"       (string, required) The transaction id.
2. dummy          (numeric, optional) API-Compatibility for previous API. Must be zero or null.
                  DEPRECATED. For forward compatibility use named arguments and omit this parameter.
3. fee_delta      (numeric, required) The fee value (in satoshis) to add (or subtract, if negative).
                  The fee is not actually paid, only the algorithm for selecting transactions into a block
                  considers the transaction as it would have paid a higher (or lower) fee.
```

**Result**

```text
true              (boolean) Returns true
```

**Examples**

```text
> aokchain-cli prioritisetransaction "txid" 0.0 10000
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "prioritisetransaction", "params": ["txid", 0.0, 10000] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### setgenerate

```text
setgenerate generate ( genproclimit )
```

Set 'generate' true or false to turn generation on or off. Generation is limited to 'genproclimit' processors, -1 is unlimited. See the getgenerate call for the current setting.

**Arguments**

```text
1. generate         (boolean, required) Set to true to turn on generation, false to turn off.
2. genproclimit     (numeric, optional) Set the processor limit for when generation is on. Can be -1 for unlimited.
```

**Examples**

```text
Set the generation on with a limit of one processor
> aokchain-cli setgenerate true 1

Check the setting
> aokchain-cli getgenerate

Turn off generation
> aokchain-cli setgenerate false

Using json rpc
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "setgenerate", "params": [true, 1] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### submitblock

```text
submitblock "hexdata"  ( "dummy" )
```

Attempts to submit new block to network. See https://en.aokchain.it/wiki/BIP\_0022 for full specification.

**Arguments**

```text
1. "hexdata"        (string, required) the hex-encoded block data to submit
2. "dummy"          (optional) dummy value, for compatibility with BIP22. This value is ignored.
```

**Result**

**Examples**

```text
> aokchain-cli submitblock "mydata"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "submitblock", "params": ["mydata"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```
