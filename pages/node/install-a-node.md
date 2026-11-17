---
title: Install a node
description: "Get AokChain Core 4.0 as a package or build it from source, and check what a node needs in disk, memory and network."
order: 10
aliases: [node]
---

A node is a copy of AokChain Core that keeps the whole chain, checks every block and answers [[json-rpc|JSON-RPC]] calls. This page gets the programs onto the computer. The next steps are [[configure-a-node]], [[start-and-stop]] and [[fast-sync]].

## The programs

| Program | What it is |
|---|---|
| `aokchaind` | The node without a window. It syncs the chain, keeps the wallets and answers RPC calls. |
| `aokchain-cli` | Sends one RPC command to a running node and prints the answer. |
| `aokchain-qt` | The desktop wallet: the same node with a window. See [[desktop-wallet]]. |
| `aokchain-tx` | Creates and edits raw transactions without a node. See [[raw-transactions]]. |
| `aokchain-wallet` | Looks into a wallet file, creates one or salvages one, while no node uses it. |

`aokchaind` and `aokchain-qt` are the same node. Only one program can use a data directory at a time; a second one refuses to start.

## What a node needs

| | |
|---|---|
| System | Linux x86_64 with glibc 2.34 or later (Ubuntu 22.04, Debian 12 or newer) for the Linux package. Windows 64-bit. The macOS package is being prepared. |
| Disk | The blocks alone are 2.1 GB (blocks 1 to 3,031,432); with the chain state and the indexes, plan for 5 GB or more, growing with the chain. A node started from the chain state snapshot needs about 1.1 GB, and about 3.5 GB once it has fetched the past blocks (see [[fast-sync]]). An SSD makes the first sync much faster. |
| Memory | 4 GB or more is comfortable. The database cache takes 1024 MiB by default on a computer with at least 4 GB of memory, 450 MiB on a smaller one (`dbcache`). |
| Network | Outgoing TCP connections to port 33441 of other nodes. Incoming connections are optional; see [[ports-and-peers]]. |
| Clock | A correct system clock. Blocks and transactions carry a time, and a node refuses blocks that are too far ahead of its own clock. Keep the system's time sync on. |

## Get the package

Downloads of the 4.0 programs are being prepared at [@@site_host@@/download](@@site@@/download/). Official downloads are listed on that site only, each with its SHA-256 checksum.

1. Download the archive for your system and the checksum file `SHA256SUMS.txt`.
2. Check the archive against the checksum file:

   ```bash
   sha256sum -c SHA256SUMS.txt --ignore-missing
   ```

   The line of your archive must end in `OK`.
3. Unpack it and put the programs where the system finds them. On Linux:

   ```bash
   tar xzf aokchain-4.0.6-linux-x86_64.tar.gz
   sudo install -m 0755 aokchain-4.0.6-linux-x86_64/aokchain* /usr/local/bin/
   aokchaind -version
   ```

   The first line says `AokChain Core Daemon version v4.0.6.0-` followed by the build's commit.

The Linux package holds `aokchaind`, `aokchain-cli`, `aokchain-tx` and `aokchain-wallet`; the libraries they need are built in. On Windows, unpack the archive into a folder of your choice. The Windows programs are not code-signed, so Windows asks for a confirmation the first time it starts them.

> [!WARNING]
> Install only programs whose checksum matches the one published on @@site_host@@. A wallet program from anywhere else can steal the keys of every wallet it opens.

## Build from source

The 4.0 source code is published at [github.com/AokChain/AokChain](https://github.com/AokChain/AokChain) with the release. Build the release tag. These steps build the node and the tools on Ubuntu 22.04 or 24.04.

1. Install the build tools:

   ```bash
   sudo apt-get install -y build-essential libtool autotools-dev automake pkg-config bsdmainutils python3 curl
   ```

2. Build the libraries that the release packages use, once, without the GUI. They include Berkeley DB 4.8, the wallet database of every release package:

   ```bash
   make -C depends NO_QT=1 -j"$(nproc)"
   ```

3. Configure against them and build:

   ```bash
   ./autogen.sh
   CONFIG_SITE=$PWD/depends/x86_64-pc-linux-gnu/share/config.site \
     ./configure --prefix=/ --without-gui --disable-bench --disable-tests --with-tx
   make -j"$(nproc)"
   ```

   The programs are `src/aokchaind`, `src/aokchain-cli`, `src/aokchain-tx` and `src/aokchain-wallet`. `aokchain-tx` is built only with `--with-tx`.

The build needs a C++17 compiler (GCC 13 is known to work) and about 1.5 GB of free memory per compiler job.

### The desktop wallet on Linux

The desktop wallet for Linux is built against the system's libraries and Qt 5:

```bash
sudo apt-get install -y libevent-dev libboost-dev libboost-system-dev libboost-filesystem-dev \
  libboost-program-options-dev libboost-thread-dev libboost-chrono-dev libssl-dev libdb5.3++-dev \
  libminiupnpc-dev libzmq3-dev qtbase5-dev qttools5-dev qttools5-dev-tools libprotobuf-dev \
  protobuf-compiler libqrencode-dev
./autogen.sh
./configure --with-incompatible-bdb --with-gui=qt5 --disable-bench --disable-tests
make -j"$(nproc)"
```

The program is `src/qt/aokchain-qt`.

> [!IMPORTANT]
> `--with-incompatible-bdb` uses the system's Berkeley DB (5.3 on Ubuntu). A wallet file that such a build has opened may no longer open in the release programs, which use Berkeley DB 4.8. Keep such a build away from wallets that hold real coins, or work on a copy.

## Next

- [[configure-a-node]]: where `aokchain.conf` and the data directory are.
- [[start-and-stop]]: run the node in the background and as a service.
- [[fast-sync]]: reach the tip in minutes instead of hours.
- [[upgrade-to-4-0]]: replace a 3.0.x node.
