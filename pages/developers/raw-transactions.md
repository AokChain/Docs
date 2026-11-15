---
title: Raw transactions
description: "The AokChain transaction format with its time field, and how to create, fund, sign, check and send transactions with the raw transaction RPCs and aokchain-tx."
order: 30
---

How to build a transaction by hand: the byte format, which differs from Bitcoin's, and the commands that create, sign, check and send it. The full help of each command is on [[rpc-rawtransactions]].

## The format

An AokChain transaction is a Bitcoin transaction with a time after the version:

| Field | Size | Notes |
|---|---|---|
| `version` | 4 bytes, little endian | 1, or 2 for a transaction with a message. Version 2 is standard since the governance height. |
| `time` | 4 bytes, little endian | Unix time of the transaction. |
| inputs | count, then each input | As in Bitcoin: previous txid, output index, script, sequence. |
| outputs | count, then each output | As in Bitcoin: value in satoshis (8 bytes), script. |
| `locktime` | 4 bytes, little endian | As in Bitcoin. |
| `message` | string | Only when `version` is 2 or higher. Public on the chain; `decoderawtransaction` shows it as `message`. |

There is no SegWit on mainnet and testnet. Transaction test vectors and parsers made for Bitcoin do not work unchanged because of the time field. The block format differs too (see [[network-parameters]]).

`aokchain-tx` shows the layout:

```bash
aokchain-tx -create time=1700000000 outaddr=1:KacWDE2Fyqywwr6YDKt1FYthycv3Ee7dqv
```

```text
0100000000f15365000100e1f505000000001976a9142c966965f2218330c3a76188bb105a4bd503abb388ac00000000
```

`01000000` is the version, `00f15365` the time 1700000000, `00` no inputs, `01` one output of `00e1f50500000000` satoshis (1 AOK) to the script after `19`, and `00000000` the lock time.

`decoderawtransaction` and `getrawtransaction <txid> 1` print the transaction time as `timestamp`; `time` and `blocktime` in the answer of `getrawtransaction` are the time of its block.

## Rules for the time

| Rule | Effect |
|---|---|
| A node takes a transaction into its mempool only if its time is at most 10 minutes ahead of the node's clock. | Otherwise: `time-too-new`. |
| A block may contain a transaction only if the block time is not earlier than the transaction time. | A transaction dated in the future waits for a block that late. |
| Below height 695,000 the time also had to be at least the time of every input. | Not enforced at today's heights. |

`createrawtransaction` sets the time to the node's clock. `aokchain-tx -create` starts with time 0; give `time=<unix time>` (this command of `aokchain-tx` is not in its help).

## Create, fund, sign and send

1. **Pick the inputs.** `listunspent` lists the wallet's coins. To let the wallet choose, skip this step and use `fundrawtransaction` in step 3.
2. **Create.** Inputs and outputs in JSON; amounts in AOK:

   ```bash
   aokchain-cli createrawtransaction \
     '[{"txid":"8574966f6199e8fb499f74c75b594639bad716e1b9b62fc2f114662fdde0b469","vout":1}]' \
     '{"Krp9Fwe7rEZm6Y6YxnngFc9to7y1Q4QX9W":9.99}'
   ```

   The third argument is the lock time. An output `"data":"<hex>"` adds a null-data output.
3. **Fund** (optional). `fundrawtransaction <hex>` adds inputs from the wallet, a change output and the fee. It returns `hex`, `fee` and `changepos`.
4. **Sign.**
   - With the wallet's keys: `signrawtransactionwithwallet <hex>`.
   - With given keys, no wallet needed: `signrawtransactionwithkey <hex> '["<WIF key>"]' '[<prevtxs>]'`.
   - `signrawtransaction` does both and stays for programs written for 3.0.x.

   `prevtxs` describes inputs the node does not know: `[{"txid":"...","vout":0,"scriptPubKey":"<hex>","amount":20.0}]`, with `"redeemScript"` for a P2SH input. The answer has `hex` and `complete`, which is `1` when every input is signed; otherwise `errors` names the inputs that still need signatures.
5. **Check.** `testmempoolaccept '["<signed hex>"]'` runs every mempool check and changes nothing. `"allowed": 1`, or `reject-reason`.
6. **Send.** `sendrawtransaction <signed hex>` returns the txid. The second argument is either `true` (allow high fees) or a fee rate in AOK/kB above which the transaction is refused, `0` accepting any fee; without it the limit is `maxtxfee` (10 AOK) for the whole transaction. A fee over the limit gives `absurdly-high-fee`.

Sending a transaction that is already in the mempool returns its txid again. One that is already in a block gives error `-27`.

## Scripts

| Output type | Script | Notes |
|---|---|---|
| Pay to public key hash | `OP_DUP OP_HASH160 <20 bytes> OP_EQUALVERIFY OP_CHECKSIG` | Addresses starting with `K`. |
| Pay to script hash | `OP_HASH160 <20 bytes> OP_EQUAL` | Addresses starting with `k`; multisig, see [[multisig-rpc]]. |
| Pay to public key | `<public key> OP_CHECKSIG` | Stakes pay to a public key. Wallets and the address index show the matching `K` address. |
| Time locked | `<height or time> OP_CHECKLOCKTIMEVERIFY OP_DROP` followed by a pay to public key hash script | Decoded as type `cltv`. A value below 500,000,000 is a height, otherwise a Unix time. |
| Token | a pay to public key hash (or script hash) script, then `OP_TOKEN_SCRIPT` (`0xc0`), one data push, `OP_DROP` | Value 0. See below. |
| Offline staking | begins with `OP_OFFLINE_STAKE` (`0xc6`) | Two keys: one that can only stake, one that spends. Addresses starting with `2` on mainnet. |
| Null data | `OP_RETURN <data>` | Relayed when the whole script is at most 83 bytes (`datacarriersize`). |

To spend a time-locked output, set the transaction's lock time to at least the lock value and the input's sequence below `0xffffffff` (for example `0xfffffffe`).

## Token transfers

A token output carries the token in its script and 0 AOK. The data push of a transfer is:

| Bytes | Contents |
|---|---|
| `616c7074` | `alpt`: an AokChain token transfer |
| 1 byte, then the name | Length and name of the token |
| 8 bytes, little endian | Amount in the token's base unit (10^8 per token) |
| 4 bytes, little endian | Lock: 0, or a height below 500,000,000 or a Unix time before which the output cannot be spent |

The output of 50 `DOCTOKEN` to `KacWDE2Fyqywwr6YDKt1FYthycv3Ee7dqv`:

```text
76a9142c966965f2218330c3a76188bb105a4bd503abb388ac c0 19 616c7074 08 444f43544f4b454e 00f2052a01000000 00000000 75
```

With `createrawtransaction` a transfer is an output object:

```bash
aokchain-cli createrawtransaction \
  '[{"txid":"<AOK input>","vout":0},{"txid":"<token input>","vout":1}]' \
  '{"Krp9Fwe7rEZm6Y6YxnngFc9to7y1Q4QX9W":{"transfer":{"DOCTOKEN":50}},
    "KacWDE2Fyqywwr6YDKt1FYthycv3Ee7dqv":{"transfer":{"DOCTOKEN":950}},
    "KhsXjhrb7hKpz4Mj2n15TrGVKDxz2PnLzd":0.99}'
```

Here the token input holds 1,000 `DOCTOKEN`: 50 go to the recipient, 950 come back, and 0.99 AOK is the AOK change. Each address can appear only once in the JSON object, so the AOK change goes to a third address.

- The token outputs must add up to exactly the tokens of the inputs: send the rest back to yourself as a second transfer output. Otherwise the transaction is refused with `bad-tx-inputs-outputs-mismatch ... Tokens would be burnt`.
- The amount of a transfer is in tokens (`50` is 50 tokens). The outputs keep the order of the JSON object.
- The fee is paid in AOK from the AOK inputs.
- Issuing and reissuing tokens pay a cost in AOK to the token fee address. The help text of `createrawtransaction` shows example amounts from older code; the real costs and the address are what `issuanceinfo` answers. See [[token-names-and-costs]].

The wallet's `transfer`, `transfermany` and `issue` build all of this; raw transactions are for wallets that keep their keys elsewhere. The explorer API serves the unspent outputs, scripts and fee rates such a wallet needs ([[explorer-api]]).
