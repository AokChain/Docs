---
title: Upgrade to 4.0
description: "Replace a 3.0.x node with AokChain Core 4.0, check it afterwards and go back if needed; notes for staking, exchange and explorer nodes."
order: 50
---

AokChain Core 4.0 runs on the same chain as 3.0.x. There is no hard fork and no activation height: a 4.0 node and a 3.0.x node follow the same chain and connect to each other, so each node can be upgraded on its own, at any time. 4.0 includes security fixes; every node should be upgraded.

## What stays the same

- **The data directory.** 4.0 uses the existing blocks, chain state and indexes (`txindex`, `addressindex`, `spentindex`, `tokenindex`, `timestampindex`). No reindex and no new download; only a node with an address index should rebuild it once (see [Explorers and indexers](#explorers-and-indexers)).
- **The wallet file.** The release programs use Berkeley DB 4.8 like the 3.0.x releases. A 3.0.x `wallet.dat` opens as before, and 3.0.x can open it again after 4.0 has used it.
- **`aokchain.conf`.** Every option of 3.0.x still exists.
- **The RPC interface.** Every command of 3.0.x still exists with the same arguments. 4.0 adds commands; 4.0.4 changed how the address index calls read their argument and what `mediantime` means (see below and [[aokchain-4-0]]).

## Steps

1. **Back up.** Stop the node and copy the wallet, or the whole data directory, to a safe place:

   ```bash
   aokchain-cli stop
   while [ -e ~/.aokchain/aokchaind.pid ]; do sleep 1; done
   tail -1 ~/.aokchain/debug.log          # Shutdown: done
   cp -a ~/.aokchain/wallets ~/aok-wallets-$(date +%F)   # or ~/.aokchain/wallet.dat in older data directories
   ```

   With systemd, `sudo systemctl stop aokchaind` waits until the node has ended. Note the balance first (`aokchain-cli getbalance`, `listmytokens`) so that you can compare it later.

2. **Keep the old programs** and put the new ones in their place:

   ```bash
   sudo mv /usr/local/bin/aokchaind    /usr/local/bin/aokchaind-3.0
   sudo mv /usr/local/bin/aokchain-cli /usr/local/bin/aokchain-cli-3.0
   sudo install -m 0755 aokchain-4.0.10-linux-x86_64/aokchain* /usr/local/bin/
   ```

   Get and check the 4.0 package as [[install-a-node]] describes.

3. **Start the node** the way it ran before (`aokchaind -daemon` or `sudo systemctl start aokchaind`).

4. **Check it**, a minute later:

   ```bash
   aokchain-cli getnetworkinfo | grep subversion       # "/AokChain:4.0.10/"
   aokchain-cli getblockcount                          # rises to the height of the other nodes
   aokchain-cli getwalletinfo | grep -E '"balance"|immature|txcount'
   ```

## Going back

Stop the node, put the old programs back and start it:

```bash
aokchain-cli stop
while [ -e ~/.aokchain/aokchaind.pid ]; do sleep 1; done
sudo mv /usr/local/bin/aokchaind-3.0    /usr/local/bin/aokchaind
sudo mv /usr/local/bin/aokchain-cli-3.0 /usr/local/bin/aokchain-cli
aokchaind -daemon
```

From 4.0.10 on, stop the node normally before an earlier version uses its data directory again, as these commands do. What to do when that was not possible is under [Between 4.0 versions](#between-40-versions).

## Staking nodes

- **Repair the coins once.** A node that staked under 3.0.x may have coins without their transaction time in its chain state; a reorganization removed it. 4.0 stakes such coins correctly, and `repaircoins` puts the time back into the chain state:

  ```bash
  aokchain-cli repaircoins true     # count only
  aokchain-cli repaircoins          # repair
  ```

  The coins keep their age; staking goes on at once.
- **Larger staking coins.** A stake now gathers the small coins of its address up to twice `stakecombinethreshold` (default 1,000 AOK) and splits into two coins above that. Over the following days the staking coins grow to between 1,000 and 2,000 AOK and the wallet holds far fewer of them. Nothing has to be done.
- **Encrypt the wallet** and unlock it for staking only, so that the server can stake but not spend. How, and what to do after each restart, is on [[stake-with-a-full-node]] and [[encrypt-your-wallet]].
- **Several wallets.** With `staking=1` every wallet that the node has open stakes, and since 4.0.7 that includes a wallet that is opened while the node runs. A node that stakes with one wallet and opens others for a service names its staking wallet with `stakingwallet` in `aokchain.conf` before the first start of the new version, so that the other wallets do not begin to stake; see [[stake-with-a-full-node#several-wallets|Several wallets]].
- `getstakinginfo` now reports `staking` and `expectedtime` correctly, and the stakes, lost stakes and rewards of the last 24 hours (`stakes_24h`, `orphaned_24h`, `reward_24h`).

## Exchange nodes

- Stop deposits and withdrawals for the minutes of the upgrade, back up the wallet first and compare the balance afterwards.
- The calls an exchange uses (`getnewaddress`, `sendtoaddress`, `sendmany`, `listtransactions`, `listsinceblock`, `gettransaction`, `getrawtransaction`, `signrawtransaction`, `sendrawtransaction`, the token calls) answer as before.
- Since 4.0.6, `sendtoaddress` and `sendfrom` refuse a `lock_time` from 1 to 255 or below 0 (error `-8`), which made an output without a lock before; `conf_target` and `estimate_mode` of `sendtoaddress` and `sendmany` work; the token calls refuse an offline staking address with error `-5`. See [[version-history]].
- New and useful: `testmempoolaccept` checks a withdrawal before it is sent, `sendrawtransaction` takes a fee rate limit, `rpcwhitelist` limits an RPC user to a list of commands, `scantxoutset` reads the unspent outputs of an address without a wallet (time-locked ones excepted), and `getbalances` separates locked and immature coins. See [[exchange-integration]].

## Explorers and indexers

- A node with `addressindex`, `spentindex` and `txindex` starts on its existing data.
- **Rebuild the address index once.** After the upgrade to 4.0.8 or later, start a node that runs with `addressindex=1` once with `-reindex`, also when its index was rebuilt under an earlier 4.0 version. The rebuild corrects the records of earlier blocks: token outputs other than transfers are stored without a lock time, and an index that was kept under 3.0.x or under 4.0 before 4.0.5 has every unspent output again. New blocks are right without it. Rebuilding takes about as long as a full sync; you can rebuild a copy of the data directory on another machine and swap it in.
- 4.0.4 changed two answers: the address index calls take `{"addresses": [...]}` as their help says, and `getaddressutxos` can page with `limit` and `after`; `mediantime` of `getblock` and `getblockheader` is now the median time past instead of the block time. See [[version-history]].
- A cron line that restarts the node within a minute of every stop gets in the way of an upgrade; use a systemd unit instead ([[start-and-stop]]).

## Mixed networks

4.0 nodes and 3.0.x nodes keep connecting to each other. 4.0 announces protocol version 70021; `getpeerinfo` shows the `version` and `subver` of every peer:

```bash
aokchain-cli getpeerinfo | grep '"subver"' | sort | uniq -c
```

## Between 4.0 versions

A 4.0 node is upgraded to a later 4.0 version by the same steps: stop it normally, replace the programs, start it. Nothing changes in `aokchain.conf`, and nothing changes for wallets. What 4.0.10 adds for the operator:

- **The first start after an earlier version.** A node that was stopped normally before the upgrade does not rebuild. A node that was killed or crashed under the earlier version rebuilds its chain state once at its first start under 4.0.10. That takes some tens of minutes on the main network; the node does not stake meanwhile, and the wallet is not touched.
- **Where you have to ask for that rebuild.** The node knows such a stop by the pid file that the earlier version left in the data directory. It cannot see it on Windows, which has no pid file, when the pid file is kept outside the data directory (`-pid`), and when a service manager removes it (`PIDFile=` in a systemd unit, as on [[start-and-stop]]). If the earlier version was not stopped normally in one of these cases, start 4.0.10 once with `-reindex-chainstate`.
- **A start after a stop without a shutdown.** Start the node as usual. It brings its databases in step and, when it cannot go on from them, rebuilds them from the block files by itself. What the log says then is on [[start-and-stop#after-a-stop-without-a-shutdown|Start and stop]].
- **`autorebuild=0`** in `aokchain.conf` keeps the decision about a rebuild with you. The node then stops with a message that names the option to use ([[configuration-options]]).
- **Keep `Restart=on-failure` in the service unit.** When a block that the node had validated before does not connect any more, the node says "The databases of this node are damaged. They are built again from the block files at the next start: start the program again, no option is needed." and ends with exit code 1. Started again, it rebuilds.
- **`coins_missing` in `getstakinginfo`.** Above 0, the chain state of the node does not hold coins that the wallet would stake. The wallet goes on staking with its other coins, and the log names the coins. Rebuild the chain state at a convenient time with `-reindex-chainstate`; the wallet is not touched by it.
- **Going back to 4.0.9.** Stop the node normally, put the old programs back and start it. If the node was not stopped normally, start 4.0.10 once more, stop it normally, and only then put the old programs back; when that is not possible, rebuild the chain state after going back.

The other changes of each version are on [[version-history]].
