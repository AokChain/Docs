---
title: Send and receive AOK
description: Get an address to be paid, send AOK to one or more recipients, and send coins with a time lock in the desktop wallet.
order: 30
---

This page covers AOK in the desktop wallet. For tokens, see [[send-tokens]].

## Receive

1. Open **Receive**.
2. Optionally fill in **Label** (who or what the payment is for), **Amount** and **Message** (shown to the payer when the request is opened).
3. Click **Request payment**. The address appears under **Receiving address** with its QR code.
4. Click **Copy address**, or **Copy QR code**, and give it to the payer.

Every request gives a new address, which keeps your payments apart. To receive again on an address you gave out before, tick **Reuse an address I already gave to someone**. Earlier requests are listed under **Request history**; **Show** opens one again.

The QR code holds a payment link with the address, and the amount, label and message if you entered them, so the payer can see the label too. None of them is written to the chain. See [[payment-links]].

An incoming payment shows under **Pending** on the **Overview** page until a block includes it, and then under **Available**.

## Send

1. Open **Send** and stay on the **AOK** tab.
2. In **Recipient address**, paste the address with the paste button, or pick one from your address book with the address book button. You can also type a username such as `@ALICE`; it is resolved to its address when you send. A line under the field tells you whether the address is valid.
3. Enter the **Amount**. **All** puts in your whole available balance and takes the fee from it.
4. Choose the **Fee**: **Slow**, **Normal** or **Custom**. **Normal** suits almost every payment.
5. Check the **Summary** on the right and click the send button below it, which shows the amount, for example **Send 5 AOK**.
6. Enter your passphrase if the wallet asks for it.
7. The window **Check before sending** shows the coin, the amount, the recipient with the whole address, the fee and your balance after sending. Compare the address with the one you were given, then click **Send**.

The wallet then shows the transaction ID. **Copy the transaction ID** lets you look the payment up on the [[block-explorer]].

> [!CAUTION]
> A transaction that has been sent cannot be cancelled. If the confirmation window says "Not in the address book: nothing was sent to this address from this wallet before", check the address character by character.

### More than one recipient

Click **Add recipient** for each further address. All of them are paid in one transaction with one fee.

### Options

- **Label** saves the address with a name in your address book.
- **Subtract the fee from the amount** makes the recipient receive the amount minus the fee.
- **Coin Control Features** appear on the page when **Settings › Wallet › Enable coin control features** is on. **Inputs...** lets you pick the coins that the payment spends.

## Send with a lock

A locked payment arrives at once, but the recipient cannot spend it before a time you choose.

1. Fill in the recipient and the amount as above.
2. Click **Send with a lock**.
3. Pick **1 month**, **3 months**, **6 months** or **1 year**, or set a date and time, and click **OK**. The recipient card shows **Locked until** with the time.
4. Send as usual.

The recipient's desktop wallet shows the coins under **Pending** until the lock ends, and as available after that. A lock cannot be lifted early, not even by you.

## See your payments

The **Transactions** page lists every payment. The tabs **All**, **Received**, **Sent** and **Staking** and the search box narrow the list; double-click a row for its details. The right mouse button offers **Copy transaction ID** and **Show in the explorer**. **Export to CSV** saves the list as a file.
