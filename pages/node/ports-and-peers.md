---
title: Ports and peers
description: "The P2P and RPC ports of each network, how a node finds peers, how to accept incoming connections, and the commands that manage peers."
order: 60
---

Which ports a node uses, how it finds other nodes, and what to do when it finds none.

## Ports

| Network | P2P port | RPC port |
|---|---|---|
| Mainnet | 33441 | 33440 |
| Testnet | 44551 | 44550 |
| Regtest | 18444 | 44550 |

- The P2P port is where other nodes connect. Change it with `port=<n>`.
- The RPC port answers [[json-rpc|JSON-RPC]] and `aokchain-cli`. By default it listens on `127.0.0.1` and `::1` only. Change it with `rpcport=<n>`. Testnet and regtest share 44550, so give one of them another `rpcport` to run both on one computer.
- Keep the RPC port closed to the internet. It controls the node and its wallets.

## How a node finds peers

1. It reads the addresses it learned before from `peers.dat`.
2. On mainnet it asks the DNS seed `dns.aok.network` when it knows too few addresses.
3. It tries a list of fixed seed nodes built into the program.
4. Connected peers tell it more addresses.

A node keeps up to 16 outgoing connections, plus up to 8 to nodes given with `addnode`. `maxconnections` (default 125) limits all connections together, incoming included.

## When the node has no peers

`getconnectioncount` stays at 0, and `getblockchaininfo` shows no progress. Add a node you know is running:

```bash
aokchain-cli addnode "203.0.113.10:33441" "onetry"
```

To keep the connection across restarts, add it to `aokchain.conf`:

```ini
addnode=203.0.113.10
addnode=203.0.113.11
```

A node that already has peers prints their addresses with `getpeerinfo`, so another node of yours can tell you where to connect. Other causes of 0 peers: a firewall that blocks outgoing TCP to port 33441, or a proxy setting that does not work.

## Accept incoming connections

A node accepts incoming connections when `listen=1` (the default unless `proxy` or `connect` is set) and other nodes can reach its P2P port.

1. Allow incoming TCP to port 33441 in the firewall, for example `sudo ufw allow 33441/tcp`.
2. Forward the port on the router if the node is behind NAT. `upnp=1` asks the router to do it; it is off by default.
3. Check from `getnetworkinfo`: `localaddresses` lists the addresses the node announces, and `getpeerinfo` shows peers with `"inbound": 1` once others connect.

`externalip=<ip>` sets the address that the node announces, `bind=<addr>` the local address it listens on. `discover=0` stops it from looking up its own addresses.

A node started from the chain state snapshot does not serve the blocks before the snapshot until it has fetched them (see [[fast-sync]]). Nodes that run all the time, such as exchange and staking servers, help the network most when they keep all blocks.

## Commands

| Command | Use |
|---|---|
| `getpeerinfo` | Every connected peer: address, `version` (70021 for 4.0), `subver` (for example `/AokChain:4.0.7/`), `startingheight`, ping. |
| `getconnectioncount` | The number of peers. |
| `getnetworkinfo` | Version, protocol, local addresses, proxies, relay fee. |
| `getnodeaddresses` | Known peer addresses, a random selection. |
| `addnode <node> add\|remove\|onetry` | Add or remove a node to keep connected, or try it once. |
| `getaddednodeinfo` | The nodes added with `addnode`. |
| `disconnectnode <address>` | Drop a connection. |
| `setban <ip or subnet> add\|remove` | Ban or unban; `listbanned` and `clearbanned` show and clear the list. |
| `setnetworkactive false\|true` | Turn all P2P traffic off and on. |
| `getnettotals` | Bytes sent and received. |

The full help of each is on [[rpc-network]].

## Proxies and Tor

`proxy=127.0.0.1:9050` sends outgoing connections through a SOCKS5 proxy such as Tor, and `onlynet=<net>` limits the node to one network. The onion service of the node (`listenonion`) and `.onion` peer addresses use the old version 2 format of Tor, which current Tor releases no longer support, so a node cannot be reached as an onion service.

## Protocol versions

AokChain Core 4.0 speaks protocol version 70021 and connects to 3.0.x nodes (70020) as before. It accepts peers from version 60018 on. The network message start of each network is on [[network-parameters]].
