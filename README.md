# Xaidens Tools

## Overview

Xaidens Tools is a selfbot for Discord that provides various functionalities, including message spamming, server nuking, mass banning, and more.

![Main Menu](https://i.imgur.com/FfIAGJ0.png)

## Features

- Message Spammer
- Server Nuker
- Mass Ban
- Mass DM
- Server Info
- Account Nuker
- Server Permissions
- Webhook Spammer
- Mass @everyone Ping
- Mass Channel Create
- Purge messages
- Full Nuke(Channels And MSpam Make Channels)

## Prerequisites

Before running the selfbot, make sure you have the following:

- Python 3.8 or higher
- Discord.py library
- Colorama library
- Discord.py-self libray

You can install the required libraries using:

```bash
pip install discord.py colorama discord.py-self
```


# Getting Your Discord Token
To use the selfbot, you need your Discord user token. Follow these steps to obtain it:

Open Discord in your web browser (not the desktop app).
Log in to your account if you haven't already.
Open Developer Tools:
Right-click anywhere on the page and select Inspect or press Ctrl + Shift + I (Cmd + Option + I on Mac).
Go to the Network tab in Developer Tools.
Filter by "XHR" to see only XMLHttpRequests.
Perform any action on Discord (like sending a message).
Click on the request that was made when you performed the action.
In the Headers tab, look for a section labeled Request Headers.
Find the header called Authorization. Your token will be in the format Bot <your_token> or just <your_token>.
Copy the token (everything after Bot if it's there) and keep it safe.
Important: Treat your token like a password. Do not share it with anyone or expose it publicly.
