"""__main__.py

Entry point.
"""

from .client import LocalBot
from .secrets import BOT_TOKEN


def main() -> None:
    """Main driver function."""
    bot = LocalBot()
    bot.run(BOT_TOKEN)


if __name__ == "__main__":
    main()
