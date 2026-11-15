---
title: Run a node
description: Install aokchaind, write aokchain.conf, start the node and stop it again.
order: 1
aliases: [node, full-node]
---

A node keeps a full copy of the chain, checks every block and answers RPC commands. It runs on Linux, macOS and Windows.

## Install

A release has two programs:

- `aokchaind`, the node, which syncs the chain and holds the wallet
- `aokchain-cli`, which sends commands to a running node

Build from source with the code on [GitHub](https://github.com/AokChain/AokChain), or use a published release.

## Configure

The node reads `aokchain.conf` from its data folder (`~/.aokchain` on Linux, `%APPDATA%\AokChain` on Windows):

```ini
# RPC access for aokchain-cli and your own programs
rpcuser=nodeuser
rpcpassword=use-a-long-random-password
rpcallowip=127.0.0.1

# Run in the background and stake
daemon=1
staking=1
```

> [!WARNING]
> Never open the RPC port to the internet. Keep `rpcallowip` on the machines you trust.

Every option is listed in [[configuration]].

## Start

```bash
./aokchaind -daemon
```

Use `-printtoconsole` instead of `-daemon` to watch the log in the terminal. The first sync downloads every block since 2020.

## Check the sync

```bash
aokchain-cli getblockchaininfo
```

The node is up to date when `blocks` equals `headers`.

## Stop

```bash
aokchain-cli stop
```
