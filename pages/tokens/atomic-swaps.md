---
title: Atomic swaps
description: Trade one token for another in a single transaction that both sides sign, with createrawtransaction and signrawtransactionwithwallet.
order: 90
aliases: [atomic]
---

An atomic swap trades tokens between two people in one transaction. The transaction moves both tokens at once, so either both sides get what they agreed or nothing happens. It needs a node or the console of the desktop wallet (**Settings › Debug window**, **Console** tab, where you type the commands without `aokchain-cli`).

The example: Andy has 1,000 APPLES, Barb has 1,000 BANANAS. Andy gives Barb 2 APPLES for 1 BANANAS, and Andy pays the fee.

## 1. Find the inputs

The transaction spends three outputs: an AOK coin of Andy for the fee, Andy's APPLES and Barb's BANANAS.

Andy picks an AOK coin with `listunspent` and notes its `txid`, `vout` and `amount`:

```bash
aokchain-cli listunspent
```

Each of them finds the output that holds the token with `listmytokens` and `true`:

```bash
aokchain-cli listmytokens "APPLES" true
```

```json
{
  "APPLES": {
    "balance": 1000,
    "outpoints": [
      {
        "txid": "<apples txid>",
        "vout": 3,
        "amount": 1000,
        "satoshis": 100000000000
      }
    ]
  }
}
```

Barb does the same for BANANAS and sends Andy her `txid` and `vout`.

## 2. Make the addresses

Five new addresses take the outputs:

| Who makes it | Command | It receives |
| --- | --- | --- |
| Andy | `getrawchangeaddress` | Andy's AOK change |
| Andy | `getnewaddress` | the BANANAS for Andy |
| Barb | `getrawchangeaddress` | Barb's BANANAS change |
| Barb | `getnewaddress` | the APPLES for Barb |
| Andy | `getrawchangeaddress` | Andy's APPLES change |

Barb sends her two addresses to Andy.

## 3. Balance the outputs

Every token that goes in has to come out: 1,000 APPLES in, so 2 to Barb and 998 back to Andy; 1,000 BANANAS in, so 1 to Andy and 999 back to Barb. For AOK, whatever is not paid out is the fee. If Andy's coin holds 50,000 AOK and the fee is 0.01 AOK, his change is 49,999.99 AOK.

> [!CAUTION]
> Check every amount twice. An AOK amount that you forget to pay out goes to the staker as a fee.

## 4. Create the transaction

Andy passes the inputs and the outputs to `createrawtransaction`. A token output is written as `{"transfer":{"NAME":quantity}}`:

```bash
aokchain-cli createrawtransaction '[{"txid":"<andy aok txid>","vout":0},{"txid":"<apples txid>","vout":3},{"txid":"<bananas txid>","vout":3}]' '{"<andy aok change>":49999.99,"<andy bananas address>":{"transfer":{"BANANAS":1}},"<barb bananas change>":{"transfer":{"BANANAS":999}},"<barb apples address>":{"transfer":{"APPLES":2}},"<andy apples change>":{"transfer":{"APPLES":998}}}'
```

It returns the unsigned transaction as hex.

## 5. Sign it, one after the other

Andy signs first:

```bash
aokchain-cli signrawtransactionwithwallet "<hex>"
```

The result has `"complete": 0` and an error for Barb's input: "Unable to sign input, invalid stack size (possibly missing key)". That is expected, since Andy does not have Barb's key. Andy sends the new `hex` to Barb.

Barb first reads what she is about to sign:

```bash
aokchain-cli decoderawtransaction "<hex from andy>"
```

She checks every output: the address, the token and the quantity. Then she signs:

```bash
aokchain-cli signrawtransactionwithwallet "<hex from andy>"
```

Now the result has `"complete": 1`. Each signature covers the whole transaction, so if anyone changed an output after Andy signed, his signature would no longer fit and the network would refuse the transaction.

`signrawtransaction` takes the same arguments and works the same way.

## 6. Send it

Barb can test the transaction first and then send it:

```bash
aokchain-cli testmempoolaccept '["<signed hex>"]'
aokchain-cli sendrawtransaction "<signed hex>"
```

`sendrawtransaction` returns the transaction ID. Once a block includes it, `listmytokens` shows 998 APPLES and 1 BANANAS for Andy, and 2 APPLES and 999 BANANAS for Barb.

## If the swap does not go ahead

Until the transaction is sent, nothing has moved. A half-signed transaction cannot be sent by anyone. Once Barb holds the fully signed transaction, she can send it at any time as long as its inputs are unspent; to call the swap off before that, Andy spends his APPLES or his AOK coin in another transaction.

For more on raw transactions, see [[raw-transactions]].
