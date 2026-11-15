---
title: "RPC: Wallet"
description: "RPC reference: keys, addresses, balances, payments, backups, encryption and the wallet files."
order: 29
generated_by: tools/rpc_reference.py
---

The help text of every command in the wallet category, as AokChain Core 4.0.5 prints it with `aokchain-cli help <command>`. All categories are on [[rpc]].

> [!NOTE]
> Many examples in these help texts come from the upstream code: their addresses are often
> Bitcoin addresses, and their `curl` lines use port 8766. An AokChain node answers JSON-RPC on
> port 33440 (mainnet) or 44550 (testnet and regtest) unless `rpcport` says otherwise; see [[json-rpc]].

| Command | Summary |
|---|---|
| [abandontransaction](#abandontransaction) | Mark in-wallet transaction &lt;txid&gt; as abandoned |
| [abortrescan](#abortrescan) | Stops current wallet rescan triggered e.g. by an importprivkey call. |
| [addmultisigaddress](#addmultisigaddress) | Add a nrequired-to-sign multisignature address to the wallet. |
| [addwitnessaddress](#addwitnessaddress) | Add a witness address for a script (with pubkey or redeemscript known). |
| [backupwallet](#backupwallet) | Safely copies current wallet file to destination, which can be a directory or a path with filename. |
| [bumpfee](#bumpfee) | bumpfee has been deprecated on the AOK Wallet. |
| [createwallet](#createwallet) | Creates and loads a new wallet. |
| [dumpprivkey](#dumpprivkey) | Reveals the private key corresponding to 'address'. |
| [dumpwallet](#dumpwallet) | Dumps all wallet keys in a human-readable format to a server-side file. |
| [encryptwallet](#encryptwallet) | Encrypts the wallet with 'passphrase'. |
| [getaccount](#getaccount) | DEPRECATED. Returns the account associated with the given address. |
| [getaccountaddress](#getaccountaddress) | DEPRECATED. Returns the current Bitcoin address for receiving payments to this account. |
| [getaddressesbyaccount](#getaddressesbyaccount) | DEPRECATED. Returns the list of addresses for the given account. |
| [getaddressesbylabel](#getaddressesbylabel) | Returns the list of addresses assigned the specified label. |
| [getaddressinfo](#getaddressinfo) | Returns what the wallet knows about an address. |
| [getbalance](#getbalance) | If account is not specified, returns the server's total available balance. |
| [getbalances](#getbalances) | Returns all balances of the wallet in AOK. |
| [getnewaddress](#getnewaddress) | Returns a new AokChain address for receiving payments. |
| [getofflinestakingaddress](#getofflinestakingaddress) | Returns a offline staking address based on two address inputs |
| [getrawchangeaddress](#getrawchangeaddress) | Returns a new AokChain address, for receiving change. |
| [getreceivedbyaddress](#getreceivedbyaddress) | Returns the total amount received by the given address in transactions with at least minconf confirmations. |
| [getreceivedbylabel](#getreceivedbylabel) | Returns the total amount received by addresses with &lt;label&gt; in transactions with at least \[minconf\] confirmations. |
| [gettransaction](#gettransaction) | Get detailed information about in-wallet transaction &lt;txid&gt; |
| [getunconfirmedbalance](#getunconfirmedbalance) | Returns the server's total unconfirmed balance |
| [getwalletinfo](#getwalletinfo) | Returns an object containing various wallet state info. |
| [importaddress](#importaddress) | Adds a script (in hex) or address that can be watched as if it were in your wallet but cannot be used to spend. |
| [importmnemonic](#importmnemonic) | Adds the keys of another wallet to this wallet, from its BIP39 mnemonic (recovery words). |
| [importmulti](#importmulti) | Import addresses/scripts (with private or public keys, redeem script (P2SH)), rescanning all addresses in one-shot-only (rescan can be disabled ... |
| [importprivkey](#importprivkey) | Adds a private key (as returned by dumpprivkey) to your wallet. |
| [importprunedfunds](#importprunedfunds) | Imports funds without rescan. |
| [importpubkey](#importpubkey) | Adds a public key (in hex) that can be watched as if it were in your wallet but cannot be used to spend. |
| [importwallet](#importwallet) | Imports keys from a wallet dump file (see dumpwallet). |
| [keypoolrefill](#keypoolrefill) | Fills the keypool. |
| [listaccounts](#listaccounts) | DEPRECATED. Returns Object that has account names as keys, account balances as values. |
| [listaddressgroupings](#listaddressgroupings) | Lists groups of addresses which have had their common ownership made public by common use as inputs or as the resulting change in past transactions |
| [listlabels](#listlabels) | Returns the list of all labels, or labels that are assigned to addresses with a specific purpose. |
| [listlockunspent](#listlockunspent) | Returns list of temporarily unspendable outputs. |
| [listreceivedbyaddress](#listreceivedbyaddress) | List balances by receiving address. |
| [listreceivedbylabel](#listreceivedbylabel) | List received transactions by label. |
| [listsinceblock](#listsinceblock) | Get all transactions in blocks since block \[blockhash\], or all transactions if omitted. |
| [listtransactions](#listtransactions) | Returns up to 'count' most recent transactions skipping the first 'from' transactions for account 'account'. |
| [listunspent](#listunspent) | Returns array of unspent transaction outputs with between minconf and maxconf (inclusive) confirmations. |
| [listunspenttoken](#listunspenttoken) | Returns array of unspent transaction outputs with between minconf and maxconf (inclusive) confirmations. |
| [listwalletdir](#listwalletdir) | Returns a list of wallets in the wallet directory. |
| [listwallets](#listwallets) | Returns a list of currently loaded wallets. |
| [loadwallet](#loadwallet) | Loads a wallet from a wallet file or directory. |
| [lockunspent](#lockunspent) | Updates list of temporarily unspendable outputs. |
| [move](#move) | DEPRECATED. Move a specified amount from one account in your wallet to another. |
| [purgeorphanstakes](#purgeorphanstakes) | Deletes this wallet's orphaned coinstake transactions from the wallet. |
| [removeaddress](#removeaddress) | Remove a script (in hex) or address that can be watched as if it were in your wallet but cannot be used to spend. |
| [removeprunedfunds](#removeprunedfunds) | Deletes the specified transaction from the wallet. |
| [rescanblockchain](#rescanblockchain) | Rescan the local blockchain for wallet related transactions. |
| [restorewallet](#restorewallet) | Restores a wallet from a backup file (of backupwallet, or a copy of a wallet.dat) and loads it. |
| [sendfrom](#sendfrom) | DEPRECATED (use sendtoaddress). |
| [sendmany](#sendmany) | Send multiple times. |
| [sendtoaddress](#sendtoaddress) | Send an amount to a given address. |
| [setlabel](#setlabel) | Sets the label associated with the given address. |
| [settxfee](#settxfee) | Set the transaction fee per kB. |
| [signmessage](#signmessage) | Sign a message with the private key of an address |
| [unloadwallet](#unloadwallet) | Unloads a wallet that was loaded with loadwallet, createwallet or a second -wallet option. |
| [walletlock](#walletlock) | Removes the wallet encryption key from memory, locking the wallet. |
| [walletpassphrase](#walletpassphrase) | Stores the wallet decryption key in memory for 'timeout' seconds. |
| [walletpassphrasechange](#walletpassphrasechange) | Changes the wallet passphrase from 'oldpassphrase' to 'newpassphrase'. |

### abandontransaction

```text
abandontransaction "txid"
```

Mark in-wallet transaction &lt;txid&gt; as abandoned This will mark this transaction and all its in-wallet descendants as abandoned which will allow for their inputs to be respent.  It can be used to replace "stuck" or evicted transactions. It only works on transactions which are not included in a block and are not currently in the mempool. It has no effect on transactions which are already abandoned.

**Arguments**

```text
1. "txid"    (string, required) The transaction id
```

**Result**

**Examples**

```text
> aokchain-cli abandontransaction "1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "abandontransaction", "params": ["1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### abortrescan

```text
abortrescan
```

Stops current wallet rescan triggered e.g. by an importprivkey call.

**Examples**

```text
Import a private key
> aokchain-cli importprivkey "mykey"

Abort the running wallet rescan
> aokchain-cli abortrescan

As a JSON-RPC call
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "abortrescan", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### addmultisigaddress

```text
addmultisigaddress nrequired ["key",...] ( "label" )
```

Add a nrequired-to-sign multisignature address to the wallet. Each key is a AokChain address or hex-encoded public key. If 'label' is specified, assign address to that label.

**Arguments**

```text
1. nrequired        (numeric, required) The number of required signatures out of the n keys or addresses.
2. "keys"         (string, required) A json array of aokchain addresses or hex-encoded public keys
     [
       "address"  (string) aokchain address or hex-encoded public key
       ...,
     ]
3. "label"        (string, optional) A label to assign the addresses to.
```

**Result**

```text
"address"         (string) A aokchain address associated with the keys.
```

**Examples**

```text
Add a multisig address from 2 addresses
> aokchain-cli addmultisigaddress 2 "[\"16sSauSf5pF2UkUwvKGq4qjNRzBZYqgEL5\",\"171sgjn4YtPu27adkKGrdDwzRTxnRkBfKV\"]"

As json rpc call
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "addmultisigaddress", "params": [2, "[\"16sSauSf5pF2UkUwvKGq4qjNRzBZYqgEL5\",\"171sgjn4YtPu27adkKGrdDwzRTxnRkBfKV\"]"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### addwitnessaddress

```text
addwitnessaddress "address"
```

Add a witness address for a script (with pubkey or redeemscript known). It returns the witness script.

**Arguments**

```text
1. "address"       (string, required) An address known to the wallet
```

**Result**

```text
"witnessaddress",  (string) The value of the new address (P2SH of witness script).
}
```

### backupwallet

```text
backupwallet "destination"
```

Safely copies current wallet file to destination, which can be a directory or a path with filename.

**Arguments**

```text
1. "destination"   (string) The destination directory or file
```

**Examples**

```text
> aokchain-cli backupwallet "backup.dat"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "backupwallet", "params": ["backup.dat"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### bumpfee

bumpfee has been deprecated on the AOK Wallet.

### createwallet

```text
createwallet "wallet_name"
```

Creates and loads a new wallet.

**Arguments**

```text
1. "wallet_name"    (string, required) The name for the new wallet. If this is a path, the wallet will be created at the path location.
```

**Result**

```text
{
  "name" :    <wallet_name>,        (string) The wallet name if created successfully. If the wallet was created using a full path, the wallet_name will be the full path.
  "warning" : <warning>,            (string) Warning message if wallet was not loaded cleanly.
}
```

**Examples**

```text
> aokchain-cli createwallet "testwallet"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "createwallet", "params": ["testwallet"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### dumpprivkey

```text
dumpprivkey "address"
```

Reveals the private key corresponding to 'address'. Then the importprivkey can be used with this output

**Arguments**

```text
1. "address"   (string, required) The aokchain address for the private key
```

**Result**

```text
"key"                (string) The private key
```

**Examples**

```text
> aokchain-cli dumpprivkey "myaddress"
> aokchain-cli importprivkey "mykey"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "dumpprivkey", "params": ["myaddress"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### dumpwallet

```text
dumpwallet "filename"
```

Dumps all wallet keys in a human-readable format to a server-side file. This does not allow overwriting existing files.

**Arguments**

```text
1. "filename"    (string, required) The filename with path (either absolute or relative to aokchaind)
```

**Result**

```text
{                           (json object)
  "filename" : {        (string) The filename with full absolute path
}
```

**Examples**

```text
> aokchain-cli dumpwallet "test"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "dumpwallet", "params": ["test"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### encryptwallet

```text
encryptwallet "passphrase"
```

Encrypts the wallet with 'passphrase'. This is for first time encryption. After this, any calls that interact with private keys such as sending or signing will require the passphrase to be set prior the making these calls. Use the walletpassphrase call for this, and then walletlock call. If the wallet is already encrypted, use the walletpassphrasechange call. Note that this will shutdown the server.

**Arguments**

```text
1. "passphrase"    (string) The pass phrase to encrypt the wallet with. It must be at least 1 character, but should be long.
```

**Examples**

```text
Encrypt your wallet
> aokchain-cli encryptwallet "my pass phrase"

Now set the passphrase to use the wallet, such as for signing or sending aokchain
> aokchain-cli walletpassphrase "my pass phrase"

Now we can do something like sign
> aokchain-cli signmessage "address" "test message"

Now lock the wallet again by removing the passphrase
> aokchain-cli walletlock

As a json rpc call
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "encryptwallet", "params": ["my pass phrase"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getaccount

```text
getaccount "address"
```

DEPRECATED. Returns the account associated with the given address.

**Arguments**

```text
1. "address"         (string, required) The aokchain address for account lookup.
```

**Result**

```text
"accountname"        (string) the account address
```

**Examples**

```text
> aokchain-cli getaccount "1D1ZrZNe3JUo7ZycKEYQQiQAWd9y54F4XX"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getaccount", "params": ["1D1ZrZNe3JUo7ZycKEYQQiQAWd9y54F4XX"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getaccountaddress

```text
getaccountaddress "account"
```

DEPRECATED. Returns the current Bitcoin address for receiving payments to this account.

**Arguments**

```text
1. "account"       (string, required) The account for the address. It can also be set to the empty string "" to represent the default account. The account does not need to exist, it will be created and a new address created  if there is no account by the given name.
```

**Result**

```text
"address"          (string) The account bitcoin address
```

**Examples**

```text
> aokchain-cli getaccountaddress
> aokchain-cli getaccountaddress ""
> aokchain-cli getaccountaddress "myaccount"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getaccountaddress", "params": ["myaccount"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getaddressesbyaccount

```text
getaddressesbyaccount "account"
```

DEPRECATED. Returns the list of addresses for the given account.

**Arguments**

```text
1. "account"        (string, required) The account name.
```

**Result**

```text
[                     (json array of string)
  "address"         (string) a aokchain address associated with the given account
  ,...
]
```

**Examples**

```text
> aokchain-cli getaddressesbyaccount "tabby"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getaddressesbyaccount", "params": ["tabby"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getaddressesbylabel

```text
getaddressesbylabel "label"
```

Returns the list of addresses assigned the specified label.

**Arguments**

```text
1. "label"  (string, required) The label.
```

**Result**

```text
{ (json object with addresses as keys)
  "address": { (json object with information about address)
    "purpose": "string" (string)  Purpose of address ("send" for sending address, "receive" for receiving address)
  },...
}
```

**Examples**

```text
> aokchain-cli getaddressesbylabel "tabby"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getaddressesbylabel", "params": ["tabby"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getaddressinfo

```text
getaddressinfo "address"
```

Returns what the wallet knows about an address. The fields are those of validateaddress without "isvalid" (an invalid address is an error here), with the label of the address.

**Arguments**

```text
1. "address"     (string, required) The address to look up
```

**Result**

```text
{
  "address" : "address",   (string) The address
  "scriptPubKey" : "hex",  (string) The hex encoded scriptPubKey of the address
  "ismine" : true|false,    (boolean) If the address is yours
  "iswatchonly" : true|false, (boolean) If the address is watch-only
  "isscript" : true|false,  (boolean) If the key is a script
  "pubkey" : "hex",        (string) The hex value of the raw public key (when the wallet has it)
  "label" : "label",       (string) The label of the address ("" without one)
  "labels" : [ { "name": "label", "purpose": "send|receive" } ],
  ...                        (the other fields of validateaddress)
}
```

**Examples**

```text
> aokchain-cli getaddressinfo "address"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getaddressinfo", "params": ["address"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getbalance

```text
getbalance ( "account" minconf include_watchonly )
```

If account is not specified, returns the server's total available balance. If account is specified (DEPRECATED), returns the balance in the account. Note that the account "" is not the same as leaving the parameter out. The server total may be different to the balance in the default "" account.

**Arguments**

```text
1. "account"         (string, optional) DEPRECATED. The account string may be given as a
                     specific account name to find the balance associated with wallet keys in
                     a named account, or as the empty string ("") to find the balance
                     associated with wallet keys not in any named account, or as "*" to find
                     the balance associated with all wallet keys regardless of account.
                     When this option is specified, it calculates the balance in a different
                     way than when it is not specified, and which can count spends twice when
                     there are conflicting pending transactions (such as those created by
                     the bumpfee command), temporarily resulting in low or even negative
                     balances. In general, account balance calculation is not considered
                     reliable and has resulted in confusing outcomes, so it is recommended to
                     avoid passing this argument.
2. minconf           (numeric, optional, default=1) Only include transactions confirmed at least this many times.
3. include_watchonly (bool, optional, default=false) Also include balance in watch-only addresses (see 'importaddress')
```

**Result**

```text
amount              (numeric) The total amount in AOK received for this account.
```

**Examples**

```text
The total amount in the wallet with 1 or more confirmations
> aokchain-cli getbalance

The total amount in the wallet at least 6 blocks confirmed
> aokchain-cli getbalance "*" 6

As a json rpc call
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getbalance", "params": ["*", 6] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getbalances

```text
getbalances
```

Returns all balances of the wallet in AOK.

**Result**

```text
{
  "mine": {
    "trusted": xxx,            (numeric) balance that can be spent
    "untrusted_pending": xxx,  (numeric) received and not confirmed yet
    "immature": xxx,           (numeric) stake and coinbase rewards that are not mature yet
    "staked": xxx,             (numeric) coins that are tied up in stakes that are not mature yet
    "locked": xxx,             (numeric) coins in time locked outputs
    "offline_staking": xxx     (numeric) coins in offline staking outputs
  },
  "watchonly": {               (only when the wallet watches addresses)
    "trusted": xxx, "untrusted_pending": xxx, "immature": xxx
  }
}
```

**Examples**

```text
> aokchain-cli getbalances
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getbalances", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getnewaddress

```text
getnewaddress ( "label" )
```

Returns a new AokChain address for receiving payments. If 'label' is specified, it is added to the address book so payments received with the address will be associated with 'label'.

**Arguments**

```text
1. "label"          (string, optional) The label name for the address to be linked to. If not provided, the default label "" is used. It can also be set to the empty string "" to represent the default label. The label does not need to exist, it will be created if there is no label by the given name.
```

**Result**

```text
"address"    (string) The new aokchain address
```

**Examples**

```text
> aokchain-cli getnewaddress
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getnewaddress", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getofflinestakingaddress

```text
getofflinestakingaddress "stakingaddress" "spendingaddress"
```

Returns a offline staking address based on two address inputs

**Arguments**

```text
1. "stakingaddress"  (string, required) The staking address.
2. "spendingaddress" (string, required) The spending address.
```

**Examples**

```text
> aokchain-cli getofflinestakingaddress "KgZDBz1dV8H4zcZUZ3yV1336bKkQ5L4FXv" "Ktf4i17uoofsKJqMTuLsqGBzHY92bfjPux"

As a json rpc call
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getofflinestakingaddress", "params": ["KgZDBz1dV8H4zcZUZ3yV1336bKkQ5L4FXv", "Ktf4i17uoofsKJqMTuLsqGBzHY92bfjPux"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getrawchangeaddress

```text
getrawchangeaddress
```

Returns a new AokChain address, for receiving change. This is for use with raw transactions, NOT normal use.

**Result**

```text
"address"    (string) The address
```

**Examples**

```text
> aokchain-cli getrawchangeaddress
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getrawchangeaddress", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getreceivedbyaddress

```text
getreceivedbyaddress "address" ( minconf )
```

Returns the total amount received by the given address in transactions with at least minconf confirmations.

**Arguments**

```text
1. "address"         (string, required) The aokchain address for transactions.
2. minconf             (numeric, optional, default=1) Only include transactions confirmed at least this many times.
```

**Result**

```text
amount   (numeric) The total amount in AOK received at this address.
```

**Examples**

```text
The amount from transactions with at least 1 confirmation
> aokchain-cli getreceivedbyaddress "1D1ZrZNe3JUo7ZycKEYQQiQAWd9y54F4XX"

The amount including unconfirmed transactions, zero confirmations
> aokchain-cli getreceivedbyaddress "1D1ZrZNe3JUo7ZycKEYQQiQAWd9y54F4XX" 0

The amount with at least 6 confirmations
> aokchain-cli getreceivedbyaddress "1D1ZrZNe3JUo7ZycKEYQQiQAWd9y54F4XX" 6

As a json rpc call
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getreceivedbyaddress", "params": ["1D1ZrZNe3JUo7ZycKEYQQiQAWd9y54F4XX", 6] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getreceivedbylabel

```text
getreceivedbylabel "label" ( minconf )
```

Returns the total amount received by addresses with &lt;label&gt; in transactions with at least \[minconf\] confirmations.

**Arguments**

```text
1. "label"        (string, required) The selected label, may be the default label using "".
2. minconf          (numeric, optional, default=1) Only include transactions confirmed at least this many times.
```

**Result**

```text
amount              (numeric) The total amount in AOK received for this label.
```

**Examples**

```text
Amount received by the default label with at least 1 confirmation
> aokchain-cli getreceivedbylabel ""

Amount received at the tabby label including unconfirmed amounts with zero confirmations
> aokchain-cli getreceivedbylabel "tabby" 0

The amount with at least 6 confirmations
> aokchain-cli getreceivedbylabel "tabby" 6

As a json rpc call
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getreceivedbylabel", "params": ["tabby", 6] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### gettransaction

```text
gettransaction "txid" ( include_watchonly )
```

Get detailed information about in-wallet transaction &lt;txid&gt;

**Arguments**

```text
1. "txid"                  (string, required) The transaction id
2. "include_watchonly"     (bool, optional, default=false) Whether to include watch-only addresses in balance calculation and details[]
```

**Result**

```text
{
  "amount" : x.xxx,        (numeric) The transaction amount in AOK
  "fee": x.xxx,            (numeric) The amount of the fee in AOK. This is negative and only available for the
                              'send' category of transactions.
  "confirmations" : n,     (numeric) The number of confirmations
  "blockhash" : "hash",  (string) The block hash
  "blockindex" : xx,       (numeric) The index of the transaction in the block that includes it
  "blocktime" : ttt,       (numeric) The time in seconds since epoch (1 Jan 1970 GMT)
  "txid" : "transactionid",   (string) The transaction id.
  "time" : ttt,            (numeric) The transaction time in seconds since epoch (1 Jan 1970 GMT)
  "timereceived" : ttt,    (numeric) The time received in seconds since epoch (1 Jan 1970 GMT)
  "bip125-replaceable": "yes|no|unknown",  (string) Whether this transaction could be replaced due to BIP125 (replace-by-fee);
                                                   may be unknown for unconfirmed transactions not in the mempool
  "details" : [
    {
      "account" : "accountname",      (string) DEPRECATED. The account name involved in the transaction, can be "" for the default account.
      "address" : "address",          (string) The aokchain address involved in the transaction
      "category" : "send|receive",    (string) The category, either 'send' or 'receive'
      "amount" : x.xxx,                 (numeric) The amount in AOK
      "label" : "label",              (string) A comment for the address/transaction, if any
      "vout" : n,                       (numeric) the vout value
      "fee": x.xxx,                     (numeric) The amount of the fee in AOK. This is negative and only available for the
                                           'send' category of transactions.
      "abandoned": xxx                  (bool) 'true' if the transaction has been abandoned (inputs are respendable). Only available for the
                                           'send' category of transactions.
    }
    ,...
  ],
  "token_details" : [
    {
      "token_type" : "new_token|transfer_token|reissue_token", (string) The type of token transaction
      "token_name" : "token_name",          (string) The name of the token
      "amount" : x.xxx,                 (numeric) The amount in AOK
      "address" : "address",          (string) The aokchain address involved in the transaction
      "vout" : n,                       (numeric) the vout value
      "category" : "send|receive",    (string) The category, either 'send' or 'receive'
    }
    ,...
  ],
  "hex" : "data"         (string) Raw data for transaction
}
```

**Examples**

```text
> aokchain-cli gettransaction "1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d"
> aokchain-cli gettransaction "1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d" true
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "gettransaction", "params": ["1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getunconfirmedbalance

```text
getunconfirmedbalance
```

Returns the server's total unconfirmed balance

### getwalletinfo

```text
getwalletinfo
```

Returns an object containing various wallet state info.

**Result**

```text
{
  "walletname": xxxxx,             (string) the wallet name
  "walletversion": xxxxx,          (numeric) the wallet version
  "balance": xxxxxxx,              (numeric) the total confirmed balance of the wallet in AOK
  "unconfirmed_balance": xxx,      (numeric) the total unconfirmed balance of the wallet in AOK
  "immature_balance": xxxxxx,      (numeric) the total immature balance of the wallet in AOK
  "txcount": xxxxxxx,              (numeric) the total number of transactions in the wallet
  "keypoololdest": xxxxxx,         (numeric) the timestamp (seconds since Unix epoch) of the oldest pre-generated key in the key pool
  "keypoolsize": xxxx,             (numeric) how many new keys are pre-generated (only counts external keys)
  "keypoolsize_hd_internal": xxxx, (numeric) how many new keys are pre-generated for internal use (used for change outputs, only appears if the wallet is using this feature, otherwise external keys are used)
  "unlocked_until": ttt,           (numeric) the timestamp in seconds since epoch (midnight Jan 1 1970 GMT) that the wallet is unlocked for transfers, or 0 if the wallet is locked
  "paytxfee": x.xxxx,              (numeric) the transaction fee configuration, set in AOK/kB
  "hdseedid": "<hash160>"          (string, optional) the Hash160 of the HD seed (only present when HD is enabled)
  "hdmasterkeyid": "<hash160>"     (string, optional) alias for hdseedid retained for backwards-compatibility. Will be removed in V0.18.
}
```

**Examples**

```text
> aokchain-cli getwalletinfo
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getwalletinfo", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### importaddress

```text
importaddress "address" ( "label" rescan p2sh )
```

Adds a script (in hex) or address that can be watched as if it were in your wallet but cannot be used to spend.

**Arguments**

```text
1. "script"           (string, required) The hex-encoded script (or address)
2. "label"            (string, optional, default="") An optional label
3. rescan               (boolean, optional, default=true) Rescan the wallet for transactions
4. p2sh                 (boolean, optional, default=false) Add the P2SH version of the script as well

Note: This call can take minutes to complete if rescan is true.
If you have the full public key, you should call importpubkey instead of this.

Note: If you import a non-standard raw script in hex form, outputs sending to it will be treated
as change, and not show up in many RPCs.
```

**Examples**

```text
Import a script with rescan
> aokchain-cli importaddress "myscript"

Import using a label without rescan
> aokchain-cli importaddress "myscript" "testing" false

As a JSON-RPC call
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "importaddress", "params": ["myscript", "testing", false] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### importmnemonic

```text
importmnemonic "mnemonic" ( "passphrase" "address" rescan validate )
```

Adds the keys of another wallet to this wallet, from its BIP39 mnemonic (recovery words). The usual key paths are searched for addresses that hold coins now (unspent outputs of the chain); the keys of those paths are imported up to 20 places past the last one in use, together with the matching change path. If an address of that wallet is given, its path is searched among all coin types (up to a minute) and imported even if it holds nothing now. The keys are separate from the HD seed of this wallet: make a new backup afterwards. WARNING: anyone who sees the mnemonic can spend the coins.

**Arguments**

```text
1. "mnemonic"    (string, required) The 12 to 24 words, separated by spaces (English or Korean word list)
2. "passphrase"  (string, optional, default="") The optional BIP39 passphrase ("25th word")
3. "address"     (string, optional, default="") An address of the wallet that created the mnemonic
4. rescan        (boolean, optional, default=true) Rescan the chain for the transactions of the imported keys
5. validate      (boolean, optional, default=true) Check the BIP39 checksum of the words. Some wallets, such as the
                 AOK mobile wallet, make words without it: with false a wrong checksum is accepted (the
                 words must still be words of the English or Korean list)
```

**Result**

```text
{
  "language": "xxx",   (string) word list of the mnemonic
  "searched": n,       (numeric) number of keys tried
  "imported": n,       (numeric) number of keys added to the wallet
  "found": [           (array) addresses that hold coins now
    { "path": "xxx", "address": "xxx", "amount": x.xxx, "outputs": n, "tokens": true|false }, ...
  ]
}
```

**Examples**

```text
> aokchain-cli importmnemonic "word1 word2 ... word12"
```

### importmulti

```text
importmulti "requests" ( "options" )
```

Import addresses/scripts (with private or public keys, redeem script (P2SH)), rescanning all addresses in one-shot-only (rescan can be disabled via options).

**Arguments**

```text
1. requests     (array, required) Data to be imported
  [     (array of json objects)
    {
      "scriptPubKey": "<script>" | { "address":"<address>" }, (string / json, required) Type of scriptPubKey (string for script, json for address)
      "timestamp": timestamp | "now"                        , (integer / string, required) Creation time of the key in seconds since epoch (Jan 1 1970 GMT),
                                                              or the string "now" to substitute the current synced blockchain time. The timestamp of the oldest
                                                              key will determine how far back blockchain rescans need to begin for missing wallet transactions.
                                                              "now" can be specified to bypass scanning, for keys which are known to never have been used, and
                                                              0 can be specified to scan the entire blockchain. Blocks up to 2 hours before the earliest key
                                                              creation time of all keys being imported by the importmulti call will be scanned.
      "redeemscript": "<script>"                            , (string, optional) Allowed only if the scriptPubKey is a P2SH address or a P2SH scriptPubKey
      "pubkeys": ["<pubKey>", ... ]                         , (array, optional) Array of strings giving pubkeys that must occur in the output or redeemscript
      "keys": ["<key>", ... ]                               , (array, optional) Array of strings giving private keys whose corresponding public keys must occur in the output or redeemscript
      "internal": <true>                                    , (boolean, optional, default: false) Stating whether matching outputs should be treated as not incoming payments
      "watchonly": <true>                                   , (boolean, optional, default: false) Stating whether matching outputs should be considered watched even when they're not spendable, only allowed if keys are empty
      "label": <label>                                      , (string, optional, default: '') Label to assign to the address (aka account name, for now), only allowed with internal=false
    }
  ,...
  ]
2. options                 (json, optional)
  {
     "rescan": <false>,         (boolean, optional, default: true) Stating if should rescan the blockchain after all imports
  }
```

**Examples**

```text
> aokchain-cli importmulti '[{ "scriptPubKey": { "address": "<my address>" }, "timestamp":1455191478 }, { "scriptPubKey": { "address": "<my 2nd address>" }, "label": "example 2", "timestamp": 1455191480 }]'
> aokchain-cli importmulti '[{ "scriptPubKey": { "address": "<my address>" }, "timestamp":1455191478 }]' '{ "rescan": false}'

Response is an array with the same size as the input that has the execution result :
  [{ "success": true } , { "success": false, "error": { "code": -1, "message": "Internal Server Error"} }, ... ]
```

### importprivkey

```text
importprivkey "privkey" ( "label" ) ( rescan )
```

Adds a private key (as returned by dumpprivkey) to your wallet.

**Arguments**

```text
1. "privkey"          (string, required) The private key (see dumpprivkey)
2. "label"            (string, optional, default="") An optional label
3. rescan               (boolean, optional, default=true) Rescan the wallet for transactions

Note: This call can take minutes to complete if rescan is true.
```

**Examples**

```text
Dump a private key
> aokchain-cli dumpprivkey "myaddress"

Import the private key with rescan
> aokchain-cli importprivkey "mykey"

Import using a label and without rescan
> aokchain-cli importprivkey "mykey" "testing" false

Import using default blank label and without rescan
> aokchain-cli importprivkey "mykey" "" false

As a JSON-RPC call
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "importprivkey", "params": ["mykey", "testing", false] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### importprunedfunds

```text
importprunedfunds
```

Imports funds without rescan. Corresponding address or script must previously be included in wallet. Aimed towards pruned wallets. The end-user is responsible to import additional transactions that subsequently spend the imported outputs or rescan after the point in the blockchain the transaction is included.

**Arguments**

```text
1. "rawtransaction" (string, required) A raw transaction in hex funding an already-existing address in wallet
2. "txoutproof"     (string, required) The hex output from gettxoutproof that contains the transaction
```

### importpubkey

```text
importpubkey "pubkey" ( "label" rescan )
```

Adds a public key (in hex) that can be watched as if it were in your wallet but cannot be used to spend.

**Arguments**

```text
1. "pubkey"           (string, required) The hex-encoded public key
2. "label"            (string, optional, default="") An optional label
3. rescan               (boolean, optional, default=true) Rescan the wallet for transactions

Note: This call can take minutes to complete if rescan is true.
```

**Examples**

```text
Import a public key with rescan
> aokchain-cli importpubkey "mypubkey"

Import using a label without rescan
> aokchain-cli importpubkey "mypubkey" "testing" false

As a JSON-RPC call
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "importpubkey", "params": ["mypubkey", "testing", false] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### importwallet

```text
importwallet "filename"
```

Imports keys from a wallet dump file (see dumpwallet).

**Arguments**

```text
1. "filename"    (string, required) The wallet file
```

**Examples**

```text
Dump the wallet
> aokchain-cli dumpwallet "test"

Import the wallet
> aokchain-cli importwallet "test"

Import using the json rpc call
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "importwallet", "params": ["test"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### keypoolrefill

```text
keypoolrefill ( newsize )
```

Fills the keypool. Requires wallet passphrase to be set with walletpassphrase call.

**Arguments**

```text
1. newsize     (numeric, optional, default=100) The new keypool size
```

**Examples**

```text
> aokchain-cli keypoolrefill
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "keypoolrefill", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### listaccounts

```text
listaccounts ( minconf include_watchonly)
```

DEPRECATED. Returns Object that has account names as keys, account balances as values.

**Arguments**

```text
1. minconf             (numeric, optional, default=1) Only include transactions with at least this many confirmations
2. include_watchonly   (bool, optional, default=false) Include balances in watch-only addresses (see 'importaddress')
```

**Result**

```text
{                      (json object where keys are account names, and values are numeric balances
  "account": x.xxx,  (numeric) The property name is the account name, and the value is the total balance for the account.
  ...
}
```

**Examples**

```text
List account balances where there at least 1 confirmation
> aokchain-cli listaccounts

List account balances including zero confirmation transactions
> aokchain-cli listaccounts 0

List account balances for 6 or more confirmations
> aokchain-cli listaccounts 6

As json rpc call
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "listaccounts", "params": [6] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### listaddressgroupings

```text
listaddressgroupings
```

Lists groups of addresses which have had their common ownership made public by common use as inputs or as the resulting change in past transactions

**Result**

```text
[
  [
    [
      "address",            (string) The aokchain address
      amount,                 (numeric) The amount in AOK
      "label"               (string, optional) The label
    ]
    ,...
  ]
  ,...
]
```

**Examples**

```text
> aokchain-cli listaddressgroupings
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "listaddressgroupings", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### listlabels

```text
listlabels ( "purpose" )
```

Returns the list of all labels, or labels that are assigned to addresses with a specific purpose.

**Arguments**

```text
1. "purpose"    (string, optional) Address purpose to list labels for ('send','receive'). An empty string is the same as not providing this argument.
```

**Result**

```text
[               (json array of string)
  "label",      (string) Label name
  ...
]
```

**Examples**

```text
List all labels
> aokchain-cli listlabels

List labels that have receiving addresses
> aokchain-cli listlabels receive

List labels that have sending addresses
> aokchain-cli listlabels send

As json rpc call
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "listlabels", "params": [receive] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### listlockunspent

```text
listlockunspent
```

Returns list of temporarily unspendable outputs. See the lockunspent call to lock and unlock transactions for spending.

**Result**

```text
[
  {
    "txid" : "transactionid",     (string) The transaction id locked
    "vout" : n                      (numeric) The vout value
  }
  ,...
]
```

**Examples**

```text
List the unspent transactions
> aokchain-cli listunspent

Lock an unspent transaction
> aokchain-cli lockunspent false "[{\"txid\":\"a08e6907dbbd3d809776dbfc5d82e371b764ed838b5655e72f463568df1aadf0\",\"vout\":1}]"

List the locked transactions
> aokchain-cli listlockunspent

Unlock the transaction again
> aokchain-cli lockunspent true "[{\"txid\":\"a08e6907dbbd3d809776dbfc5d82e371b764ed838b5655e72f463568df1aadf0\",\"vout\":1}]"

As a json rpc call
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "listlockunspent", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### listreceivedbyaddress

```text
listreceivedbyaddress ( minconf include_empty include_watchonly address_filter)
```

List balances by receiving address.

**Arguments**

```text
1. minconf           (numeric, optional, default=1) The minimum number of confirmations before payments are included.
2. include_empty     (bool, optional, default=false) Whether to include addresses that haven't received any payments.
3. include_watchonly (bool, optional, default=false) Whether to include watch-only addresses (see 'importaddress').
4. address_filter    (string, optional) If present, only return information on this address.
```

**Result**

```text
[
  {
    "involvesWatchonly" : true,        (bool) Only returned if imported addresses were involved in transaction
    "address" : "receivingaddress",  (string) The receiving address
    "account" : "accountname",       (string) DEPRECATED. Backwards compatible alias for label.
    "amount" : x.xxx,                  (numeric) The total amount in AOK received by the address
    "confirmations" : n,               (numeric) The number of confirmations of the most recent transaction included
    "label" : "label",               (string) The label of the receiving address. The default label is "".
    "txids": [
       n,                                (numeric) The ids of transactions received with the address
       ...
    ]
  }
  ,...
]
```

**Examples**

```text
> aokchain-cli listreceivedbyaddress
> aokchain-cli listreceivedbyaddress 6 true
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "listreceivedbyaddress", "params": [6, true, true] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "listreceivedbyaddress", "params": [6, true, true, "1M72Sfpbz1BPpXFHz9m3CdqATR44Jvaydd"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### listreceivedbylabel

```text
listreceivedbylabel ( minconf include_empty include_watchonly)
```

List received transactions by label.

**Arguments**

```text
1. minconf           (numeric, optional, default=1) The minimum number of confirmations before payments are included.
2. include_empty     (bool, optional, default=false) Whether to include labels that haven't received any payments.
3. include_watchonly (bool, optional, default=false) Whether to include watch-only addresses (see 'importaddress').
```

**Result**

```text
[
  {
    "involvesWatchonly" : true,   (bool) Only returned if imported addresses were involved in transaction
    "account" : "accountname",  (string) DEPRECATED. Backwards compatible alias for label.
    "amount" : x.xxx,             (numeric) The total amount received by addresses with this label
    "confirmations" : n,          (numeric) The number of confirmations of the most recent transaction included
    "label" : "label"           (string) The label of the receiving address. The default label is "".
  }
  ,...
]
```

**Examples**

```text
> aokchain-cli listreceivedbylabel
> aokchain-cli listreceivedbylabel 6 true
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "listreceivedbylabel", "params": [6, true, true] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### listsinceblock

```text
listsinceblock ( "blockhash" target_confirmations include_watchonly include_removed )
```

Get all transactions in blocks since block \[blockhash\], or all transactions if omitted. If "blockhash" is no longer a part of the main chain, transactions from the fork point onward are included. Additionally, if include\_removed is set, transactions affecting the wallet which were removed are returned in the "removed" array.

**Arguments**

```text
1. "blockhash"            (string, optional) The block hash to list transactions since
2. target_confirmations:    (numeric, optional, default=1) Return the nth block hash from the main chain. e.g. 1 would mean the best block hash. Note: this is not used as a filter, but only affects [lastblock] in the return value
3. include_watchonly:       (bool, optional, default=false) Include transactions to watch-only addresses (see 'importaddress')
4. include_removed:         (bool, optional, default=true) Show transactions that were removed due to a reorg in the "removed" array
                                                           (not guaranteed to work on pruned nodes)
```

**Result**

```text
{
  "transactions": [
    "account":"accountname",       (string) DEPRECATED. The account name associated with the transaction. Will be "" for the default account.
    "address":"address",    (string) The aokchain address of the transaction. Not present for move transactions (category = move).
    "category":"send|receive",     (string) The transaction category. 'send' has negative amounts, 'receive' has positive amounts.
    "amount": x.xxx,          (numeric) The amount in AOK. This is negative for the 'send' category, and for the 'move' category for moves
                                          outbound. It is positive for the 'receive' category, and for the 'move' category for inbound funds.
    "vout" : n,               (numeric) the vout value
    "fee": x.xxx,             (numeric) The amount of the fee in AOK. This is negative and only available for the 'send' category of transactions.
    "confirmations": n,       (numeric) The number of confirmations for the transaction. Available for 'send' and 'receive' category of transactions.
                                          When it's < 0, it means the transaction conflicted that many blocks ago.
    "blockhash": "hashvalue",     (string) The block hash containing the transaction. Available for 'send' and 'receive' category of transactions.
    "blockindex": n,          (numeric) The index of the transaction in the block that includes it. Available for 'send' and 'receive' category of transactions.
    "blocktime": xxx,         (numeric) The block time in seconds since epoch (1 Jan 1970 GMT).
    "txid": "transactionid",  (string) The transaction id. Available for 'send' and 'receive' category of transactions.
    "time": xxx,              (numeric) The transaction time in seconds since epoch (Jan 1 1970 GMT).
    "timereceived": xxx,      (numeric) The time received in seconds since epoch (Jan 1 1970 GMT). Available for 'send' and 'receive' category of transactions.
    "bip125-replaceable": "yes|no|unknown",  (string) Whether this transaction could be replaced due to BIP125 (replace-by-fee);
                                                   may be unknown for unconfirmed transactions not in the mempool
    "abandoned": xxx,         (bool) 'true' if the transaction has been abandoned (inputs are respendable). Only available for the 'send' category of transactions.
    "comment": "...",       (string) If a comment is associated with the transaction.
    "label" : "label"       (string) A comment for the address/transaction, if any
    "to": "...",            (string) If a comment to is associated with the transaction.
  ],
  "removed": [
    <structure is the same as "transactions" above, only present if include_removed=true>
    Note: transactions that were readded in the active chain will appear as-is in this array, and may thus have a positive confirmation count.
  ],
  "lastblock": "lastblockhash"     (string) The hash of the block (target_confirmations-1) from the best block on the main chain. This is typically used to feed back into listsinceblock the next time you call it. So you would generally use a target_confirmations of say 6, so you will be continually re-notified of transactions until they've reached 6 confirmations plus any new ones
}
```

**Examples**

```text
> aokchain-cli listsinceblock
> aokchain-cli listsinceblock "000000000000000bacf66f7497b7dc45ef753ee9a7d38571037cdb1a57f663ad" 6
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "listsinceblock", "params": ["000000000000000bacf66f7497b7dc45ef753ee9a7d38571037cdb1a57f663ad", 6] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### listtransactions

```text
listtransactions ( "account" count skip include_watchonly)
```

Returns up to 'count' most recent transactions skipping the first 'from' transactions for account 'account'.

**Arguments**

```text
1. "account"    (string, optional) DEPRECATED. The account name. Should be "*".
2. count          (numeric, optional, default=10) The number of transactions to return
3. skip           (numeric, optional, default=0) The number of transactions to skip
4. include_watchonly (bool, optional, default=false) Include transactions to watch-only addresses (see 'importaddress')
5. include_offline_staking (bool, optional, default=true) Include transactions to offline staking addresses
```

**Result**

```text
[
  {
    "account":"accountname",       (string) DEPRECATED. The account name associated with the transaction.
                                                It will be "" for the default account.
    "address":"address",    (string) The aokchain address of the transaction. Not present for
                                                move transactions (category = move).
    "category":"send|receive|move", (string) The transaction category. 'move' is a local (off blockchain)
                                                transaction between accounts, and not associated with an address,
                                                transaction id or block. 'send' and 'receive' transactions are
                                                associated with an address, transaction id and block details
    "amount": x.xxx,          (numeric) The amount in AOK. This is negative for the 'send' category, and for the
                                         'move' category for moves outbound. It is positive for the 'receive' category,
                                         and for the 'move' category for inbound funds.
    "label": "label",       (string) A comment for the address/transaction, if any
    "vout": n,                (numeric) the vout value
    "fee": x.xxx,             (numeric) The amount of the fee in AOK. This is negative and only available for the
                                         'send' category of transactions.
    "confirmations": n,       (numeric) The number of confirmations for the transaction. Available for 'send' and
                                         'receive' category of transactions. Negative confirmations indicate the
                                         transaction conflicts with the block chain
    "trusted": xxx,           (bool) Whether we consider the outputs of this unconfirmed transaction safe to spend.
    "blockhash": "hashvalue", (string) The block hash containing the transaction. Available for 'send' and 'receive'
                                          category of transactions.
    "blockindex": n,          (numeric) The index of the transaction in the block that includes it. Available for 'send' and 'receive'
                                          category of transactions.
    "blocktime": xxx,         (numeric) The block time in seconds since epoch (1 Jan 1970 GMT).
    "txid": "transactionid", (string) The transaction id. Available for 'send' and 'receive' category of transactions.
    "time": xxx,              (numeric) The transaction time in seconds since epoch (midnight Jan 1 1970 GMT).
    "timereceived": xxx,      (numeric) The time received in seconds since epoch (midnight Jan 1 1970 GMT). Available
                                          for 'send' and 'receive' category of transactions.
    "comment": "...",       (string) If a comment is associated with the transaction.
    "otheraccount": "accountname",  (string) DEPRECATED. For the 'move' category of transactions, the account the funds came
                                          from (for receiving funds, positive amounts), or went to (for sending funds,
                                          negative amounts).
    "bip125-replaceable": "yes|no|unknown",  (string) Whether this transaction could be replaced due to BIP125 (replace-by-fee);
                                                     may be unknown for unconfirmed transactions not in the mempool
    "abandoned": xxx          (bool) 'true' if the transaction has been abandoned (inputs are respendable). Only available for the
                                         'send' category of transactions.
  }
]
```

**Examples**

```text
List the most recent 10 transactions in the systems
> aokchain-cli listtransactions

List transactions 100 to 120
> aokchain-cli listtransactions "*" 20 100

As a json rpc call
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "listtransactions", "params": ["*", 20, 100] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### listunspent

```text
listunspent ( minconf maxconf  ["addresses",...] [include_unsafe] [query_options])
```

Returns array of unspent transaction outputs with between minconf and maxconf (inclusive) confirmations. Optionally filter to only include txouts paid to specified addresses.

**Arguments**

```text
1. minconf          (numeric, optional, default=1) The minimum confirmations to filter
2. maxconf          (numeric, optional, default=9999999) The maximum confirmations to filter
3. "addresses"      (string) A json array of aokchain addresses to filter
    [
      "address"     (string) aokchain address
      ,...
    ]
4. include_unsafe (bool, optional, default=true) Include outputs that are not safe to spend
                  See description of "safe" attribute below.
5. query_options    (json, optional) JSON with query options
    {
      "minimumAmount"    (numeric or string, default=0) Minimum value of each UTXO in AOK
      "maximumAmount"    (numeric or string, default=unlimited) Maximum value of each UTXO in AOK
      "maximumCount"     (numeric or string, default=unlimited) Maximum number of UTXOs
      "minimumSumAmount" (numeric or string, default=unlimited) Minimum sum value of all UTXOs in AOK
    }
```

**Result**

```text
[                   (array of json object)
  {
    "txid" : "txid",          (string) the transaction id
    "vout" : n,               (numeric) the vout value
    "address" : "address",    (string) the aokchain address
    "label" : "label",        (string) The associated label, or "" for the default label
    "account" : "account",    (string) DEPRECATED. Backwards compatible alias for label.
    "scriptPubKey" : "key",   (string) the script key
    "amount" : x.xxx,         (numeric) the transaction output amount in AOK
    "confirmations" : n,      (numeric) The number of confirmations
    "redeemScript" : n        (string) The redeemScript if scriptPubKey is P2SH
    "spendable" : xxx,        (bool) Whether we have the private keys to spend this output
    "solvable" : xxx,         (bool) Whether we know how to spend this output, ignoring the lack of keys
    "safe" : xxx              (bool) Whether this output is considered safe to spend. Unconfirmed transactions
                              from outside keys and unconfirmed replacement transactions are considered unsafe
                              and are not eligible for spending by fundrawtransaction and sendtoaddress.
  }
  ,...
]
```

**Examples**

```text
> aokchain-cli listunspent
> aokchain-cli listunspent 6 9999999 "[\"1PGFqEzfmQch1gKD3ra4k18PNj3tTUUSqg\",\"1LtvqCaApEdUGFkpKMM4MstjcaL4dKg8SP\"]"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "listunspent", "params": [6, 9999999 "[\"1PGFqEzfmQch1gKD3ra4k18PNj3tTUUSqg\",\"1LtvqCaApEdUGFkpKMM4MstjcaL4dKg8SP\"]"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
> aokchain-cli listunspent 6 9999999 '[]' true '{ "minimumAmount": 0.005 }'
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "listunspent", "params": [6, 9999999, [] , true, { "minimumAmount": 0.005 } ] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### listunspenttoken

```text
listunspenttoken ( token_name minconf maxconf  ["addresses",...] [include_unsafe] [query_options])
```

Returns array of unspent transaction outputs with between minconf and maxconf (inclusive) confirmations. Optionally filter to only include txouts paid to specified addresses.

**Arguments**

```text
1. name             (string) Name of the token
2. minconf          (numeric, optional, default=1) The minimum confirmations to filter
3. maxconf          (numeric, optional, default=9999999) The maximum confirmations to filter
4. "addresses"      (string) A json array of aokchain addresses to filter
    [
      "address"     (string) aokchain address
      ,...
    ]
5. include_unsafe (bool, optional, default=true) Include outputs that are not safe to spend
                  See description of "safe" attribute below.
6. query_options    (json, optional) JSON with query options
    {
      "minimumAmount"    (numeric or string, default=0) Minimum value of each UTXO in AOK
      "maximumAmount"    (numeric or string, default=unlimited) Maximum value of each UTXO in AOK
      "maximumCount"     (numeric or string, default=unlimited) Maximum number of UTXOs
      "minimumSumAmount" (numeric or string, default=unlimited) Minimum sum value of all UTXOs in AOK
    }
```

**Result**

```text
[                   (array of json object)
  {
    "txid" : "txid",          (string) the transaction id
    "vout" : n,               (numeric) the vout value
    "address" : "address",    (string) the aokchain address
    "label" : "label",        (string) The associated label, or "" for the default label
    "account" : "account",    (string) DEPRECATED. Backwards compatible alias for label.
    "scriptPubKey" : "key",   (string) the script key
    "amount" : x.xxx,         (numeric) the transaction output amount in AOK
    "confirmations" : n,      (numeric) The number of confirmations
    "redeemScript" : n        (string) The redeemScript if scriptPubKey is P2SH
    "spendable" : xxx,        (bool) Whether we have the private keys to spend this output
    "solvable" : xxx,         (bool) Whether we know how to spend this output, ignoring the lack of keys
    "safe" : xxx              (bool) Whether this output is considered safe to spend. Unconfirmed transactions
                              from outside keys and unconfirmed replacement transactions are considered unsafe
                              and are not eligible for spending by fundrawtransaction and sendtoaddress.
  }
  ,...
]
```

**Examples**

```text
> aokchain-cli listunspenttoken
> aokchain-cli listunspenttoken EXAMPLE 6 9999999 "[\"1PGFqEzfmQch1gKD3ra4k18PNj3tTUUSqg\",\"1LtvqCaApEdUGFkpKMM4MstjcaL4dKg8SP\"]"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "listunspenttoken", "params": [EXAMPLE 6, 9999999 "[\"1PGFqEzfmQch1gKD3ra4k18PNj3tTUUSqg\",\"1LtvqCaApEdUGFkpKMM4MstjcaL4dKg8SP\"]"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
> aokchain-cli listunspenttoken EXAMPLE 6 9999999 '[]' true '{ "minimumAmount": 0.005 }'
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "listunspenttoken", "params": [EXAMPLE 6, 9999999, [] , true, { "minimumAmount": 0.005 } ] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### listwalletdir

```text
listwalletdir
```

Returns a list of wallets in the wallet directory.

```text
{
  "wallets" : [                (json array of objects)
    {
      "name" : "name"          (string) The wallet name
    }
    ,...
  ]
}
```

**Examples**

```text
> aokchain-cli listwalletdir
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "listwalletdir", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### listwallets

```text
listwallets
```

Returns a list of currently loaded wallets. For full information on the wallet, use "getwalletinfo"

**Result**

```text
[                         (json array of strings)
  "walletname"            (string) the wallet name
   ...
]
```

**Examples**

```text
> aokchain-cli listwallets
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "listwallets", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### loadwallet

```text
loadwallet "filename"
```

Loads a wallet from a wallet file or directory. Note that all wallet command-line options used when starting bitcoind will be applied to the new wallet (eg -zapwallettxes, upgradewallet, rescan, etc).

**Arguments**

```text
1. "filename"    (string, required) The wallet directory or .dat file.
```

**Result**

```text
{
  "name" :    <wallet_name>,        (string) The wallet name if loaded successfully.
  "warning" : <warning>,            (string) Warning message if wallet was not loaded cleanly.
}
```

**Examples**

```text
> aokchain-cli loadwallet "test.dat"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "loadwallet", "params": ["test.dat"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### lockunspent

```text
lockunspent unlock ([{"txid":"txid","vout":n},...])
```

Updates list of temporarily unspendable outputs. Temporarily lock (unlock=false) or unlock (unlock=true) specified transaction outputs. If no transaction outputs are specified when unlocking then all current locked transaction outputs are unlocked. A locked transaction output will not be chosen by automatic coin selection, when spending aokchains. Locks are stored in memory only. Nodes start with zero locked outputs, and the locked output list is always cleared (by virtue of process exit) when a node stops or fails. Also see the listunspent call

**Arguments**

```text
1. unlock            (boolean, required) Whether to unlock (true) or lock (false) the specified transactions
2. "transactions"  (string, optional) A json array of objects. Each object the txid (string) vout (numeric)
     [           (json array of json objects)
       {
         "txid":"id",    (string) The transaction id
         "vout": n         (numeric) The output number
       }
       ,...
     ]
```

**Result**

```text
true|false    (boolean) Whether the command was successful or not
```

**Examples**

```text
List the unspent transactions
> aokchain-cli listunspent

Lock an unspent transaction
> aokchain-cli lockunspent false "[{\"txid\":\"a08e6907dbbd3d809776dbfc5d82e371b764ed838b5655e72f463568df1aadf0\",\"vout\":1}]"

List the locked transactions
> aokchain-cli listlockunspent

Unlock the transaction again
> aokchain-cli lockunspent true "[{\"txid\":\"a08e6907dbbd3d809776dbfc5d82e371b764ed838b5655e72f463568df1aadf0\",\"vout\":1}]"

As a json rpc call
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "lockunspent", "params": [false, "[{\"txid\":\"a08e6907dbbd3d809776dbfc5d82e371b764ed838b5655e72f463568df1aadf0\",\"vout\":1}]"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### move

```text
move "fromaccount" "toaccount" amount ( minconf "comment" )
```

DEPRECATED. Move a specified amount from one account in your wallet to another.

**Arguments**

```text
1. "fromaccount"   (string, required) The name of the account to move funds from. May be the default account using "".
2. "toaccount"     (string, required) The name of the account to move funds to. May be the default account using "".
3. amount            (numeric) Quantity of AOK to move between accounts.
4. (dummy)           (numeric, optional) Ignored. Remains for backward compatibility.
5. "comment"       (string, optional) An optional comment, stored in the wallet only.
```

**Result**

```text
true|false           (boolean) true if successful.
```

**Examples**

```text
Move 0.01 AOK from the default account to the account named tabby
> aokchain-cli move "" "tabby" 0.01

Move 0.01 AOK timotei to akiko with a comment and funds have 6 confirmations
> aokchain-cli move "timotei" "akiko" 0.01 6 "happy birthday!"

As a json rpc call
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "move", "params": ["timotei", "akiko", 0.01, 6, "happy birthday!"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### purgeorphanstakes

```text
purgeorphanstakes ( minage )
```

Deletes this wallet's orphaned coinstake transactions from the wallet. A coinstake is orphaned when the block it was staked in lost against another block. The wallet abandons it and frees the staked coins at that moment, but keeps the transaction forever, which makes the wallet file and its loading time grow on a staking wallet. Balances are not affected. If the orphaned block ever becomes part of the best chain again, the transaction is added back.

**Arguments**

```text
1. minage    (numeric, optional, default=86400) Only delete transactions the wallet received at least this many seconds ago
```

**Result**

```text
n            (numeric) The number of transactions deleted
```

**Examples**

```text
> aokchain-cli purgeorphanstakes
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "purgeorphanstakes", "params": [3600] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### removeaddress

```text
importaddress "address" ( "label" rescan p2sh )
```

> [!NOTE]
> The usage line of this help text names `importaddress`; the command is `removeaddress`.

Remove a script (in hex) or address that can be watched as if it were in your wallet but cannot be used to spend.

**Arguments**

```text
1. "script"           (string, required) The hex-encoded script (or address)

Note: This call can take minutes to complete if rescan is true.
If you have the full public key, you should call importpubkey instead of this.
```

**Examples**

```text
Remove a script with rescan
> aokchain-cli removeaddress "myscript"
```

### removeprunedfunds

```text
removeprunedfunds "txid"
```

Deletes the specified transaction from the wallet. Meant for use with pruned wallets and as a companion to importprunedfunds. This will affect wallet balances.

**Arguments**

```text
1. "txid"           (string, required) The hex-encoded id of the transaction you are deleting
```

**Examples**

```text
> aokchain-cli removeprunedfunds "a8d0c0184dde994a09ec054286f1ce581bebf46446a512166eae7628734ea0a5"

As a JSON-RPC call
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "removeprunedfunds", "params": ["a8d0c0184dde994a09ec054286f1ce581bebf46446a512166eae7628734ea0a5"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### rescanblockchain

```text
rescanblockchain ("start_height") ("stop_height")
```

Rescan the local blockchain for wallet related transactions.

**Arguments**

```text
1. "start_height"    (numeric, optional) block height where the rescan should start
2. "stop_height"     (numeric, optional) the last block height that should be scanned
```

**Result**

```text
{
  "start_height"     (numeric) The block height where the rescan has started. If omitted, rescan started from the genesis block.
  "stop_height"      (numeric) The height of the last rescanned block. If omitted, rescan stopped at the chain tip.
}
```

**Examples**

```text
> aokchain-cli rescanblockchain 100000 120000
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "rescanblockchain", "params": [100000, 120000] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### restorewallet

```text
restorewallet "wallet_name" "backup_file"
```

Restores a wallet from a backup file (of backupwallet, or a copy of a wallet.dat) and loads it. The backup is copied to the folder &lt;wallet\_name&gt; in the wallet directory; the backup file itself is not changed. What happened to the wallet after the backup is found by the rescan that loading does.

**Arguments**

```text
1. "wallet_name"    (string, required) The name of the new wallet; there must be no wallet of that name
2. "backup_file"    (string, required) The backup file to restore from
```

**Result**

```text
{
  "name" :    <wallet_name>,        (string) The wallet name if restored successfully.
  "warning" : <warning>,            (string) Warning message if wallet was not loaded cleanly.
}
```

**Examples**

```text
> aokchain-cli restorewallet "restored" "/home/user/backup.dat"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "restorewallet", "params": ["restored", "/home/user/backup.dat"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### sendfrom

```text
sendfrom "fromaccount" "toaddress" amount ( minconf "comment" "comment_to" )
```

DEPRECATED (use sendtoaddress). Sent an amount from an account to a aokchain address. Requires wallet passphrase to be set with walletpassphrase call.

**Arguments**

```text
1. "fromaccount"       (string, required) The name of the account to send funds from. May be the default account using "".
                       Specifying an account does not influence coin selection, but it does associate the newly created
                       transaction with the account, so the account's balance computation and transaction history can reflect
                       the spend.
2. "toaddress"         (string, required) The aokchain address to send funds to.
3. amount                (numeric or string, required) The amount in AOK (transaction fee is added on top).
4. "lock_time"          (integer, optional, default=0) Locktime for transaction, could be height or timestamp
5. minconf               (numeric, optional, default=1) Only use funds with at least this many confirmations.
6. "comment"           (string, optional) A comment used to store what the transaction is for.
                                     This is not part of the transaction, just kept in your wallet.
7. "comment_to"        (string, optional) An optional comment to store the name of the person or organization
                                     to which you're sending the transaction. This is not part of the transaction,
                                     it is just kept in your wallet.
8. subtractfeefromamount  (boolean, optional, default=false) The fee will be deducted from the amount being sent.
```

**Result**

```text
"txid"                 (string) The transaction id.
```

**Examples**

```text
Send 0.01 AOK from the default account to the address, must have at least 1 confirmation
> aokchain-cli sendfrom "" "1M72Sfpbz1BPpXFHz9m3CdqATR44Jvaydd" 0.01

Send 0.01 from the tabby account to the given address, funds must have at least 6 confirmations
> aokchain-cli sendfrom "tabby" "1M72Sfpbz1BPpXFHz9m3CdqATR44Jvaydd" 0.01 6 "donation" "seans outpost"

As a json rpc call
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "sendfrom", "params": ["tabby", "1M72Sfpbz1BPpXFHz9m3CdqATR44Jvaydd", 0.01, 6, "donation", "seans outpost"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### sendmany

```text
sendmany "fromaccount" {"address":amount,...} ( minconf "message" ["address",...] replaceable conf_target "estimate_mode")
```

Send multiple times. Amounts are double-precision floating point numbers. Requires wallet passphrase to be set with walletpassphrase call.

**Arguments**

```text
1. "fromaccount"         (string, required) DEPRECATED. The account to send the funds from. Should be "" for the default account
2. "amounts"             (string, required) A json object with addresses and amounts
    {
      "address":amount   (numeric or string) The aokchain address is the key, the numeric amount (can be string) in AOK is the value
      ,...
    }
3. minconf                 (numeric, optional, default=1) Only use the balance confirmed at least this many times.
4. "message"             (string, optional, default=) Message attached to transaction.
5. subtractfeefrom         (array, optional) A json array with addresses.
                           The fee will be equally deducted from the amount of each selected address.
                           Those recipients will receive less aokchains than you enter in their corresponding amount field.
                           If no addresses are specified here, the sender pays the fee.
    [
      "address"          (string) Subtract fee from this address
      ,...
    ]
6. conf_target            (numeric, optional) Confirmation target (in blocks)
7. "estimate_mode"      (string, optional, default=UNSET) The fee estimate mode, must be one of:
       "UNSET"
       "ECONOMICAL"
       "CONSERVATIVE"
```

**Result**

```text
"txid"                   (string) The transaction id for the send. Only 1 transaction is created regardless of
                                    the number of addresses.
```

**Examples**

```text
Send two amounts to two different addresses:
> aokchain-cli sendmany "" "{\"1D1ZrZNe3JUo7ZycKEYQQiQAWd9y54F4XX\":0.01,\"1353tsE8YMTA4EuV7dgUXGjNFf9KpVvKHz\":0.02}"

Send two amounts to two different addresses setting the confirmation and comment:
> aokchain-cli sendmany "" "{\"1D1ZrZNe3JUo7ZycKEYQQiQAWd9y54F4XX\":0.01,\"1353tsE8YMTA4EuV7dgUXGjNFf9KpVvKHz\":0.02}" 6 "testing"

Send two amounts to two different addresses, subtract fee from amount:
> aokchain-cli sendmany "" "{\"1D1ZrZNe3JUo7ZycKEYQQiQAWd9y54F4XX\":0.01,\"1353tsE8YMTA4EuV7dgUXGjNFf9KpVvKHz\":0.02}" 1 "" "[\"1D1ZrZNe3JUo7ZycKEYQQiQAWd9y54F4XX\",\"1353tsE8YMTA4EuV7dgUXGjNFf9KpVvKHz\"]"

As a json rpc call
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "sendmany", "params": ["", "{\"1D1ZrZNe3JUo7ZycKEYQQiQAWd9y54F4XX\":0.01,\"1353tsE8YMTA4EuV7dgUXGjNFf9KpVvKHz\":0.02}", 6, "testing"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### sendtoaddress

```text
sendtoaddress "address" amount ( "message" "comment_to" subtractfeefromamount replaceable conf_target "estimate_mode")
```

Send an amount to a given address.

Requires wallet passphrase to be set with walletpassphrase call.

**Arguments**

```text
1. "address"            (string, required) The aokchain address to send to.
2. "amount"             (numeric or string, required) The amount in AOK to send. eg 0.1
3. "lock_time"          (integer, optional, default=0) Locktime for transaction, could be height or timestamp
5. "message"            (string, optional, default=) Message attached to transaction.
                             This is not part of the transaction, just kept in your wallet.
5. "comment_to"         (string, optional) A comment to store the name of the person or organization
                             to which you're sending the transaction. This is not part of the
                             transaction, just kept in your wallet.
6. subtractfeefromamount  (boolean, optional, default=false) The fee will be deducted from the amount being sent.
                             The recipient will receive less aokchains than you enter in the amount field.
7. conf_target            (numeric, optional) Confirmation target (in blocks)
8. "estimate_mode"      (string, optional, default=UNSET) The fee estimate mode, must be one of:
       "UNSET"
       "ECONOMICAL"
       "CONSERVATIVE"
```

**Result**

```text
"txid"                  (string) The transaction id.
```

**Examples**

```text
> aokchain-cli sendtoaddress "1M72Sfpbz1BPpXFHz9m3CdqATR44Jvaydd" 0.1
> aokchain-cli sendtoaddress "1M72Sfpbz1BPpXFHz9m3CdqATR44Jvaydd" 0.1 "donation" "seans outpost"
> aokchain-cli sendtoaddress "1M72Sfpbz1BPpXFHz9m3CdqATR44Jvaydd" 0.1 "" "" true
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "sendtoaddress", "params": ["1M72Sfpbz1BPpXFHz9m3CdqATR44Jvaydd", 0.1, "donation", "seans outpost"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### setlabel

```text
setlabel "address" "label"
```

Sets the label associated with the given address.

**Arguments**

```text
1. "address"         (string, required) The bitcoin address to be associated with a label.
2. "label"           (string, required) The label to assign to the address.
```

**Examples**

```text
> aokchain-cli setlabel "1D1ZrZNe3JUo7ZycKEYQQiQAWd9y54F4XX" "tabby"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "setlabel", "params": ["1D1ZrZNe3JUo7ZycKEYQQiQAWd9y54F4XX", "tabby"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### settxfee

```text
settxfee amount
```

Set the transaction fee per kB. Overwrites the paytxfee parameter.

**Arguments**

```text
1. amount         (numeric or string, required) The transaction fee in AOK/kB
```

**Result**

```text
true|false        (boolean) Returns true if successful
```

**Examples**

```text
> aokchain-cli settxfee 0.00001
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "settxfee", "params": [0.00001] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### signmessage

```text
signmessage "address" "message"
```

Sign a message with the private key of an address Requires wallet passphrase to be set with walletpassphrase call.

**Arguments**

```text
1. "address"         (string, required) The aokchain address to use for the private key.
2. "message"         (string, required) The message to create a signature of.
```

**Result**

```text
"signature"          (string) The signature of the message encoded in base 64
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
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "signmessage", "params": ["1D1ZrZNe3JUo7ZycKEYQQiQAWd9y54F4XX", "my message"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### unloadwallet

```text
unloadwallet ( "wallet_name" )
```

Unloads a wallet that was loaded with loadwallet, createwallet or a second -wallet option. The wallet is taken from the request endpoint (/wallet/&lt;name&gt;) if no name is given. The first wallet cannot be unloaded: it stakes, and the GUI shows it. To run without it, restart the node with another -wallet option.

**Arguments**

```text
1. "wallet_name"    (string, optional) The name of the wallet to unload, as listwallets shows it.
```

**Examples**

```text
> aokchain-cli unloadwallet "test.dat"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "unloadwallet", "params": ["test.dat"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### walletlock

```text
walletlock
```

Removes the wallet encryption key from memory, locking the wallet. After calling this method, you will need to call walletpassphrase again before being able to call any methods which require the wallet to be unlocked.

**Examples**

```text
Set the passphrase for 2 minutes to perform a transaction
> aokchain-cli walletpassphrase "my pass phrase" 120

Perform a send (requires passphrase set)
> aokchain-cli sendtoaddress "1M72Sfpbz1BPpXFHz9m3CdqATR44Jvaydd" 1.0

Clear the passphrase since we are done before 2 minutes is up
> aokchain-cli walletlock

As json rpc call
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "walletlock", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### walletpassphrase

```text
walletpassphrase "passphrase" timeout
```

Stores the wallet decryption key in memory for 'timeout' seconds. This is needed prior to performing transactions related to private keys such as sending aokchains

**Arguments**

```text
1. "passphrase"     (string, required) The wallet passphrase
2. timeout            (numeric, required) The time to keep the decryption key in seconds.
3. stakingonly        (bool, optional, default=false) Unlock wallet for staking only. With a timeout of 0
                      the wallet then stays open for staking until it is locked or the node stops.

Note:
Issuing the walletpassphrase command while the wallet is already unlocked will set a new unlock
time that overrides the old one.
```

**Examples**

```text
Unlock the wallet for 60 seconds
> aokchain-cli walletpassphrase "my pass phrase" 60

Lock the wallet again (before 60 seconds)
> aokchain-cli walletlock

As json rpc call
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "walletpassphrase", "params": ["my pass phrase", 60] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### walletpassphrasechange

```text
walletpassphrasechange "oldpassphrase" "newpassphrase"
```

Changes the wallet passphrase from 'oldpassphrase' to 'newpassphrase'.

**Arguments**

```text
1. "oldpassphrase"      (string) The current passphrase
2. "newpassphrase"      (string) The new passphrase
```

**Examples**

```text
> aokchain-cli walletpassphrasechange "old one" "new one"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "walletpassphrasechange", "params": ["old one", "new one"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```
