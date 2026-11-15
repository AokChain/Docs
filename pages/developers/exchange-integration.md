---
title: Exchange integration
description: "Run AOK and token deposits and withdrawals on an AokChain node: addresses, detecting deposits, confirmations, locked coins, fees, balances and safety."
order: 70
---

How an exchange, payment processor or custodian runs AOK and AokChain tokens on its own node. Everything here was checked against AokChain Core 4.0; where AokChain behaves differently from Bitcoin Core, the page says so. Calls are written for `aokchain-cli`; over JSON-RPC they are the same methods ([[json-rpc]]).

## The node

- Run AokChain Core 4.0 ([[install-a-node]], [[upgrade-to-4-0]]). Use the release programs, whose wallet files are Berkeley DB 4.8.
- Keep the defaults for indexes (`txindex=1`). An address index is not needed for a wallet-based integration.
- Give the application its own RPC user with `rpcauth`, and limit it with `rpcwhitelist` to the commands it uses ([[json-rpc#limit-a-user-to-some-commands]]). Never expose the RPC port.
- Keep the system clock right. Every transaction carries the node's time; a transaction more than 10 minutes ahead of other nodes' clocks is refused (`time-too-new`).
- Leave `staking` off on the hot wallet unless you mean to stake with it. Staking ties coins up for 60 blocks at a time.

## Deposit addresses

Give every customer, or every deposit, its own address:

```bash
aokchain-cli getnewaddress "user-1042"
```

- Addresses start with `K` (pay to public key hash) or `k` (pay to script hash) on mainnet. See [[network-parameters#addresses-and-keys]].
- The wallet is an HD wallet (`getwalletinfo` shows `hdseedid`), so a backup made after it was created also covers the addresses made later. Keys imported with `importprivkey` need a new backup.
- An encrypted wallet hands out addresses from its key pool while it is locked. When the pool is empty, `getnewaddress` fails with error `-12`; unlock the wallet and run `keypoolrefill`. A larger pool (`keypool=10000`) means fewer refills.

> [!WARNING]
> The label of `getnewaddress` is also the legacy "account" of the address. `sendmany` sends only from the balance of the account it names, so with labeled deposit addresses `sendmany ""` fails with `Account has insufficient funds` even when the wallet has the coins. Use the withdrawal methods below, not `sendmany`.

## Detect AOK deposits

Poll `listsinceblock` with the last block you processed, or call it when `walletnotify` or `blocknotify` fires:

```bash
aokchain-cli listsinceblock "<lastblock of the previous call>" 6
```

```json
{
  "transactions": [
    {
      "address": "KacWDE2Fyqywwr6YDKt1FYthycv3Ee7dqv",
      "category": "receive",
      "amount": 10.0,
      "label": "user-1042",
      "vout": 1,
      "confirmations": 1,
      "blockhash": "6e03922e674e98e2b3b2fa3c2689272acb2ae6763c0fad932cd018b7f2d6ef9e",
      "txid": "8574966f6199e8fb499f74c75b594639bad716e1b9b62fc2f114662fdde0b469",
      "time": 1794743210
    }
  ],
  "removed": [],
  "lastblock": "..."
}
```

- A deposit is an entry with `"category": "receive"`. One transaction can pay several of your addresses; it then has one entry per output (`vout`). Key your records by `txid` and `vout`.
- `lastblock` is the block to pass next time. With a second argument `n`, it is the block `n - 1` below the tip, so that transactions with fewer than `n` confirmations come up again in the next call.
- `removed` lists wallet transactions that a reorganization took out of the chain.
- Look at `confirmations` in every call, and with `gettransaction <txid>` before you credit. 0 means the transaction is not in a block (again, after a reorganization) and may still confirm. A negative number means that a conflicting transaction is in the chain: the payment was replaced and will not confirm; `walletconflicts` names the transactions it conflicts with.

### walletnotify

`walletnotify=<command>` runs the command with the transaction id (`%s`) whenever a wallet transaction is added or changes: when it arrives in the mempool, when it is confirmed in a block, and once more for each wallet of the node that holds it. One payment therefore runs the command several times, and the command does not say which wallet it was. Treat it as a signal to look the transaction up with `gettransaction`, and make the processing idempotent.

## Detect token deposits

> [!CAUTION]
> `listsinceblock` does not list token transfers, and `listtransactions` lists them with `"category": "receive"` and an `amount` that is the token quantity, not AOK. A program that credits every `receive` entry as AOK credits tokens as AOK. Always check `token_name`, and `locktime` (see [Locked deposits](#locked-deposits)).

A token deposit in `listtransactions`:

```json
{
  "token_type": "transfer_token",
  "token_name": "DOCTOKEN",
  "amount": 50.0,
  "address": "KacWDE2Fyqywwr6YDKt1FYthycv3Ee7dqv",
  "vout": 0,
  "category": "receive",
  "confirmations": 1,
  "txid": "275adebb9099a31020ffc95c05f5269602ba8311a205d14cf6bff19d101b774b"
}
```

To find token deposits, take every transaction id from `walletnotify` (it fires for token transfers too) and read it with `gettransaction`:

```bash
aokchain-cli gettransaction 275adebb9099a31020ffc95c05f5269602ba8311a205d14cf6bff19d101b774b
```

- `details` lists the AOK outputs of the transaction for this wallet.
- `token_details` lists its token outputs, each with `token_name`, `amount` (tokens), `address`, `vout` and `category`.

`listtransactions "*" <count> <skip>` also lists both kinds and can be used for polling. `listmytokens` gives the token balances of the wallet.

## Locked deposits

A payment can lock its output until a block height or a time (a `CHECKLOCKTIMEVERIFY` output; `sendtoaddress` makes one when its third argument, `lock_time`, is 256 or more). Tokens can be locked the same way. The wallet treats such deposits differently:

- A locked AOK output is not listed by `listtransactions` or `listsinceblock` and is not in `getbalance` until the lock has passed. `getbalances` counts it under `mine.locked`, and `listunspent` shows it with `"spendable": 0`. `getreceivedbyaddress` never counts such an output, also after the lock.
- When the lock has passed, `listtransactions` lists the payment (with a `locktime` field) under its original block, and the coins are spendable. `listsinceblock` with a later block does not report it then.
- Locked tokens are different: a locked token transfer appears at once in `listtransactions` and in `token_details` of `gettransaction`, as a `receive` entry with a `locktime` field. Do not credit such an entry before that height or time. The wallet counts the tokens in `listmylockedtokens`, not in `listmytokens`, until then.

To catch them, check `getbalances` regularly: a `locked` amount above 0 means locked coins are waiting. `listunspent` lists them with `"spendable": 0` and their script, which begins with the lock height or time. Credit them when they are spendable, or tell customers that time-locked deposits are not accepted.

## Confirmations

| Fact | Value |
|---|---|
| Target block interval | 64 seconds |
| Confirmations after which the desktop wallet shows a payment as confirmed | 6 |
| Deepest reorganization a node accepts | 500 blocks |
| Blocks before a staked coin or a stake reward can be spent | 60 |

On a proof-of-stake chain the newest block is sometimes replaced by a competing block of the same height. Do not credit unconfirmed deposits. Wait for at least the 6 confirmations of the desktop wallet, and for more for large amounts; the right number is a risk decision of your own.

Deposits are ordinary transactions and are spendable as soon as they are confirmed. Maturity applies only to the outputs of stakes and of proof-of-work blocks; `getbalances` shows such coins under `immature` and `staked`.

## Balances

| Call | Gives |
|---|---|
| `getbalance` | The spendable AOK of the whole wallet. |
| `getbalance "*" 6` | A legacy calculation: what was received with at least 6 confirmations, minus everything spent, plus your own unconfirmed change. For the coins that have 6 confirmations, add up `listunspent 6`. |
| `getbalances` | `mine.trusted`, `untrusted_pending`, `immature`, `staked`, `locked`, `offline_staking`, in AOK. |
| `listmytokens`, `listmylockedtokens` | Token balances, free and locked. |
| `listunspent` | Every unspent AOK output of the wallet, with `confirmations`; time-locked ones have `"spendable": 0`. |
| `scantxoutset start '["addr(K...)"]'` | The unspent outputs of any address from the chain state, without a wallet; token outputs are marked `"token": 1`. Time-locked outputs are not matched by `addr()`; find them with `raw(<script hex>)`. |

`getbalance ""` and `getbalance "<label>"` give legacy account balances, which can be negative. Do not use them for accounting.

## Withdrawals

1. **Check the address.** `validateaddress <address>` must answer `"isvalid": 1`. Then `checkfreeze <address>`: `true` means governance has frozen the address, and coins sent there cannot be moved while it stays frozen ([[address-freezing]]). Refuse such withdrawals.
2. **Send AOK** with named arguments:

   ```bash
   aokchain-cli -named sendtoaddress address=Krp9Fwe7rEZm6Y6YxnngFc9to7y1Q4QX9W amount=12.5
   ```

   Over JSON-RPC, pass `params` as an object: `{"address": "...", "amount": 12.5}`. `subtractfeefromamount=true` takes the fee out of the amount, and `comment_to` is a note that stays in your wallet.

   - The `message` argument is written into the transaction (as a version 2 transaction, at most 120 bytes) and is public on the chain; the help text of versions before 4.0.6 says it stays in the wallet. Put no customer data there.
   - `conf_target` and `estimate_mode` work from 4.0.6 on. While `estimatesmartfee` has no data, the wallet pays the `fallbackfee` rate with or without them. Older versions fail with either of them (`JSON value is not an integer as expected` or `JSON value is not a string as expected`), so leave them out there.

   > [!IMPORTANT]
   > The third positional argument of `sendtoaddress` is `lock_time`, not the `comment` of Bitcoin Core. Code written for Bitcoin Core that passes positional arguments must be changed: a value of 256 or more there locks the coins of the recipient until that height or time. 4.0.6 refuses 1 to 255 and negative values (error `-8`, `Invalid lock_time`); older versions sent such a payment without a lock.

3. **Batch many withdrawals into one transaction** with a raw transaction funded by the wallet:

   ```bash
   RAW=$(aokchain-cli createrawtransaction '[]' '{"KhsXjhrb7hKpz4Mj2n15TrGVKDxz2PnLzd": 0.5, "KeVweW7eX9LRrv6vAFuht1ggdTWb7zgAJ4": 1.25}')
   FUNDED=$(aokchain-cli fundrawtransaction "$RAW" | jq -r .hex)
   SIGNED=$(aokchain-cli signrawtransactionwithwallet "$FUNDED" | jq -r .hex)
   aokchain-cli testmempoolaccept "[\"$SIGNED\"]"
   aokchain-cli sendrawtransaction "$SIGNED"
   ```

   `fundrawtransaction` picks the inputs, adds change and the fee; `testmempoolaccept` runs every check without sending (`"allowed": 1`). Sending the same signed transaction again while it is in the mempool returns its id again; once it is in a block, the answer is error `-27`.
4. **Send tokens** with `transfer`:

   ```bash
   aokchain-cli transfer "DOCTOKEN" 10 "Krp9Fwe7rEZm6Y6YxnngFc9to7y1Q4QX9W"
   ```

   It returns an array with the transaction id. The fee is paid in AOK, so the wallet needs some AOK besides the tokens. Tokens cannot go to an offline staking address (`validateaddress` shows `isofflinestaking` for one): the call fails with error `-5`, `Tokens cannot be sent to an offline staking address` (before 4.0.6 with error `-25`, `Transaction amount too small`). `transfermany` and `transfermanyoutputs` send to several recipients ([[rpc-tokens]]).

An encrypted wallet has to be unlocked for each payment: `walletpassphrase "<passphrase>" 30` opens it for 30 seconds (use `aokchain-cli -stdin` so that the passphrase does not land in the shell history).

## Fees

| Setting | Default | Effect |
|---|---|---|
| `fallbackfee` | 0.01025 AOK/kB | The rate the wallet uses when it has no fee estimate. AokChain has too little traffic for estimates, so this is the usual rate. |
| `mintxfee` | 0.01 AOK/kB | The lowest rate the wallet uses. |
| `paytxfee`, `settxfee` | not set | A fixed rate for the wallet's transactions. |
| `minrelaytxfee` | 0.0001 AOK/kB | The lowest rate nodes relay. |
| `maxtxfee` | 10 AOK | The highest total fee of one wallet or raw transaction. |

At the default rate a payment with one input and two outputs (about 230 bytes) costs about 0.0024 AOK. `estimatesmartfee` answers `Insufficient data or no feerate found`. Transactions are not replaceable by default (`walletrbf=0`), and `bumpfee` is not available; a transaction that does not confirm and has left the mempool can be released with `abandontransaction`, which frees its coins for a new payment.

## Safety

- Encrypt the hot wallet and keep the passphrase off the server's disk; unlock it only for the seconds a payment takes.
- Keep most coins in a wallet that is not on the server; watch it with `importaddress` (watch-only) if needed.
- Back up the wallet after creating it, after `encryptwallet` and after importing keys: `backupwallet "/secure/place/wallet-$(date +%F).dat"`.
- Compare the wallet balance with your books every day, including `getbalances` (`locked`, `immature`) and the tokens.
- `getblockcount` of your node should match other nodes; an explorer is a useful second view ([[explorer-api]]).
