---
title: Create a token
description: Create a main token or a sub token in the desktop wallet's advanced view or with the issue command, and what it costs.
order: 20
---

Creating a token takes one transaction. It pays the creation cost in AOK and sends the new token and its owner token to your wallet.

## Before you start

- Pick a name and check that it follows the rules: see [[token-names-and-costs]].
- Have enough AOK for the cost and the fee. The cost is set by governance and shown next to each token type.
- Decide the quantity, the units and whether the token is reissuable. The name can never change, and the units can only be raised later. See [[token-basics#settings-of-a-token|Settings of a token]].

## Turn on the advanced view

The pages **Create Tokens** and **Manage Tokens** appear in the side bar of the desktop wallet when it runs with the advanced view.

1. Go to **Settings › Open Configuration File**.
2. Add this line to `aokchain.conf` and save the file:

   ```ini
   advancedui=1
   ```

3. Restart AokChain Core.

Starting the program with `-advancedui` has the same effect.

## Create a main token

1. Open **Create Tokens**.
2. Under **Token Type**, keep **Main Token**. The amount in brackets is what creating it costs.
3. Enter the **Name** and click **Check Availabilty**. The wallet turns the letters into capitals; **Valid Token** means the name is free.
4. Enter the **Quantity** and the **Units** (the number of decimals; the example next to the field shows what one unit looks like).
5. Leave **Reissuable** ticked if you may want to issue more later.
6. To link a description file, tick **Add JSON Meta Data Hash** and paste its IPFS hash. See [[token-metadata]].
7. Click **Create Token** and enter your passphrase.
8. The confirmation lists the cost (paid to the address that governance has set for it), the token sent to your address, the fee and the total. Click **Yes**.

The wallet shows the transaction ID. You can send the new token once a block includes the transaction.

The desktop wallet takes whole quantities up to 21,000,000,000. For more, or for a quantity with decimals, use the `issue` command below.

## Create a sub token

You need the owner token of the parent, for example `ORCHARD!` to create `ORCHARD/GREEN`.

1. Open **Create Tokens** and choose **Sub Token** under **Token Type**.
2. Pick the parent token in the list next to it.
3. Enter the part of the name after the `/`, click **Check Availabilty**, and go on as for a main token.

The wallet sends the parent's owner token back to one of your own addresses in the same transaction.

If you hold an owner token, clicking that token on the **Overview** page also offers **Issue Sub Token**, **Issue Unique Token** and **Reissue Token**. These open the same pages, also without the advanced view.

Unique tokens are on [[unique-tokens]], usernames on [[usernames]].

## With a node

```bash
aokchain-cli issue "ORCHARD" 1000000 "" "" 0 true
```

| Argument | Example | Meaning |
| --- | --- | --- |
| `token_name` | `"ORCHARD"` | Name of the new token; `"ORCHARD/GREEN"` for a sub token |
| `qty` | `1000000` | Quantity to issue |
| `to_address` | `""` | Address for the token; empty makes a new one |
| `change_address` | `""` | Address for the AOK change; empty makes a new one |
| `units` | `0` | Decimals, 0 to 8 |
| `reissuable` | `true` | Whether more can be issued later |
| `has_ipfs` | `false` | Whether an IPFS hash follows |
| `ipfs_hash` | | The IPFS hash, `Qm...` |

The command returns the transaction ID in a list. When a block includes it, check the token:

```bash
aokchain-cli gettokendata "ORCHARD"
```

```json
{
  "name": "ORCHARD",
  "amount": 1000000,
  "units": 0,
  "reissuable": 1,
  "has_ipfs": 0
}
```

`issuanceinfo` shows the current costs. See [[rpc-tokens]] for all token commands.
