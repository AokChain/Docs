---
title: ZeroMQ notifications
description: Have the node push new blocks and transactions to your program over ZeroMQ: the four topics, the message layout and a subscriber in Python.
order: 90
---

Instead of polling, a program can subscribe to the node and receive every new block and transaction as it happens. AokChain Core publishes them over ZeroMQ; the release programs are built with it.

## Turn it on

Give each topic an address to publish on, in `aokchain.conf` or on the command line:

```ini
zmqpubhashblock=tcp://127.0.0.1:28441
zmqpubrawtx=tcp://127.0.0.1:28441
```

| Option | Publishes |
|---|---|
| `zmqpubhashblock=<address>` | The hash of every new tip block. |
| `zmqpubrawblock=<address>` | The whole new tip block, serialized. |
| `zmqpubhashtx=<address>` | The id of every transaction the node sees. |
| `zmqpubrawtx=<address>` | Every such transaction, serialized. |

Several topics can share one address. The node only sends: a subscriber connects to it, and nothing comes back. Bind to `127.0.0.1` or a private network; ZeroMQ has no authentication here.

## Messages

Each message has three parts:

1. the topic: `hashblock`, `hashtx`, `rawblock` or `rawtx`;
2. the body: a 32-byte hash (in the byte order that RPC prints), or the serialized block or transaction;
3. a 4-byte little-endian sequence number, counted per topic. A gap means messages were lost.

When they are sent:

- **Blocks:** when the tip changes, not while the node is in its initial sync. After a reorganization only the new tip is announced.
- **Transactions:** when a transaction enters the mempool, and again for every transaction of a block that is connected or disconnected. The same transaction therefore arrives more than once; use the messages as a signal and keep your own state.

The raw formats are AokChain's: a transaction has a time field after its version ([[raw-transactions]]), and a block carries its signature after the transactions. A block hash is the BLAKE2b-256 hash of the 80-byte header, not the double SHA-256 of Bitcoin; transaction ids are double SHA-256 as in Bitcoin.

ZeroMQ does not guarantee delivery. After a restart of either side, or a gap in the sequence, catch up with RPC (`getbestblockhash`, `getblock`, `listsinceblock`).

## A subscriber in Python

With `pip install pyzmq`:

```bash
python3 - <<'EOF'
import struct, zmq
sock = zmq.Context().socket(zmq.SUB)
sock.connect("tcp://127.0.0.1:28441")
for topic in (b"hashblock", b"rawtx"):
    sock.setsockopt(zmq.SUBSCRIBE, topic)
while True:
    topic, body, seq = sock.recv_multipart()
    n = struct.unpack("<I", seq)[0]
    if topic == b"hashblock":
        print(n, "block", body.hex())
    else:
        print(n, "tx of", len(body), "bytes")
EOF
```

Decode a raw transaction with `aokchain-cli decoderawtransaction <hex>`, or with your own parser that knows the time field.
