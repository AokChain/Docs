---
title: Usernames
description: Register a username such as @ALICE that people can pay instead of an address, look it up, and move it to another address.
order: 60
---

A username such as `@ALICE` is a token that stands for the address that holds it. People can pay `@ALICE` instead of typing your address: the wallet looks up the address that holds the username and pays it.

## Rules

- `@` followed by 4 to 30 characters: capital letters `A-Z`, digits `0-9`, dot and underscore. Dots and underscores can stand anywhere, also side by side: `@AB..CD` is a username.
- A username exists once on the chain. Its quantity is 1 and it cannot be reissued.
- Registering one costs the username cost set by governance, plus the fee. See [[token-names-and-costs]].

## Register a username

The desktop wallet has no page for this. Use `aokchain-cli` on a node, or type the same command without `aokchain-cli` in **Settings › Debug window**, on the **Console** tab:

```bash
aokchain-cli registerusername "@ALICE"
```

This sends the username to a new address of your wallet. To choose the address, add it:

```bash
aokchain-cli registerusername "@ALICE" "<your address>"
```

The command returns the transaction ID. The username works once a block includes the transaction.

A name that breaks the rules is refused with `Invalid username: <name>` and the rule. The address cannot be an offline staking address, which cannot hold tokens.

## Pay a username

Type the username where an address is expected:

- in the **Recipient address** field of the **Send** page, for AOK and for tokens; the line under the field says "A username: it is resolved to its address when sending";
- in `sendtoaddress`, `sendmany`, `transfer` and `transfermany` on a node.

Check the username before you send: `@ALICE` and `@ALICE_` are different names that can belong to different people.

## Look up a username

```bash
aokchain-cli getusernameaddress @ALICE
```

```json
{
  "address": "<the address that holds @ALICE>"
}
```

The search box of [@@explorer_host@@](@@explorer@@) finds usernames as well.

## Move a username to another address

Send the username token like any token, with a quantity of 1:

```bash
aokchain-cli transfer "@ALICE" 1 "<new address>"
```

From then on, payments to `@ALICE` go to the new address. If you send the username to someone else, payments to it go to them.
