---
title: "RPC: Generating"
description: "RPC reference: making proof-of-work blocks on regtest, and the generate setting."
order: 23
generated_by: tools/rpc_reference.py
---

The help text of every command in the generating category, as AokChain Core 4.0.8 prints it with `aokchain-cli help <command>`. All categories are on [[rpc]].

> [!NOTE]
> The addresses in the examples of these help texts are example addresses that belong to nobody.
> Their `curl` lines use port 33440, where a node of the main network answers JSON-RPC; on testnet
> and regtest it is port 44550, and `rpcport` sets another one. See [[json-rpc]].

| Command | Summary |
|---|---|
| [generate](#generate) | Mine up to nblocks blocks immediately (before the RPC call returns) to an address in the wallet. |
| [generatetoaddress](#generatetoaddress) | Mine blocks immediately to a specified address (before the RPC call returns) |
| [getgenerate](#getgenerate) | Return if the server is set to generate coins or not. |

### generate

```text
generate nblocks ( maxtries )
```

Mine up to nblocks blocks immediately (before the RPC call returns) to an address in the wallet.

**Arguments**

```text
1. nblocks      (numeric, required) How many blocks are generated immediately.
2. maxtries     (numeric, optional) How many iterations to try (default = 1000000).
```

**Result**

```text
[ blockhashes ]     (array) hashes of blocks generated
```

**Examples**

```text
Generate 11 blocks
> aokchain-cli generate 11
```

### generatetoaddress

```text
generatetoaddress nblocks address (maxtries)
```

Mine blocks immediately to a specified address (before the RPC call returns)

**Arguments**

```text
1. nblocks      (numeric, required) How many blocks are generated immediately.
2. address      (string, required) The address to send the newly generated aokchain to.
3. maxtries     (numeric, optional) How many iterations to try (default = 1000000).
```

**Result**

```text
[ blockhashes ]     (array) hashes of blocks generated
```

**Examples**

```text
Generate 11 blocks to myaddress
> aokchain-cli generatetoaddress 11 "myaddress"
```

### getgenerate

```text
getgenerate
```

Return if the server is set to generate coins or not. The default is false. It is set with the command line argument -gen (or aokchain.conf setting gen) It can also be set with the setgenerate call.

**Result**

```text
true|false      (boolean) If the server is set to generate coins or not
```

**Examples**

```text
> aokchain-cli getgenerate
> curl --user myusername --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getgenerate", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:33440/
```
