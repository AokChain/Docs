---
title: Multisig with RPC
description: "Create an M-of-N multisig address, fund it and spend from it with partly signed raw transactions, compatible with the desktop wallet's multisig pages."
order: 40
---

A multisig address needs several keys to spend from it, for example two of three. AokChain uses pay-to-script-hash (P2SH) multisig as Bitcoin does. This page builds one with RPC commands; the desktop wallet does the same on its Sign page ([[multisig-wallets]]), and addresses made here open there when the keys are sorted as below.

## 1. Collect the public keys

Every participant gives a compressed public key (66 hex characters). From an address of their own wallet:

```bash
aokchain-cli getaddressinfo KacWDE2Fyqywwr6YDKt1FYthycv3Ee7dqv
```

`pubkey` in the answer is the key. Each participant keeps the address and its private key; nobody hands out a private key.

## 2. Make the address

Sort the keys as hex text, then:

```bash
aokchain-cli createmultisig 2 '["027cb153be078ab2d7df12e618868f0cf68237d8817dabedc656a81201ca63dcfd","0284625c5a7cd69f57e0a17375eaefc8a85794b9c77f04f38850f65ff80c9b0e3c","02fc9acf46f2bd2134f071b606d043e6e9e0bd51cce016b5ab315b82aefda78ba9"]'
```

```json
{
  "address": "k...",
  "redeemScript": "5221027cb1...ba953ae"
}
```

- The address depends on the order of the keys. The desktop wallet sorts them as hex text, so that every participant gets the same address whatever order they enter; sort them the same way to stay compatible.
- `redeemScript` is `<m> <key 1> ... <key n> <n> OP_CHECKMULTISIG`. Every participant needs it to sign. Keep it with the backup: without it nobody can spend from the address.
- Up to 15 compressed keys fit into the 520 bytes a redeem script may have.

To let a wallet watch the address and count its coins, add it to the wallet of each participant:

```bash
aokchain-cli addmultisigaddress 2 '["027c...","0284...","02fc..."]' "team funds"
```

or, with the redeem script only, as the desktop wallet does:

```bash
aokchain-cli importaddress "5221027cb1...ba953ae" "team funds" false true
```

The last `true` tells `importaddress` that the hex is a redeem script (P2SH). The third argument is a rescan for earlier payments: `false` for a new address, `true` for one that may have received coins already. Coins of the address count as watch-only and are not used for staking.

## 3. Fund it

Send AOK to the `k...` address like to any address.

## 4. Spend

1. **Find the output** to spend: its `txid`, `vout`, `scriptPubKey` and `amount`, for example from `getrawtransaction <txid> 1` or `listunspent`.
2. **Create the transaction**, with change back to the multisig address:

   ```bash
   aokchain-cli createrawtransaction '[{"txid":"99fda8be...","vout":0}]' \
     '{"Krp9Fwe7rEZm6Y6YxnngFc9to7y1Q4QX9W":12.0,"k...":7.99}'
   ```

   The difference between the inputs and the outputs is the fee. A fully signed 2-of-3 spend of one input is about 345 bytes with one output and about 380 bytes with a change output; at the wallet's usual rate of 0.01025 AOK/kB that is about 0.004 AOK.
3. **First signature.** The first participant signs with their key and describes the input:

   ```bash
   aokchain-cli signrawtransactionwithkey "<hex>" '["<WIF key 1>"]' \
     '[{"txid":"99fda8be...","vout":0,"scriptPubKey":"a9147b25...87","redeemScript":"5221027cb1...ba953ae","amount":20.0}]'
   ```

   The answer has `"complete": 0`, and `errors` says that the input is not fully signed yet (`invalid stack size (possibly missing key)`). That is expected. A participant whose wallet has the key and the redeem script can use `signrawtransactionwithwallet "<hex>" '[...]'` instead (unlock the wallet first).
4. **Second signature.** The next participant signs the hex of step 3 the same way with their key. With two of three signatures the answer is `"complete": 1`.

   Participants can also sign the unsigned transaction separately and put the results together:

   ```bash
   aokchain-cli combinerawtransaction '["<hex signed by A>","<hex signed by C>"]'
   ```

5. **Check and send:**

   ```bash
   aokchain-cli testmempoolaccept '["<complete hex>"]'
   aokchain-cli sendrawtransaction "<complete hex>"
   ```

Before signing, decode what you are asked to sign with `decoderawtransaction "<hex>"`: check every output address and amount, and that the inputs belong to the multisig address. A signature covers the whole transaction; if anyone changes an output afterwards, the signatures no longer fit.

## The desktop wallet's exchange formats

The Sign page of the desktop wallet passes keys, wallets and signing requests between participants as one line of text, which programs can read and write too:

| Prefix | Contents |
|---|---|
| `aokms-key1:` | A compressed public key, 66 hex characters. |
| `aokms-wallet1:` | Base64 of the JSON `{"v":1,"name","m","keys":[{"name","pubkey"}],"address","redeemScript"}`. No private keys. |
| `aokms-req1:` | Base64 of the JSON `{"v":1,"wallet","address","redeemScript","memo","to","amount","tx","prevouts":[{"txid","vout","scriptPubKey","amount"}],"created"}`. `tx` is the partly signed transaction in hex. |

The wallet does not trust `to`, `amount` or `memo` of a request; it decodes `tx` and reads the inputs from its own node. A program should do the same.

## Limits

- P2SH multisig with compressed keys only; no SegWit multisig and no PSBT.
- The desktop wallet's multisig pages send AOK only.
- Changing the keys or the number of signatures means a new address: create it and move the coins.
