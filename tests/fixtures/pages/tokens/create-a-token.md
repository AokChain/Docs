---
title: Create a token
description: Issue a token, a sub token or a unique token, and what each one costs.
order: 1
---

A token has a name, an amount and a number of decimals (its units). Issuing it also creates the owner token `NAME!`, which you need to reissue it or to create sub tokens.

## Kinds of tokens

| Kind | Name | Amount | Decimals |
|---|---|--:|:-:|
| Token | `ROOT` | up to 21 billion | 0–8 |
| Sub token | `ROOT/SUB` | up to 21 billion | 0–8 |
| Unique token | `ROOT#TAG` | 1 | 0 |
| User name | `@name` | 1 | 0 |

## Issue a token

```bash
aokchain-cli issue "ROOT" 1000 "" "" 0 true
```

The arguments are the name, the amount, the address that receives it (empty for a new one), the change address, the units and whether it can be reissued.

> [!TIP]
> Pick the units carefully: they cannot be lowered once the token exists.

## Reissue

```bash
aokchain-cli reissue "ROOT" 500 "<address>"
```

Reissuing needs the owner token `ROOT!` in the same wallet. ~~Units can go down~~ Units can only go up.

Metadata for a token is described in [[token-metadata]].
