# Scout (formerly mmmyea)
web app and discord bot with helpful utilities for overwatch teams. can currently scout for teams that exist on the tepsa leaderboard.

## requirements
* python >= 3.6
* discord.py==1.2.4
* requests
* scrapy

## usage
* obtain a discord bot token from dev portal and substitute it in `discord_bot.py`
* verify that the tespa url is correct in `scrape_tespa.py` (different url for each season)
* run `scrape_tespa.py` to update to latest data (or rewrite the code to fetch stats from tespa on demand)
* run `discord_bot.py` to start the bot
* invite the bot to your server by generating an invite link through the dev portal
