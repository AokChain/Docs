---
title: "Configuration options"
description: "Every option of aokchaind, the GUI wallet and the command-line tools, from the programs' own help, grouped as -help prints them."
order: 11
generated_by: tools/options_reference.py
---

The options of AokChain Core 4.0.6, as `aokchaind -help` prints them. Give an option on the command line as `-name=value`, or write it as a line `name=value` in `aokchain.conf` (where the file lives is on [[configure-a-node]]). A setting on the command line wins over the same setting in the file. A switch such as `-txindex` is turned on with `1` and off with `0`, and `-nofoo` is the same as `-foo=0`.

The GUI wallet, `aokchain-qt`, takes the same options except `-daemon` and `-daemonwait`, and the few of its own listed under [GUI options](#gui-options).

## Contents

- [General options](#general-options)
- [Connection options](#connection-options)
- [Wallet options](#wallet-options)
- [ZeroMQ notification options](#zeromq-notification-options)
- [Debugging/Testing options](#debuggingtesting-options)
- [Chain selection options](#chain-selection-options)
- [Node relay options](#node-relay-options)
- [Block creation options](#block-creation-options)
- [RPC server options](#rpc-server-options)
- [GUI options](#gui-options)
- [Options not listed by -help](#options-not-listed-by--help)
- [Debugging options](#debugging-options)
- [aokchain-cli options](#aokchain-cli-options)
- [aokchain-tx](#aokchain-tx)
- [aokchain-wallet](#aokchain-wallet)

## General options

| Option | Description |
|---|---|
| `-?` | Print this help message and exit |
| `-version` | Print version and exit |
| `-alertnotify=<cmd>` | Execute command when a relevant alert is received or we see a really long fork (%s in cmd is replaced by message) |
| `-blocknotify=<cmd>` | Execute command when the best block changes (%s in cmd is replaced by block hash) |
| `-startupnotify=<cmd>` | Execute command when the node has started and answers RPC requests |
| `-shutdownnotify=<cmd>` | Execute command immediately before beginning shutdown; the node waits for it to finish |
| `-assumevalid=<hex>` | If this block is in the chain assume that it and its ancestors are valid and potentially skip their script verification (0 to verify all, default: 27a0660bf43381e7d367472a74d696873ff69bb36582031f9c2ed2ae1c58bdf1, testnet: 0000000000000000000000000000000000000000000000000000000000000000) |
| `-conf=<file>` | Specify configuration file (default: aokchain.conf) |
| `-daemon` | Run in the background as a daemon and accept commands |
| `-daemonwait` | Run in the background as a daemon like -daemon, and return when the node has started and accepts commands |
| `-datadir=<dir>` | Specify data directory |
| `-dbcache=<n>` | Set database cache size in megabytes (4 to 16384, default: 1024) |
| `-loadblock=<file>` | Imports blocks from external blk000??.dat file on startup |
| `-bootstrapurl=<url>` | Fetch the blocks as archives from this address when the node is far behind, instead of from peers. Every block is validated as usual. Can be given several times: mirrors, tried in this order. (default: none; on the main network the GUI wallet uses https://github.com/AokChain/Mainnet-blocks/releases/download/mainnet/) |
| `-bootstrapdir=<dir>` | Import the block archives (manifest.json and the files it lists) from this folder, which is only read. Every block is validated as usual. |
| `-bootstrap` | Use the block archives of -bootstrapurl or -bootstrapdir (default: 1) |
| `-snapshot` | In a new data directory, start from the chain state snapshot that this program accepts instead of validating every block from the first one. The snapshot is taken from -bootstrapurl or -bootstrapdir and is used only when its content has the hashes that are compiled into this program. (default: 1) |
| `-fetchblocks` | After a start from a chain state snapshot, download the past blocks in the background (default: 0) |
| `-bootstrapminblocks=<n>` | Use the block archives only when the node is at least this many blocks behind them (default: 20000) |
| `-maxreorg=<n>` | Set the Maximum reorg depth (default: 500) |
| `-maxorphantx=<n>` | Keep at most &lt;n&gt; unconnectable transactions in memory (default: 100) |
| `-maxmempool=<n>` | Keep the transaction memory pool below &lt;n&gt; megabytes (default: 300) |
| `-mempoolexpiry=<n>` | Do not keep transactions in the mempool longer than &lt;n&gt; hours (default: 336) |
| `-persistmempool` | Whether to save the mempool on shutdown and load on restart (default: 1) |
| `-blockreconstructionextratxn=<n>` | Extra transactions to keep in memory for compact block reconstructions (default: 100) |
| `-par=<n>` | Set the number of script verification threads (-8 to 16, 0 = auto, &lt;0 = leave that many cores free, default: 0) |
| `-pid=<file>` | Specify pid file (default: aokchaind.pid) |
| `-prune=<n>` | Reduce storage requirements by enabling pruning (deleting) of old blocks. This allows the pruneblockchain RPC to be called to delete specific blocks, and enables automatic pruning of old blocks if a target size in MiB is provided. This mode is incompatible with -txindex and -rescan. Warning: Reverting this setting requires re-downloading the entire blockchain. (default: 0 = disable pruning blocks, 1 = allow manual pruning via RPC, &gt;550 = automatically prune block files to stay under the specified target size in MiB) |
| `-reindex-chainstate` | Rebuild chain state from the currently indexed blocks |
| `-reindex` | Rebuild chain state and block index from the blk\*.dat files on disk |
| `-sysperms` | Create new files with system default permissions, instead of umask 077 (only effective with disabled wallet functionality) |
| `-txindex` | Maintain a full transaction index, used by the getrawtransaction rpc call (default: 1) |
| `-addressindex` | Maintain a full address index, used to query for the balance, txids and unspent outputs for addresses (default: 0) |
| `-timestampindex` | Maintain a timestamp index for block hashes, used to query blocks hashes by a range of timestamps (default: 0) |
| `-spentindex` | Maintain a full spent index, used to query the spending txid and input index for an outpoint (default: 0) |

> [!NOTE]
> `-dbcache`: The default is 1024 MiB on a computer with at least 4 GiB of memory and 450 MiB otherwise; the help prints the value for the computer it runs on.


## Connection options

| Option | Description |
|---|---|
| `-addnode=<ip>` | Add a node to connect to and attempt to keep the connection open (see the \`addnode\` RPC command help for more info) |
| `-banscore=<n>` | Threshold for disconnecting misbehaving peers (default: 100) |
| `-bantime=<n>` | Number of seconds to keep misbehaving peers from reconnecting (default: 86400) |
| `-bind=<addr>` | Bind to given address and always listen on it. Use \[host\]:port notation for IPv6 |
| `-connect=<ip>` | Connect only to the specified node(s); -connect=0 disables automatic connections (the rules for this peer are the same as for -addnode) |
| `-discover` | Discover own IP addresses (default: 1 when listening and no -externalip or -proxy) |
| `-dns` | Allow DNS lookups for -addnode, -seednode and -connect (default: 1) |
| `-dnsseed` | Query for peer addresses via DNS lookup, if low on addresses (default: 1 unless -connect used) |
| `-externalip=<ip>` | Specify your own public address |
| `-forcednsseed` | Always query for peer addresses via DNS lookup (default: 1) |
| `-listen` | Accept connections from outside (default: 1 if no -proxy or -connect) |
| `-listenonion` | Automatically create Tor hidden service (default: 1) |
| `-maxconnections=<n>` | Maintain at most &lt;n&gt; connections to peers (default: 125) |
| `-maxreceivebuffer=<n>` | Maximum per-connection receive buffer, &lt;n&gt;\*1000 bytes (default: 5000) |
| `-maxsendbuffer=<n>` | Maximum per-connection send buffer, &lt;n&gt;\*1000 bytes (default: 1000) |
| `-maxtimeadjustment` | Maximum allowed median peer time offset adjustment. Local perspective of time may be influenced by peers forward or backward by this amount. (default: 4200 seconds) |
| `-onion=<ip:port>` | Use separate SOCKS5 proxy to reach peers via Tor hidden services (default: -proxy) |
| `-onlynet=<net>` | Only connect to nodes in network &lt;net&gt; (ipv4, ipv6 or onion) |
| `-permitbaremultisig` | Relay non-P2SH multisig (default: 1) |
| `-peerbloomfilters` | Support filtering of blocks and transaction with bloom filters (default: 1) |
| `-port=<port>` | Listen for connections on &lt;port&gt; (default: 33441 or testnet: 44551) |
| `-proxy=<ip:port>` | Connect through SOCKS5 proxy |
| `-proxyrandomize` | Randomize credentials for every proxy connection. This enables Tor stream isolation (default: 1) |
| `-seednode=<ip>` | Connect to a node to retrieve peer addresses, and disconnect |
| `-timeout=<n>` | Specify connection timeout in milliseconds (minimum: 1, default: 5000) |
| `-torcontrol=<ip>:<port>` | Tor control port to use if onion listening enabled (default: 127.0.0.1:9051) |
| `-torpassword=<pass>` | Tor control port password (default: empty) |
| `-upnp` | Use UPnP to map the listening port (default: 0) |
| `-whitebind=<addr>` | Bind to given address and whitelist peers connecting to it. Use \[host\]:port notation for IPv6 |
| `-whitelist=<IP address or network>` | Whitelist peers connecting from the given IP address (e.g. 1.2.3.4) or CIDR notated network (e.g. 1.2.3.0/24). Can be specified multiple times. Whitelisted peers cannot be DoS banned and their transactions are always relayed, even if they are already in the mempool, useful e.g. for a gateway |
| `-maxuploadtarget=<n>` | Tries to keep outbound traffic under the given target (in MiB per 24h), 0 = no limit (default: 0) |


## Wallet options

| Option | Description |
|---|---|
| `-disablewallet` | Do not load the wallet and disable wallet RPC calls |
| `-keypool=<n>` | Set key pool size to &lt;n&gt; (default: 1000) |
| `-fallbackfee=<amt>` | A fee rate (in AOK/kB) that will be used when fee estimation has insufficient data (default: 0.01025) |
| `-discardfee=<amt>` | The fee rate (in AOK/kB) that indicates your tolerance for discarding change by adding it to the fee (default: 0.00025). Note: An output is discarded if it is dust at this rate, but we will always discard up to the dust relay fee and a discard fee above that is limited by the fee estimate for the longest target |
| `-mintxfee=<amt>` | Fees (in AOK/kB) smaller than this are considered zero fee for transaction creation (default: 0.01) |
| `-paytxfee=<amt>` | Fee (in AOK/kB) to add to transactions you send (default: 0.00) |
| `-rescan` | Rescan the block chain for missing wallet transactions on startup |
| `-salvagewallet` | Attempt to recover private keys from a corrupt wallet on startup |
| `-spendzeroconfchange` | Spend unconfirmed change when sending transactions (default: 1) |
| `-spendofflinestaking` | Let a payment take coins at an offline staking address on its own. Otherwise they are spent only when they are selected, with coin control or in a raw transaction (default: 0) |
| `-stakecombinethreshold=<amt>` | A stake gathers the coins of its address that are smaller than this amount (in AOK) and is split in two when it reaches twice the amount, so the staking coins end up between one and two times this size (default: 1000.00) |
| `-txconfirmtarget=<n>` | If paytxfee is not set, include enough fee so transactions begin confirmation on average within n blocks (default: 6) |
| `-walletrbf` | Send transactions with full-RBF opt-in enabled (default: 0) |
| `-upgradewallet` | Upgrade wallet to latest format on startup |
| `-wallet=<path>` | Specify wallet database path. Can be specified multiple times to load multiple wallets. Path is interpreted relative to &lt;walletdir&gt; if it is not absolute, and will be created if it does not exist (as a directory containing a wallet.dat file and log files). For backwards compatibility this will also accept names of existing data files in &lt;walletdir&gt;.) |
| `-walletbroadcast` | Make the wallet broadcast transactions (default: 1) |
| `-walletdir=<dir>` | Specify directory to hold wallets (default: &lt;datadir&gt;/wallets if it exists, otherwise &lt;datadir&gt;) |
| `-walletnotify=<cmd>` | Execute command when a wallet transaction changes (%s in cmd is replaced by TxID) |
| `-zapwallettxes=<mode>` | Delete all wallet transactions and only recover those parts of the blockchain through -rescan on startup (1 = keep tx meta data e.g. account owner and payment request information, 2 = drop tx meta data) |


## ZeroMQ notification options

| Option | Description |
|---|---|
| `-zmqpubhashblock=<address>` | Enable publish hash block in &lt;address&gt; |
| `-zmqpubhashtx=<address>` | Enable publish hash transaction in &lt;address&gt; |
| `-zmqpubrawblock=<address>` | Enable publish raw block in &lt;address&gt; |
| `-zmqpubrawtx=<address>` | Enable publish raw transaction in &lt;address&gt; |


## Debugging/Testing options

| Option | Description |
|---|---|
| `-uacomment=<cmt>` | Append comment to the user agent string |
| `-debug=<category>` | Output debugging information (default: 0, supplying &lt;category&gt; is optional). If &lt;category&gt; is not supplied or if &lt;category&gt; = 1, output all debugging information. &lt;category&gt; can be: net, tor, mempool, http, bench, zmq, db, rpc, estimatefee, addrman, selectcoins, reindex, cmpctblock, rand, prune, proxy, mempoolrej, libevent, coindb, qt, leveldb, coinstake. |
| `-debugexclude=<category>` | Exclude debugging information for a category. Can be used in conjunction with -debug=1 to output debug logs for all categories except one or more specified categories. |
| `-help-debug` | Show all debugging options (usage: --help -help-debug) |
| `-logips` | Include IP addresses in debug output (default: 0) |
| `-logtimestamps` | Prepend debug output with timestamp (default: 1) |
| `-logratelimit` | Suppress a source location that logs more than 1 MiB within an hour, for the rest of that hour (default: 1) |
| `-maxtxfee=<amt>` | Maximum total fees (in AOK) to use in a single wallet transaction or raw transaction; setting this too low may abort large transactions (default: 10.00) |
| `-printtoconsole` | Send trace/debug info to console instead of debug.log file |
| `-shrinkdebugfile` | Shrink debug.log file on client startup (default: 1 when no -debug) |


## Chain selection options

| Option | Description |
|---|---|
| `-testnet` | Use the test chain |


## Node relay options

| Option | Description |
|---|---|
| `-bytespersigop` | Equivalent bytes per sigop in transactions for relay and mining (default: 20) |
| `-datacarrier` | Relay and mine data carrier transactions (default: 1) |
| `-datacarriersize` | Maximum size of data in data carrier transactions we relay and mine (default: 83) |
| `-mempoolreplacement` | Enable transaction replacement in the memory pool (default: 0) |
| `-minrelaytxfee=<amt>` | Fees (in AOK/kB) smaller than this are considered zero fee for relaying, mining and transaction creation (default: 0.0001) |
| `-whitelistrelay` | Accept relayed transactions received from whitelisted peers even when not relaying transactions (default: 1) |
| `-whitelistforcerelay` | Force relay of transactions from whitelisted peers even if they violate local relay policy (default: 1) |


## Block creation options

| Option | Description |
|---|---|
| `-blockmaxweight=<n>` | Set maximum BIP141 block weight (default: 7996000) |
| `-blockmaxsize=<n>` | Set maximum BIP141 block weight to this \* 4. Deprecated, use blockmaxweight |
| `-blockmintxfee=<amt>` | Set lowest fee rate (in AOK/kB) for transactions to be included in block creation. (default: 0.00001) |


## RPC server options

| Option | Description |
|---|---|
| `-server` | Accept command line and JSON-RPC commands |
| `-rest` | Accept public REST requests (default: 0) |
| `-rpcbind=<addr>[:port]` | Bind to given address to listen for JSON-RPC connections. This option is ignored unless -rpcallowip is also passed. Port is optional and overrides -rpcport. Use \[host\]:port notation for IPv6. This option can be specified multiple times (default: 127.0.0.1 and ::1 i.e., localhost, or if -rpcallowip has been specified, 0.0.0.0 and :: i.e., all addresses) |
| `-rpccookiefile=<loc>` | Location of the auth cookie (default: data dir) |
| `-rpcuser=<user>` | Username for JSON-RPC connections |
| `-rpcpassword=<pw>` | Password for JSON-RPC connections |
| `-rpcauth=<userpw>` | Username and hashed password for JSON-RPC connections. The field &lt;userpw&gt; comes in the format: &lt;USERNAME&gt;:&lt;SALT&gt;$&lt;HASH&gt;. A canonical python script is included in share/rpcuser. The client then connects normally using the rpcuser=&lt;USERNAME&gt;/rpcpassword=&lt;PASSWORD&gt; pair of arguments. This option can be specified multiple times |
| `-rpcwhitelist=<whitelist>` | Set a whitelist to filter incoming RPC calls for a specific user. The field &lt;whitelist&gt; comes in the format: &lt;USERNAME&gt;:&lt;rpc 1&gt;,&lt;rpc 2&gt;,...,&lt;rpc n&gt;. Several whitelists for one user are added together. |
| `-rpcwhitelistdefault` | Sets default behavior for rpc whitelisting. Unless rpcwhitelistdefault is set to 0, if any -rpcwhitelist is set, the rpc server acts as if all rpc users are subject to empty-unless-otherwise-specified whitelists. If rpcwhitelistdefault is set to 1 and no -rpcwhitelist is set, rpc server acts as if all rpc users are subject to empty whitelists. |
| `-rpcport=<port>` | Listen for JSON-RPC connections on &lt;port&gt; (default: 33440 or testnet: 44550) |
| `-rpcallowip=<ip>` | Allow JSON-RPC connections from specified source. Valid for &lt;ip&gt; are a single IP (e.g. 1.2.3.4), a network/netmask (e.g. 1.2.3.4/255.255.255.0) or a network/CIDR (e.g. 1.2.3.4/24). This option can be specified multiple times |
| `-rpcserialversion` | Sets the serialization of raw transaction or block hex returned in non-verbose mode, non-segwit(0) or segwit(1) (default: 1) |
| `-rpcthreads=<n>` | Set the number of threads to service RPC calls (default: 4) |


## GUI options

Only `aokchain-qt` reads these.

| Option | Description |
|---|---|
| `-choosedatadir` | Choose data directory on startup (default: 0) |
| `-lang=<lang>` | Set language, for example "de\_DE" (default: system locale) |
| `-min` | Start minimized |
| `-rootcertificates=<file>` | Set SSL root certificates for payment request (default: -system-) |
| `-splash` | Show splash screen on startup (default: 1) |
| `-resetguisettings` | Reset all settings changed in the GUI |


## Options not listed by -help

The programs read these options although `-help` does not show them.

| Option | Description |
|---|---|
| `-staking` | Search for stakes with the wallets that are loaded, from the start (default: 0). The GUI wallet starts with the staking switch in this position. `getstakinginfo` reports it as `enabled`. |
| `-tokenindex` | Maintain the token address index, used by listaddressesbytoken, listtokenbalancesbyaddress and listuniquetokenholders (default: 1). Changing it needs a rebuild with -reindex. |

## Debugging options

`aokchaind -help -help-debug` adds these options for testing and debugging. Several of them only work on regtest. They are grouped as the help groups them.

### General options (debugging)

| Option | Description |
|---|---|
| `-blocksonly` | Whether to operate in a blocks only mode (default: 0) |
| `-dbbatchsize` | Maximum database write batch size in bytes (default: 16777216) |
| `-feefilter` | Tell other nodes to filter invs to us by our mempool min fee (default: 1) |
| `-minimumchainwork=<hex>` | Minimum work assumed to exist on a valid chain in hex (default: 00000000000000000000000000000000000000000000044f3a55ad8aa699012a, testnet: 0000000000000000000000000000000000000000000000000000000000000000) |


### Wallet debugging/testing options

| Option | Description |
|---|---|
| `-checkwalletlive` | Verify the wallet's index of unspent transactions against a full scan on every use; slow, for tests (default: 0) |
| `-dblogsize=<n>` | Flush wallet database activity from memory to disk log every &lt;n&gt; megabytes (default: 100) |
| `-flushwallet` | Run a thread to flush wallet periodically (default: 1) |
| `-privdb` | Sets the DB\_PRIVATE flag in the wallet db environment (default: 1) |
| `-walletrejectlongchains` | Wallet will not create transactions that violate mempool chain limits (default: 0) |


### Debugging/Testing options (debugging)

| Option | Description |
|---|---|
| `-checkblocks=<n>` | How many blocks to check at startup (default: 30, 0 = all) |
| `-checklevel=<n>` | How thorough the block verification of -checkblocks is (0-4, default: 4) |
| `-checkblockindex` | Do a full consistency check for mapBlockIndex, setBlockIndexCandidates, chainActive and mapBlocksUnlinked occasionally. Also sets -checkmempool (default: 0) |
| `-checkstaketime` | Read the staked transaction of every proof-of-stake block from disk and compare its time with the time that the coin records (default: 0) |
| `-checkmempool=<n>` | Run checks every &lt;n&gt; transactions (default: 0) |
| `-checkpoints` | Disable expensive verification for known chain history (default: 1) |
| `-disablesafemode` | Disable safemode, override a real safe mode event (default: 1) |
| `-deprecatedrpc=<method>` | Allows deprecated RPC method(s) to be used |
| `-testsafemode` | Force safe mode (default: 0) |
| `-dropmessagestest=<n>` | Randomly drop 1 of every &lt;n&gt; network messages |
| `-fuzzmessagestest=<n>` | Randomly fuzz 1 of every &lt;n&gt; network messages |
| `-stopafterblockimport` | Stop running after importing blocks from disk (default: 0) |
| `-stopatheight` | Stop running after reaching the given height in the main chain (default: 0) |
| `-limitancestorcount=<n>` | Do not accept transactions if number of in-mempool ancestors is &lt;n&gt; or more (default: 200) |
| `-limitancestorsize=<n>` | Do not accept transactions whose size with all in-mempool ancestors exceeds &lt;n&gt; kilobytes (default: 202) |
| `-limitdescendantcount=<n>` | Do not accept transactions if any ancestor would have &lt;n&gt; or more in-mempool descendants (default: 200) |
| `-limitdescendantsize=<n>` | Do not accept transactions if any ancestor would have more than &lt;n&gt; kilobytes of in-mempool descendants (default: 202). |
| `-lastpowblock=<height>` | Height of the last proof-of-work block; later blocks must be proof-of-stake (regtest-only) |
| `-maxblocksperstake=<n>` | Blocks with the same stake (coin and time) that are stored; further ones are stored only when a block builds on them (default: 4) |
| `-masteraddress=<address>` | Governance master address, to test governance commands with a key of the test (regtest-only) |
| `-futuredriftheight=<height>` | Height from which a proof-of-stake block may be at most 60 seconds ahead of the clock (regtest-only) |
| `-restorecointime` | Give the coins of a disconnected block their transaction time back; 0 loses it as versions before 4.0 did (regtest-only, default: 1) |
| `-snapshotparams=<height:block:utxo:tokens:governance:index[:archive]>` | The chain state snapshot that is accepted, as getstatehashes prints it, and optionally the SHA-256 of its files (regtest-only) |
| `-oldpeercutoffheight=<height>` | Chain height from which peers below the current protocol version are disconnected (regtest-only) |
| `-vbparams=deployment:start:end` | Use given start/end times for specified version bits deployment (regtest-only) |
| `-logtimemicros` | Add microsecond precision to debug timestamps (default: 0) |
| `-mocktime=<n>` | Replace actual time with &lt;n&gt; seconds since epoch (default: 0) |
| `-maxsigcachesize=<n>` | Limit sum of signature cache and script execution cache sizes to &lt;n&gt; MiB (default: 32) |
| `-maxtipage=<n>` | Maximum tip age in seconds to consider node in initial block download (default: 86400) |
| `-printpriority` | Log transaction fee per kB when mining blocks (default: 0) |


### Chain selection options (debugging)

| Option | Description |
|---|---|
| `-regtest` | Enter regression test mode, which uses a special chain in which blocks can be solved instantly. This is intended for regression testing tools and app development. |


### Node relay options (debugging)

| Option | Description |
|---|---|
| `-acceptnonstdtxn` | Relay and mine "non-standard" transactions (testnet/regtest only; default: 0) |
| `-incrementalrelayfee=<amt>` | Fee rate (in AOK/kB) used to define cost of relay, used for mempool limiting and BIP 125 replacement. (default: 0.00001) |
| `-dustrelayfee=<amt>` | Fee rate (in AOK/kB) used to defined dust, the value of an output such that it will cost more than its value in fees at this fee rate to spend it. (default: 0.00003) |


### Block creation options (debugging)

| Option | Description |
|---|---|
| `-blockversion=<n>` | Override block version to test forking scenarios |


### RPC server options (debugging)

| Option | Description |
|---|---|
| `-rpcworkqueue=<n>` | Set the depth of the work queue to service RPC calls (default: 16) |
| `-rpcservertimeout=<n>` | Timeout during HTTP requests (default: 30) |


### GUI options (debugging)

| Option | Description |
|---|---|
| `-allowselfsignedrootcertificates` | Allow self signed root certificates (default: 0) |
| `-uiplatform` | Select platform to customize UI for (one of windows, macosx, other; default: other) |


## aokchain-cli options

`aokchain-cli` sends one command to a running node (see [[json-rpc]]). It reads the RPC settings (`rpcuser`, `rpcpassword`, `rpcport`, `rpcconnect`) from the same `aokchain.conf`, or uses the cookie file of the data directory. These are its options, as `aokchain-cli -help` prints them.

| Option | Description |
|---|---|
| `-?` | This help message |
| `-conf=<file>` | Specify configuration file (default: aokchain.conf) |
| `-datadir=<dir>` | Specify data directory |
| `-getinfo` | Get general information from the remote server. Note that unlike server-side RPC calls, the results of -getinfo is the result of multiple non-atomic requests. Some entries in the result may represent results from different states (e.g. wallet balance may be as of a different block from the chain state reported) |
| `-testnet` | Use the test chain |
| `-regtest` | Enter regression test mode, which uses a special chain in which blocks can be solved instantly. This is intended for regression testing tools and app development. |
| `-named` | Pass named instead of positional arguments (default: false) |
| `-rpcconnect=<ip>` | Send commands to node running on &lt;ip&gt; (default: 127.0.0.1) |
| `-rpcport=<port>` | Connect to JSON-RPC on &lt;port&gt; (default: 33440 or testnet: 44550) |
| `-rpcwait` | Wait for RPC server to start |
| `-rpcuser=<user>` | Username for JSON-RPC connections |
| `-rpcpassword=<pw>` | Password for JSON-RPC connections |
| `-rpcclienttimeout=<n>` | Timeout in seconds during HTTP requests, or 0 for no timeout. (default: 900) |
| `-stdinrpcpass` | Read RPC password from standard input as a single line.  When combined with -stdin, the first line from standard input is used for the RPC password. |
| `-stdin` | Read extra arguments from standard input, one per line until EOF/Ctrl-D (recommended for sensitive information such as passphrases). When combined with -stdinrpcpass, the first line from standard input is used for the RPC password. |
| `-rpcwallet=<walletname>` | Send RPC for non-default wallet on RPC server (needs to exactly match corresponding -wallet option passed to aokchaind) |


## aokchain-tx

`aokchain-tx` creates and changes raw transactions without a node (see [[raw-transactions]]). This is its help. It also takes `time=<unix time>`, which sets the time of the transaction and is not listed.

```text
Usage:
  aokchain-tx [options] <hex-tx> [commands]  Update hex-encoded aokchain transaction
  aokchain-tx [options] -create [commands]   Create hex-encoded aokchain transaction

Options:

  -?
       This help message

  -create
       Create new, empty TX.

  -json
       Select JSON output

  -txid
       Output only the hex-encoded transaction id of the resultant transaction.

Chain selection options:

  -testnet
       Use the test chain

  -regtest
       Enter regression test mode, which uses a special chain in which blocks
       can be solved instantly. This is intended for regression testing
       tools and app development.

Commands:

  delin=N
       Delete input N from TX

  delout=N
       Delete output N from TX

  in=TXID:VOUT(:SEQUENCE_NUMBER)
       Add input to TX

  locktime=N
       Set TX lock time to N

  nversion=N
       Set TX version to N

  replaceable(=N)
       Set RBF opt-in sequence number for input N (if not provided, opt-in all
       available inputs)

  outaddr=VALUE:ADDRESS
       Add address-based output to TX

  outpubkey=VALUE:PUBKEY[:FLAGS]
       Add pay-to-pubkey output to TX. Optionally add the "W" flag to produce a
       pay-to-witness-pubkey-hash output. Optionally add the "S" flag to
       wrap the output in a pay-to-script-hash.

  outdata=[VALUE:]DATA
       Add data-based output to TX

  outscript=VALUE:SCRIPT[:FLAGS]
       Add raw script output to TX. Optionally add the "W" flag to produce a
       pay-to-witness-script-hash output. Optionally add the "S" flag to
       wrap the output in a pay-to-script-hash.

  outmultisig=VALUE:REQUIRED:PUBKEYS:PUBKEY1:PUBKEY2:....[:FLAGS]
       Add Pay To n-of-m Multi-sig output to TX. n = REQUIRED, m = PUBKEYS.
       Optionally add the "W" flag to produce a
       pay-to-witness-script-hash output. Optionally add the "S" flag to
       wrap the output in a pay-to-script-hash.

  sign=SIGHASH-FLAGS
       Add zero or more signatures to transaction. This command requires JSON
       registers:prevtxs=JSON object, privatekeys=JSON object. See
       signrawtransaction docs for format of sighash flags, JSON
       objects.

Register Commands:

  load=NAME:FILENAME
       Load JSON file FILENAME into register NAME

  set=NAME:JSON-STRING
       Set register NAME to given JSON-STRING
```

## aokchain-wallet

`aokchain-wallet` works on a wallet file while no node uses it. This is its help.

```text
Looks into a wallet file, creates one or salvages one. No node is needed, and the node that
uses the wallet must not be running.

Usage:
  aokchain-wallet -wallet=<wallet> [options] <command>

Commands:
  info        Show what the wallet file contains: format, encryption, HD seed, number of keys,
              transactions and address book entries
  addresses   List the addresses of the address book with their labels (-allkeys: every key of
              the wallet, with the key pool and the change keys). The balance of an address is
              not in the wallet file: ask a node with scantxoutset
  create      Create a new wallet with an HD seed and a key pool (not encrypted). <wallet> becomes
              a folder with the file wallet.dat in it; give that folder to the node as -wallet
  salvage     Try to recover the private keys of a damaged wallet file; the file is kept as
              <name>.<time>.bak

Options:
  -wallet=<wallet>    A wallet file (a path), or the name of a wallet in the wallet directory
  -datadir=<dir>      The data directory whose wallet directory is used for a name
  -walletdir=<dir>    The wallet directory for a name
  -allkeys            addresses: list every key
  -testnet, -regtest  The network of the wallet (for the form of the addresses)
```
