---
title: Token metadata
description: Describe a token with a JSON file on IPFS and link it with an IPFS hash. The schema, an example, and how to attach and change the hash.
order: 80
aliases: [metadata]
---

A token can carry an IPFS hash that points to a JSON file describing it: a name, a description, an image and any other properties. The file itself is not on the chain; the chain holds only the hash.

## The schema

The format follows the ERC-1155 metadata JSON schema loosely:

```json
{
  "title": "Token Metadata",
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "Identifies the name of given token."
    },
    "description": {
      "type": "string",
      "description": "Describes the token and its purpose."
    },
    "image": {
      "type": "string",
      "description": "A URI pointing to a resource with mime type image/* representing the asset to which this token represents. Consider making any images at a width between 320 and 1080 pixels and aspect ratio between 1.91:1 and 4:5 inclusive."
    },
    "properties": {
      "type": "object",
      "description": "Arbitrary properties. Values may be strings, numbers, object or arrays."
    }
  }
}
```

## An example

```json
{
  "name": "Mjölnir",
  "description": "Mjölnir is the hammer of the thunder god Thor in Norse mythology, used both as a devastating weapon and as a divine instrument to provide blessings.",
  "image": "ipfs://QmeJPx9UpmyZ4536oSp4cNb9C1aSX4PzT8n9mrYppQ2KrN",
  "properties": {
    "simple_property": "example value",
    "rich_property": {
      "name": "Name",
      "value": "123",
      "display_value": "123 Example Value",
      "class": "emphasis",
      "css": {
        "color": "#ffffff",
        "font-weight": "bold",
        "text-decoration": "underline"
      }
    },
    "array_property": {
      "name": "Name",
      "value": [1, 2, 3, 4],
      "class": "emphasis"
    }
  }
}
```

The block explorer reads files in this format: the page of a token shows its IPFS hash and, under **Metadata**, the name, the description, the properties and the image.

## The IPFS hash

Add the JSON file to IPFS and use the hash IPFS gives you. AokChain accepts IPFS version 0 hashes only: 46 characters that start with `Qm`. Keep the file available on IPFS, for example with a pinning service; if nobody serves it, the hash leads nowhere.

## Attach the hash

| When | Desktop wallet | Node |
| --- | --- | --- |
| Creating a main token or a sub token | Tick **Add JSON Meta Data Hash** on **Create Tokens** | `issue "NAME" qty "" "" units reissuable true "Qm..."` |
| Creating unique tokens | Tick **Add JSON Meta Data Hash** on **Create Tokens** | `issueunique "NAME" '["tag"]' '["Qm..."]'` |
| Changing it later | Tick **Change IPFS Hash** on **Manage Tokens** | `reissue "NAME" 0 "<address>" "" true -1 "Qm..."` |

Changing the hash later is a reissue: the token has to be reissuable, and the reissue cost applies. A unique token cannot be reissued, so its hash cannot change.

`gettokendata "NAME"` shows the hash of a token:

```json
{
  "name": "PEARS",
  "amount": 100,
  "units": 0,
  "reissuable": 1,
  "has_ipfs": 1,
  "ipfs_hash": "QmTqu3Lk3gmTsQVtjU7rYYM37EAW4xNmbuEAp2Mjr4AV7E"
}
```
