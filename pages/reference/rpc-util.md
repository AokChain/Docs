---
title: RPC: Utilities
description: RPC reference: multisig addresses, fee estimates, message signatures, address checks and recovery words.
order: 28
generated_by: tools/rpc_reference.py
---

The help text of every command in the utilities category, as AokChain Core 4.0.5 prints it with `aokchain-cli help <command>`. All categories are on [[rpc]].

> [!NOTE]
> Many examples in these help texts come from the upstream code: their addresses are often
> Bitcoin addresses, and their `curl` lines use port 8766. An AokChain node answers JSON-RPC on
> port 33440 (mainnet) or 44550 (testnet and regtest) unless `rpcport` says otherwise; see [[json-rpc]].

| Command | Summary |
|---|---|
| [createmultisig](#createmultisig) | Creates a multi-signature address with n signature of m keys required. |
| [estimatefee](#estimatefee) | DEPRECATED. Please use estimatesmartfee for more intelligent estimates. |
| [estimatesmartfee](#estimatesmartfee) | Estimates the approximate fee per kilobyte needed for a transaction to begin confirmation within conf\_target blocks if possible and return the ... |
| [mnemonicfindaddress](#mnemonicfindaddress) | Find the key of an address among the keys a BIP39 mnemonic (recovery words) can produce. |
| [mnemonictokeys](#mnemonictokeys) | Derive private keys and addresses from a BIP39 mnemonic (recovery words) of another wallet. |
| [signmessagewithprivkey](#signmessagewithprivkey) | Sign a message with the private key of an address |
| [validateaddress](#validateaddress) | Return information about the given aokchain address. |
| [verifymessage](#verifymessage) | Verify a signed message |

### createmultisig

```text
createmultisig nrequired ["key",...]
```

Creates a multi-signature address with n signature of m keys required. It returns a json object with the address and redeemScript.

**Arguments**

```text
1. nrequired      (numeric, required) The number of required signatures out of the n keys or addresses.
2. "keys"       (string, required) A json array of keys which are aokchain addresses or hex-encoded public keys
     [
       "key"    (string) aokchain address or hex-encoded public key
       ,...
     ]
```

**Result**

```text
{
  "address":"multisigaddress",  (string) The value of the new multisig address.
  "redeemScript":"script"       (string) The string value of the hex-encoded redemption script.
}
```

**Examples**

```text
Create a multisig address from 2 addresses
> aokchain-cli createmultisig 2 "[\"16sSauSf5pF2UkUwvKGq4qjNRzBZYqgEL5\",\"171sgjn4YtPu27adkKGrdDwzRTxnRkBfKV\"]"

As a json rpc call
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "createmultisig", "params": [2, "[\"16sSauSf5pF2UkUwvKGq4qjNRzBZYqgEL5\",\"171sgjn4YtPu27adkKGrdDwzRTxnRkBfKV\"]"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### estimatefee

```text
estimatefee nblocks
```

DEPRECATED. Please use estimatesmartfee for more intelligent estimates. Estimates the approximate fee per kilobyte needed for a transaction to begin confirmation within nblocks blocks. Uses virtual transaction size of transaction as defined in BIP 141 (witness data is discounted).

**Arguments**

```text
1. nblocks     (numeric, required)
```

**Result**

```text
n              (numeric) estimated fee-per-kilobyte

A negative value is returned if not enough transactions and blocks
have been observed to make an estimate.
-1 is always returned for nblocks == 1 as it is impossible to calculate
a fee that is high enough to get reliably included in the next block.
```

**Example**

```text
> aokchain-cli estimatefee 6
```

### estimatesmartfee

```text
estimatesmartfee conf_target ("estimate_mode")
```

Estimates the approximate fee per kilobyte needed for a transaction to begin confirmation within conf\_target blocks if possible and return the number of blocks for which the estimate is valid. Uses virtual transaction size as defined in BIP 141 (witness data is discounted).

**Arguments**

```text
1. conf_target     (numeric) Confirmation target in blocks (1 - 1008)
2. "estimate_mode" (string, optional, default=CONSERVATIVE) The fee estimate mode.
                   Whether to return a more conservative estimate which also satisfies
                   a longer history. A conservative estimate potentially returns a
                   higher feerate and is more likely to be sufficient for the desired
                   target, but is not as responsive to short term drops in the
                   prevailing fee market.  Must be one of:
       "UNSET" (defaults to CONSERVATIVE)
       "ECONOMICAL"
       "CONSERVATIVE"
```

**Result**

```text
{
  "feerate" : x.x,     (numeric, optional) estimate fee rate in AOK/kB
  "errors": [ str... ] (json array of strings, optional) Errors encountered during processing
  "blocks" : n         (numeric) block number where estimate was found
}

The request target will be clamped between 2 and the highest target
fee estimation is able to return based on how long it has been running.
An error is returned if not enough transactions and blocks
have been observed to make an estimate for any number of blocks.
```

**Example**

```text
> aokchain-cli estimatesmartfee 6
```

### mnemonicfindaddress

```text
mnemonicfindaddress "mnemonic" "address" ( "passphrase" validate )
```

Find the key of an address among the keys a BIP39 mnemonic (recovery words) can produce. Use this when the derivation path of the wallet that created the mnemonic is not known. It tries the usual layouts: BIP44 (m/44'/coin'/account'/change/index) for coin types 0 to 2047, accounts 0 and 1 and indexes 0 to 19, BIP49/84 style paths for the common coin types, and simple layouts such as m/0'/0'/index' and m/0/index. This takes up to a minute. Nothing is stored and the wallet is not touched. WARNING: anyone who sees the mnemonic or the key can spend the coins.

**Arguments**

```text
1. "mnemonic"    (string, required) The 12 to 24 words, separated by spaces
2. "address"     (string, required) An address of the wallet that created the mnemonic
3. "passphrase"  (string, optional, default="") The optional BIP39 passphrase ("25th word")
4. validate      (boolean, optional, default=true) Check the words and the checksum (English and Korean word lists)
```

**Result**

```text
{
  "found": true|false,  (boolean) whether the address was found
  "searched": n,        (numeric) number of keys tried
  "path": "xxx",        (string) path of the key, if found; use its parent with mnemonictokeys for the other keys
  "address": "xxx",     (string) the address
  "compressed": true|false, (boolean) whether the address is of the compressed public key
  "privkey": "xxx"      (string) its private key, as used by importprivkey
}
```

**Examples**

```text
> aokchain-cli mnemonicfindaddress "word1 word2 ... word12" "address"
```

### mnemonictokeys

```text
mnemonictokeys "mnemonic" ( "path" count "passphrase" start validate )
```

Derive private keys and addresses from a BIP39 mnemonic (recovery words) of another wallet. Nothing is stored and the wallet is not touched; import a key with importprivkey if wanted. The path depends on the wallet that created the mnemonic. If it is not known, use mnemonicfindaddress with an address of that wallet. WARNING: anyone who sees the mnemonic or the keys can spend the coins. Use this on an offline machine if possible.

**Arguments**

```text
1. "mnemonic"    (string, required) The 12 to 24 words, separated by spaces
2. "path"        (string, optional, default=m/44'/0'/0'/0) BIP32 path of the parent of the keys; ' or h marks a hardened level
3. count         (numeric, optional, default=5) Number of keys to derive below the path (1-1000)
4. "passphrase"  (string, optional, default="") The optional BIP39 passphrase ("25th word")
5. start         (numeric, optional, default=0) Index of the first key
6. validate      (boolean, optional, default=true) Check the words and the checksum (English and Korean word lists)
```

**Result**

```text
{
  "language": "xxx",      (string) word list the mnemonic was validated against, empty if not validated
  "keys": [
    {
      "path": "xxx",      (string) path of the key
      "address": "xxx",   (string) its address
      "pubkey": "hex",    (string) its public key
      "privkey": "xxx"    (string) its private key, as used by importprivkey
    }, ...
  ]
}
```

**Examples**

```text
> aokchain-cli mnemonictokeys "word1 word2 ... word12"
> aokchain-cli mnemonictokeys "word1 word2 ... word12" "m/44'/0'/0'/0" 20
```

### signmessagewithprivkey

```text
signmessagewithprivkey "privkey" "message"
```

Sign a message with the private key of an address

**Arguments**

```text
1. "privkey"         (string, required) The private key to sign the message with.
2. "message"         (string, required) The message to create a signature of.
```

**Result**

```text
"signature"          (string) The signature of the message encoded in base 64
```

**Examples**

```text
Create the signature
> aokchain-cli signmessagewithprivkey "privkey" "my message"

Verify the signature
> aokchain-cli verifymessage "1D1ZrZNe3JUo7ZycKEYQQiQAWd9y54F4XX" "signature" "my message"

As json rpc
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "signmessagewithprivkey", "params": ["privkey", "my message"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### validateaddress

```text
validateaddress "address"
```

Return information about the given aokchain address.

**Arguments**

```text
1. "address"     (string, required) The aokchain address to validate
```

**Result**

```text
{
  "isvalid" : true|false,       (boolean) If the address is valid or not. If not, this is the only property returned.
  "address" : "address", (string) The aokchain address validated
  "scriptPubKey" : "hex",       (string) The hex encoded scriptPubKey generated by the address
  "stakingaddress" : "address", (string) The staking address part of a offline staking address
  "spendingaddress" : "aaddress", (string) The spending address part of a offline staking address
  "ismine" : true|false,        (boolean) If the address is yours or not
  "iswatchonly" : true|false,   (boolean) If the address is watchonly
  "isscript" : true|false,      (boolean) If the key is a script
  "script" : "type"             (string, optional) The output script type. Possible types: nonstandard, pubkey, pubkeyhash, scripthash, multisig, nulldata, witness_v0_keyhash, witness_v0_scripthash
  "hex" : "hex",                (string, optional) The redeemscript for the p2sh address
  "addresses"                   (string, optional) Array of addresses associated with the known redeemscript
    [
      "address"
      ,...
    ]
  "sigsrequired" : xxxxx        (numeric, optional) Number of signatures required to spend multisig output
  "pubkey" : "publickeyhex",    (string) The hex value of the raw public key
  "iscompressed" : true|false,  (boolean) If the address is compressed
  "account" : "account"         (string) DEPRECATED. The account associated with the address, "" is the default account
  "timestamp" : timestamp,        (number, optional) The creation time of the key if available in seconds since epoch (Jan 1 1970 GMT)
  "hdkeypath" : "keypath"       (string, optional) The HD keypath if the key is HD and available
  "hdmasterkeyid" : "<hash160>" (string, optional) The Hash160 of the HD master pubkey
}
```

**Examples**

```text
> aokchain-cli validateaddress "1PSSGeFHDnKNxiEyFrD1wcEaHr9hrQDDWc"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "validateaddress", "params": ["1PSSGeFHDnKNxiEyFrD1wcEaHr9hrQDDWc"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### verifymessage

```text
verifymessage "address" "signature" "message"
```

Verify a signed message

**Arguments**

```text
1. "address"         (string, required) The aokchain address to use for the signature.
2. "signature"       (string, required) The signature provided by the signer in base 64 encoding (see signmessage).
3. "message"         (string, required) The message that was signed.
```

**Result**

```text
true|false   (boolean) If the signature is verified or not.
```

**Examples**

```text
Unlock the wallet for 30 seconds
> aokchain-cli walletpassphrase "mypassphrase" 30

Create the signature
> aokchain-cli signmessage "1D1ZrZNe3JUo7ZycKEYQQiQAWd9y54F4XX" "my message"

Verify the signature
> aokchain-cli verifymessage "1D1ZrZNe3JUo7ZycKEYQQiQAWd9y54F4XX" "signature" "my message"

As json rpc
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "verifymessage", "params": ["1D1ZrZNe3JUo7ZycKEYQQiQAWd9y54F4XX", "signature", "my message"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```
