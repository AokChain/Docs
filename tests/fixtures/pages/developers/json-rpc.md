---
title: JSON-RPC
description: Send commands to a node with aokchain-cli or as JSON-RPC requests over HTTP.
order: 1
aliases: [rpc]
---

A node answers commands over JSON-RPC on port `33440`. `aokchain-cli` is the simplest client; any HTTP client works too.

> [!IMPORTANT]
> Set `rpcuser` and `rpcpassword` in `aokchain.conf` first, see [[run-a-node#configure]].

## With aokchain-cli

```bash
aokchain-cli getblock 37eb3f4b73df32d22c4a1c58e91f6e7f0bf58e34e448a8e59d6b2576eeb9c238
```

## Over HTTP

```bash
curl --user nodeuser --data-binary \
  '{"jsonrpc":"1.0","id":"docs","method":"getblockchaininfo","params":[]}' \
  -H 'content-type: text/plain;' http://127.0.0.1:33440/
```

The answer is JSON:

```json
{
  "result": {
    "chain": "main",
    "blocks": 3036561,
    "headers": 3036561,
    "verificationprogress": 1
  },
  "error": null,
  "id": "docs"
}
```

## Errors

| Code | Meaning |
|--:|---|
| `-32601` | No such method |
| `-32602` | Wrong parameters |
| `-5` | Invalid address |
| `-13` | Wallet locked: unlock it first |

Every command is in [[rpc-commands]]. Blocks and transactions are also on the [block explorer](https://v3.aokscan.com/).
