---
title: "RPC commands"
description: "Every JSON-RPC command of AokChain Core 4.0, by category, with a link to the help text of each."
order: 10
generated_by: tools/rpc_reference.py
---

Every command that AokChain Core 4.0.7 answers over JSON-RPC and `aokchain-cli`, by category. Each name links to the command's help text, the same text that `aokchain-cli help <command>` prints. How to send a call is on [[json-rpc]].

## Categories

- [[rpc-addressindex|Address index]] (7): Balances, transactions and unspent outputs of addresses, read from the address index.
- [[rpc-blockchain|Blockchain]] (36): Blocks, the chain state, the mempool, governance, the snapshot and the block archives.
- [[rpc-control|Control]] (5): Memory, running commands, uptime, help and stopping the node.
- [[rpc-generating|Generating]] (3): Making proof-of-work blocks on regtest, and the generate setting.
- [[rpc-mining|Mining]] (7): Block templates, mining and staking information, and block submission.
- [[rpc-network|Network]] (13): Peers, connections, bans and network traffic.
- [[rpc-rawtransactions|Raw transactions]] (11): Creating, signing, checking and sending transactions by hand.
- [[rpc-tokens|Tokens]] (17): Issuing, reissuing, transferring and looking up tokens and usernames.
- [[rpc-util|Utilities]] (8): Multisig addresses, fee estimates, message signatures, address checks and recovery words.
- [[rpc-wallet|Wallet]] (63): Keys, addresses, balances, payments, backups, encryption and the wallet files.
- [[rpc-hidden|Not listed by help]] (11): Commands for testing and debugging that help does not list.

`aokchain-cli help` lists 170 commands. The commands under [[rpc-hidden|Not listed by help]] are for testing and debugging; `aokchain-cli help <command>` still explains each.

> [!NOTE]
> Wallet commands act on the wallet that the node has loaded. With several wallets loaded, name one with `aokchain-cli -rpcwallet=<name>`, or send the call to the path `/wallet/<name>` of the JSON-RPC address.

## Address index

- [[rpc-addressindex#getaddressbalance|getaddressbalance]]: Returns the balance for an address(es) (requires addressindex to be enabled).
- [[rpc-addressindex#getaddressdeltas|getaddressdeltas]]: Returns all changes for an address (requires addressindex to be enabled).
- [[rpc-addressindex#getaddresses|getaddresses]]: Print a list of all addresses in the blockchain.
- [[rpc-addressindex#getaddressmempool|getaddressmempool]]: Returns all mempool deltas for an address (requires addressindex to be enabled).
- [[rpc-addressindex#getaddresstxids|getaddresstxids]]: Returns the txids for an address(es) (requires addressindex to be enabled).
- [[rpc-addressindex#getaddressutxos|getaddressutxos]]: Returns the unspent outputs of addresses that are not time locked any more (requires addressindex to be enabled), in the order of their block ...
- [[rpc-addressindex#gettokentransactions|gettokentransactions]]: Print a list of all token transactions.

## Blockchain

- [[rpc-blockchain#checkfreeze|checkfreeze]]: Returns freze status for address.
- [[rpc-blockchain#fetchblocks|fetchblocks]]: Download the past blocks of a node that started from a chain state snapshot, in the background.
- [[rpc-blockchain#freezelist|freezelist]]: Returns list of frozen addresses.
- [[rpc-blockchain#getbestblockhash|getbestblockhash]]: Returns the hash of the best (tip) block in the longest blockchain.
- [[rpc-blockchain#getblock|getblock]]: If verbosity is 0, returns a string that is serialized, hex-encoded data for block 'hash'.
- [[rpc-blockchain#getblockchaininfo|getblockchaininfo]]: Returns an object containing various state info regarding blockchain processing.
- [[rpc-blockchain#getblockcount|getblockcount]]: Returns the number of blocks in the longest blockchain.
- [[rpc-blockchain#getblockhash|getblockhash]]: Returns hash of block in best-block-chain at height provided.
- [[rpc-blockchain#getblockhashes|getblockhashes]]: Returns array of hashes of blocks within the timestamp range provided.
- [[rpc-blockchain#getblockheader|getblockheader]]: If verbose is false, returns a string that is serialized, hex-encoded data for blockheader 'hash'.
- [[rpc-blockchain#getblockstats|getblockstats]]: Computes statistics of one block of the active chain.
- [[rpc-blockchain#getbootstrapinfo|getbootstrapinfo]]: State of the block bootstrap (-bootstrapurl): block archives that are fetched over HTTP and imported.
- [[rpc-blockchain#getchaintips|getchaintips]]: Return information about all known tips in the block tree, including the main chain as well as orphaned branches.
- [[rpc-blockchain#getchaintxstats|getchaintxstats]]: Compute statistics about the total number and rate of transactions in the chain.
- [[rpc-blockchain#getdifficulty|getdifficulty]]: Returns the proof-of-work difficulty as a multiple of the minimum difficulty.
- [[rpc-blockchain#getindexinfo|getindexinfo]]: Returns the indexes that this node keeps.
- [[rpc-blockchain#getmempoolancestors|getmempoolancestors]]: If txid is in the mempool, returns all in-mempool ancestors.
- [[rpc-blockchain#getmempooldescendants|getmempooldescendants]]: If txid is in the mempool, returns all in-mempool descendants.
- [[rpc-blockchain#getmempoolentry|getmempoolentry]]: Returns mempool data for given transaction
- [[rpc-blockchain#getmempoolinfo|getmempoolinfo]]: Returns details on the active state of the TX memory pool.
- [[rpc-blockchain#getrawmempool|getrawmempool]]: Returns all transaction ids in memory pool as a json array of string transaction ids.
- [[rpc-blockchain#getsnapshotinfo|getsnapshotinfo]]: The chain state snapshot that this program accepts, whether this node started from one, and the state of the past blocks (the blocks up to the ...
- [[rpc-blockchain#getspentinfo|getspentinfo]]: Returns the txid and index where an output is spent.
- [[rpc-blockchain#getstatehashes|getstatehashes]]: Compute the hashes that identify the chain state of this node at its tip: the values that a program must have compiled in to accept a chain state ...
- [[rpc-blockchain#gettxout|gettxout]]: Returns details about an unspent transaction output.
- [[rpc-blockchain#gettxoutproof|gettxoutproof]]: Returns a hex-encoded proof that "txid" was included in a block.
- [[rpc-blockchain#gettxoutsetinfo|gettxoutsetinfo]]: Returns statistics about the unspent transaction output set.
- [[rpc-blockchain#issuanceinfo|issuanceinfo]]: Returns issuance cost for tokens.
- [[rpc-blockchain#preciousblock|preciousblock]]: Treats a block as if it were received before others with the same work.
- [[rpc-blockchain#pruneblockchain|pruneblockchain]]
- [[rpc-blockchain#repaircoins|repaircoins]]: Look for unspent outputs that have no transaction time in the chain state of this node, and give them the time and the coinstake mark of their ...
- [[rpc-blockchain#savemempool|savemempool]]: Dumps the mempool to disk.
- [[rpc-blockchain#scantxoutset|scantxoutset]]: Scans the unspent transaction outputs of the chain for outputs that pay to the given addresses or scripts.
- [[rpc-blockchain#skipbootstrap|skipbootstrap]]: Give the block bootstrap up and get the blocks from the peers.
- [[rpc-blockchain#verifychain|verifychain]]: Verifies blockchain database.
- [[rpc-blockchain#verifytxoutproof|verifytxoutproof]]: Verifies that a proof points to a transaction in a block, returning the transaction it commits to and throwing an RPC error if the block is not in ...

## Control

- [[rpc-control#getmemoryinfo|getmemoryinfo]]: Returns an object containing information about memory usage.
- [[rpc-control#getrpcinfo|getrpcinfo]]: Returns details of the RPC server.
- [[rpc-control#help|help]]: List all commands, or get help for a specified command.
- [[rpc-control#stop|stop]]: Stop AokChain server.
- [[rpc-control#uptime|uptime]]: Returns the total uptime of the server.

## Generating

- [[rpc-generating#generate|generate]]: Mine up to nblocks blocks immediately (before the RPC call returns) to an address in the wallet.
- [[rpc-generating#generatetoaddress|generatetoaddress]]: Mine blocks immediately to a specified address (before the RPC call returns)
- [[rpc-generating#getgenerate|getgenerate]]: Return if the server is set to generate coins or not.

## Mining

- [[rpc-mining#getblocktemplate|getblocktemplate]]: If the request parameters include a 'mode' key, that is used to explicitly select between the default 'template' request or a 'proposal'.
- [[rpc-mining#getmininginfo|getmininginfo]]: Returns a json object containing mining-related information.
- [[rpc-mining#getnetworkhashps|getnetworkhashps]]: Returns the estimated network hashes per second based on the last n blocks.
- [[rpc-mining#getstakinginfo|getstakinginfo]]: Returns an object containing staking-related information.
- [[rpc-mining#prioritisetransaction|prioritisetransaction]]: Accepts the transaction into mined blocks at a higher (or lower) priority
- [[rpc-mining#setgenerate|setgenerate]]: Set 'generate' true or false to turn generation on or off.
- [[rpc-mining#submitblock|submitblock]]: Attempts to submit new block to network.

## Network

- [[rpc-network#addnode|addnode]]: Attempts to add or remove a node from the addnode list.
- [[rpc-network#clearbanned|clearbanned]]: Clear all banned IPs.
- [[rpc-network#disconnectnode|disconnectnode]]: Immediately disconnects from the specified peer node.
- [[rpc-network#getaddednodeinfo|getaddednodeinfo]]: Returns information about the given added node, or all added nodes (note that onetry addnodes are not listed here)
- [[rpc-network#getconnectioncount|getconnectioncount]]: Returns the number of connections to other nodes.
- [[rpc-network#getnettotals|getnettotals]]: Returns information about network traffic, including bytes in, bytes out, and current time.
- [[rpc-network#getnetworkinfo|getnetworkinfo]]: Returns an object containing various state info regarding P2P networking.
- [[rpc-network#getnodeaddresses|getnodeaddresses]]: Returns known addresses of nodes, which can be used to find new nodes in the network.
- [[rpc-network#getpeerinfo|getpeerinfo]]: Returns data about each connected network node as a json array of objects.
- [[rpc-network#listbanned|listbanned]]: List all banned IPs/Subnets.
- [[rpc-network#ping|ping]]: Requests that a ping be sent to all other nodes, to measure ping time.
- [[rpc-network#setban|setban]]: Attempts to add or remove an IP/Subnet from the banned list.
- [[rpc-network#setnetworkactive|setnetworkactive]]: Disable/enable all p2p network activity.

## Raw transactions

- [[rpc-rawtransactions#combinerawtransaction|combinerawtransaction]]: Combine multiple partially signed transactions into one transaction.
- [[rpc-rawtransactions#createrawtransaction|createrawtransaction]]: Create a transaction spending the given inputs and creating new outputs.
- [[rpc-rawtransactions#decoderawtransaction|decoderawtransaction]]: Return a JSON object representing the serialized, hex-encoded transaction.
- [[rpc-rawtransactions#decodescript|decodescript]]: Decode a hex-encoded script.
- [[rpc-rawtransactions#fundrawtransaction|fundrawtransaction]]: Add inputs to a transaction until it has enough in value to meet its out value.
- [[rpc-rawtransactions#getrawtransaction|getrawtransaction]]: NOTE: By default this function only works for mempool transactions.
- [[rpc-rawtransactions#sendrawtransaction|sendrawtransaction]]: Submits raw transaction (serialized, hex-encoded) to local node and network.
- [[rpc-rawtransactions#signrawtransaction|signrawtransaction]]: Sign inputs for raw transaction (serialized, hex-encoded).
- [[rpc-rawtransactions#signrawtransactionwithkey|signrawtransactionwithkey]]: Signs the inputs of a raw transaction (serialized, hex-encoded) with the given private keys only; no wallet is used.
- [[rpc-rawtransactions#signrawtransactionwithwallet|signrawtransactionwithwallet]]: Signs the inputs of a raw transaction (serialized, hex-encoded) with the keys of the wallet.
- [[rpc-rawtransactions#testmempoolaccept|testmempoolaccept]]: Returns whether a raw transaction (serialized, hex-encoded) would be accepted by the mempool.

## Tokens

- [[rpc-tokens#getcacheinfo|getcacheinfo]]
- [[rpc-tokens#gettokendata|gettokendata]]: Returns tokens metadata if that token exists
- [[rpc-tokens#getusernameaddress|getusernameaddress]]
- [[rpc-tokens#issue|issue]]: Issue an token, subtoken or unique token.
- [[rpc-tokens#issueunique|issueunique]]: Issue unique token(s).
- [[rpc-tokens#listaddressesbytoken|listaddressesbytoken]]: Returns a list of all address that own the given token (with balances)
- [[rpc-tokens#listmylockedtokens|listmylockedtokens]]: Returns a list of all locked token that are owned by this wallet
- [[rpc-tokens#listmytokens|listmytokens]]: Returns a list of all token that are owned by this wallet
- [[rpc-tokens#listtokenbalancesbyaddress|listtokenbalancesbyaddress]]: Returns a list of all token balances for an address.
- [[rpc-tokens#listtokens|listtokens]]: Returns a list of all tokens
- [[rpc-tokens#listuniquetokenholders|listuniquetokenholders]]: Returns a list holders of unique
- [[rpc-tokens#registerusername|registerusername]]
- [[rpc-tokens#reissue|reissue]]: Reissues a quantity of an token to an owned address if you own the Owner Token
- [[rpc-tokens#transfer|transfer]]: Transfers a quantity of an owned token to a given address
- [[rpc-tokens#transferfromaddress|transferfromaddress]]: Transfer a quantity of an owned token in a specific address to a given address
- [[rpc-tokens#transfermany|transfermany]]: Send multiple times.
- [[rpc-tokens#transfermanyoutputs|transfermanyoutputs]]: Send transaction with multiple outputs.

## Utilities

- [[rpc-util#createmultisig|createmultisig]]: Creates a multi-signature address with n signature of m keys required.
- [[rpc-util#estimatefee|estimatefee]]: DEPRECATED. Please use estimatesmartfee for more intelligent estimates.
- [[rpc-util#estimatesmartfee|estimatesmartfee]]: Estimates the approximate fee per kilobyte needed for a transaction to begin confirmation within conf\_target blocks if possible and return the ...
- [[rpc-util#mnemonicfindaddress|mnemonicfindaddress]]: Find the key of an address among the keys a BIP39 mnemonic (recovery words) can produce.
- [[rpc-util#mnemonictokeys|mnemonictokeys]]: Derive private keys and addresses from a BIP39 mnemonic (recovery words) of another wallet.
- [[rpc-util#signmessagewithprivkey|signmessagewithprivkey]]: Sign a message with the private key of an address
- [[rpc-util#validateaddress|validateaddress]]: Return information about the given aokchain address.
- [[rpc-util#verifymessage|verifymessage]]: Verify a signed message

## Wallet

- [[rpc-wallet#abandontransaction|abandontransaction]]: Mark in-wallet transaction &lt;txid&gt; as abandoned
- [[rpc-wallet#abortrescan|abortrescan]]: Stops current wallet rescan triggered e.g. by an importprivkey call.
- [[rpc-wallet#addmultisigaddress|addmultisigaddress]]: Add a nrequired-to-sign multisignature address to the wallet.
- [[rpc-wallet#addwitnessaddress|addwitnessaddress]]: Add a witness address for a script (with pubkey or redeemscript known).
- [[rpc-wallet#backupwallet|backupwallet]]: Safely copies current wallet file to destination, which can be a directory or a path with filename.
- [[rpc-wallet#bumpfee|bumpfee]]: bumpfee has been deprecated on the AOK Wallet.
- [[rpc-wallet#createwallet|createwallet]]: Creates and loads a new wallet.
- [[rpc-wallet#dumpprivkey|dumpprivkey]]: Reveals the private key corresponding to 'address'.
- [[rpc-wallet#dumpwallet|dumpwallet]]: Dumps all wallet keys in a human-readable format to a server-side file.
- [[rpc-wallet#encryptwallet|encryptwallet]]: Encrypts the wallet with 'passphrase'.
- [[rpc-wallet#getaccount|getaccount]]: DEPRECATED. Returns the account associated with the given address.
- [[rpc-wallet#getaccountaddress|getaccountaddress]]: DEPRECATED. Returns the current Bitcoin address for receiving payments to this account.
- [[rpc-wallet#getaddressesbyaccount|getaddressesbyaccount]]: DEPRECATED. Returns the list of addresses for the given account.
- [[rpc-wallet#getaddressesbylabel|getaddressesbylabel]]: Returns the list of addresses assigned the specified label.
- [[rpc-wallet#getaddressinfo|getaddressinfo]]: Returns what the wallet knows about an address.
- [[rpc-wallet#getbalance|getbalance]]: If account is not specified, returns the server's total available balance.
- [[rpc-wallet#getbalances|getbalances]]: Returns all balances of the wallet in AOK.
- [[rpc-wallet#getnewaddress|getnewaddress]]: Returns a new AokChain address for receiving payments.
- [[rpc-wallet#getofflinestakingaddress|getofflinestakingaddress]]: Returns a offline staking address based on two address inputs
- [[rpc-wallet#getrawchangeaddress|getrawchangeaddress]]: Returns a new AokChain address, for receiving change.
- [[rpc-wallet#getreceivedbyaddress|getreceivedbyaddress]]: Returns the total amount received by the given address in transactions with at least minconf confirmations.
- [[rpc-wallet#getreceivedbylabel|getreceivedbylabel]]: Returns the total amount received by addresses with &lt;label&gt; in transactions with at least \[minconf\] confirmations.
- [[rpc-wallet#gettransaction|gettransaction]]: Get detailed information about in-wallet transaction &lt;txid&gt;
- [[rpc-wallet#getunconfirmedbalance|getunconfirmedbalance]]: Returns the server's total unconfirmed balance
- [[rpc-wallet#getwalletinfo|getwalletinfo]]: Returns an object containing various wallet state info.
- [[rpc-wallet#importaddress|importaddress]]: Adds a script (in hex) or address that can be watched as if it were in your wallet but cannot be used to spend.
- [[rpc-wallet#importmnemonic|importmnemonic]]: Adds the keys of another wallet to this wallet, from its BIP39 mnemonic (recovery words).
- [[rpc-wallet#importmulti|importmulti]]: Import addresses/scripts (with private or public keys, redeem script (P2SH)), rescanning all addresses in one-shot-only (rescan can be disabled ...
- [[rpc-wallet#importprivkey|importprivkey]]: Adds a private key (as returned by dumpprivkey) to your wallet.
- [[rpc-wallet#importprunedfunds|importprunedfunds]]: Imports funds without rescan.
- [[rpc-wallet#importpubkey|importpubkey]]: Adds a public key (in hex) that can be watched as if it were in your wallet but cannot be used to spend.
- [[rpc-wallet#importwallet|importwallet]]: Imports keys from a wallet dump file (see dumpwallet).
- [[rpc-wallet#keypoolrefill|keypoolrefill]]: Fills the keypool.
- [[rpc-wallet#listaccounts|listaccounts]]: DEPRECATED. Returns Object that has account names as keys, account balances as values.
- [[rpc-wallet#listaddressgroupings|listaddressgroupings]]: Lists groups of addresses which have had their common ownership made public by common use as inputs or as the resulting change in past transactions
- [[rpc-wallet#listlabels|listlabels]]: Returns the list of all labels, or labels that are assigned to addresses with a specific purpose.
- [[rpc-wallet#listlockunspent|listlockunspent]]: Returns list of temporarily unspendable outputs.
- [[rpc-wallet#listreceivedbyaddress|listreceivedbyaddress]]: List balances by receiving address.
- [[rpc-wallet#listreceivedbylabel|listreceivedbylabel]]: List received transactions by label.
- [[rpc-wallet#listsinceblock|listsinceblock]]: Get all transactions in blocks since block \[blockhash\], or all transactions if omitted.
- [[rpc-wallet#listtransactions|listtransactions]]: Returns up to 'count' most recent transactions skipping the first 'from' transactions for account 'account'.
- [[rpc-wallet#listunspent|listunspent]]: Returns array of unspent transaction outputs with between minconf and maxconf (inclusive) confirmations.
- [[rpc-wallet#listunspenttoken|listunspenttoken]]: Returns array of unspent transaction outputs with between minconf and maxconf (inclusive) confirmations.
- [[rpc-wallet#listwalletdir|listwalletdir]]: Returns a list of wallets in the wallet directory.
- [[rpc-wallet#listwallets|listwallets]]: Returns a list of currently loaded wallets.
- [[rpc-wallet#loadwallet|loadwallet]]: Loads a wallet from a wallet file or directory.
- [[rpc-wallet#lockunspent|lockunspent]]: Updates list of temporarily unspendable outputs.
- [[rpc-wallet#move|move]]: DEPRECATED. Move a specified amount from one account in your wallet to another.
- [[rpc-wallet#purgeorphanstakes|purgeorphanstakes]]: Deletes this wallet's orphaned coinstake transactions from the wallet.
- [[rpc-wallet#removeaddress|removeaddress]]: Stop watching an address that was added with importaddress: the wallet no longer takes it as its own (watch-only).
- [[rpc-wallet#removeprunedfunds|removeprunedfunds]]: Deletes the specified transaction from the wallet.
- [[rpc-wallet#rescanblockchain|rescanblockchain]]: Rescan the local blockchain for wallet related transactions.
- [[rpc-wallet#restorewallet|restorewallet]]: Restores a wallet from a backup file (of backupwallet, or a copy of a wallet.dat) and loads it.
- [[rpc-wallet#sendfrom|sendfrom]]: DEPRECATED (use sendtoaddress).
- [[rpc-wallet#sendmany|sendmany]]: Send multiple times.
- [[rpc-wallet#sendtoaddress|sendtoaddress]]: Send an amount to a given address.
- [[rpc-wallet#setlabel|setlabel]]: Sets the label associated with the given address.
- [[rpc-wallet#settxfee|settxfee]]: Set the transaction fee per kB.
- [[rpc-wallet#signmessage|signmessage]]: Sign a message with the private key of an address
- [[rpc-wallet#unloadwallet|unloadwallet]]: Unloads a wallet that was loaded with loadwallet, createwallet or a second -wallet option.
- [[rpc-wallet#walletlock|walletlock]]: Removes the wallet encryption key from memory, locking the wallet.
- [[rpc-wallet#walletpassphrase|walletpassphrase]]: Stores the wallet decryption key in memory for 'timeout' seconds.
- [[rpc-wallet#walletpassphrasechange|walletpassphrasechange]]: Changes the wallet passphrase from 'oldpassphrase' to 'newpassphrase'.

## Not listed by help

- [[rpc-hidden#echo|echo]]: Simply echo back the input arguments.
- [[rpc-hidden#echojson|echojson]]: Simply echo back the input arguments.
- [[rpc-hidden#estimaterawfee|estimaterawfee]]: WARNING: This interface is unstable and may disappear or change!
- [[rpc-hidden#invalidateblock|invalidateblock]]: Permanently marks a block as invalid, as if it violated a consensus rule.
- [[rpc-hidden#logging|logging]]: Gets and sets the logging configuration.
- [[rpc-hidden#reconsiderblock|reconsiderblock]]: Removes invalidity status of a block and its descendants, reconsider them for activation.
- [[rpc-hidden#resendwallettransactions|resendwallettransactions]]: Immediately re-broadcast unconfirmed wallet transactions to all peers.
- [[rpc-hidden#setmocktime|setmocktime]]: Set the local time to given timestamp (-regtest only)
- [[rpc-hidden#waitforblock|waitforblock]]: Waits for a specific new block and returns useful info about it.
- [[rpc-hidden#waitforblockheight|waitforblockheight]]: Waits for (at least) block height and returns the height and hash of the current tip.
- [[rpc-hidden#waitfornewblock|waitfornewblock]]: Waits for a specific new block and returns useful info about it.
