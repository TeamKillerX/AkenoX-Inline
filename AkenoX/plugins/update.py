from AkenoX import *
import os
import subprocess
import sys
from pyrogram import filters

@RENDYDEV.user(prefix=["update"], filters=filters.me)
async def update_bot(client, message):
    """Pulls updates, rebuilds, and restarts the bot inside Docker."""
    
    msg = await message.reply_text("🔄 Updating bot, please wait...")

    try:
        # Pull latest changes from GitHub
        process = subprocess.run(["git", "pull"], capture_output=True, text=True)
        git_output = process.stdout + process.stderr

        if "Already up to date." in git_output:
            return await msg.edit("✅ Bot is already up to date!")

        # Check if running inside Docker
        if os.path.exists("/.dockerenv"):
            await msg.edit("🔄 Update pulled! Restarting bot in Docker...")

            # Run shell command to restart Docker container
            subprocess.run("docker compose down && docker compose up --build -d", shell=True)

            return  # Exit after restart

        # If not running in Docker, restart manually
        await msg.edit("🔄 Update pulled! Restarting bot...")

        os.execl(sys.executable, sys.executable, "-m", "AkenoX")

    except Exception as e:
        await msg.edit(f"❌ Update failed!\n\nError:\n`{str(e)}`")
