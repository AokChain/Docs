---
title: Token metadata
description: The JSON format for a token's name, description, image and properties.
order: 2
aliases: [metadata]
---

A token can point to a JSON document that describes it. The format follows the ERC-1155 metadata schema loosely.

## Schema

```json
{
  "title": "Token Metadata",
  "type": "object",
  "properties": {
    "name": { "type": "string", "description": "The name of the token." },
    "description": { "type": "string", "description": "What the token is for." },
    "image": { "type": "string", "description": "A URI of an image of the token, 320 to 1080 pixels wide." },
    "properties": { "type": "object", "description": "Any other properties." }
  }
}
```

## Example

```json
{
  "name": "Mjolnir",
  "description": "The hammer of the thunder god in Norse mythology.",
  "image": "ipfs://QmeJPx9UpmyZ4536oSp4cNb9C1aSX4PzT8n9mrYppQ2KrN",
  "properties": {
    "simple_property": "example value",
    "array_property": { "name": "Name", "value": [1, 2, 3, 4], "class": "emphasis" }
  }
}
```

## Fields

| Field | Type | Required |
|---|---|:-:|
| `name` | string | yes |
| `description` | string | yes |
| `image` | URI | no |
| `properties` | object | no |
