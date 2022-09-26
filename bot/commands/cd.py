"""cd.py

Defines the cd command.
"""

from pathlib import Path

from discord import Interaction, app_commands

from ..client import CWD, LocalBot


@app_commands.command(name="cd", description="Change the working directory")
@app_commands.describe(path_str="Absolute or relative path to directory")
@app_commands.rename(path_str="path")
async def cd_command(interaction: Interaction, path_str: str) -> None:
    # Resolve path object based on absolute or relative path provided
    path = Path(path_str.strip("\"'"))
    if not path.is_absolute():
        path = CWD.path / path

    # Validate path
    if not path.exists():
        return await interaction.response.send_message(
            f"**{path}** does not exist!",
            ephemeral=True
        )
    if not path.is_dir():
        return await interaction.response.send_message(
            f"**{path}** is not a directory!",
            ephemeral=True
        )

    CWD.path = path.resolve()
    await interaction.response.send_message(
        f"Changed working directory to **{CWD.path}**."
    )


async def setup(bot: LocalBot) -> None:
    """Required entry point for load_extension()."""
    bot.tree.add_command(cd_command)
