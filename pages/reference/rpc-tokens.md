---
title: "RPC: Tokens"
description: "RPC reference: issuing, reissuing, transferring and looking up tokens and usernames."
order: 27
generated_by: tools/rpc_reference.py
---

The help text of every command in the tokens category, as AokChain Core 4.0.7 prints it with `aokchain-cli help <command>`. All categories are on [[rpc]].

> [!NOTE]
> Many examples in these help texts come from the upstream code: their addresses are often
> Bitcoin addresses, and their `curl` lines use port 8766. An AokChain node answers JSON-RPC on
> port 33440 (mainnet) or 44550 (testnet and regtest) unless `rpcport` says otherwise; see [[json-rpc]].

| Command | Summary |
|---|---|
| [getcacheinfo](#getcacheinfo) |  |
| [gettokendata](#gettokendata) | Returns tokens metadata if that token exists |
| [getusernameaddress](#getusernameaddress) |  |
| [issue](#issue) | Issue an token, subtoken or unique token. |
| [issueunique](#issueunique) | Issue unique token(s). |
| [listaddressesbytoken](#listaddressesbytoken) | Returns a list of all address that own the given token (with balances) |
| [listmylockedtokens](#listmylockedtokens) | Returns a list of all locked token that are owned by this wallet |
| [listmytokens](#listmytokens) | Returns a list of all token that are owned by this wallet |
| [listtokenbalancesbyaddress](#listtokenbalancesbyaddress) | Returns a list of all token balances for an address. |
| [listtokens](#listtokens) | Returns a list of all tokens |
| [listuniquetokenholders](#listuniquetokenholders) | Returns a list holders of unique |
| [registerusername](#registerusername) |  |
| [reissue](#reissue) | Reissues a quantity of an token to an owned address if you own the Owner Token |
| [transfer](#transfer) | Transfers a quantity of an owned token to a given address |
| [transferfromaddress](#transferfromaddress) | Transfer a quantity of an owned token in a specific address to a given address |
| [transfermany](#transfermany) | Send multiple times. |
| [transfermanyoutputs](#transfermanyoutputs) | Send transaction with multiple outputs. |

### getcacheinfo

```text
getcacheinfo
```

**Result**

```text
[
  uxto cache size:
  token total (exclude dirty):
  token address map:
  token address balance:
  my unspent token:
  reissue data:
  token metadata map:
  token metadata list (est):
  dirty cache (est):
]
```

**Examples**

```text
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getcacheinfo", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
> aokchain-cli getcacheinfo
```

### gettokendata

```text
gettokendata "token_name"
```

Returns tokens metadata if that token exists

**Arguments**

```text
1. "token_name"               (string, required) the name of the token
```

**Result**

```text
{
  name: (string),
  amount: (number),
  units: (number),
  reissuable: (number),
  has_ipfs: (number),
  ipfs_hash: (hash) (only if has_ipfs = 1)
}
```

**Examples**

```text
> aokchain-cli getalltokens "TOKEN_NAME"
```

### getusernameaddress

```text
getusernameaddress @USERNAME
```

**Example**

```text
> aokchain-cli getusernameaddress @USERNAME
```

### issue

```text
issue "token_name" qty "( to_address )" "( change_address )" ( units ) ( reissuable ) ( has_ipfs ) "( ipfs_hash )
```

Issue an token, subtoken or unique token. Token name must not conflict with any existing token. Unit as the number of decimals precision for the token (0 for whole units ("1"), 8 for max precision ("1.00000000") Reissuable is true/false for whether additional units can be issued by the original issuer. If issuing a unique token these values are required (and will be defaulted to): qty=1, units=0, reissuable=false.

**Arguments**

```text
1. "token_name"            (string, required) a unique name
2. "qty"                   (numeric, optional, default=1) the number of units to be issued
3. "to_address"            (string), optional, default=""), address token will be sent to, if it is empty, address will be generated for you
4. "change_address"        (string), optional, default=""), address the the AOK change will be sent to, if it is empty, change address will be generated for you
5. "units"                 (integer, optional, default=0, min=0, max=8), the number of decimals precision for the token (0 for whole units ("1"), 8 for max precision ("1.00000000")
6. "reissuable"            (boolean, optional, default=true (false for unique tokens)), whether future reissuance is allowed
7. "has_ipfs"              (boolean, optional, default=false), whether ifps hash is going to be added to the token
8. "ipfs_hash"             (string, optional but required if has_ipfs = 1), an ipfs hash (only sha2-256 hashes currently supported -- Qm...)
```

**Result**

```text
"txid"                     (string) The transaction id
```

**Examples**

```text
> aokchain-cli issue "TOKEN_NAME" 1000
> aokchain-cli issue "TOKEN_NAME" 1000 "myaddress"
> aokchain-cli issue "TOKEN_NAME" 1000 "myaddress" "changeaddress" 4
> aokchain-cli issue "TOKEN_NAME" 1000 "myaddress" "changeaddress" 2 true
> aokchain-cli issue "TOKEN_NAME" 1000 "myaddress" "changeaddress" 8 false true Qma21aBaw7pZmt1nV5MZKuGGeamDiZY34UbErV949wv2pg
> aokchain-cli issue "TOKEN_NAME/SUB_TOKEN" 1000 "myaddress" "changeaddress" 2 true
> aokchain-cli issue "TOKEN_NAME#uniquetag"
```

### issueunique

```text
issueunique "root_name" [token_tags] ( [ipfs_hashes] ) "( to_address )" "( change_address )"
```

Issue unique token(s). root\_name is a token or a sub token whose owner token (root\_name!) is in the wallet. A token root\_name#tag will be created for each element of token\_tags. If provided ipfs\_hashes must be the same length as token\_tags. Each unique token costs the fee for a unique token in AOK, paid to the token fee address (issuanceinfo shows the fee and the address).

**Arguments**

```text
1. "root_name"             (string, required) name of the token or sub token the unique token(s) are being issued under
2. "token_tags"            (array, required) the unique tag for each token which is to be issued
3. "ipfs_hashes"           (array, optional) ipfs hashes corresponding to each supplied tag (should be same size as "token_tags") (only sha2-256 hashes currently supported -- Qm...)
4. "to_address"            (string, optional, default=""), address tokens will be sent to, if it is empty, address will be generated for you
5. "change_address"        (string, optional, default=""), address the the AOK change will be sent to, if it is empty, change address will be generated for you
```

**Result**

```text
"txid"                     (string) The transaction id
```

**Examples**

```text
> aokchain-cli issueunique "MY_TOKEN" '["primo","secundo"]'
> aokchain-cli issueunique "MY_TOKEN" '["primo","secundo"]' '["first_hash","second_hash"]'
> aokchain-cli issueunique "MY_TOKEN/SUB_TOKEN" '["primo"]'
```

### listaddressesbytoken

```text
listaddressesbytoken "token_name" (onlytotal) (count) (start)
```

Returns a list of all address that own the given token (with balances) Or returns the total size of how many address own the given token

**Arguments**

```text
1. "token_name"               (string, required) name of token
2. "onlytotal"                (boolean, optional, default=false) when false result is just a list of addresses with balances -- when true the result is just a single number representing the number of addresses
3. "count"                    (integer, optional, default=50000, MAX=50000) truncates results to include only the first _count_ tokens found
4. "start"                    (integer, optional, default=0) results skip over the first _start_ tokens found (if negative it skips back from the end)
```

**Result**

```text
[   (address): balance,
  ...
]
```

**Examples**

```text
> aokchain-cli listaddressesbytoken "TOKEN_NAME" false 2 0
> aokchain-cli listaddressesbytoken "TOKEN_NAME" true
> aokchain-cli listaddressesbytoken "TOKEN_NAME"
```

### listmylockedtokens

```text
listmylockedtokens "( token )" ( verbose ) ( count ) ( start )
```

Returns a list of all locked token that are owned by this wallet

**Arguments**

```text
1. "token"                    (string, optional, default="*") filters results -- must be an token name or a partial token name followed by '*' ('*' matches all trailing characters)
2. "verbose"                  (boolean, optional, default=false) when false results only contain balances -- when true results include outpoints
3. "count"                    (integer, optional, default=ALL) truncates results to include only the first _count_ tokens found
4. "start"                    (integer, optional, default=0) results skip over the first _start_ tokens found (if negative it skips back from the end)
```

**Result (verbose=false)**

```text
{
  (token_name): balance,
  ...
}
```

**Result (verbose=true)**

```text
{
  (token_name):
    {
      "balance": balance,
      "outpoints":
        [
          {
            "txid": txid,
            "vout": vout,
            "amount": amount
          }
          {...}, {...}
        ]
    }
}
{...}, {...}
```

**Examples**

```text
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "listmylockedtokens", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
> aokchain-cli listmylockedtokens TOKEN
> aokchain-cli listmylockedtokens "TOKEN*" true 10 20
```

### listmytokens

```text
listmytokens "( token )" ( verbose ) ( count ) ( start )
```

Returns a list of all token that are owned by this wallet

**Arguments**

```text
1. "token"                    (string, optional, default="*") filters results -- must be an token name or a partial token name followed by '*' ('*' matches all trailing characters)
2. "verbose"                  (boolean, optional, default=false) when false results only contain balances -- when true results include outpoints
3. "count"                    (integer, optional, default=ALL) truncates results to include only the first _count_ tokens found
4. "start"                    (integer, optional, default=0) results skip over the first _start_ tokens found (if negative it skips back from the end)
```

**Result (verbose=false)**

```text
{
  (token_name): balance,
  ...
}
```

**Result (verbose=true)**

```text
{
  (token_name):
    {
      "balance": balance,
      "outpoints":
        [
          {
            "txid": txid,
            "vout": vout,
            "amount": amount
          }
          {...}, {...}
        ]
    }
}
{...}, {...}
```

**Examples**

```text
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "listmytokens", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
> aokchain-cli listmytokens TOKEN
> aokchain-cli listmytokens "TOKEN*" true 10 20
```

### listtokenbalancesbyaddress

```text
listtokenbalancesbyaddress "address" (onlytotal) (count) (start)
```

Returns a list of all token balances for an address.

**Arguments**

```text
1. "address"                  (string, required) a aokchain address
2. "onlytotal"                (boolean, optional, default=false) when false result is just a list of tokens balances -- when true the result is just a single number representing the number of tokens
3. "count"                    (integer, optional, default=50000, MAX=50000) truncates results to include only the first _count_ tokens found
4. "start"                    (integer, optional, default=0) results skip over the first _start_ tokens found (if negative it skips back from the end)
```

**Result**

```text
{
  (token_name) : (quantity),
  ...
}
```

**Examples**

```text
> aokchain-cli listtokenbalancesbyaddress "myaddress" false 2 0
> aokchain-cli listtokenbalancesbyaddress "myaddress" true
> aokchain-cli listtokenbalancesbyaddress "myaddress"
```

### listtokens

```text
listtokens "( token )" ( verbose ) ( count ) ( start )
```

Returns a list of all tokens

This could be a slow/expensive operation as it reads from the database

**Arguments**

```text
1. "token"                    (string, optional, default="*") filters results -- must be an token name or a partial token name followed by '*' ('*' matches all trailing characters)
2. "verbose"                  (boolean, optional, default=false) when false result is just a list of token names -- when true results are token name mapped to metadata
3. "count"                    (integer, optional, default=ALL) truncates results to include only the first _count_ tokens found
4. "start"                    (integer, optional, default=0) results skip over the first _start_ tokens found (if negative it skips back from the end)
```

**Result (verbose=false)**

```text
[
  token_name,
  ...
]
```

**Result (verbose=true)**

```text
{
  (token_name):
    {
      amount: (number),
      units: (number),
      reissuable: (number),
      has_ipfs: (number),
      ipfs_hash: (hash) (only if has_ipfs = 1)
    },
  {...}, {...}
}
```

**Examples**

```text
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "listtokens", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
> aokchain-cli listtokens TOKEN
> aokchain-cli listtokens "TOKEN*" true 10 20
```

### listuniquetokenholders

```text
listuniquetokenholders ["TOKEN_NAME"]
```

Returns a list holders of unique

**Arguments**

```text
1. "tokens"               (string, required) Array of token names
```

**Result**

```text
{
  (token_name) : (holders),
  ...
}
```

**Examples**

```text
> aokchain-cli listuniquetokenholders ["TOKEN_NAME"]
```

### registerusername

```text
registerusername "username" "( to_address )"
```

**Arguments**

```text
1. "username"              (string, required) a unique username: @ followed by at least 4 characters,
                             each one of A-Z 0-9 _ . (at most 31 characters with the @)
2. "to_address"            (string), optional, default=""), address token will be sent to, if it is empty, address will be generated for you
```

**Result**

```text
"txid"                     (string) The transaction id
```

**Examples**

```text
> aokchain-cli registerusername "@USERNAME"
> aokchain-cli registerusername "@USERNAME" "myaddress"
```

### reissue

```text
reissue "token_name" qty "to_address" "change_address" ( reissuable ) ( new_unit ) "( new_ipfs )"
```

Reissues a quantity of an token to an owned address if you own the Owner Token Can change the reissuable flag during reissuance Can change the ipfs hash during reissuance

**Arguments**

```text
1. "token_name"               (string, required) name of token that is being reissued
2. "qty"                      (numeric, required) number of tokens to reissue
3. "to_address"               (string, required) address to send the token to
4. "change_address"           (string, optional) address that the change of the transaction will be sent to
5. "reissuable"               (boolean, optional, default=true), whether future reissuance is allowed
6. "new_unit"                 (numeric, optional, default=-1), the new units that will be associated with the token
7. "new_ifps"                 (string, optional, default=""), whether to update the current ipfshash (only sha2-256 hashes currently supported -- Qm...)
```

**Result**

```text
"txid"                     (string) The transaction id
```

**Examples**

```text
> aokchain-cli reissue "TOKEN_NAME" 20 "address"
> aokchain-cli reissue "TOKEN_NAME" 20 "address" "change_address" "true" 8
> aokchain-cli reissue "TOKEN_NAME" 20 "address" "change_address" "false" 2 Qma21aBaw7pZmt1nV5MZKuGGeamDiZY34UbErV949wv2pg
```

### transfer

```text
transfer "token_name" qty "to_address" "token_lock_time" "message"
```

Transfers a quantity of an owned token to a given address

**Arguments**

```text
1. "token_name"               (string, required) name of token
2. "qty"                      (numeric, required) number of tokens you want to send to the address
3. "to_address"               (string, required) address to send the token to
4. "token_lock_time"          (integer, optional, default=0) Locktime for token UTXOs, could be height or timestamp
5. "message"                  (string, optional, default=) Message attached to transaction.
```

**Result**

```text
txid[
txid
]
```

**Examples**

```text
> aokchain-cli transfer "TOKEN_NAME" 20 "address"
> aokchain-cli transfer "TOKEN_NAME" 20 "address" 120000
```

### transferfromaddress

```text
transferfromaddress "address" "token_name" qty "to_address" "token_lock_time"
```

Transfer a quantity of an owned token in a specific address to a given address

**Arguments**

```text
1. "address"                  (string, required) valid AOK address
2. "token_name"               (string, required) name of token
3. "qty"                      (numeric, required) number of tokens you want to send to the address
4. "to_address"               (string, required) address to send the token to
5. "token_lock_time"          (integer, optional, default=0) Locktime for token UTXOs, could be height or timestamp
```

**Result**

```text
txid[
txid
]
```

**Examples**

```text
> aokchain-cli transferfromaddress "address" "ASSET_NAME" 20 "address" "token_lock_time"
```

### transfermany

```text
transfermany "token_name" {"address":amount,...} "message"
```

Send multiple times. Amounts are double-precision floating point numbers.

**Arguments**

```text
1. "token_name"          (string, required) name of token
2. "amounts"             (object, required) A json object with addresses and amounts
    {
      "address":amount   (numeric or string) The aokchain address is the key, the numeric amount (can be string) in AOK is the value
      ,...
    }
3. "message"             (string, optional, default=) Message attached to transaction.
```

**Result**

```text
"txid"                   (string) The transaction id for the send. Only 1 transaction is created regardless of
                                    the number of addresses.
```

**Examples**

```text
Send two amounts to two different addresses:
> aokchain-cli transfermany "TOKEN_NAME" "{\"1D1ZrZNe3JUo7ZycKEYQQiQAWd9y54F4XX\":0.01,\"1353tsE8YMTA4EuV7dgUXGjNFf9KpVvKHz\":0.02}"
```

### transfermanyoutputs

```text
transfermanyoutputs [{"address":"Kb9ma4bw6aRcB6CrbE67VPzGH8VUyafTrh",...}]
```

Send transaction with multiple outputs.

**Arguments**

```text
1. "outputs"             (array, required) name of token
```

**Result**

```text
"txid"                   (string) The transaction id for the send. Only 1 transaction is created regardless of
                                    the number of addresses.
```

**Examples**

```text
Send two amounts to two different addresses:
> aokchain-cli transfermanyoutputs [{"address":"Kb9ma4bw6aRcB6CrbE67VPzGH8VUyafTrh",...}]
```
