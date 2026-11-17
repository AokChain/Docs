---
title: "RPC: Raw transactions"
description: "RPC reference: creating, signing, checking and sending transactions by hand."
order: 26
generated_by: tools/rpc_reference.py
---

The help text of every command in the raw transactions category, as AokChain Core 4.0.9 prints it with `aokchain-cli help <command>`. All categories are on [[rpc]].

> [!NOTE]
> The addresses in the examples of these help texts are example addresses that belong to nobody.
> Their `curl` lines use port 33440, where a node of the main network answers JSON-RPC; on testnet
> and regtest it is port 44550, and `rpcport` sets another one. See [[json-rpc]].

| Command | Summary |
|---|---|
| [combinerawtransaction](#combinerawtransaction) | Combine multiple partially signed transactions into one transaction. |
| [createrawtransaction](#createrawtransaction) | Create a transaction spending the given inputs and creating new outputs. |
| [decoderawtransaction](#decoderawtransaction) | Return a JSON object representing the serialized, hex-encoded transaction. |
| [decodescript](#decodescript) | Decode a hex-encoded script. |
| [fundrawtransaction](#fundrawtransaction) | Add inputs to a transaction until it has enough in value to meet its out value. |
| [getrawtransaction](#getrawtransaction) | NOTE: By default this function only works for mempool transactions. |
| [sendrawtransaction](#sendrawtransaction) | Submits raw transaction (serialized, hex-encoded) to local node and network. |
| [signrawtransaction](#signrawtransaction) | Sign inputs for raw transaction (serialized, hex-encoded). |
| [signrawtransactionwithkey](#signrawtransactionwithkey) | Signs the inputs of a raw transaction (serialized, hex-encoded) with the given private keys only; no wallet is used. |
| [signrawtransactionwithwallet](#signrawtransactionwithwallet) | Signs the inputs of a raw transaction (serialized, hex-encoded) with the keys of the wallet. |
| [testmempoolaccept](#testmempoolaccept) | Returns whether a raw transaction (serialized, hex-encoded) would be accepted by the mempool. |

### combinerawtransaction

```text
combinerawtransaction ["hexstring",...]
```

Combine multiple partially signed transactions into one transaction. The combined transaction may be another partially signed transaction or a fully signed transaction.

**Arguments**

```text
1. "txs"         (string) A json array of hex strings of partially signed transactions
    [
      "hexstring"     (string) A transaction hash
      ,...
    ]
```

**Result**

```text
"hex"            (string) The hex-encoded raw transaction with signature(s)
```

**Examples**

```text
> aokchain-cli combinerawtransaction ["myhex1", "myhex2", "myhex3"]
```

### createrawtransaction

```text
createrawtransaction [{"txid":"id","vout":n},...] {"address":(amount or object),"data":"hex",...} ( locktime )
```

Create a transaction spending the given inputs and creating new outputs. Outputs are addresses (paired with an AOK amount, data or object specifying a token operation) or data. Returns hex-encoded raw transaction. Note that the transaction's inputs are not signed, and it is not stored in the wallet or transmitted to the network.

Paying for Token Operations:

```text
  issue, issue_unique and reissue pay a fee in AOK, in an output to the token fee address.
  The fees and the address are set by governance: issuanceinfo shows them. A transfer pays
  no such fee.
```

Ownership:

```text
  These operations require an ownership token input for the token being operated upon:
    issue_unique
    reissue
```

Output Ordering:

```text
  Token operations require the following:
    1) All coin outputs come first (including the fee output).
    2) The owner token change output comes next (if required).
    3) An issue, issue_unique, reissue or any number of transfers comes last
       (different types can't be mixed in a single transaction).
```

**Arguments**

```text
1. "inputs"                                (array, required) A json array of json objects
     [
       {
         "txid":"id",                      (string, required) The transaction id
         "vout":n,                         (numeric, required) The output number
         "sequence":n                      (numeric, optional) The sequence number
       }
       ,...
     ]
2. "outputs"                               (object, required) a json object with outputs
     {
       "address":                          (string, required) The destination aokchain address.  Each output must have a different address.
         x.xxx                             (numeric or string, required) The AOK amount
           or
         {                                 (object) A json object of tokens to send
           "transfer":
             {
               "token-name":               (string, required) token name
               token-quantity              (numeric, required) the quantity of the token to transfer
               ,...
             }
         }
           or
         {                                 (object) A json object describing new tokens to issue
           "issue":
             {
               "token_name":"token-name",  (string, required) new token name
               "token_quantity":n,         (number, required) the quantity to issue
               "units":[0-8],              (number, required) display units, between 0 (whole units) and 8 (max precision)
               "reissuable":[0-1],         (number, required) 1=reissuable token
               "has_ipfs":[0-1],           (number, required) 1=passing ipfs_hash
               "ipfs_hash":"hash"          (string, optional) an ipfs hash for discovering token metadata
             }
         }
           or
         {                                 (object) A json object describing new unique tokens to issue
           "issue_unique":
             {
               "root_name":"root-name",         (string, required) name of the token the unique token(s) are being issued under
               "token_tags":["token_tag", ...], (array, required) the unique tag for each token which is to be issued
               "ipfs_hashes":["hash", ...],     (array, optional) ipfs hashes corresponding to each supplied tag (should be same size as "token_tags")
             }
         }
           or
         {                                 (object) A json object describing follow-on token issue.  Requires matching ownership input.
           "reissue":
             {
               "token_name":"token-name",  (string, required) name of token to be reissued
               "token_quantity":n,         (number, required) the quantity to add
               "reissuable":[0-1],         (number, optional) default is 1, 1=reissuable token
               "ipfs_hash":"hash"          (string, optional) a new ipfs hash for the token
             }
         }
         or
       "data": "hex"                       (string, required) The key is "data", the value is hex encoded data
       ,...
     }
3. locktime                  (numeric, optional, default=0) Raw locktime. Non-0 value also locktime-activates inputs
```

**Result**

```text
"transaction"              (string) hex string of the transaction
```

**Examples**

```text
> aokchain-cli createrawtransaction "[{\"txid\":\"mycoin\",\"vout\":0}]" "{\"address\":0.01}"
> aokchain-cli createrawtransaction "[{\"txid\":\"mycoin\",\"vout\":0}]" "{\"data\":\"00010203\"}"
> aokchain-cli createrawtransaction "[{\"txid\":\"mycoin\",\"vout\":0}]" "{\"KaokChainExampLeAddressFirstxCXj28\":10000,\"change_address\":change_amount,\"issuer_address\":{\"issue\":{\"token_name\":\"MYTOKEN\",\"token_quantity\":1000000,\"units\":1,\"reissuable\":0,\"has_ipfs\":0}}}"
> aokchain-cli createrawtransaction "[{\"txid\":\"mycoin\",\"vout\":0},{\"txid\":\"myownership\",\"vout\":0}]" "{\"KaokChainExampLeAddressFirstxCXj28\":200,\"change_address\":change_amount,\"issuer_address\":{\"issue_unique\":{\"root_name\":\"MYTOKEN\",\"token_tags\":[\"ALPHA\",\"BETA\"]}}}"
> aokchain-cli createrawtransaction "[{\"txid\":\"mycoin\",\"vout\":0},{\"txid\":\"mytoken\",\"vout\":0}]" "{\"address\":{\"transfer\":{\"MYTOKEN\":50}}}"
> aokchain-cli createrawtransaction "[{\"txid\":\"mycoin\",\"vout\":0},{\"txid\":\"myownership\",\"vout\":0}]" "{\"KaokChainExampLeAddressFirstxCXj28\":10000,\"change_address\":change_amount,\"issuer_address\":{\"reissue\":{\"token_name\":\"MYTOKEN\",\"token_quantity\":2000000}}}"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "createrawtransaction", "params": ["[{\"txid\":\"mycoin\",\"vout\":0}]", "{\"data\":\"00010203\"}"] }' -H 'content-type: text/plain;' http://127.0.0.1:33440/
```

### decoderawtransaction

```text
decoderawtransaction "hexstring"
```

Return a JSON object representing the serialized, hex-encoded transaction.

**Arguments**

```text
1. "hexstring"      (string, required) The transaction hex string
```

**Result**

```text
{
  "txid" : "id",        (string) The transaction id
  "hash" : "id",        (string) The transaction hash (differs from txid for witness transactions)
  "size" : n,             (numeric) The transaction size
  "vsize" : n,            (numeric) The virtual transaction size (differs from size for witness transactions)
  "version" : n,          (numeric) The version
  "locktime" : ttt,       (numeric) The lock time
  "vin" : [               (array of json objects)
     {
       "txid": "id",    (string) The transaction id
       "vout": n,         (numeric) The output number
       "scriptSig": {     (json object) The script
         "asm": "asm",  (string) asm
         "hex": "hex"   (string) hex
       },
       "txinwitness": ["hex", ...] (array of string) hex-encoded witness data (if any)
       "sequence": n     (numeric) The script sequence number
     }
     ,...
  ],
  "vout" : [             (array of json objects)
     {
       "value" : x.xxx,            (numeric) The value in AOK
       "n" : n,                    (numeric) index
       "scriptPubKey" : {          (json object)
         "asm" : "asm",          (string) the asm
         "hex" : "hex",          (string) the hex
         "reqSigs" : n,            (numeric) The required sigs
         "type" : "pubkeyhash",  (string) The type, eg 'pubkeyhash'
         "addresses" : [           (json array of string)
           "KaokChainExampLeAddressFirstxCXj28"   (string) aokchain address
           ,...
         ]
       }
     }
     ,...
  ],
}
```

**Examples**

```text
> aokchain-cli decoderawtransaction "hexstring"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "decoderawtransaction", "params": ["hexstring"] }' -H 'content-type: text/plain;' http://127.0.0.1:33440/
```

### decodescript

```text
decodescript "hexstring"
```

Decode a hex-encoded script.

**Arguments**

```text
1. "hexstring"     (string) the hex encoded script
```

**Result**

```text
{
  "asm":"asm",   (string) Script public key
  "hex":"hex",   (string) hex encoded public key
  "type":"type", (string) The output type
  "reqSigs": n,    (numeric) The required signatures
  "addresses": [   (json array of string)
     "address"     (string) aokchain address
     ,...
  ],
  "p2sh":"address",       (string) address of P2SH script wrapping this redeem script (not returned if the script is already a P2SH).
  "(The following only appears if the script is a token script)
  "token_name":"name",      (string) Name of the token.
  "amount":"x.xx",          (numeric) The amount of tokens interacted with.
  "units": n,                (numeric) The units of the token. (Only appears in the type (new_token))
  "reissuable": true|false, (boolean) If this token is reissuable. (Only appears in type (new_token|reissue_token))
  "hasIPFS": true|false,    (boolean) If this token has an IPFS hash. (Only appears in type (new_token if hasIPFS is true))
  "ipfs_hash": "hash",      (string) The ipfs hash for the new token. (Only appears in type (new_token))
  "new_ipfs_hash":"hash",    (string) If new ipfs hash (Only appears in type. (reissue_token))
}
```

**Examples**

```text
> aokchain-cli decodescript "hexstring"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "decodescript", "params": ["hexstring"] }' -H 'content-type: text/plain;' http://127.0.0.1:33440/
```

### fundrawtransaction

```text
fundrawtransaction "hexstring" ( options )
```

Add inputs to a transaction until it has enough in value to meet its out value. This will not modify existing inputs, and will add at most one change output to the outputs. No existing outputs will be modified unless "subtractFeeFromOutputs" is specified. Note that inputs which were signed may need to be resigned after completion since in/outputs have been added. The inputs added will not be signed, use signrawtransaction for that. Note that all existing inputs must have their previous output transaction be in the wallet. Note that all inputs selected must be of standard form and P2SH scripts must be in the wallet using importaddress or addmultisigaddress (to calculate fees). You can see whether this is the case by checking the "solvable" field in the listunspent output. Only pay-to-pubkey, multisig, and P2SH versions thereof are currently supported for watch-only

**Arguments**

```text
1. "hexstring"           (string, required) The hex string of the raw transaction
2. options                 (object, optional)
   {
     "changeAddress"          (string, optional, default pool address) The aokchain address to receive the change
     "changePosition"         (numeric, optional, default random) The index of the change output
     "includeWatching"        (boolean, optional, default false) Also select inputs which are watch only
     "lockUnspents"           (boolean, optional, default false) Lock selected unspent outputs
     "feeRate"                (numeric, optional, default not set: makes wallet determine the fee) Set a specific fee rate in AOK/kB
     "subtractFeeFromOutputs" (array, optional) A json array of integers.
                              The fee will be equally deducted from the amount of each specified output.
                              The outputs are specified by their zero-based index, before any change output is added.
                              Those recipients will receive less AOK than you enter in their corresponding amount field.
                              If no outputs are specified here, the sender pays the fee.
                                  [vout_index,...]
                              Allows this transaction to be replaced by a transaction with higher fees
     "conf_target"            (numeric, optional) Confirmation target (in blocks)
     "estimate_mode"          (string, optional, default=UNSET) The fee estimate mode, must be one of:
         "UNSET"
         "ECONOMICAL"
         "CONSERVATIVE"
   }
                         for backward compatibility: passing in a true instead of an object will result in {"includeWatching":true}
```

**Result**

```text
{
  "hex":       "value", (string)  The resulting raw transaction (hex-encoded string)
  "fee":       n,         (numeric) Fee in AOK the resulting transaction pays
  "changepos": n          (numeric) The position of the added change output, or -1
}
```

**Examples**

```text
Create a transaction with no inputs
> aokchain-cli createrawtransaction "[]" "{\"myaddress\":0.01}"

Add sufficient unsigned inputs to meet the output value
> aokchain-cli fundrawtransaction "rawtransactionhex"

Sign the transaction
> aokchain-cli signrawtransaction "fundedtransactionhex"

Send the transaction
> aokchain-cli sendrawtransaction "signedtransactionhex"
```

### getrawtransaction

```text
getrawtransaction "txid" ( verbose )
```

NOTE: By default this function only works for mempool transactions. If the -txindex option is enabled, it also works for blockchain transactions. DEPRECATED: for now, it also works for transactions with unspent outputs.

Return the raw transaction data.

If verbose is 'true', returns an Object with information about 'txid'. If verbose is 'false' or omitted, returns a string that is serialized, hex-encoded data for 'txid'.

**Arguments**

```text
1. "txid"      (string, required) The transaction id
2. verbose       (bool, optional, default=false) If false, return a string, otherwise return a json object
```

**Result (if verbose is not set or set to false)**

```text
"data"      (string) The serialized, hex-encoded data for 'txid'
```

**Result (if verbose is set to true)**

```text
{
  "hex" : "data",       (string) The serialized, hex-encoded data for 'txid'
  "txid" : "id",        (string) The transaction id (same as provided)
  "hash" : "id",        (string) The transaction hash (differs from txid for witness transactions)
  "size" : n,             (numeric) The serialized transaction size
  "vsize" : n,            (numeric) The virtual transaction size (differs from size for witness transactions)
  "version" : n,          (numeric) The version
  "locktime" : ttt,       (numeric) The lock time
  "vin" : [               (array of json objects)
     {
       "txid": "id",    (string) The transaction id
       "vout": n,         (numeric)
       "scriptSig": {     (json object) The script
         "asm": "asm",  (string) asm
         "hex": "hex"   (string) hex
       },
       "sequence": n      (numeric) The script sequence number
       "txinwitness": ["hex", ...] (array of string) hex-encoded witness data (if any)
     }
     ,...
  ],
  "vout" : [              (array of json objects)
     {
       "value" : x.xxx,            (numeric) The value in AOK
       "n" : n,                    (numeric) index
       "scriptPubKey" : {          (json object)
         "asm" : "asm",          (string) the asm
         "hex" : "hex",          (string) the hex
         "reqSigs" : n,            (numeric) The required sigs
         "type" : "pubkeyhash",  (string) The type, eg 'pubkeyhash'
         "addresses" : [           (json array of string)
           "address"        (string) aokchain address
           ,...
         ]
       }
     }
     ,...
  ],
  "blockhash" : "hash",   (string) the block hash
  "confirmations" : n,      (numeric) The confirmations
  "time" : ttt,             (numeric) The transaction time in seconds since epoch (Jan 1 1970 GMT)
  "blocktime" : ttt         (numeric) The block time in seconds since epoch (Jan 1 1970 GMT)
}
```

**Examples**

```text
> aokchain-cli getrawtransaction "mytxid"
> aokchain-cli getrawtransaction "mytxid" true
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getrawtransaction", "params": ["mytxid", true] }' -H 'content-type: text/plain;' http://127.0.0.1:33440/
```

### sendrawtransaction

```text
sendrawtransaction "hexstring" ( allowhighfees|maxfeerate )
```

Submits raw transaction (serialized, hex-encoded) to local node and network.

Also see createrawtransaction and signrawtransaction calls.

**Arguments**

```text
1. "hexstring"    (string, required) The hex string of the raw transaction)
2. allowhighfees    (boolean, optional, default=false) Allow high fees
   or maxfeerate    (numeric or string) Reject the transaction if its fee rate is above this value in AOK/kB;
                    0 accepts any fee. Without this argument the limit is -maxtxfee for the whole transaction.
```

**Result**

```text
"hex"             (string) The transaction hash in hex
```

**Examples**

```text
Create a transaction
> aokchain-cli createrawtransaction "[{\"txid\" : \"mytxid\",\"vout\":0}]" "{\"myaddress\":0.01}"
Sign the transaction, and get back the hex
> aokchain-cli signrawtransaction "myhex"

Send the transaction (signed hex)
> aokchain-cli sendrawtransaction "signedhex"

As a json rpc call
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "sendrawtransaction", "params": ["signedhex"] }' -H 'content-type: text/plain;' http://127.0.0.1:33440/
```

### signrawtransaction

```text
signrawtransaction "hexstring" ( [{"txid":"id","vout":n,"scriptPubKey":"hex","redeemScript":"hex"},...] ["privatekey1",...] sighashtype )
```

Sign inputs for raw transaction (serialized, hex-encoded). The second optional argument (may be null) is an array of previous transaction outputs that this transaction depends on but may not yet be in the block chain. The third optional argument (may be null) is an array of base58-encoded private keys that, if given, will be the only keys used to sign the transaction.

Requires wallet passphrase to be set with walletpassphrase call.

**Arguments**

```text
1. "hexstring"     (string, required) The transaction hex string
2. "prevtxs"       (string, optional) An json array of previous dependent transaction outputs
     [               (json array of json objects, or 'null' if none provided)
       {
         "txid":"id",             (string, required) The transaction id
         "vout":n,                  (numeric, required) The output number
         "scriptPubKey": "hex",   (string, required) script key
         "redeemScript": "hex",   (string, required for P2SH or P2WSH) redeem script
         "amount": value            (numeric, required) The amount spent
       }
       ,...
    ]
3. "privkeys"     (string, optional) A json array of base58-encoded private keys for signing
    [                  (json array of strings, or 'null' if none provided)
      "privatekey"   (string) private key in base58-encoding
      ,...
    ]
4. "sighashtype"     (string, optional, default=ALL) The signature hash type. Must be one of
       "ALL"
       "NONE"
       "SINGLE"
       "ALL|ANYONECANPAY"
       "NONE|ANYONECANPAY"
       "SINGLE|ANYONECANPAY"
```

**Result**

```text
{
  "hex" : "value",           (string) The hex-encoded raw transaction with signature(s)
  "complete" : true|false,   (boolean) If the transaction has a complete set of signatures
  "errors" : [                 (json array of objects) Script verification errors (if there are any)
    {
      "txid" : "hash",           (string) The hash of the referenced, previous transaction
      "vout" : n,                (numeric) The index of the output to spent and used as input
      "scriptSig" : "hex",       (string) The hex-encoded signature script
      "sequence" : n,            (numeric) Script sequence number
      "error" : "text"           (string) Verification or signing error related to the input
    }
    ,...
  ]
}
```

**Examples**

```text
> aokchain-cli signrawtransaction "myhex"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "signrawtransaction", "params": ["myhex"] }' -H 'content-type: text/plain;' http://127.0.0.1:33440/
```

### signrawtransactionwithkey

```text
signrawtransactionwithkey "hexstring" ["privatekey1",...] ( [{"txid":"id","vout":n,"scriptPubKey":"hex","redeemScript":"hex"},...] sighashtype )
```

Signs the inputs of a raw transaction (serialized, hex-encoded) with the given private keys only; no wallet is used. The arguments and the result are those of signrawtransaction, with the keys in second place.

**Arguments**

```text
1. "hexstring"   (string, required) The transaction hex string
2. "privkeys"    (array, required) Base58-encoded private keys for signing
3. "prevtxs"     (array, optional) Previous dependent transaction outputs, as for signrawtransaction
4. "sighashtype" (string, optional, default=ALL) The signature hash type
```

**Result**

```text
{
  "hex" : "value",      (string) The hex-encoded raw transaction with signature(s)
  "complete" : true|false, (boolean) If the transaction has a complete set of signatures
  "errors" : [ ... ]      (array) Script verification errors (if there are any)
}
```

**Examples**

```text
> aokchain-cli signrawtransactionwithkey "myhex" '["privatekey"]'
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "signrawtransactionwithkey", "params": ["myhex", ["privatekey"]] }' -H 'content-type: text/plain;' http://127.0.0.1:33440/
```

### signrawtransactionwithwallet

```text
signrawtransactionwithwallet "hexstring" ( [{"txid":"id","vout":n,"scriptPubKey":"hex","redeemScript":"hex"},...] sighashtype )
```

Signs the inputs of a raw transaction (serialized, hex-encoded) with the keys of the wallet. The arguments and the result are those of signrawtransaction without the list of keys.

**Arguments**

```text
1. "hexstring"   (string, required) The transaction hex string
2. "prevtxs"     (array, optional) Previous dependent transaction outputs, as for signrawtransaction
3. "sighashtype" (string, optional, default=ALL) The signature hash type
```

**Result**

```text
{
  "hex" : "value",      (string) The hex-encoded raw transaction with signature(s)
  "complete" : true|false, (boolean) If the transaction has a complete set of signatures
  "errors" : [ ... ]      (array) Script verification errors (if there are any)
}
```

**Examples**

```text
> aokchain-cli signrawtransactionwithwallet "myhex"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "signrawtransactionwithwallet", "params": ["myhex"] }' -H 'content-type: text/plain;' http://127.0.0.1:33440/
```

### testmempoolaccept

```text
testmempoolaccept ["rawtx"] ( allowhighfees|maxfeerate )
```

Returns whether a raw transaction (serialized, hex-encoded) would be accepted by the mempool. The transaction is checked against the consensus and policy rules and is neither added to the mempool nor sent to the network.

See sendrawtransaction for how to send it.

**Arguments**

```text
1. ["rawtx"]      (array, required) An array with one hex string of a raw transaction.
2. allowhighfees    (boolean, optional, default=false) Allow high fees
   or maxfeerate    (numeric or string) Reject the transaction if its fee rate is above this value in AOK/kB; 0 accepts any fee
```

**Result**

```text
[                   (array) One result for each transaction of the array
 {
  "txid"           (string) The transaction hash in hex
  "allowed"        (boolean) Whether the mempool would accept it
  "reject-reason"  (string) Why it was rejected (only when it is not allowed)
 }
]
```

**Examples**

```text
> aokchain-cli testmempoolaccept "[\"signedhex\"]"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "testmempoolaccept", "params": [["signedhex"]] }' -H 'content-type: text/plain;' http://127.0.0.1:33440/
```
