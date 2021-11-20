# Full node

In order to sync AOK blockchain you must setup full node. This guide describes setup process and some concepts like intraction with your node via command line interface.

## Getting started

AOK software runs on all operating systems: Linux, macOS and Windows. You can get latest binaries from [GitHub](github.com/AokChain/AokChain/releases/latest) or build it on your own using code from [master](https://github.com/AokChain/AokChain/tree/master) branch.

Once you downloaded (or compiled) binaries at your machine, you will have this two binaries:

 - `aokchaind` - headless AOK daemon responsible for syncing blockchain and providing wallet service
 - `aokchain-cli` - command line client which allows interact with AOK node and wallet

## Configuration

You can specify node params in `aokchain.conf` file at `.aokchain` folder (or `C:\Users\Username\AppData\Roaming\AokChain` on Windows).

Example config file looks like this:

```
rpcuser=nodeuser
rpcpassword=supersecurepassword
daemon=1
``` 

## Running node

Running AOK node pretty straightforward, you can use `-printtoconsole` flag to see the output or use `-daemon` to run it in headless daemon mode. This flags can also be specified in config file instead.

```
./aokchaind -daemon
```

## Stopping node

If you launched AOK node in daemon mode, it can be stopped using cli utility like this:

```
aokchain-cli stop
```