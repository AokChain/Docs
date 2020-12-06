# Full node

The purpose of this document is to describe the process of setting up AOK full node and command line wallet.

## Getting started

AOK software runs on all operating systems: Linux, Mac OS and Windows. You can get latest binaries from [here](github.com/AokChain/AokChain/releases/latest) or build it on your own using code from [master](https://github.com/AokChain/AokChain/tree/master) branch.

Once you downloaded and extracted latest binaries at your machine, you will see two binaries:

 - `aokchaind` - headless AOK daemon responsible for syncing blockchain and providing wallet service
 - `aokchain-cli` - command line client which allows interact with AOK node and wallet

## Running node

!!! hint
    You can secure your full node by specifying `rpcuser` and `rpcpassword` in `~/.aokchain/aokchain.conf` file.

Running AOK node pretty straightforward, you can use `-printtoconsole` flag to see the output or use `-daemon` to run it in headless daemon mode. Those flags can be specified in conf file as well.

```
./aokchaind -daemon
```

## Stopping node

If you launched AOK node in daemon mode, it can be stopped using cli utility like this:

```
aokchain-cli stop
```