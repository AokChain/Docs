---
title: Atomic swaps
description: Trade one token for another in a single transaction that both sides sign.
order: 3
aliases: [atomic]
---

An atomic swap is one transaction with inputs from both parties. Either both transfers happen or neither does.

Andy has 1,000 `APPLES`. Barb has 1,000 `BANANAS`. Andy gives Barb 2 apples for 1 banana, and Andy pays the network fee.

## Find the inputs

Each side lists the outputs it will spend:

```bash
aokchain-cli listunspent
aokchain-cli listmytokens APPLES true
```

```json
{
  "APPLES": {
    "balance": 1000,
    "outpoints": [
      { "txid": "744c61abe6d237939c3567bc44b912ff4c375984229908c964be44f36dec79e3", "vout": 3, "amount": 1000 }
    ]
  }
}
```

## Build the transaction

Token transfers must balance: 1,000 `APPLES` in means 1,000 out, 2 to Barb and 998 back to Andy.

```bash
aokchain-cli createrawtransaction '[{"txid":"631cf1566165803f0b89fbfb169d8f0c89129ec3f8536a48e4c4f0f3c4081cff","vout":0},{"txid":"744c61abe6d237939c3567bc44b912ff4c375984229908c964be44f36dec79e3","vout":3},{"txid":"8468ef5193b1f5d6a7bd501f5f8ef5aec7c3d86fa87cec5a0b6f6d86fba78a4f","vout":3}]' '{"KZzymtqctNdW4fWhLdWKRYUDGXP3KzG8Y9":4.8827125,"KiNMHYArytp2D6jQSPHrGd7rq3qAxvpdt5":{"transfer":{"BANANAS":1}},"KtPia5TPzjw1XibYh3de3RKxcpq9gusCBu":{"transfer":{"APPLES":2}}}'
```

## Sign and send

1. Andy signs with `signrawtransaction`. He sees `Unable to sign input`, because Barb's inputs are not his. That is expected.
2. Andy sends the hex to Barb.
3. Barb signs the rest and sends it with `sendrawtransaction`.

The raw transaction RPC commands are listed in [[rpc-commands#raw-transactions|the RPC reference]].
