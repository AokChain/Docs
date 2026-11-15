---
title: Configuration
description: The options of aokchain.conf that most nodes need, with their defaults.
order: 2
---

Options go in `aokchain.conf`, one per line, or on the command line with a leading `-`. A command line option wins over the file.

## Network

| Option | Default | What it does |
|---|--:|---|
| `port` | `33441` | Port for peer connections |
| `listen` | `1` | Accept connections from peers |
| `maxconnections` | `125` | Most peers at a time |
| `addnode` | | Connect to this node too (repeatable) |

## RPC

| Option | Default | What it does |
|---|--:|---|
| `rpcport` | `33440` | Port for JSON-RPC |
| `rpcuser` | | User name for JSON-RPC |
| `rpcpassword` | | Password for JSON-RPC |
| `rpcallowip` | `127.0.0.1` | Hosts allowed to connect (repeatable) |

## Wallet and staking

| Option | Default | What it does |
|---|--:|---|
| `staking` | `0` | Stake with the coins in the wallet |
| `disablewallet` | `0` | Run without a wallet |
| `walletnotify` | | Run a command when a wallet transaction changes |

## A full example

```ini
listen=1
maxconnections=64
rpcuser=nodeuser
rpcpassword=use-a-long-random-password
rpcallowip=127.0.0.1
staking=1
```

Start the node with these options; see [[run-a-node#start]].
