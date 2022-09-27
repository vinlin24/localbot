"""cd.py

Defines the cd command.
"""

from pathlib import Path

from discord import Interaction, app_commands
from discord.app_commands import Choice

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


@cd_command.autocomplete("path_str")
async def cd_autocomplete(interaction: Interaction,
                          current: str
                          ) -> list[Choice[str]]:
    # Pretend the current string is a path
    # The autocomplete options then are its "siblings"

    # TODO: Doesn't work as expected for partial inputs with trailing slash
    # e.g. repos/counters/ doesn't bring up children of the counters dir
    # This also causes . and .. to not work as expected

    path = Path(current)
    if path.is_absolute():
        siblings = path.parent.iterdir() if current else path.iterdir()
    else:
        parent = (CWD.path / path).parent if current else CWD.path
        siblings = parent.iterdir()

    result = []
    for sibling in siblings:
        if len(result) == 25:
            break
        if sibling.is_dir() and path.name in sibling.name:
            full_path = sibling.resolve()
            print(full_path)
            result.append(Choice(
                name=str(full_path),
                value=str(full_path)
            ))
    return result


async def setup(bot: LocalBot) -> None:
    """Required entry point for load_extension()."""
    bot.tree.add_command(cd_command)
