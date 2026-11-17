---
title: Explorer API
description: "API v3 of the AokChain block explorer: blocks, transactions, addresses, tokens, supply and wallet calls over HTTPS, with its conventions and examples."
order: 80
---

API v3 answers questions about the chain over HTTPS, from the index behind the block explorer at [@@explorer_host@@](@@explorer@@/). Use it when you need data about any address without running a node with an address index, or as a second view next to your own node. The reference with every parameter, a real answer for each endpoint and a playground is at [@@site_host@@/api](@@site@@/api/); its OpenAPI description is [openapi.json](@@api@@/openapi.json).

```bash
curl -s @@api@@/status
```

```json
{
  "index": {"height": 3037566, "hash": "4e15215a1276d3b56bf10dbc739a7dc1d340b61aee562f18875a2f6fd31a351d",
            "time": 1794744928, "mtp": 1794744608, "age": 99, "lag": 0},
  "node": {"height": 3037566, "headers": 3037566, "version": "/AokChain:4.0.5/", "protocol": 70021,
           "connections": 4, "net_stake_weight": "234243710196720", "pos_difficulty": 316065.9566365251},
  "mempool": {"count": 0}
}
```

## Conventions

- **Base address:** `@@api@@`.
- **Amounts are strings of integer satoshis** (1 AOK = 100000000), because the AOK supply and many token amounts do not fit into the safe integer range of JavaScript. Token amounts use the same base unit of 8 decimals; `units` is the precision a token is displayed with. Parse them with a big-integer or decimal type. A few fields are in AOK instead, written with a decimal point: the issuing costs of `/governance`, `cost.amount` of `/tokens/issuance` and `/tokens/check` (next to `cost.sats` in satoshis), and `total_coins` of `/supply`.
- **Pages** are cursors: pass the `next` value of a page back as `before` or `after`, as the endpoint says. The endpoints with an `offset` parameter (`/block/{id}/txs`, `/richlist`, `/token/{name}/holders`) page by offset instead.
- **Errors** have a real HTTP status and a body `{"error": {"code": "...", "message": "..."}}`: 400 for bad input, 404 for something unknown (`"code": "not_found"`), 422 when the node refused a transaction (with the node's reason under `error.node`), 502 and 503 when the node or the index is not available.
- **Fresh data:** `/status` shows the height of the index (`index.height`) and of its node (`node.height`); `lag` says how many blocks the index is behind its node.
- The service is rate limited per client. Cache what does not change (blocks deep in the chain, old transactions) and back off when you get errors.

## Explorer endpoints

| Method and path | Returns |
|---|---|
| `GET /status` | Height and tip of the index and its node, the mempool size. |
| `GET /blocks?limit=&before=` | The latest blocks, newest first. |
| `GET /block/{height or hash}` | One block. |
| `GET /block/{height or hash}/txs?offset=&limit=` | Its transactions. |
| `GET /tx/{txid}` | A transaction with inputs, outputs, addresses and tokens. |
| `GET /tx/{txid}/raw` | The transaction in raw hex. |
| `GET /tx/{txid}/status` | Confirmations of a transaction. |
| `GET /address/{address}` | Balances per currency, transaction count, user names, first and last use. |
| `GET /address/{address}/txs?currency=&before=&limit=` | Transactions of an address, newest first. |
| `GET /address/{address}/utxos?currency=&after=&limit=` | Unspent outputs of an address. |
| `GET /address/{address}/frozen` | Whether governance has frozen the address. |
| `GET /mempool?limit=` | Unconfirmed transactions. |
| `GET /search?q=` | What a block height, hash, txid, address, token or user name refers to. |
| `GET /richlist?currency=&limit=&offset=` | The largest balances of AOK or a token. |
| `GET /supply`, `GET /supply/plain` | The AOK supply at the tip; `/supply/plain` is the total in AOK as plain text, for listing sites. |
| `GET /tokens?kind=&q=&after=&limit=` | Tokens. |
| `GET /tokens/catalogue?sort=` | Top-level tokens with holders, sub token and unique token counts. |
| `POST /tokens/info` | Several tokens at once: units, supply, IPFS metadata. Body `{"names": [...]}`. |
| `GET /token/{name}`, `/holders`, `/txs`, `/transfers`, `/children` | One token, its holders, transactions, transfers, and its sub tokens or unique tokens. URL-encode `#`, `/` and `@` in names. |
| `GET /tokens/issuance` | What issuing each kind of token costs, and the address the cost is paid to. |
| `GET /tokens/check?name=` | Whether a token name is valid and still free, with the cost. The API checks the name with its own copy of the node's rules. |
| `GET /governance` | Issuing costs and the list of frozen addresses, refreshed every 30 minutes. |
| `GET /username/{name}` | The address that holds a user name now. |
| `POST /verify` | Checks a signed message ([[message-signing]]). Body `{"address", "message", "signature"}`. |
| `GET /stats/daily?days=` | Chain activity per day (UTC). |
| `GET /network` | Peer count and the versions of the peers, as the index's node sees them. |

Examples:

```bash
curl -s @@api@@/address/KacWDE2Fyqywwr6YDKt1FYthycv3Ee7dqv
curl -s '@@api@@/address/KacWDE2Fyqywwr6YDKt1FYthycv3Ee7dqv/utxos?limit=100'
curl -s @@api@@/tokens/issuance
curl -s -X POST @@api@@/verify -H 'Content-Type: application/json' \
  -d '{"address":"KgF2VA2npjK7bYitFfrvoZa9FXNPieuRDF","message":"I control this address. 2026-11-15","signature":"IFH7dGp1q987L4SN0jQoHNUE/mpKl9rWz//GCw6wc7s0LCyGYWKDZGEIcf41TMB9erXvEVH2ocr8vkYzKHnMIfw="}'
```

The last one answers `{"valid":true,"address":"KgF2VA2npjK7bYitFfrvoZa9FXNPieuRDF"}`.

## Wallet endpoints

These serve wallets that keep their keys on the device and leave the chain to the API. The server never sees keys: requests carry addresses, or optionally the extended public key (xpub) of an account, from which the server derives the receiving (0) and change (1) chains with a gap limit (default 20).

| Method and path | Returns |
|---|---|
| `POST /wallet/addresses` | For each address: used or not, transaction count, balances. For a gap search on the device. |
| `POST /wallet/discover` | The used addresses of an account xpub. |
| `POST /wallet/balance` | Balances per currency: confirmed, unconfirmed, locked, immature, spendable. |
| `POST /wallet/utxos` | Unspent outputs, without those that a mempool transaction spends, with the script and lock and maturity details needed to sign. |
| `POST /wallet/history` | Transactions of the address set, newest first, pending ones first. |
| `POST /wallet/nfts` | Unique tokens held, with titles and thumbnails. |
| `GET /wallet/fees` | Fee rates in satoshis per kB: `min_relay` and `recommended`. These are lower than the default rate of the AokChain Core wallet (0.01025 AOK/kB), which uses its own `fallbackfee`. |
| `POST /wallet/broadcast` | Checks a signed transaction with the node (`testmempoolaccept`) and sends it. Body `{"hex": "..."}`; a refused transaction answers 422 with the node's reason. |

```bash
curl -s -X POST @@api@@/wallet/balance -H 'Content-Type: application/json' \
  -d '{"addresses":["KacWDE2Fyqywwr6YDKt1FYthycv3Ee7dqv","Krp9Fwe7rEZm6Y6YxnngFc9to7y1Q4QX9W"]}'
```

A wallet that signs its own transactions needs the AokChain transaction format with its time field ([[raw-transactions]]). Do not trust the device clock blindly: a transaction more than 10 minutes ahead of the nodes' clocks is refused. Every answer of the API carries the server's time in its HTTP `Date` header.

The `push` endpoints register the devices of the AOK wallet apps for payment notifications.

## Your own node or the API

| | Your node | API v3 |
|---|---|---|
| Trust | You validate every block yourself. | You trust the operator of the service. |
| Any address | Needs `addressindex=1` ([[indexes]]). | Built in. |
| Your wallet's coins and keys | Yes. | No keys; it only reads the chain and relays signed transactions. |
| Availability | Yours to run. | A public service with rate limits. |

For an exchange or any service that credits money, take the decision from your own node, and use the API as a cross-check.
