---
title: Start and stop
description: "Run aokchaind in the foreground, in the background and as a systemd service, check that it is up, and stop it without damaging its data."
order: 30
---

How to start `aokchaind`, see that it is running, and stop it cleanly. A node that is killed in the middle of writing has to repair its databases at the next start, so always stop it the way this page shows.

## Start

In the foreground, with the log on the terminal:

```bash
aokchaind -printtoconsole
```

In the background:

```bash
aokchaind -daemon
```

`-daemonwait` works like `-daemon` but returns only when the node has started and answers commands, and returns an error status when the start failed. That suits scripts:

```bash
aokchaind -daemonwait && echo started
```

`-daemon` and `-daemonwait` exist on Linux and macOS. On Windows, run `aokchaind.exe` in a terminal, or use the desktop wallet.

Both can also be set in `aokchain.conf` (`daemon=1`). Give `-datadir=<dir>` to every command, `aokchaind` and `aokchain-cli`, when the data directory is not the default one.

## Check that it runs

```bash
aokchain-cli -rpcwait getblockchaininfo
```

While the node loads its databases, RPC calls answer with error `-28` and a message such as `Loading block index...`; `-rpcwait` waits until it can answer, also while a node that has just started has not written its cookie file yet. (Versions before 4.0.6 fail at that moment with `Could not locate RPC credentials`; with them, start the node with `-daemonwait` when a script calls it right away.) Then:

| Command | What to look at |
|---|---|
| `aokchain-cli getblockcount` | The height. It rises until it reaches the height of the other nodes. |
| `aokchain-cli getblockchaininfo` | `blocks`, `headers` and `verificationprogress` show how far the sync is. |
| `aokchain-cli getconnectioncount` | The number of peers. 0 for minutes means the node finds no peers; see [[ports-and-peers]]. |
| `aokchain-cli getnetworkinfo` | `subversion` is the version, for example `/AokChain:4.0.6/`. |
| `tail -f ~/.aokchain/debug.log` | What the node is doing. |

## Stop

```bash
aokchain-cli stop
```

It answers `AokChain server stopping` at once. The node then writes its caches to disk, which can take a while on a busy node. It is gone when its process has ended: `aokchaind.pid` is removed from the data directory and the last line of `debug.log` is `Shutdown: done`. Wait for that before you copy files, replace the program or start it again.

```bash
aokchain-cli stop
while [ -e ~/.aokchain/aokchaind.pid ]; do sleep 1; done
tail -1 ~/.aokchain/debug.log
```

`SIGTERM` and `SIGINT` (Ctrl+C in the terminal) stop the node the same way. `SIGHUP` makes it reopen `debug.log`, which log rotation needs.

> [!WARNING]
> Do not stop the node with `kill -9`, by switching the computer off, or by a service manager that gives up after a few seconds. The databases then have to be checked or rebuilt at the next start, which can take as long as a new sync.

## Run it as a systemd service

A unit for a node that runs as the user `aok` with the default data directory:

```ini
# /etc/systemd/system/aokchaind.service
[Unit]
Description=AokChain Core node
After=network-online.target
Wants=network-online.target

[Service]
User=aok
Group=aok
Type=forking
PIDFile=/home/aok/.aokchain/aokchaind.pid
ExecStart=/usr/local/bin/aokchaind -daemon -pid=/home/aok/.aokchain/aokchaind.pid
ExecStop=/usr/local/bin/aokchain-cli stop
TimeoutStopSec=600
Restart=on-failure
RestartSec=30

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now aokchaind
systemctl status aokchaind
```

- `TimeoutStopSec=600` gives the node ten minutes to write its data. With a short timeout, systemd kills a node that is still shutting down.
- `systemctl stop aokchaind` waits until the node has ended.
- For another data directory add `-datadir=<dir>` to `ExecStart` and `ExecStop`, and point `PIDFile` and `-pid` into it.

Do not also keep a node alive with a cron line such as `* * * * * aokchaind -daemon`. Such a line starts the node again within a minute of every stop, also while you replace the programs.

## Run commands at start and stop

| Option | Runs |
|---|---|
| `-startupnotify=<cmd>` | When the node has started and answers RPC requests. |
| `-shutdownnotify=<cmd>` | Right before the shutdown begins; the node waits for it to finish. |
| `-blocknotify=<cmd>` | When the best block changes; `%s` is the block hash. |
| `-walletnotify=<cmd>` | When a wallet transaction is added or changes; `%s` is the transaction id. See [[exchange-integration]]. |
