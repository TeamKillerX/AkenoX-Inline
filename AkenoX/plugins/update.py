import os
import subprocess
import sys

from pyrogram import filters

from AkenoX import *

@RENDYDEV.user(prefix=["update"], filters=filters.me)
async def update_bot(client, message):
    """Pulls updates, rebuilds, and restarts the bot inside Docker."""
    msg = await message.reply_text("🔄 Updating bot, please wait...")
    try:
        process = subprocess.run(["git", "pull"], capture_output=True, text=True)
        git_output = process.stdout + process.stderr

        if "Already up to date." in git_output:
            return await msg.edit("✅ Bot is already up to date!")

        if os.path.exists("/.dockerenv"):
            await msg.edit("🔄 Update pulled! Restarting bot in Docker...")
            subprocess.run("docker compose down && docker compose up --build -d", shell=True)
            return

        await msg.edit("🔄 Update pulled! Restarting bot...")

        os.execl(sys.executable, sys.executable, "-m", "AkenoX")

    except Exception as e:
        await msg.edit(f"❌ Update failed!\n\nError:\n`{str(e)}`")
