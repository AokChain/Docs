---
title: Frozen addresses
description: What a frozen address is, how to look one up and what it means for your coins.
order: 1
---

Governance commands are signed transactions that can freeze or unfreeze an address. A frozen address cannot send AOK or tokens until it is unfrozen.

## Look up an address

The explorer marks frozen addresses with a **Frozen** chip. On a node:

```bash
aokchain-cli isfrozen <address>
```

## Why an address is frozen

Freezing is used against stolen funds and attacks on the network. Each governance command is on the chain and can be read in the explorer.

> [!NOTE]
> Sending to a frozen address works; spending from it does not.
