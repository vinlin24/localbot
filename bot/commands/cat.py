"""cat.py

Defines the cat command.
"""

from pathlib import Path

from discord import File, Interaction, app_commands

from ..client import CWD, LocalBot
from ..utils import MESSAGE_LENGTH_LIMIT


@app_commands.command(name="cat", description="Display file content")
@app_commands.describe(path_str="Absolute or relative path to file",
                       encoding="Encoding to read the file with (defaults to UTF-8)")
@app_commands.rename(path_str="path")
async def cat_command(interaction: Interaction, path_str: str, encoding: str = "utf-8") -> None:
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
    if path.is_dir():
        return await interaction.response.send_message(
            f"**{path}** is a directory!",
            ephemeral=True
        )

    # Try to read content
    try:
        with path.open("rt", encoding=encoding) as f:
            content = f.read()
    except Exception as error:
        return await interaction.response.send_message(
            f"Could not read content from **{path}**:\n"
            f"```{type(error).__name__}: {error}```"
        )

    # Determine if the message needs to be sent as a file
    # TODO: maybe use pagination to split up content instead
    content = f"```{content}```"
    if len(content) > MESSAGE_LENGTH_LIMIT:
        file = File(path)
        await interaction.response.send_message(file=file)
    else:
        await interaction.response.send_message(content)


async def setup(bot: LocalBot) -> None:
    """Required entry point for load_extension()."""
    bot.tree.add_command(cat_command)
