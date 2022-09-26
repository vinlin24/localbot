"""pwd.py

Defines the pwd command.
"""

from discord import Interaction, app_commands

from ..client import CWD, LocalBot


@app_commands.command(name="pwd", description="Display the current working directory")
async def pwd_command(interaction: Interaction) -> None:
    await interaction.response.send_message(CWD.path)


async def setup(bot: LocalBot) -> None:
    """Required entry point for load_extension()."""
    bot.tree.add_command(pwd_command)
