---
title: Node troubleshooting
description: "What to do when a node does not start, does not sync, finds no peers, or refuses an RPC call, with the messages it prints."
order: 80
---

Common problems of `aokchaind` and the desktop wallet, by the symptom or the message you see. The log is `debug.log` in the data directory (`testnet1/debug.log` on the test network); most answers start there.

```bash
tail -n 50 ~/.aokchain/debug.log
```

## The node does not start

| Message | Cause and fix |
|---|---|
| `Cannot obtain a lock on data directory ... AokChain Core is probably already running.` | Another `aokchaind` or `aokchain-qt` uses this data directory, or one is still shutting down. Wait until its process has ended (see [[start-and-stop]]). |
| `Incorrect or no genesis block found. Wrong datadir for network?` | The data directory belongs to another network, for example a testnet folder used for mainnet. |
| `You need to rebuild the database using -reindex to change -txindex` (or `-tokenIndex`, `-addressindex`, `-spentindex`, `-timestampindex`) | An index option differs from the one the data directory was built with. Put the old value back, or rebuild once with `-reindex`; `-reindex-chainstate` does not change indexes. See [[indexes]]. |
| `Corrupted block database detected` or `Error opening block database` | The databases were damaged, usually by a crash or a full disk. Start once with `-reindex`. |
| `This node started from a chain state snapshot and does not have the blocks before it, so it cannot rebuild its databases from the blocks.` | `-reindex` on a node that started from the snapshot. Run `fetchblocks` first, or start again with an empty data directory. |
| `Error loading ...: Wallet corrupted` | Stop the node, copy the wallet file, and run `aokchain-wallet -wallet=<copy> salvage` on the copy. |
| `Error loading ...: Wallet requires newer version of AokChain Core` | The wallet was written by a newer program. Open it with that program, or with a newer one. |
| `Error: Disk space is low!` | Free space on the disk of the data directory; the node stops before the disk is full. |

## The node does not sync

1. **Peers.** `aokchain-cli getconnectioncount` must be above 0. If it stays at 0, add a peer with `addnode` ([[ports-and-peers]]).
2. **Progress.** `aokchain-cli getblockchaininfo` shows `blocks` and `headers`. `headers` far ahead of `blocks` is normal during the first sync: the node knows the chain and is validating it. While it imports the block archives it gets only headers from its peers.
3. **The height of the peers.** `aokchain-cli getpeerinfo` lists `startingheight` and `synced_blocks` of every peer. A node whose height stays below its peers' for a long time while it has peers is stuck; look in `debug.log` for `ERROR` or `InvalidChainFound` lines about the tip.
4. **The clock.** `Please check that your computer's date and time are correct!` means the clock of the computer is far from the clocks of the peers. Blocks more than 10 minutes ahead of the node's time are refused, and a staker with a wrong clock makes blocks that others refuse. Turn on the time sync of the system.

A first sync that only downloads from peers takes hours; [[fast-sync]] takes minutes. One processor core at 100% during a sync is normal: connecting blocks runs on one thread.

Lines such as `InvalidChainFound` or `bad-cs-proofhash` about a block on a short side branch mean the node refused a block that a peer sent. If `getblockcount` keeps rising with the other nodes, nothing needs to be done.

## The fast sync is not used

| Log line | Meaning |
|---|---|
| `Bootstrap: off. The files at https://... need https, which this program does not do.` | `aokchaind` cannot fetch the built-in GitHub address. Download the files and use `bootstrapdir` ([[fast-sync]]). |
| `Snapshot: not used, because an option of this start needs the blocks to be validated here` | A non-default index, `prune` or `-reindex` was given. The node validates the blocks instead. |
| `Snapshot: not used, there is no address or folder to take it from.` | No `bootstrapdir` or `http://` `bootstrapurl` was given. |
| `Snapshot: the server has a snapshot for height ..., this program accepts the one at height ...` | The files belong to another program version. |
| `Bootstrap: notneeded: the node is at height ..., the archives end at ...` | The node is less than 20,000 blocks behind the archives. |
| `Bootstrap: notneeded: the chain of this node is recent` | Its last block is less than three days old. |

`getbootstrapinfo` and `getsnapshotinfo` show the state at any time.

## aokchain-cli cannot reach the node

| Message | Cause and fix |
|---|---|
| `couldn't connect to server: ... (make sure server is running and you are connecting to the correct RPC port)` | The node is not running, still starting, or listens on another port. Use `-rpcwait` while it starts; give `-datadir` or `-rpcport` if they are not the defaults. |
| `error code: -28` with `Loading block index...` or `Fast start: ...` | The node is starting. Wait, or use `-rpcwait`. |
| `Could not locate RPC credentials. No authentication cookie could be found, and RPC password is not set.` | The CLI looks in another data directory than the node's (give the same `-datadir`), the node has not written its cookie file yet (just started; see `-daemonwait` on [[start-and-stop]]), or it does not run. |
| `incorrect rpcuser or rpcpassword (authorization failed)` | The password in `aokchain.conf` and the one the CLI uses differ. With `rpcpassword` set, no cookie file is written. |
| `server returned HTTP error 403` | `rpcwhitelist` does not allow this user that command. With any `rpcwhitelist` line, users without one, the cookie user of `aokchain-cli` included, may call nothing unless `rpcwhitelistdefault=0`. See [[json-rpc#limit-a-user-to-some-commands]]. |
| `Wallet file not specified (must request wallet RPC through /wallet/<filename> uri-path).` | Several wallets are loaded. Add `-rpcwallet=<name>`; the first wallet is `-rpcwallet=` with an empty name. |

## Wallet calls fail

| Message | Cause and fix |
|---|---|
| `Error: Please enter the wallet passphrase with walletpassphrase first.` | The wallet is encrypted and locked. `walletpassphrase "<passphrase>" 60` opens it for 60 seconds. |
| `Error: Wallet unlocked for staking only, unable to create transaction.` | The wallet is unlocked for staking only. Unlock it with a timeout for the payment; it returns to staking only afterwards. |
| `Insufficient funds` | Not enough spendable coins. Coins that are immature, time locked or held at an offline staking address do not count; `getbalances` shows each kind. |
| `Requested wallet does not exist or is not loaded` | A wallet made with `createwallet` is not loaded again at the next start. Load it with `loadwallet <name>`, or add `wallet=<name>` to `aokchain.conf`. |

## A transaction is refused

`sendrawtransaction` and `testmempoolaccept` give the reason. Some that are particular to AokChain:

| Reason | Meaning |
|---|---|
| `time-too-new` | The transaction time is more than 10 minutes ahead of the node's clock. |
| `bad-txns-address-frozen` | An input belongs to an address that governance has frozen ([[address-freezing]]). |
| `absurdly-high-fee` | The fee is above the limit: `-maxtxfee` (10 AOK) or the fee rate given to `sendrawtransaction`. |
| `non-final` | The transaction has a lock time in the future. |
| `txn-mempool-conflict`, `missing-inputs` | An input is already spent, or not known to this node. |

## Starting over

To sync again from nothing, stop the node, move the wallet files out of the data directory, delete or rename the rest of the data directory, put the wallet files back into a new, empty data directory and start. Keep the old copy until the new node is synced and the wallet shows the right balance.
