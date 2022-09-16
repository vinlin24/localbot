"""listener.py

Defines the callback called from on_message when I send a message in
the dedicated command channel.
"""

import asyncio
import os
import shlex
import subprocess
import traceback

import discord

MESSAGE_LENGTH_LIMIT = 2000
"""Default Discord message length limit in characters."""


def _get_traceback(error: Exception) -> str:
    """Helper function for extracting traceback as a string."""
    return "\n".join(traceback.format_exception(error))


async def _send_content(message: discord.Message,
                        content: str
                        ) -> discord.Message:
    """Send the content as a file if it exceeds the character limit.

    Args:
        message (discord.Message): Message to reply to.
        content (str): Content to try to send to the message's channel.
        Should already include markup, if any.

    Returns:
        discord.Message: The message sent.
    """
    temp_file_path = os.path.join(os.path.dirname(__file__),
                                  "temp.txt")
    if len(content) > MESSAGE_LENGTH_LIMIT:
        with open(temp_file_path, "wb") as fp:  # Create temp file
            fp.write(content.encode("utf-8"))
        file = discord.File(temp_file_path, filename="content.txt")
        sent = await message.channel.send(file=file, reference=message)
        os.remove(temp_file_path)  # Delete temp file
        return sent
    return await message.channel.send(content, reference=message)


async def shell_command_callback(message: discord.Message,
                                 loop: asyncio.AbstractEventLoop
                                 ) -> None:
    """Handle messsages sent in the dedicated shell channel.

    Args:
        message (discord.Message): Message instance from on_message.
        The content is interpreted as a PowerShell command.
        loop (AbstractEventLoop): Event loop to execute subprocess in.
        Caller should pass in the bot's event loop.

    Postcondition:
        Handles responding to the message by displaying the stdout and
        stderr of the PowerShell command ran in a subprocess.
    """
    # Interpret message content as PowerShell command and args
    command = shlex.split(message.content, posix=False)

    # Run the subprocess asynchronously
    # TODO: Somehow maintain the cwd since it's bound to the subprocesses
    def run_process() -> subprocess.CompletedProcess[bytes]:
        return subprocess.run(
            ["powershell.exe"] + command,
            capture_output=True
        )
    try:
        completed = await loop.run_in_executor(None, run_process)
    except Exception as e:
        tb = _get_traceback(e)
        print(tb)
        content = ("⚠️ **Could not complete executing command:** ⚠️\n"
                   f"```{tb}```")
        await message.channel.send(content, reference=message)
        return

    # Extract output of subprocess if subprocess itself completed successfully
    stdout = completed.stdout.decode("utf-8")
    stderr = completed.stderr.decode("utf-8")

    # No output at all, just react as the response
    if not stdout and not stderr:
        await message.add_reaction("✅")
        return

    # Format stdout and/or stderr output
    content = ""
    if stdout:
        content += f"**Below is the stdout:**\n```{stdout}```\n"
    if stderr:
        content += f"**Below is the stderr:**\n```{stderr}```\n"
    await _send_content(message, content)
