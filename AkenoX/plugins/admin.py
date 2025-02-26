from pyrogram.enums import ParseMode

from AkenoX import *
from AkenoX.plugins.helper.custom import get_user_info, temporary_mute_user
from AkenoX.plugins.libso.funcs_admin import *


@RENDYDEV.user(prefix=["id"], filters=(filters.me & ~filters.forwarded))
async def id_handler(client, message):
    if message.reply_to_message and message.reply_to_message.from_user:
        # Fetch User ID from the replied message
        user = message.reply_to_message.from_user
        user_info = f"<blockquote><b>User ID:</b> <code>{user.id}</code></blockquote>"
    else:
        # Fetch Chat ID if no user is replied to
        chat = message.chat
        user_info = f"<blockquote><b>Chat ID:</b> <code>{chat.id}</code></blockquote>"

    await message.reply_text(user_info, parse_mode=ParseMode.HTML)





@RENDYDEV.user(prefix=["info"], filters=(filters.me & ~filters.forwarded))
async def userinfo_handler(client, message):
    if message.reply_to_message and message.reply_to_message.from_user:
        user = message.reply_to_message.from_user
    else:
        user = message.from_user

    chat = message.chat

    user_info = (
        f"Name: {user.first_name} {user.last_name or ''}\n"
        f"User ID: {user.id}\n"
        f"Username: @{user.username if user.username else 'N/A'}\n"
        f"Chat ID: {chat.id}\n"
    )

    await message.reply_text(user_info)



@RENDYDEV.user(prefix=["promote", "fullpromote"], filters=(filters.me & ~filters.forwarded))
async def promoted_handler(client, message):
    await promotte_user(client, message)


@RENDYDEV.user(prefix=["demote"], filters=(filters.me & ~filters.forwarded))
async def demote_handler(client, message):
    await demote_user(client, message)


@RENDYDEV.user(prefix=["ban", "dban"], filters=(filters.me & ~filters.forwarded))
async def member_ban_handler(client, message):
    await member_ban_user(client, message)


@RENDYDEV.user(prefix="unmute", filters=(filters.me & ~filters.forwarded))
async def unmute_handler(client, message):
    await unmute_user(client, message)


@RENDYDEV.user(prefix="pin", filters=(filters.me & ~filters.forwarded))
async def pin_handler(client, message):
    await pin_message(client, message)


@RENDYDEV.user(prefix=["mute", "dmute"], filters=(filters.me & ~filters.forwarded))
async def mute_handler(client, message):
    await mute_user(client, message)


@RENDYDEV.user(prefix=["kick", "dkick"], filters=(filters.me & ~filters.forwarded))
async def kick_handler(client, message):
    await kick_user(client, message)


@RENDYDEV.user(prefix=["tmute"], filters=(filters.me & ~filters.forwarded))
async def tmute_handler(client, message):
    await temporary_mute_user(client, message)  # Function to handle temporary mute


RENDYDEV.buttons(
    "admin",
    [
        ["id [reply/username/userid]", "Fetch User ID & Chat ID."],
        ["userinfo [reply/username/userid]", "Fetch user details (name, username, ID, mention)."],
        ["ban [reply/username/userid]", "Ban someone."],
        ["dban [reply]", "dban a user deleting the replied to message."],
        ["unban [reply/username/userid]", "Unban someone."],
        ["kick [reply/username/userid]", "Kick out someone from your group."],
        ["dkick [reply]", "dkick a user deleting the replied to message."],
        ["promote `or` .fullpromote", "Promote someone."],
        ["demote", "Demote someone."],
        ["mute [reply/username/userid]", "Mute someone."],
        ["dmute [reply]", "dmute a user deleting the replied to message."],
        ["tmute [reply] <time>", "Temporarily mute a user for a set duration."],
        ["unmute [reply/username/userid]", "Unmute someone."],
        ["pin [reply]", "To pin any message."],
        ["unpin [reply]", "To unpin any message."],
    ],
)
