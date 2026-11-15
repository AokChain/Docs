---
title: Configure a node
description: Where the data directory and aokchain.conf are on each system, how the file is written, and settings for common kinds of nodes.
order: 20
---

A node reads its settings from the command line and from the file `aokchain.conf`. This page says where that file and the data directory are, how the file is written, and gives starting points for common setups. Every option is listed on [[configuration-options]].

## The data directory

The data directory holds the chain, the indexes, the wallets, the log and `aokchain.conf`.

| System | Default data directory |
|---|---|
| Linux | `~/.aokchain` |
| macOS | `~/.aokchain` |
| Windows | `%APPDATA%\AokChain`, usually `C:\Users\<name>\AppData\Roaming\AokChain` |

- `-datadir=<dir>` chooses another one. The folder must exist.
- The test network uses the subfolder `testnet1`, regtest the subfolder `regtest`. `aokchain.conf` stays at the top of the data directory for every network.
- The desktop wallet asks for the data directory on its first start and remembers the choice; `-choosedatadir` asks again.

What you find in it:

| Path | Contents |
|---|---|
| `blocks/` | The blocks (`blk*.dat`), their undo data (`rev*.dat`) and, in `blocks/index/`, the block index with the transaction and address indexes. |
| `chainstate/` | The unspent outputs at the tip. |
| `tokens/`, `governance/` | The token database and the governance state (frozen addresses, issuing costs). |
| `wallets/` | Wallet files. A data directory made by 3.0.x or earlier has `wallet.dat` at the top instead; that layout keeps working. |
| `debug.log` | The log. |
| `peers.dat`, `banlist.dat` | Known peer addresses and the bans you set. |
| `mempool.dat`, `fee_estimates.dat` | Written at shutdown and read at the next start. |
| `.cookie` | The RPC password of this run, while the node runs (see [[json-rpc]]). |
| `aokchaind.pid` | The process id of a running `aokchaind`, removed at shutdown. |

> [!CAUTION]
> The wallet files are the coins. Back them up, and copy them only while the node is stopped or with `backupwallet`. Never copy `blocks/` or `chainstate/` out of a running node either; stop it first.

## aokchain.conf

The file does not exist until you create it. It is plain text, one setting per line, written as the option name without the leading dash:

```ini
# a comment
txindex=1
addnode=203.0.113.10
addnode=203.0.113.11
```

- `name=value` sets an option; `name=1` and `name=0` turn a switch on and off, and `noname=1` is the same as `name=0`.
- Options that can be given more than once (`addnode`, `rpcauth`, `wallet`, `bootstrapurl` and others) take one line each.
- A `#` starts a comment, also in the middle of a line: everything after it is ignored. A value cannot contain `#`, so do not use it in passwords.
- A setting on the command line wins over the same setting in the file.
- Section headers such as `[test]` do not select a network; settings below them are ignored. Use separate data directories or `-conf=<file>` to keep settings for different networks apart.
- `-conf=<file>` reads another file. A relative path is relative to the data directory.

Restart the node after you change the file. A few settings, such as the indexes, need more than a restart; see [[indexes]].

## Starting points

### A node for your own use

```ini
server=1
```

`aokchaind` answers RPC calls from the same computer without further settings: `aokchain-cli` reads the cookie file. `server=1` matters for the desktop wallet, which answers RPC calls only with it.

### A node that helps the network

```ini
listen=1
maxconnections=64
```

Open TCP port 33441 in the firewall so that other nodes can connect. See [[ports-and-peers]].

### A staking node

```ini
staking=1
```

`staking` is not listed by `aokchaind -help`, but the node reads it: the wallet looks for stakes from the start. An encrypted wallet has to be unlocked for staking first; see [[stake-with-a-full-node]].

### An RPC server for an application on another computer

```ini
server=1
rpcbind=127.0.0.1
rpcbind=192.0.2.10
rpcallowip=192.0.2.0/24
rpcauth=app:<salt>$<hash>
```

`rpcbind` is ignored unless `rpcallowip` is set as well. `rpcauth` gives the application its own name and password; [[json-rpc#rpcauth-users-with-hashed-passwords|JSON-RPC]] shows how to make the line and how to limit the user to some commands with `rpcwhitelist`. Never expose the RPC port to the internet.

### An exchange or payment node

```ini
server=1
walletnotify=/usr/local/bin/aok-wallet-event %s
blocknotify=/usr/local/bin/aok-block-event %s
```

The transaction index (`txindex`) is on by default. [[exchange-integration]] explains deposits, confirmations and withdrawals.

### An explorer or indexer node

```ini
server=1
addressindex=1
spentindex=1
timestampindex=1
```

These indexes have to be built from the blocks: set them before the first start, or rebuild with `-reindex`. A new data directory with them does not start from the snapshot. See [[indexes]].

## The settings page of the desktop wallet

The desktop wallet keeps the settings of its settings page (window, language, network and proxy choices, fast synchronization) in its own storage, not in `aokchain.conf`. An option set in `aokchain.conf` or on the command line takes precedence; the settings page then shows a note that some options are set elsewhere. `-resetguisettings` clears the stored GUI settings.
