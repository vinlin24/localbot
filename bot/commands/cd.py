"""cd.py

Defines the cd command.
"""

from discord import Interaction, app_commands

from ..client import CWD, LocalBot
from ..utils import escape_path, get_path, validate_path


@app_commands.command(name="cd", description="Change the working directory")
@app_commands.describe(path_str="Absolute or relative path to directory")
@app_commands.rename(path_str="path")
async def cd_command(interaction: Interaction, path_str: str) -> None:
    # Resolve path object based on absolute or relative path provided
    path = get_path(path_str)

    # Validate path
    valid = await validate_path(interaction, path, dir=True)
    if not valid:
        return  # validate_path already responded

    CWD.path = path.resolve()
    await interaction.response.send_message(
        f"Changed working directory to **{escape_path(CWD.path)}**."
    )


async def setup(bot: LocalBot) -> None:
    """Required entry point for load_extension()."""
    bot.tree.add_command(cd_command)
