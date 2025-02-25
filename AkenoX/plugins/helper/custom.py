from AkenoX import *
import asyncio
from datetime import timedelta
from pyrogram.errors import RPCError

async def temporary_mute_user(client, message):
    try:
        args = message.text.split()
        if len(args) < 2:
            return await message.reply_text("Usage: `tmute [reply] <time>`\nExample: `tmute 10m`")

        if not message.reply_to_message:
            return await message.reply_text("Reply to a user to mute them temporarily.")

        duration = args[1]
        time_units = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        time_value = int(duration[:-1]) if duration[:-1].isdigit() else None
        time_multiplier = time_units.get(duration[-1])

        if time_value is None or time_multiplier is None:
            return await message.reply_text("Invalid time format! Use: `10s`, `5m`, `2h`, `1d`.")

        mute_time = time_value * time_multiplier

        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        await client.restrict_chat_member(chat_id, user_id, permissions=pyrogram.types.ChatPermissions())

        await message.reply_text(f"Muted user `{user_id}` for {duration}.")

        await asyncio.sleep(mute_time)

        await client.restrict_chat_member(chat_id, user_id, permissions=pyrogram.types.ChatPermissions(can_send_messages=True))
        await message.reply_text(f"User `{user_id}` has been unmuted after {duration}.")

    except RPCError as e:
        await message.reply_text(f"Error: {e}")
