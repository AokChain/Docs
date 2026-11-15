---
title: Send tokens
description: Send tokens from the desktop wallet or a node, to an address or a username, with an optional time lock or message.
order: 40
---

Tokens are sent like AOK, and the fee is paid in AOK, so the wallet needs a little AOK as well. A token can be sent once a block includes the transaction that created or delivered it.

## In the desktop wallet

1. Open **Send** and choose the **Tokens** tab. You can also click **Send** on a token card of the **Tokens** page, or click a token on the **Overview** page and choose **Send Token**.
2. Under **Token to send**, pick the token. The wallet shows how much of it is **Available**.
3. In **Recipient address**, enter an address or a username such as `@ALICE`.
4. Enter the **Quantity**. **All** sends everything the wallet holds of this token.
5. Click **Send** and enter your passphrase if asked.
6. The window **Check before sending** says "You are sending a token" and names it. Check that the recipient expects this token, then click **Send**.

**Add recipient** sends the same token to several addresses in one transaction. **Send with a lock** keeps the recipient from spending the tokens before a time you choose, as for AOK: see [[send-and-receive#send-with-a-lock|Send with a lock]].

### Send an owner token

Sending an owner token such as `ORCHARD!` hands over the control of the token. In the advanced view (see [[create-a-token#turn-on-the-advanced-view|Turn on the advanced view]]) the **Tokens** tab of **Send** has a **Transfer Administrator Token** box; tick it and pick the owner token in **Token:**.

## With a node

```bash
aokchain-cli transfer "ORCHARD" 250 "<address>"
```

| Argument | Meaning |
| --- | --- |
| `token_name` | The token |
| `qty` | How many to send |
| `to_address` | An address or a username |
| `token_lock_time` | Optional: the tokens cannot be spent before this block height, or this time in seconds since 1970 if the number is 500,000,000 or more |
| `message` | Optional: a message of up to 120 characters |

The message is written into the transaction, where everyone can read it.

Tokens cannot be sent to an offline staking address (on the main network one that starts with `2`): its script cannot carry tokens. The **Send** page says so under the address field, and `transfer` and the other token commands refuse it with error `-5`, `Tokens cannot be sent to an offline staking address`. Versions before 4.0.6 refused a transfer there with `Transaction amount too small`.

Other commands:

| Command | What it does |
| --- | --- |
| `transfermany "ORCHARD" '{"<address 1>":10,"<address 2>":20}'` | Sends one token to several addresses in one transaction |
| `transferfromaddress "<from address>" "ORCHARD" 5 "<to address>"` | Sends only tokens that are at one address of the wallet |
| `listmytokens` | Lists the tokens of the wallet; `listmytokens "ORCHARD" true` adds the outputs that hold them |
| `listmylockedtokens` | Lists tokens of the wallet that are still locked |

## Locked tokens

Tokens sent with a lock arrive at once, but they stay locked until the height or time. `listmylockedtokens` lists them, and the address page of the block explorer shows them in the **Locked** column.
