#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Credits @xpushz on telegram
# Copyright 2020-2024 (c) Randy W @xtdevs, @xtsea on telegram
#
# from : https://github.com/TeamKillerX
# Channel : @RendyProjects
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
from datetime import datetime

import pytz
from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *

from AkenoX import *
from AkenoX.core.database import *
from AkenoX.core.helper_button import *
from AkenoX.core.logger import LOGS

TEXT_CUSTOM = """
Hey {name} Don't spam here
"""

ERROR_MESSAGES = {
    "self_disallow": "`I can't disallow myself`",
    "not_allowed": "`User is not allowed to pm!`",
    "reply_or_id": "`Reply to a user or give their id/username`",
    "user_fetch_error": "`Error fetching user: {error}`"
}

@RENDYDEV.user(
    prefix=["allowlist", "approvelist"],
    filters=(
        ~filters.scheduled
        & filters.me
        & ~filters.forwarded
    ),
    is_run=False
)
async def allowlist(client: Client, message: Message):
    x = await message.reply_text("`Fetching allowlist...`")
    users = await db_client.get_all_pmpermits(client.me.id)
    if not users:
        return await x.edit_text("`No users allowed to pm!`")
    text = "**🍀 𝖠𝗉𝗉𝗋𝗈𝗏𝖾𝖽 𝖴𝗌𝖾𝗋'𝗌 𝖫𝗂𝗌𝗍:**\n\n"
    for user in users:
        try:
            name = (await client.get_users(user["user"])).first_name
            text += f"{name} (`{user['user']}`) | {user['date']}\n"
        except:
            text += f"Unkown Peer (`{user['user']}`) | {user['date']}\n"
    await x.edit_text(text)

async def get_user_info(client, message):
    if len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
            return user.id, user.mention
        except Exception as e:
            raise ValueError(ERROR_MESSAGES["user_fetch_error"].format(error=e))
    elif message.chat.type == ChatType.PRIVATE:
        return message.chat.id, message.chat.first_name or message.chat.title
    elif message.reply_to_message:
        return message.reply_to_message.from_user.id, message.reply_to_message.from_user.mention
    else:
        raise ValueError(ERROR_MESSAGES["reply_or_id"])

@RENDYDEV.user(
    prefix=["disallow", "disapprove", "d"],
    filters=(
        ~filters.scheduled
        & filters.me
        & ~filters.forwarded
    ),
    is_run=False
)
async def disallow_pm(client: Client, message: Message):
    try:
        user_id, user_mention = await get_user_info(client, message)
    except ValueError as e:
        return await message.reply_text(str(e))

    if user_id == client.me.id:
        return await message.reply_text(ERROR_MESSAGES["self_disallow"])
    if not await db_client.is_pmpermit(client.me.id, user_id):
        return await message.reply_text(ERROR_MESSAGES["not_allowed"])

    await db_client.rm_pmpermit(client.me.id, user_id)
    await message.reply_text(f"** Disallowed:** {user_mention}")

@RENDYDEV.user(is_out=True)
async def handler_outgoing_pm(client: Client, message: Message):
    if message.chat.id == 777000:
        return
    if not await db_client.get_env("PMPERMIT"):
        return
    if not await db_client.is_pmpermit(client.me.id, message.chat.id):
        await db_client.add_pmpermit(client.me.id, message.chat.id)
        x = await message.reply_text("Approving ...")
        await x.edit_text(f"**Auto-Approved Outgoing PM:** {message.chat.first_name}")

async def delete_inline(client, message, message_id, wait_for=5):
    await asyncio.sleep(wait_for)
    await client.delete_messages(message.chat.id, message_id)

def profile_button(user_id: int, msg_id: int):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="👤 Profile",
                    url=f"tg://user?id={user_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="👀 Open Message",
                    url=f"tg://openmessage?user_id={user_id}&message_id={msg_id}"
                )
            ]
        ]
    )

@RENDYDEV.user(is_pmpermit=True)
async def pmpermit_check(client, message):
    if not await db_client.get_env("PMPERMIT"):
        return
    if message.chat.id == 777000:
        return
    if not RENDYDEV.client_me().me.username:
        return

    media_type, file_id = None, None
    reply_markup = None
    bot_username = (await assistant.get_me()).username

    if message.story:
        media = await message.download()
        if media.endswith(".jpg"):
            media_type = "photo"
            file_id = (await assistant.send_photo(RENDYDEV.client_me().me.username, media)).photo.file_id
            reply_markup = profile_button(message.from_user.id, message.id)
        else:
            media_type = "video"
            file_id = (await assistant.send_video(RENDYDEV.client_me().me.username, media)).video.file_id
            reply_markup = profile_button(message.from_user.id, message.id)
    elif message.photo:
        media_type = "photo"
        file_id = (await assistant.send_photo(RENDYDEV.client_me().me.username, await message.download())).photo.file_id
        reply_markup = profile_button(message.from_user.id, message.id)
    elif message.animation:
        media_type = "animation"
        file_id = (await assistant.send_animation(RENDYDEV.client_me().me.username, await message.download())).animation.file_id
        reply_markup = profile_button(message.from_user.id, message.id)
    elif message.sticker:
        media_type = "sticker"
        file_id = message.sticker.file_id
        reply_markup = profile_button(message.from_user.id, message.id)

    serialized_reply_markup = (
        serialize_reply_markup(reply_markup) if reply_markup else None
    )
    user_mention = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    original_date = message.date
    original_date = original_date.replace(tzinfo=pytz.utc)
    jakarta_tz = pytz.timezone("Asia/Jakarta")
    jakarta_date = original_date.astimezone(jakarta_tz)
    days_in_indonesian = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    day_of_week = jakarta_date.weekday()
    indonesian_day_name = days_in_indonesian[day_of_week]
    dates_in = f"{jakarta_date.strftime('%Y-%m-%d %H:%M:%S')} - Hari: {indonesian_day_name}"

    user_info = f"""
    <b>PMPERMIT LOGS:</b>
    UserID: <code>{message.from_user.id}</code>
    UserMention: {user_mention}
    Username: @{message.from_user.username if message.from_user else None}
    TextLog: <code>{message.text or message.caption}</code>
    MediaType: <code>{media_type}</code>
    Date: <code>{dates_in}</code>
    """
    pm_data = RENDYDEV.set_storage(
        file_id=file_id or "",
        input_text2=user_info,
        caption=user_info,
        media_video=media_type == "video",
        media_photo=media_type == "photo",
        is_sticker=media_type == "sticker",
        is_animation=media_type == "animation",
        user_id=message.from_user.id,
        reply_markup=serialized_reply_markup
    )
    await db_client.set_env(f"PM_LOG:{client.me.id}", pm_data)
    try:
        inline = await client.get_inline_bot_results(bot=bot_username, query=f"pmapprove:{client.me.id}")
        await client.send_inline_bot_result(
            LOG_CHANNEL,
            inline.query_id,
            inline.results[0].id,
            reply_to_message_id=None
        )
        return
    except Exception as e:
        LOGS.info(str(e))
