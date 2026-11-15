---
title: Multisig wallets
description: Make a multisig wallet with other people in the desktop wallet, receive to it, and send from it with a signing request.
order: 80
---

A multisig address lets coins go out only when a set number of several people sign, for example any two of three (2-of-3). The mistake of one person, or a theft from one person, does not move the coins. Everything below happens on the **Sign** page of the desktop wallet (**Sign message** in the side bar).

## Before you start

- Agree on the rule (how many people, how many must sign) and on who takes part. The rule and the participants cannot be changed later; to change them, make a new multisig wallet and move the coins.
- A multisig wallet has 2 to 15 participants. Each one needs their own desktop wallet.
- Only AOK can be sent from a multisig address in the desktop wallet; tokens cannot.
- If so many participants lose their wallets that fewer than the required number are left, nobody can take the coins out, not the developers either.

## 1. Gather the public keys

Every participant except the one who makes the wallet:

1. Opens **Sign** and clicks **Copy my public key** under **My multisig wallets**.
2. Sends the copied key (it starts with `aokms-key1:`) to the maker, by messenger or mail.

A public key is safe to share. Never send your passphrase, your wallet file or a private key to anyone, also not to the other participants.

## 2. Make the multisig wallet

The maker:

1. Clicks **Make a multisig wallet**.
2. **Set the rule:** enters a **Name of the multisig wallet** and picks **2-of-2**, **2-of-3**, **3-of-5** or **Other**, then clicks **Next: gather the participants**.
3. **Gather the participants:** gives each participant a name and pastes their public key. The maker's own key is filled in.
4. **Check and finish:** compares the participants with what was agreed and clicks **Make the multisig wallet**.
5. Clicks **Save the multisig information file** (or **Copy the information code**, which starts with `aokms-wallet1:`) and sends it to the other participants.

The keys are put in a fixed order, so every participant gets the same address whatever the order in which they were entered.

## 3. Add the wallet you were invited to

Every other participant:

1. Clicks **Add a multisig wallet I was invited to**.
2. Pastes the information code, or clicks **Open a file...** for the information file.
3. Compares the rule, the participants and the address with what the maker told you. The wallet says whether one of the keys is yours: "One of the public keys belongs to this wallet: you are a signer."
4. Ticks **Look for earlier transactions of this address** if coins were already paid to it, and clicks **Add the multisig wallet**.

## Receive

Give the multisig address to the payer like any other address; it starts with `k`. Its coins are listed under **My multisig wallets**, and in your balance as watch-only. They are not staked.

## Send from the multisig wallet

1. Under **My multisig wallets**, click **Send** next to the wallet.
2. Fill in the **Recipient address**, the **Amount** (or **All**), an optional memo for the other participants and the **Fee** (**Normal** or **Faster**, which pays twice the fee).
3. Click **Make the send request** and confirm. Your signature is in the request; nothing is sent yet.
4. Pass the request on with **Save the signing request file**, **Copy the request code** (it starts with `aokms-req1:`) or **Show as QR**.

Each participant who receives it:

1. Clicks **Open a signing request** and pastes the code or opens the file.
2. Checks what the request does. The amounts, the recipient, the change and the fee are read from the transaction itself, not from what the request says about itself. Red notes mean: do not sign, and ask the sender.
3. Clicks **Sign** and confirms. If more signatures are needed, passes the request on to the next participant.

When enough participants have signed, anyone who holds the request clicks **Broadcast**. A participant can also send a signed request back to the maker, who adds its signatures with **Load signatures I received (file · paste)**.

The requests are not passed on automatically: send them yourselves, by messenger or mail.

## Cancel a request

**Cancel this request** removes it from your wallet. If you already passed it on with your signature, the others can still complete and send it. To make sure it cannot be sent, spend its coins with another transaction.

## Back up

Every participant backs up their own wallet (see [[back-up-and-restore]]) and keeps the multisig information file. With a wallet backup and that file, the multisig wallet can be added again on another computer.

## On a node

Multisig addresses can also be made and spent with RPC commands. See [[multisig-rpc]].
