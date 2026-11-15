---
title: "RPC: Control"
description: "RPC reference: memory, running commands, uptime, help and stopping the node."
order: 22
generated_by: tools/rpc_reference.py
---

The help text of every command in the control category, as AokChain Core 4.0.5 prints it with `aokchain-cli help <command>`. All categories are on [[rpc]].

> [!NOTE]
> Many examples in these help texts come from the upstream code: their addresses are often
> Bitcoin addresses, and their `curl` lines use port 8766. An AokChain node answers JSON-RPC on
> port 33440 (mainnet) or 44550 (testnet and regtest) unless `rpcport` says otherwise; see [[json-rpc]].

| Command | Summary |
|---|---|
| [getmemoryinfo](#getmemoryinfo) | Returns an object containing information about memory usage. |
| [getrpcinfo](#getrpcinfo) | Returns details of the RPC server. |
| [help](#help) | List all commands, or get help for a specified command. |
| [stop](#stop) | Stop AokChain server. |
| [uptime](#uptime) | Returns the total uptime of the server. |

### getmemoryinfo

```text
getmemoryinfo ("mode")
```

Returns an object containing information about memory usage.

**Arguments**

```text
1. "mode" determines what kind of information is returned. This argument is optional, the default mode is "stats".
  - "stats" returns general statistics about memory usage in the daemon.
  - "mallocinfo" returns an XML string describing low-level heap state (only available if compiled with glibc 2.10+).
```

**Result (mode "stats")**

```text
{
  "locked": {               (json object) Information about locked memory manager
    "used": xxxxx,          (numeric) Number of bytes used
    "free": xxxxx,          (numeric) Number of bytes available in current arenas
    "total": xxxxxxx,       (numeric) Total number of bytes managed
    "locked": xxxxxx,       (numeric) Amount of bytes that succeeded locking. If this number is smaller than total, locking pages failed at some point and key data could be swapped to disk.
    "chunks_used": xxxxx,   (numeric) Number allocated chunks
    "chunks_free": xxxxx,   (numeric) Number unused chunks
  }
}
```

**Result (mode "mallocinfo")**

```text
"<malloc version="1">..."
```

**Examples**

```text
> aokchain-cli getmemoryinfo
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getmemoryinfo", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### getrpcinfo

```text
getrpcinfo
```

Returns details of the RPC server.

**Result**

```text
{
  "active_commands": [        (array) The commands that are running now, this one included
    {
      "method": "name",       (string) The name of the command
      "duration": n            (numeric) The running time in microseconds
    }, ...
  ]
}
```

**Examples**

```text
> aokchain-cli getrpcinfo
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getrpcinfo", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```

### help

```text
help ( "command" )
```

List all commands, or get help for a specified command.

**Arguments**

```text
1. "command"     (string, optional) The command to get help on
```

**Result**

```text
"text"     (string) The help text
```

### stop

```text
stop
```

Stop AokChain server.

### uptime

```text
uptime
```

Returns the total uptime of the server.

**Result**

```text
ttt        (numeric) The number of seconds that the server has been running
```

**Examples**

```text
> aokchain-cli uptime
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "uptime", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:8766/
```
