---
title: Reissue a token
description: Issue more of a token, raise its units, replace its IPFS hash or fix its supply for good, as the holder of its owner token.
order: 30
---

The holder of a token's owner token (for example `ORCHARD!`) can reissue a reissuable token. A reissue can do any of these at once:

- issue more of the token;
- raise the units (never lower them);
- add or replace the IPFS hash;
- turn **Reissuable** off. This is final: after it, nobody can issue more or change the token.

Every reissue costs the reissue cost set by governance, plus the fee, even when it issues nothing. See [[token-names-and-costs]].

## In the desktop wallet

The page **Manage Tokens** appears in the advanced view: see [[create-a-token#turn-on-the-advanced-view|Turn on the advanced view]]. You can also click a token on the **Overview** page and choose **Reissue Token**.

1. Open **Manage Tokens**.
2. In **Select an token to reissue:**, pick the token. **Current Token Settings** shows its name, quantity, units, whether it can be reissued, and its IPFS hash.
3. Enter the **Quantity** to add (0 to add none) and, if you want, a higher **Unit**.
4. Untick **Reissuable** to fix the supply for good, or tick **Change IPFS Hash** and paste the new hash.
5. Check **Updated Token Settings** and click **Reissue Token**.
6. Enter your passphrase, check the confirmation and click **Yes**.

## With a node

```bash
aokchain-cli reissue "ORCHARD" 500000 "<address>"
```

| Argument | Meaning |
| --- | --- |
| `token_name` | The token to reissue |
| `qty` | How many to add; `0` to add none |
| `to_address` | The address that receives the new tokens |
| `change_address` | Optional: the address for the change |
| `reissuable` | Optional, default `true`; `false` fixes the supply for good |
| `new_unit` | Optional, default `-1` (no change); can only be higher than the current units |
| `new_ipfs` | Optional: a new IPFS hash |

To fix the supply of `ORCHARD` without adding any:

```bash
aokchain-cli reissue "ORCHARD" 0 "<address>" "" false
```

A wallet without the owner token gets "Wallet doesn't have token: ORCHARD!". A token whose reissuable flag is off gets "Unable to reissue token: reissuable is set to false". Lower units get "unit must be larger than current unit selection".

The total supply of a token can never exceed 25,000,000,000.
