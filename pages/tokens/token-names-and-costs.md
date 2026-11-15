---
title: Token names and costs
description: The rules for token names, quantities and units, and what creating, reissuing and registering tokens costs on the main network.
order: 70
---

## Names

| Kind | Form | Rules |
| --- | --- | --- |
| Main token | `ORCHARD` | 3 to 30 characters: `A-Z`, `0-9`, dot and underscore |
| Sub token | `ORCHARD/GREEN` | Each part follows the same rules; the whole name has at most 30 characters. A sub token can have sub tokens of its own: `ORCHARD/GREEN/SMALL`. |
| Unique token | `ORCHARD#tree-17` | The tag may use `A-Z`, `a-z`, `0-9` and `@ $ % & * ( ) [ ] { } _ . ? : -`; the whole name has at most 31 characters |
| Username | `@ALICE` | 4 to 30 characters after `@`: `A-Z`, `0-9`, dot and underscore |
| Owner token | `ORCHARD!` | Made automatically with a main token or a sub token |

For main tokens and sub tokens:

- Only capital letters. Small letters are allowed in unique tags only.
- A dot or an underscore cannot be the first or the last character of a part, and two of them cannot follow each other: `MY.TOKEN` is valid, `.MYTOKEN`, `MYTOKEN_` and `MY..TOKEN` are not.
- `AOK`, `AOKCHAIN`, `AOKCOIN`, `AOKHACOIN` and `AOKHACHAIN` are reserved.

A name belongs to whoever creates it first. A name that is already taken, or waiting in the memory pool, is refused. **Check Availabilty** in the desktop wallet tells you before you pay.

## Quantity and units

- **Units** are the number of decimals, from 0 to 8. With 2 units, the smallest amount is 0.01.
- A quantity must fit the units: with 1 unit, `10.5` is valid and `10.55` is not.
- A token can have at most 25,000,000,000 in total. The desktop wallet takes whole quantities up to 21,000,000,000; the `issue` command takes the full range.
- Unique tokens and usernames always have a quantity of 1 and 0 units, and are not reissuable. An owner token has a quantity of 1.

## Costs

Creating, reissuing and registering pay a fixed cost in AOK, on top of the normal fee. The cost goes to an address set by governance. Governance can change the amounts and the address at any time, so check them before you start.

On the main network the costs were, when this page was written:

| Action | Cost |
| --- | --- |
| Create a main token | 1,000,000 AOK |
| Create a sub token | 100,000 AOK |
| Create a unique token | 1 AOK each |
| Reissue a token | 1,000,000 AOK |
| Register a username | 1 AOK |

Where to see the current costs:

- **Desktop wallet:** the **Token Type** list of **Create Tokens** shows the cost next to each type.
- **Node:** `issuanceinfo` returns the costs and the address they are paid to:

  ```json
  {
    "cost": {
      "root": 1000000.00000000,
      "reissue": 1000000.00000000,
      "unique": 1.00000000,
      "sub": 100000.00000000,
      "username": 1.00000000
    },
    "address": "<address set by governance>"
  }
  ```

- **Explorer API:** [v3.aokscan.com/api/v3/tokens/issuance](https://v3.aokscan.com/api/v3/tokens/issuance).

How governance sets these values is described on [[how-network-rules-change]].
