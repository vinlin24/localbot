# localbot

## Description

A simple helper bot for you to use on your private server. Listens to you and only you. Performs basic operations on your local file system as if the Discord platform were like your shell. Expectedly, it must be run from your local machine, but it can be hooked up to a scheduler to make it run whenever your computer is on. More on that to come.

:hammer: **THIS BOT IS STILL IN DEVELOPMENT AND NOT READY FOR USE YET.**

## Disclaimer

:warning: **It should go without saying that since this bot has access to your local files, you should review the code yourself before attempting something that may irreversibly damage your machine. I assume no responsibility if such a situation happens.**

## Environment Setup

Repository setup (POSIX bash/zsh):
```console
git clone https://github.com/vinlin24/localbot.git
cd localbot
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
touch .env
vim .env
```

Repository setup (Windows PowerShell):
```console
git clone https://github.com/vinlin24/localbot.git
cd localbot
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
ni .env
code .env
```

The required environment variables are:

- `BOT_TOKEN`: The bot access token. Make one for yourself on the [Discord developer portal](https://discord.com/developers/applications).
- `DISCORD_USER_ID`: Your user ID, which can be found from your user's context menu when Developer Mode is enabled within User Settings.
- `PRIVATE_GUILD_ID`: The ID of the private server you intend to use this bot in.
- `COMMAND_CHANNEL_ID`: The ID of the text channel within your private server that you intend to send raw shell commands. I might remove this feature.

Running the bot (POSIX bash/zsh):
```console
python3 -m bot
```
Running the bot (Windows PowerShell):
```console
.\run.ps1  # which does "python -m bot"
```
