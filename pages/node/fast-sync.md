---
title: Fast sync
description: Start a new node from the chain state snapshot or from the published block archives instead of downloading three million blocks from peers.
order: 40
---

A new node that downloads every block from its peers needs hours, because there are few peers and the chain has more than three million blocks. AokChain Core 4.0 has two faster ways. Both use files published at [github.com/AokChain/Mainnet-blocks](https://github.com/AokChain/Mainnet-blocks), and neither asks you to trust the server that hands them out.

| | Chain state snapshot | Block archives |
|---|---|---|
| What is downloaded | The chain state at block 3,031,432: about 1.0 GB in 6 parts | Blocks 1 to 3,031,432: 1.4 GB in 15 files |
| What the node checks | The hashes of the unspent outputs, tokens, governance state and block index must equal the values built into the program | Every block, exactly like a block from a peer |
| Time to the tip | A few minutes after the download | 25 to 60 minutes on a current computer, more on a slow disk |
| Disk afterwards | About 1.1 GB; the past blocks are not there | The whole chain |
| When it is used | Only in a new data directory, with the default indexes | Whenever the node is at least 20,000 blocks behind the archives |

After either one, the node gets the newer blocks from its peers as usual. If anything is wrong with a file, the node drops it and synchronizes from its peers instead.

## The desktop wallet

The desktop wallet does all of this by itself on the main network. On a first start it downloads the snapshot (or, with indexes that the snapshot does not have, the block archives) from the built-in address `https://github.com/AokChain/Mainnet-blocks/releases/download/mainnet/`. The sync screen can skip it and fall back to the peers, or take the files from a folder you downloaded before. In the settings, the Network settings window turns it off or sets other addresses.

## aokchaind: download the files, then start from the folder

`aokchaind` fetches `http://` addresses only, not the `https://` address of GitHub. On a server, download the files first and give the folder to the node with `bootstrapdir`:

1. Download every file of the release `mainnet` into one empty folder, with the GitHub CLI or any download tool:

   ```bash
   mkdir ~/aok-mainnet-files && cd ~/aok-mainnet-files
   gh release download mainnet -R AokChain/Mainnet-blocks
   ```

   For the snapshot alone, the files `snapshot.json`, `snapshot-03031432.part01` to `part06` and `SHA256SUMS` are enough (`-p 'snapshot*' -p SHA256SUMS`). The block archives are `manifest.json` and the `blocks-*.dat.gz` files.
2. Check them:

   ```bash
   sha256sum -c SHA256SUMS --ignore-missing
   ```

3. Start the node with a new, empty data directory and the folder:

   ```bash
   aokchaind -daemon -bootstrapdir=$HOME/aok-mainnet-files
   aokchain-cli -rpcwait getblockcount
   ```

   While it unpacks and checks the snapshot, RPC calls answer with messages such as `Fast start: unpacking the snapshot...`. About a minute and a half later the node answers at height 3,031,432 and continues from its peers.
4. Check the result:

   ```bash
   aokchain-cli getsnapshotinfo
   ```

   `accepted_height` is 3031432 when the snapshot was used. `past_blocks` says whether the blocks before it are `missing`, `downloading` or `present`.

The folder is only read; the node never changes or deletes it. You can also set `bootstrapdir=<folder>` in `aokchain.conf`, and remove it after the first sync. An HTTP mirror of the same files works as `bootstrapurl=http://…/`; several `bootstrapurl` lines are tried in order.

> [!IMPORTANT]
> Import the archives with `bootstrapdir` or `bootstrapurl`, not with `-loadblock`. The bootstrap connects the blocks one by one in order, which a token and governance chain like this one needs.

## The snapshot

The program accepts exactly one snapshot: the one at block 3,031,432 (`58a07d1f4dbe68b7fa66d864272ca6351a60de13a409c132b034c9da03af909a`). Its hashes are compiled in. A snapshot with other content, a damaged download or any error while loading is removed, and the node synchronizes from the blocks as it would without it.

What you trust is the program: that its builders computed these values from a fully validated chain. That is the same kind of trust as the `assumevalid` block, with a larger effect, since the snapshot skips all checks below its height. To check the values yourself, sync a node with `-snapshot=0` and compare `aokchain-cli getstatehashes` at that height with the values built into the program.

A node starts from the snapshot only when all of these hold:

- the data directory is new (no chain yet);
- `snapshot` and `bootstrap` are not turned off;
- there is a source: `bootstrapdir`, an `http://` `bootstrapurl`, or the built-in address of the desktop wallet;
- no `-reindex`, no `prune`, and the indexes are the defaults (`txindex=1`, no `addressindex`, `spentindex` or `timestampindex`).

### The past blocks

A node started from the snapshot has no copy of blocks 1 to 3,031,432. It validates and stakes new blocks without them. A few things need them and say so until they are there:

- `getblock` and `getrawtransaction` for those blocks,
- a wallet rescan from before the snapshot, importing an existing wallet, keys or addresses with a rescan,
- serving those blocks to new nodes, and `-reindex`.

Fetch them in the background with `aokchain-cli fetchblocks`, or start with `fetchblocks=1`. They come from the block archives of the same source, are checked against the block index and stored; nothing is validated again. That takes a few minutes and about 2.4 GB more disk. Nodes that run all the time should fetch them, so that new nodes can sync from them.

## The block archives

The node imports an archive only when it is at least 20,000 blocks behind it (`bootstrapminblocks`; a folder given with `bootstrapdir` is used whenever it has blocks that the node lacks). A node whose last block is less than three days old does not look at the archives at all. While it imports, the node gets only headers from its peers; afterwards it gets the remaining blocks from them.

`getbootstrapinfo` shows the state, the archive count and the progress; `skipbootstrap` gives the archives up and switches to the peers.

## Turn it off

| Setting | Effect |
|---|---|
| `snapshot=0` | Never start from a snapshot; the block archives can still be used. |
| `bootstrap=0` | Neither the snapshot nor the block archives. |
| `assumevalid=0` | Also check the signatures below block 3,030,000, which a node otherwise skips once it has the headers past that block. |

All other checks of every block (proof of stake, amounts, double spends, token and governance rules) run in every case.
