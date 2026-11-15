---
title: Frozen addresses
description: What a frozen address is, how to look one up and what it means for your coins.
order: 1
---

Governance commands are signed transactions that can freeze or unfreeze an address. A frozen address cannot send AOK or tokens until it is unfrozen.

## Look up an address

The explorer marks frozen addresses with a **Frozen** chip. On a node:

```bash
aokchain-cli checkfreeze "<address>"
aokchain-cli freezelist
```

## Governance commands

Freezing and unfreezing are governance commands: signed transactions on the chain, so anyone can read them in the explorer.

> [!NOTE]
> `freezelist` returns every address that is frozen now.
