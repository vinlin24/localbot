"""secrets.py

Loads sensitive values from environment variables and exposes them to
the program as Python constants.
"""

import os

import discord
import dotenv

# Load from .env file if it's set up
dotenv.load_dotenv(override=True)

BOT_TOKEN = os.environ["BOT_TOKEN"]
"""Bot authentication token."""

DISCORD_USER_ID = int(os.environ["DISCORD_USER_ID"])
"""User ID of my Discord account."""

PRIVATE_GUILD = discord.Object(id=int(os.environ["PRIVATE_GUILD_ID"]))
"""Discord server that bot will be restricted to."""

COMMAND_CHANNEL_ID = int(os.environ["COMMAND_CHANNEL_ID"])
"""Channel ID for sending shell commands."""
