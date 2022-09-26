"""utils.py

Defines useful constants and helper functions.
"""

from pathlib import Path

from discord import Interaction

from .client import CWD

MESSAGE_LENGTH_LIMIT = 2000
"""Default maximum number of characters in a Discord message."""


def get_path(path_str: str) -> Path:
    """Get a Path object from an absolute or relative path string.

    Args:
        path_str (str): String representing an absolute or relative
        path. Relative paths are interpreted relative to the current
        value of `.client.CWD.path`. The string can be wrapped in
        single or double quotes as it would be in most shell settings.

    Returns:
        Path: The converted Path object.
    """
    path = Path(path_str.strip("\"'"))
    if not path.is_absolute():
        path = CWD.path / path
    return path


async def validate_path(interaction: Interaction,
                        path: Path,
                        dir: bool | None
                        ) -> bool:
    """Validate that a path is well-defined.

    Args:
        interaction (Interaction): Interaction from the application
        command using this helper function.
        path (Path): Path object to validate.
        dir (bool | None): If a bool, assert that the path is/isn't a
        directory. If None, allow either case.

    Returns:
        bool: Whether the path is valid. If False, this function
        handles responding to the interaction.
    """
    if not path.exists():
        await interaction.response.send_message(
            f"**{path}** does not exist!",
            ephemeral=True
        )
        return False
    if dir is True and not path.is_dir():
        await interaction.response.send_message(
            f"**{path}** is not a directory!",
            ephemeral=True
        )
        return False
    if dir is False and path.is_dir():
        await interaction.response.send_message(
            f"**{path}** is a directory!",
            ephemeral=True
        )
        return False
    return True


def escape_path(path: Path) -> str:
    """Return the expected render of a path."""
    # \. becomes invisible in Discord messages
    return str(path).replace("\\.", "\\\\.")
