---
title: Unique tokens
description: Create unique tokens (NFTs) under a main token or a sub token, one by one or many in one transaction, with an optional IPFS hash each.
order: 50
---

A unique token exists exactly once. It is written as its parent's name, `#`, and a tag: `ORCHARD#tree-17`, or `ORCHARD/GREEN#tree-17` under a sub token. Its quantity is 1, it has no decimals, and it cannot be reissued. The block explorer calls unique tokens NFTs.

## What you need

- The owner token of the parent, for example `ORCHARD!`.
- The cost for each unique token, set by governance, plus the fee. See [[token-names-and-costs]].
- A tag: letters `A-Z` and `a-z`, digits, and `@ $ % & * ( ) [ ] { } _ . ? : -`. The whole name, parent and tag together, has at most 31 characters. Spaces and `/` are not allowed in a tag.

## In the desktop wallet

Open **Create Tokens** (see [[create-a-token#turn-on-the-advanced-view|Turn on the advanced view]]), or click the parent token on the **Overview** page and choose **Issue Unique Token**.

1. Under **Token Type**, choose **Unique Token**. The amount in brackets is the cost.
2. Pick the parent token in the list next to it.
3. Enter the tag after the `#` and click **Check Availabilty**. Tags keep their small and capital letters.
4. To link a description file or an image, tick **Add JSON Meta Data Hash** and paste its IPFS hash. See [[token-metadata]].
5. Click **Create Token**, enter your passphrase, check the confirmation and click **Yes**.

## With a node

`issueunique` makes several unique tokens under a main token in one transaction:

```bash
aokchain-cli issueunique "ORCHARD" '["tree-17","tree-18"]'
```

With an IPFS hash for each, in the same order as the tags:

```bash
aokchain-cli issueunique "ORCHARD" '["tree-17","tree-18"]' '["<ipfs hash 1>","<ipfs hash 2>"]'
```

The cost is paid once for each token. For a unique token under a sub token, use `issue` with the whole name:

```bash
aokchain-cli issue "ORCHARD/GREEN#tree-17"
```

## Send a unique token

A unique token is sent like any token, with a quantity of 1: see [[send-tokens]].
