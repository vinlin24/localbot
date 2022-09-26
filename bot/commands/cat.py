"""cat.py

Defines the cat command.
"""

from discord import File, Interaction, app_commands

from ..client import LocalBot
from ..utils import MESSAGE_LENGTH_LIMIT, escape_path, get_path, validate_path


@app_commands.command(name="cat", description="Display file content")
@app_commands.describe(path_str="Absolute or relative path to file",
                       encoding="Encoding to read the file with (defaults to UTF-8)")
@app_commands.rename(path_str="path")
async def cat_command(interaction: Interaction, path_str: str, encoding: str = "utf-8") -> None:
    # Resolve path object based on absolute or relative path provided
    path = get_path(path_str)

    # Validate path
    valid = await validate_path(interaction, path, dir=False)
    if not valid:
        return  # validate_path already responded

    # Try to read content
    try:
        with path.open("rt", encoding=encoding) as f:
            content = f.read()
    except Exception as error:
        return await interaction.response.send_message(
            f"Could not read content from **{escape_path(path)}**:\n"
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
