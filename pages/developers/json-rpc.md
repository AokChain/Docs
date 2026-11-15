---
title: JSON-RPC
description: Call an AokChain node over HTTP: the endpoint, cookie and password authentication, rpcauth users, command whitelists, wallets, errors and curl examples.
order: 20
---

Every function of a node is a JSON-RPC command: the same commands `aokchain-cli` sends and the console of the desktop wallet runs. This page shows how to call them from a program. The list of commands is on [[rpc]].

## The endpoint

| Network | Address |
|---|---|
| Mainnet | `http://127.0.0.1:33440/` |
| Testnet, regtest | `http://127.0.0.1:44550/` |

A request is an HTTP `POST` with a JSON body and HTTP Basic authentication:

```bash
curl --user "$(cat ~/.aokchain/.cookie)" \
  --data-binary '{"jsonrpc":"1.0","id":"1","method":"getblockcount","params":[]}' \
  -H 'content-type: text/plain;' http://127.0.0.1:33440/
```

```json
{"result":3037521,"error":null,"id":"1"}
```

- `method` is the command, `params` its arguments: an array in the order of the help text, or an object with the argument names (named arguments, as `aokchain-cli -named` sends them).
- `id` comes back unchanged.
- An array of requests is a batch; the answer is an array of answers.
- `aokchaind` answers RPC by default; the desktop wallet only with `server=1`.

The same call with `aokchain-cli`:

```bash
aokchain-cli getblockcount
aokchain-cli -named getblockhash height=1
```

## Authentication

### The cookie file

When `rpcpassword` is not set, the node writes a new random password at every start into the file `.cookie` in its data directory (`testnet1/.cookie` on testnet), as `__cookie__:<password>`, and removes it at shutdown. `aokchain-cli` reads it, and any program that runs as the same user can too. This is the simplest setup for a program on the same computer.

### rpcuser and rpcpassword

```ini
rpcuser=app
rpcpassword=<a long random string>
```

One user and password in plain text. With `rpcpassword` set, no cookie file is written, and `aokchain-cli` takes the same two settings from `aokchain.conf`. The password cannot contain `#` (see [[configure-a-node]]).

### rpcauth: users with hashed passwords

`rpcauth` adds a user whose password is stored only as a salted hash, so `aokchain.conf` does not reveal it. Several `rpcauth` lines give several users, and they work together with the cookie file. The script `share/rpcuser/rpcuser.py` of the source makes a line and a password:

```bash
python3 share/rpcuser/rpcuser.py exchange
```

```text
String to be appended to aokchain.conf:
rpcauth=exchange:6e3c9f1c4a5a8f0b1d2e3f405162738a$5b5d...
Your password:
qK8V...
```

The line is `rpcauth=<user>:<salt>$<hash>`, where the hash is the hex HMAC-SHA256 of the password with the salt as key. The same in Python, if you do not have the source at hand:

```bash
python3 -c 'import hmac,hashlib,secrets,sys; u=sys.argv[1]; s=secrets.token_hex(16); p=secrets.token_urlsafe(32); print("rpcauth=%s:%s$%s" % (u, s, hmac.new(s.encode(), p.encode(), hashlib.sha256).hexdigest())); print("password:", p)' exchange
```

The client then authenticates as `exchange` with that password.

### Limit a user to some commands

`rpcwhitelist` lets a user call only the commands listed for it:

```ini
rpcauth=front:<salt>$<hash>
rpcwhitelist=front:getblockcount,getblockhash,getblock,getrawtransaction,testmempoolaccept,sendrawtransaction
rpcwhitelistdefault=0
```

- A call of any other command answers HTTP 403 with an empty body. A batch is refused as a whole if one of its commands is not allowed.
- Several `rpcwhitelist` lines for the same user are added together. A line with a user and no commands lets that user call nothing.
- `rpcwhitelistdefault` decides for users without a line. It is on as soon as one `rpcwhitelist` line exists, and then those users may call nothing, including the cookie user of `aokchain-cli`, which cannot even `stop` the node. Set `rpcwhitelistdefault=0`, as above, to leave the other users unrestricted, or give your administrator user its own line.

## Reaching the node from another computer

By default the RPC server listens on `127.0.0.1` and `::1` only. To serve a program on another computer:

```ini
rpcbind=127.0.0.1
rpcbind=192.0.2.10
rpcallowip=192.0.2.0/24
```

`rpcbind` is ignored unless `rpcallowip` is also given; `rpcallowip` takes single addresses, netmasks and CIDR ranges and can be repeated. The traffic is plain HTTP: keep it on a private network, a VPN or an SSH tunnel, and never open the port to the internet.

## Wallets

With one wallet loaded, wallet commands act on it. With several, name the wallet in the path:

```bash
curl --user "$(cat ~/.aokchain/.cookie)" \
  --data-binary '{"jsonrpc":"1.0","id":"1","method":"getbalance","params":[]}' \
  -H 'content-type: text/plain;' http://127.0.0.1:33440/wallet/exchange
```

`aokchain-cli -rpcwallet=exchange getbalance` does the same. The wallet of the data directory itself has the empty name: `/wallet/` or `-rpcwallet=`. A wallet call without a wallet name answers error `-19` when several are loaded. Wallets made with `createwallet` are not loaded again after a restart unless `aokchain.conf` names them with `wallet=<name>`; with any `wallet=` line, add `wallet=` (empty) as well to keep the default wallet loaded.

## Answers and errors

| HTTP status | Body | When |
|---|---|---|
| 200 | `{"result": ..., "error": null, "id": ...}` | Success. |
| 401 | empty | Wrong user or password. Each failed attempt is delayed by 250 ms. |
| 403 | empty | The command is not in the user's `rpcwhitelist`. |
| 404 | `{"result": null, "error": {"code": -32601, "message": "Method not found"}, ...}` | Unknown command. |
| 500 | `{"result": null, "error": {"code": -8, "message": "Block height out of range"}, ...}` | The command failed; `code` and `message` say why. |

Error codes that programs meet most:

| Code | Meaning |
|---|---|
| -28 | The node is still starting (`Loading block index...`, `Fast start: ...`). Retry. |
| -8 | Invalid parameter. |
| -5 | Invalid address or key, or unknown transaction. |
| -6 | Insufficient funds. |
| -13 | The wallet is locked: `walletpassphrase` first. |
| -14 | Wrong wallet passphrase. |
| -18, -19 | Unknown wallet; wallet not specified while several are loaded. |
| -25, -26 | A transaction was refused; the message has the reason. |
| -27 | The transaction is already in the chain. |
| -32601 | Method not found. |
| -32700 | The request is not valid JSON. |

## Values in the answers

- Amounts of AOK are JSON numbers in AOK with up to 8 decimals (`10.0`, `0.00226`). 1 AOK = 100,000,000 satoshis. The address index calls and `getblockstats` give satoshis. Parse amounts as decimals, not as binary floating point.
- Some yes-or-no fields are printed as `1` and `0` instead of `true` and `false`, for example `isvalid` of `validateaddress`, `complete` of `signrawtransaction`, `allowed` of `testmempoolaccept` and `spendable` of `listunspent`. This is kept for programs written for 3.0.x. Treat `1` and `true` alike.
- Times are Unix seconds.
- Token amounts in token commands are in token units, not AOK.

## Threads and timeouts

The server handles `rpcthreads` calls at once (default 4) and queues up to `rpcworkqueue` more (default 16). A long call such as `scantxoutset`, `gettxoutsetinfo` or a rescan holds a thread meanwhile; `getrpcinfo` lists the calls that are running. `aokchain-cli` waits up to 900 seconds for an answer (`-rpcclienttimeout`).

## Passphrases and the shell

A passphrase on the command line ends up in the shell history. `aokchain-cli -stdin` reads the arguments from standard input, one per line:

```bash
aokchain-cli -stdin walletpassphrase
```

Type the passphrase, then the timeout, then Ctrl+D.
