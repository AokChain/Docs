---
title: Stake with a full node
description: Run aokchaind as a staking server with an encrypted wallet that is unlocked for staking only, and check that it stakes.
order: 30
---

A node on a server stakes around the clock. This page assumes a node that is installed and synchronized: see [[install-a-node]].

## Set it up

1. Turn on staking in `aokchain.conf` and restart the node:

   ```ini
   staking=1
   ```

2. Encrypt the wallet, if it is not encrypted yet. The node stops when it is done; start it again.

   ```bash
   aokchain-cli encryptwallet "<passphrase>"
   ```

3. Make a new backup of the wallet: backups made before the encryption are not encrypted. See [[back-up-and-restore]].

4. Make an address and send the coins you want to stake to it:

   ```bash
   aokchain-cli getnewaddress "staking"
   ```

5. Unlock the wallet for staking only, with no time limit:

   ```bash
   aokchain-cli walletpassphrase "<passphrase>" 0 true
   ```

The wallet now signs stakes and nothing else. A payment or `dumpprivkey` answers "Wallet is unlocked for staking only" until the passphrase is given again.

> [!IMPORTANT]
> The unlock ends when the node stops. After every restart, run `walletpassphrase "<passphrase>" 0 true` again, or the node does not stake.

Do not put the passphrase into a script or into `aokchain.conf` on the same server; that would undo the encryption. Commands you type stay in the shell history, so remove the line from the history afterwards.

## Check that it stakes

```bash
aokchain-cli getstakinginfo
```

| Field | Meaning |
| --- | --- |
| `enabled` | `1` when `staking=1` is set |
| `staking` | `1` while the wallet looks for stakes |
| `weight` | Your coins that can stake now, in sats (100,000,000 = 1 AOK) |
| `netstakeweight` | Estimate of all coins that stake on the network, in sats |
| `expectedtime` | Expected seconds between two of your stakes |
| `stakes_24h` | Your stakes in the chain in the last 24 hours |
| `orphaned_24h` | Your stakes of the last 24 hours that lost against another block |
| `reward_24h` | What the stakes of the last 24 hours earned, in AOK |

`enabled` and `staking` print `1` or `0`, not `true` or `false`. `getbalances` shows the coins that are `staked` and `immature` right now.

## Coin size

A stake gathers the coins of its address that are smaller than 1,000 AOK and splits a coin of 2,000 AOK or more in two, so staking coins end up between 1,000 and 2,000 AOK. To change the size, set `stakecombinethreshold` (in AOK, at least 1):

```ini
stakecombinethreshold=1000
```

## Several wallets

A node with `staking=1` stakes with every loaded wallet. From 4.0.7 on that includes a wallet that is created or loaded while the node runs (`createwallet`, `loadwallet`, `restorewallet`); earlier versions stake only with the wallets of the start. Unlock each one with `-rpcwallet=<name>`:

```bash
aokchain-cli -rpcwallet=second walletpassphrase "<passphrase>" 0 true
```

To stake with some of the wallets only, name them with `stakingwallet` in `aokchain.conf` (from 4.0.8), one line for every wallet that stakes:

```ini
staking=1
stakingwallet=<name as listwallets shows it>
```

A wallet that is not named does not stake, whether it is opened at the start or later; `debug.log` then says `Wallet "<name>" does not stake: -stakingwallet does not name it`. A node that stakes with one wallet and opens others for a service names its staking wallet this way. Without the line every wallet stakes, as before.

`listwallets` shows the wallet that a node opens by default as `""`. To name it, write nothing after the equals sign:

```ini
staking=1
stakingwallet=
```

## Keep the owner key elsewhere

A staking server has to hold the keys of the coins it stakes. To keep the spending key off the server altogether, delegate the coins with [[offline-staking]].
