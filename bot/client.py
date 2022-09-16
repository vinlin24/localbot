"""client.py

Defines the bot class to use in this program.
"""

import os

import discord
from discord.ext import commands
from discord.ext.commands import Context

from .listener import shell_command_callback
from .secrets import COMMAND_CHANNEL_ID, DISCORD_USER_ID, PRIVATE_GUILD


class LocalBot(commands.Bot):
    """Bot to use in this program."""

    def __init__(self) -> None:
        super().__init__(command_prefix="!",
                         intents=discord.Intents.all())

    async def setup_hook(self) -> None:
        """Async code to run after login and before connection."""
        # Register slash commands
        await _load_bot_extensions(self)

        # Sync slash commands
        self.tree.copy_global_to(guild=PRIVATE_GUILD)
        await self.tree.sync(guild=PRIVATE_GUILD)
        print(f"Synced commands to guild with ID={PRIVATE_GUILD.id}.")

        # Register handler
        self.before_invoke(_before_invoke_handler)

    async def on_ready(self) -> None:
        """Event handler for when bot internal cache is ready."""
        print("Bot ready")

    async def on_message(self, message: discord.Message, /) -> None:
        # Ignore own messages and other bot messages, always
        if message.author.bot:
            return

        # Check if it's in the dedicated command channel and sender is dev
        if message.channel.id == COMMAND_CHANNEL_ID \
                and message.author.id == DISCORD_USER_ID:
            await shell_command_callback(message, self.loop)
            # Treat everything in this channel as an input, not a command
            return

        # Required when overriding on_message to not silence commands
        await self.process_commands(message)


async def _load_bot_extensions(bot: LocalBot) -> None:
    """Load every command module as a bot extension."""
    commands_dir = os.path.join(os.path.dirname(__file__), "commands")
    success = 0
    total = 0
    for filename in os.listdir(commands_dir):
        if filename.endswith(".py"):
            total += 1
            module_path = f".commands.{filename.removesuffix('.py')}"
            try:
                await bot.load_extension(module_path, package=__package__)
            except commands.ExtensionError as e:
                print(f"FAILED to load {filename} as bot extension.")
                print(f"{type(e).__name__}: {e}")
            else:
                print(f"LOADED {filename} as bot extension.")
                success += 1
    if success == total:
        print(
            f"LOADED all bot extensions successfully ({success} success/"
            f"{total} total)."
        )
    else:
        print(
            f"FAILED to load all bot extensions ({success} success/"
            f"{total} total)."
        )


async def _before_invoke_handler(ctx: Context) -> None:
    """Event handler for when a command is about to be invoked."""
    if ctx.command is None:
        command_name = "<Unknown>"
    else:
        command_name = ctx.command.name
    print(f"Invoking /{command_name}.")
