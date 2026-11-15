---
title: Address book
description: Keep your receiving addresses and the addresses you pay in the desktop wallet, with labels, QR codes and export.
order: 60
---

The **Address book** page has two lists side by side: **Receiving addresses**, the addresses of your wallet, and **Sending addresses**, the addresses you pay. Labels are kept in your wallet file only.

## Receiving addresses

- **New** makes a new address of your wallet with a label you choose.
- **Copy** copies the selected address.
- **Edit** changes its label.
- **QR code** shows the QR code of the address.

Receiving addresses cannot be deleted: the wallet keeps every key it ever made.

## Sending addresses

- **Add** saves an address with a label.
- **Copy** and **Edit** work as for receiving addresses.
- **Send** opens the **Send** page with the selected address.
- **Delete** removes the address from the list.

The **Send** page adds an address here when you give it a label there. In the confirmation window before a payment, an address that is not in the address book and was never paid before gets a warning.

## Search and export

The search box above each list finds an address by its label or by part of the address. The list shows addresses shortened to the first and last four characters; point at one to see the whole address. The download button at the bottom right of each list saves it as a CSV file.

## On a node

| Command | What it does |
| --- | --- |
| `getnewaddress "label"` | Makes a new receiving address with a label |
| `setlabel "address" "label"` | Sets the label of an address |
| `getaddressesbylabel "label"` | Lists the addresses with that label |
| `listlabels` | Lists all labels |
