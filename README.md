<a href="https://codeclimate.com/github/Kem0111/wallet_action/maintainability"><img src="https://api.codeclimate.com/v1/badges/3e8de494c6b9c185a482/maintainability" /></a> ![Deployed on AWS](https://img.shields.io/badge/Deployed%20on-AWS-orange)

Give it a shot  - you'll like it  
walletchekingbot - https://t.me/walletchekingbot

# Wallet Tracker Bot

Wallet Tracker Bot is a helpful and user-friendly Telegram bot designed to assist users in managing and monitoring their Ethereum wallets. Although currently tailored for the Russian market, an English version will be released soon.  

### Features

Add and manage multiple Ethereum wallets  
Track wallet transactions  
Display token balances  
Get a list of wallets associated with a user  
Delete a wallet from the user's list  


### How it Works

The bot interacts with users via the Telegram interface and stores user data, including wallet addresses, in a database. Each user can have multiple wallet addresses associated with their account, and each address can have multiple transactions and token balances.


### Technologies and Libraries

| Technology/Library | Purpose                                                   |
|--------------------|-----------------------------------------------------------|
| Python             | Programming language                                      |
| Aiogram            | Asynchronous framework for building Telegram bots         |
| Tortoise-ORM       | Easy-to-use asyncio ORM for Python                        |
| Postgres           | Relational database system                                |
| aiofiles           | Asynchronous file handling for Python                     |
| asyncpg            | Asynchronous PostgreSQL client for Python                 |
| aiohttp            | Asynchronous HTTP client/server framework                 |