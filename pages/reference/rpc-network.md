---
title: RPC: Network
description: RPC reference: peers, connections, bans and network traffic.
order: 25
generated_by: tools/rpc_reference.py
---

The help text of every command in the network category, as AokChain Core 4.0.5 prints it with `aokchain-cli help <command>`. All categories are on [[rpc]].

> [!NOTE]
> Many examples in these help texts come from the upstream code: their addresses are often
> Bitcoin addresses, and their `curl` lines use port 8766. An AokChain node answers JSON-RPC on
> port 33440 (mainnet) or 44550 (testnet and regtest) unless `rpcport` says otherwise; see [[json-rpc]].

| Command | Summary |
|---|---|
| [addnode](#addnode) | Attempts to add or remove a node from the addnode list. |
| [clearbanned](#clearbanned) | Clear all banned IPs. |
| [disconnectnode](#disconnectnode) | Immediately disconnects from the specified peer node. |
| [getaddednodeinfo](#getaddednodeinfo) | Returns information about the given added node, or all added nodes (note that onetry addnodes are not listed here) |
| [getconnectioncount](#getconnectioncount) | Returns the number of connections to other nodes. |
| [getnettotals](#getnettotals) | Returns information about network traffic, including bytes in, bytes out, and current time. |
| [getnetworkinfo](#getnetworkinfo) | Returns an object containing various state info regarding P2P networking. |
| [getnodeaddresses](#getnodeaddresses) | Returns known addresses of nodes, which can be used to find new nodes in the network. |
| [getpeerinfo](#getpeerinfo) | Returns data about each connected network node as a json array of objects. |
| [listbanned](#listbanned) | List all banned IPs/Subnets. |
| [ping](#ping) | Requests that a ping be sent to all other nodes, to measure ping time. |
| [setban](#setban) | Attempts to add or remove an IP/Subnet from the banned list. |
| [setnetworkactive](#setnetworkactive) | Disable/enable all p2p network activity. |

### addnode

```text
addnode "node" "add|remove|onetry"
```

Attempts to add or remove a node from the addnode list. Or try a connection to a node once. Nodes added using addnode (or -connect) are protected from DoS disconnection and are not required to be full nodes/support SegWit as other outbound peers are (though such peers will not be synced from).

**Arguments**

```text
1. "node"     (string, required) The node (see getpeerinfo for nodes)
2. "command"  (string, required) 'add' to add a node to the list, 'remove' to remove a node from the list, 'onetry' to try a connection to the node once
```

**Examples**

```text
> aokchain-cli addnode "192.168.0.6:8767" "onetry"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "addnode", "params": ["192.168.0.6:8767", "onetry"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### clearbanned

```text
clearbanned
```

Clear all banned IPs.

**Examples**

```text
> aokchain-cli clearbanned
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "clearbanned", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### disconnectnode

```text
disconnectnode "[address]" [nodeid]
```

Immediately disconnects from the specified peer node.

Strictly one out of 'address' and 'nodeid' can be provided to identify the node.

To disconnect by nodeid, either set 'address' to the empty string, or call using the named 'nodeid' argument only.

**Arguments**

```text
1. "address"     (string, optional) The IP address/port of the node
2. "nodeid"      (number, optional) The node ID (see getpeerinfo for node IDs)
```

**Examples**

```text
> aokchain-cli disconnectnode "192.168.0.6:8767"
> aokchain-cli disconnectnode "" 1
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "disconnectnode", "params": ["192.168.0.6:8767"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "disconnectnode", "params": ["", 1] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getaddednodeinfo

```text
getaddednodeinfo ( "node" )
```

Returns information about the given added node, or all added nodes (note that onetry addnodes are not listed here)

**Arguments**

```text
1. "node"   (string, optional) If provided, return information about this specific node, otherwise all nodes are returned.
```

**Result**

```text
[
  {
    "addednode" : "192.168.0.201",   (string) The node IP address or name (as provided to addnode)
    "connected" : true|false,          (boolean) If connected
    "addresses" : [                    (list of objects) Only when connected = true
       {
         "address" : "192.168.0.201:8767",  (string) The aokchain server IP and port we're connected to
         "connected" : "outbound"           (string) connection, inbound or outbound
       }
     ]
  }
  ,...
]
```

**Examples**

```text
> aokchain-cli getaddednodeinfo "192.168.0.201"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getaddednodeinfo", "params": ["192.168.0.201"] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getconnectioncount

```text
getconnectioncount
```

Returns the number of connections to other nodes.

**Result**

```text
n          (numeric) The connection count
```

**Examples**

```text
> aokchain-cli getconnectioncount
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getconnectioncount", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getnettotals

```text
getnettotals
```

Returns information about network traffic, including bytes in, bytes out, and current time.

**Result**

```text
{
  "totalbytesrecv": n,   (numeric) Total bytes received
  "totalbytessent": n,   (numeric) Total bytes sent
  "timemillis": t,       (numeric) Current UNIX time in milliseconds
  "uploadtarget":
  {
    "timeframe": n,                         (numeric) Length of the measuring timeframe in seconds
    "target": n,                            (numeric) Target in bytes
    "target_reached": true|false,           (boolean) True if target is reached
    "serve_historical_blocks": true|false,  (boolean) True if serving historical blocks
    "bytes_left_in_cycle": t,               (numeric) Bytes left in current time cycle
    "time_left_in_cycle": t                 (numeric) Seconds left in current time cycle
  }
}
```

**Examples**

```text
> aokchain-cli getnettotals
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getnettotals", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getnetworkinfo

```text
getnetworkinfo
```

Returns an object containing various state info regarding P2P networking.

**Result**

```text
{
  "version": xxxxx,                      (numeric) the server version
  "subversion": "/Satoshi:x.x.x/",     (string) the server subversion string
  "protocolversion": xxxxx,              (numeric) the protocol version
  "localservices": "xxxxxxxxxxxxxxxx", (string) the services we offer to the network
  "localrelay": true|false,              (bool) true if transaction relay is requested from peers
  "timeoffset": xxxxx,                   (numeric) the time offset
  "connections": xxxxx,                  (numeric) the number of connections
  "networkactive": true|false,           (bool) whether p2p networking is enabled
  "networks": [                          (array) information per network
  {
    "name": "xxx",                     (string) network (ipv4, ipv6 or onion)
    "limited": true|false,               (boolean) is the network limited using -onlynet?
    "reachable": true|false,             (boolean) is the network reachable?
    "proxy": "host:port"               (string) the proxy that is used for this network, or empty if none
    "proxy_randomize_credentials": true|false,  (string) Whether randomized credentials are used
  }
  ,...
  ],
  "relayfee": x.xxxxxxxx,                (numeric) minimum relay fee for transactions in AOK/kB
  "incrementalfee": x.xxxxxxxx,          (numeric) minimum fee increment for mempool limiting or BIP 125 replacement in AOK/kB
  "localaddresses": [                    (array) list of local addresses
  {
    "address": "xxxx",                 (string) network address
    "port": xxx,                         (numeric) network port
    "score": xxx                         (numeric) relative score
  }
  ,...
  ]
  "warnings": "..."                    (string) any network and blockchain warnings
}
```

**Examples**

```text
> aokchain-cli getnetworkinfo
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getnetworkinfo", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getnodeaddresses

```text
getnodeaddresses ( count )
```

Returns known addresses of nodes, which can be used to find new nodes in the network.

**Arguments**

```text
1. count    (numeric, optional, default=1) How many addresses to return, at most 2500; 0 returns all that are known
```

**Result**

```text
[
  {
    "time": ttt,          (numeric) Timestamp in seconds since the epoch when the node was last seen
    "services": n,        (numeric) The services offered
    "address": "host",    (string) The address of the node
    "port": n             (numeric) The port of the node
  }, ...
]
```

**Examples**

```text
> aokchain-cli getnodeaddresses 8
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getnodeaddresses", "params": [8] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getpeerinfo

```text
getpeerinfo
```

Returns data about each connected network node as a json array of objects.

**Result**

```text
[
  {
    "id": n,                   (numeric) Peer index
    "addr":"host:port",      (string) The IP address and port of the peer
    "addrbind":"ip:port",    (string) Bind address of the connection to the peer
    "addrlocal":"ip:port",   (string) Local address as reported by the peer
    "services":"xxxxxxxxxxxxxxxx",   (string) The services offered
    "relaytxes":true|false,    (boolean) Whether peer has asked us to relay transactions to it
    "lastsend": ttt,           (numeric) The time in seconds since epoch (Jan 1 1970 GMT) of the last send
    "lastrecv": ttt,           (numeric) The time in seconds since epoch (Jan 1 1970 GMT) of the last receive
    "bytessent": n,            (numeric) The total bytes sent
    "bytesrecv": n,            (numeric) The total bytes received
    "conntime": ttt,           (numeric) The connection time in seconds since epoch (Jan 1 1970 GMT)
    "timeoffset": ttt,         (numeric) The time offset in seconds
    "pingtime": n,             (numeric) ping time (if available)
    "minping": n,              (numeric) minimum observed ping time (if any at all)
    "pingwait": n,             (numeric) ping wait (if non-zero)
    "version": v,              (numeric) The peer version, such as 7001
    "subver": "/Satoshi:0.8.5/",  (string) The string version
    "inbound": true|false,     (boolean) Inbound (true) or Outbound (false)
    "addnode": true|false,     (boolean) Whether connection was due to addnode/-connect or if it was an automatic/inbound connection
    "startingheight": n,       (numeric) The starting height (block) of the peer
    "banscore": n,             (numeric) The ban score
    "synced_headers": n,       (numeric) The last header we have in common with this peer
    "synced_blocks": n,        (numeric) The last block we have in common with this peer
    "inflight": [
       n,                        (numeric) The heights of blocks we're currently asking from this peer
       ...
    ],
    "whitelisted": true|false, (boolean) Whether the peer is whitelisted
    "bytessent_per_msg": {
       "addr": n,              (numeric) The total bytes sent aggregated by message type
       ...
    },
    "bytesrecv_per_msg": {
       "addr": n,              (numeric) The total bytes received aggregated by message type
       ...
    }
  }
  ,...
]
```

**Examples**

```text
> aokchain-cli getpeerinfo
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getpeerinfo", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### listbanned

```text
listbanned
```

List all banned IPs/Subnets.

**Examples**

```text
> aokchain-cli listbanned
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "listbanned", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### ping

```text
ping
```

Requests that a ping be sent to all other nodes, to measure ping time. Results provided in getpeerinfo, pingtime and pingwait fields are decimal seconds. Ping command is handled in queue with all other commands, so it measures processing backlog, not just network ping.

**Examples**

```text
> aokchain-cli ping
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "ping", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### setban

```text
setban "subnet" "add|remove" (bantime) (absolute)
```

Attempts to add or remove an IP/Subnet from the banned list.

**Arguments**

```text
1. "subnet"       (string, required) The IP/Subnet (see getpeerinfo for nodes IP) with an optional netmask (default is /32 = single IP)
2. "command"      (string, required) 'add' to add an IP/Subnet to the list, 'remove' to remove an IP/Subnet from the list
3. "bantime"      (numeric, optional) time in seconds how long (or until when if [absolute] is set) the IP is banned (0 or empty means using the default time of 24h which can also be overwritten by the -bantime startup argument)
4. "absolute"     (boolean, optional) If set, the bantime must be an absolute timestamp in seconds since epoch (Jan 1 1970 GMT)
```

**Examples**

```text
> aokchain-cli setban "192.168.0.6" "add" 86400
> aokchain-cli setban "192.168.0.0/24" "add"
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "setban", "params": ["192.168.0.6", "add", 86400] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### setnetworkactive

```text
setnetworkactive true|false
```

Disable/enable all p2p network activity.

**Arguments**

```text
1. "state"        (boolean, required) true to enable networking, false to disable
```
