"""ping.py

Defines the ping command.
"""

from discord import Interaction, app_commands

from ..client import LocalBot


@app_commands.command(name="ping", description="Display bot latency")
async def ping_command(interaction: Interaction) -> None:
    latency = round(interaction.client.latency * 1000)
    await interaction.response.send_message(
        f"Bot latency: **{latency}** ms"
    )


async def setup(bot: LocalBot) -> None:
    """Required entry point for load_extension()."""
    bot.tree.add_command(ping_command)
