---
title: "RPC: Not listed by help"
description: "RPC reference: commands for testing and debugging that help does not list."
order: 30
generated_by: tools/rpc_reference.py
---

`aokchain-cli help` does not list these commands. They are meant for testing and debugging; some of them change what the node considers valid until they are undone. This is the help text that AokChain Core 4.0.6 prints for each with `aokchain-cli help <command>`. All categories are on [[rpc]].

> [!NOTE]
> Many examples in these help texts come from the upstream code: their addresses are often
> Bitcoin addresses, and their `curl` lines use port 8766. An AokChain node answers JSON-RPC on
> port 33440 (mainnet) or 44550 (testnet and regtest) unless `rpcport` says otherwise; see [[json-rpc]].

| Command | Summary |
|---|---|
| [echo](#echo) | Simply echo back the input arguments. |
| [echojson](#echojson) | Simply echo back the input arguments. |
| [estimaterawfee](#estimaterawfee) | WARNING: This interface is unstable and may disappear or change! |
| [invalidateblock](#invalidateblock) | Permanently marks a block as invalid, as if it violated a consensus rule. |
| [logging](#logging) | Gets and sets the logging configuration. |
| [reconsiderblock](#reconsiderblock) | Removes invalidity status of a block and its descendants, reconsider them for activation. |
| [resendwallettransactions](#resendwallettransactions) | Immediately re-broadcast unconfirmed wallet transactions to all peers. |
| [setmocktime](#setmocktime) | Set the local time to given timestamp (-regtest only) |
| [waitforblock](#waitforblock) | Waits for a specific new block and returns useful info about it. |
| [waitforblockheight](#waitforblockheight) | Waits for (at least) block height and returns the height and hash of the current tip. |
| [waitfornewblock](#waitfornewblock) | Waits for a specific new block and returns useful info about it. |

### echo

```text
echo|echojson "message" ...
```

Simply echo back the input arguments. This command is for testing.

The difference between echo and echojson is that echojson has argument conversion enabled in the client-side table inaokchain-cli and the GUI. There is no server-side difference.

### echojson

```text
echo|echojson "message" ...
```

Simply echo back the input arguments. This command is for testing.

The difference between echo and echojson is that echojson has argument conversion enabled in the client-side table inaokchain-cli and the GUI. There is no server-side difference.

### estimaterawfee

```text
estimaterawfee conf_target (threshold)
```

WARNING: This interface is unstable and may disappear or change!

WARNING: This is an advanced API call that is tightly coupled to the specific

```text
         implementation of fee estimation. The parameters it can be called with
         and the results it returns will change if the internal implementation changes.
```

Estimates the approximate fee per kilobyte needed for a transaction to begin confirmation within conf\_target blocks if possible. Uses virtual transaction size as defined in BIP 141 (witness data is discounted).

**Arguments**

```text
1. conf_target (numeric) Confirmation target in blocks (1 - 1008)
2. threshold   (numeric, optional) The proportion of transactions in a given feerate range that must have been
               confirmed within conf_target in order to consider those feerates as high enough and proceed to check
               lower buckets.  Default: 0.95
```

**Result**

```text
{
  "short" : {            (json object, optional) estimate for short time horizon
      "feerate" : x.x,        (numeric, optional) estimate fee rate in AOK/kB
      "decay" : x.x,          (numeric) exponential decay (per block) for historical moving average of confirmation data
      "scale" : x,            (numeric) The resolution of confirmation targets at this time horizon
      "pass" : {              (json object, optional) information about the lowest range of feerates to succeed in meeting the threshold
          "startrange" : x.x,     (numeric) start of feerate range
          "endrange" : x.x,       (numeric) end of feerate range
          "withintarget" : x.x,   (numeric) number of txs over history horizon in the feerate range that were confirmed within target
          "totalconfirmed" : x.x, (numeric) number of txs over history horizon in the feerate range that were confirmed at any point
          "inmempool" : x.x,      (numeric) current number of txs in mempool in the feerate range unconfirmed for at least target blocks
          "leftmempool" : x.x,    (numeric) number of txs over history horizon in the feerate range that left mempool unconfirmed after target
      },
      "fail" : { ... },       (json object, optional) information about the highest range of feerates to fail to meet the threshold
      "errors":  [ str... ]   (json array of strings, optional) Errors encountered during processing
  },
  "medium" : { ... },    (json object, optional) estimate for medium time horizon
  "long" : { ... }       (json object) estimate for long time horizon
}

Results are returned for any horizon which tracks blocks up to the confirmation target.
```

**Example**

```text
> aokchain-cli estimaterawfee 6 0.9
```

### invalidateblock

```text
invalidateblock "blockhash"
```

Permanently marks a block as invalid, as if it violated a consensus rule.

**Arguments**

```text
1. "blockhash"   (string, required) the hash of the block to mark as invalid
```

**Result**

**Examples**

```text
> aokchain-cli invalidateblock "blockhash"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "invalidateblock", "params": ["blockhash"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### logging

```text
logging [include,...] <exclude>
```

Gets and sets the logging configuration. When called without an argument, returns the list of categories that are currently being debug logged. When called with arguments, adds or removes categories from debug logging. The valid logging categories are: net, tor, mempool, http, bench, zmq, db, rpc, estimatefee, addrman, selectcoins, reindex, cmpctblock, rand, prune, proxy, mempoolrej, libevent, coindb, qt, leveldb, coinstake libevent logging is configured on startup and cannot be modified by this RPC during runtime.Arguments:

```text
1. "include" (array of strings) add debug logging for these categories.
2. "exclude" (array of strings) remove debug logging for these categories.
```

Result: &lt;categories&gt;  (string): a list of the logging categories that are active.

**Examples**

```text
> aokchain-cli logging "[\"all\"]" "[\"http\"]"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "logging", "params": [["all"], "[libevent]"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### reconsiderblock

```text
reconsiderblock "blockhash"
```

Removes invalidity status of a block and its descendants, reconsider them for activation. This can be used to undo the effects of invalidateblock.

**Arguments**

```text
1. "blockhash"   (string, required) the hash of the block to reconsider
```

**Result**

**Examples**

```text
> aokchain-cli reconsiderblock "blockhash"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "reconsiderblock", "params": ["blockhash"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### resendwallettransactions

```text
resendwallettransactions
```

Immediately re-broadcast unconfirmed wallet transactions to all peers. Intended only for testing; the wallet code periodically re-broadcasts automatically. Returns an RPC error if -walletbroadcast is set to false. Returns array of transaction ids that were re-broadcast.

### setmocktime

```text
setmocktime timestamp
```

Set the local time to given timestamp (-regtest only)

**Arguments**

```text
1. timestamp  (integer, required) Unix seconds-since-epoch timestamp
   Pass 0 to go back to using the system time.
```

### waitforblock

```text
waitforblock <blockhash> (timeout)
```

Waits for a specific new block and returns useful info about it.

Returns the current block on timeout or exit.

**Arguments**

```text
1. "blockhash" (required, string) Block hash to wait for.
2. timeout       (int, optional, default=0) Time in milliseconds to wait for a response. 0 indicates no timeout.
```

**Result**

```text
{                           (json object)
  "hash" : {       (string) The blockhash
  "height" : {     (int) Block height
}
```

**Examples**

```text
> aokchain-cli waitforblock "0000000000079f8ef3d2c688c244eb7a4570b24c9ed7b4a8c619eb02596f8862", 1000
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "waitforblock", "params": ["0000000000079f8ef3d2c688c244eb7a4570b24c9ed7b4a8c619eb02596f8862", 1000] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### waitforblockheight

```text
waitforblockheight <height> (timeout)
```

Waits for (at least) block height and returns the height and hash of the current tip.

Returns the current block on timeout or exit.

**Arguments**

```text
1. height  (required, int) Block height to wait for (int)
2. timeout (int, optional, default=0) Time in milliseconds to wait for a response. 0 indicates no timeout.
```

**Result**

```text
{                           (json object)
  "hash" : {       (string) The blockhash
  "height" : {     (int) Block height
}
```

**Examples**

```text
> aokchain-cli waitforblockheight "100", 1000
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "waitforblockheight", "params": ["100", 1000] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### waitfornewblock

```text
waitfornewblock (timeout)
```

Waits for a specific new block and returns useful info about it.

Returns the current block on timeout or exit.

**Arguments**

```text
1. timeout (int, optional, default=0) Time in milliseconds to wait for a response. 0 indicates no timeout.
```

**Result**

```text
{                           (json object)
  "hash" : {       (string) The blockhash
  "height" : {     (int) Block height
}
```

**Examples**

```text
> aokchain-cli waitfornewblock 1000
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "waitfornewblock", "params": [1000] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```
