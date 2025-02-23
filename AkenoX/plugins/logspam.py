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

from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *

from AkenoX import *
from AkenoX.core.helper_button import *
from AkenoX.core.database import *
from AkenoX.core.logger import LOGS

TAGLOG_KEY = "TAGLOG"
TAG_LINK_KEY = "TAG_LINK"

@RENDYDEV.user(
    prefix=["taglog"],
    filters=(
        ~filters.scheduled
        & filters.me
        & ~filters.forwarded
    ),
    is_run=False
)
async def taglog_setting(_, message: Message):
    if len(message.command) < 2:
        status = await db_client.get_env(TAGLOG_KEY)
        text = "Enabled" if status else "Disabled"
        await message.reply_text(
            f"**Current TagLog Setting:** `{text}`\n\nTo change the setting give either `on` or `off` as argument.",
        )
        return

    cmd = message.command[1].lower().strip()
    if cmd == "on":
        await db_client.set_env(TAGLOG_KEY, True)
        await message.reply_text("**TagLog Enabled!**")
    elif cmd == "off":
        await db_client.set_env(TAGLOG_KEY, False)
        await message.reply_text("**TagLog Disabled!**")
    else:
        await message.reply_text("**Invalid Argument!**")


@RENDYDEV.user(is_log=True)
async def logs_channel(client, message):
    if not await db_client.get_env(TAGLOG_KEY):
        return
    if message.reply_to_message and message.reply_to_message.from_user:
        if message.reply_to_message.from_user.id != client.me.id:
            return

    if message.from_user.status == UserStatus.LONG_AGO:
        if message.reply_to_message.id:
            await message.reply_to_message.delete()
            return
    user_info = get_user_info(client, message)
    if message.entities:
        await process_entities(client, message, user_info)
    else:
        await process_no_entities(client, message, user_info)


def get_user_info(client, message):
    if message.chat.type == ChatType.PRIVATE:
        return f"""
        First Name: {message.from_user.first_name}
        UserID: `{message.from_user.id}`
        Username: {message.from_user.username if message.from_user else None}
        Text: `{message.text}`
        """
    else:
        return f"""
        Group Title: {message.chat.title}
        Group ID: {message.chat.id}

        First Name: {message.from_user.first_name}
        UserID: `{message.from_user.id}`
        Username: {message.from_user.username if message.from_user else None}
        Text: `{message.text}`
        """


async def process_entities(client, message, user_info):
    for entity in message.entities:
        if entity.type == MessageEntityType.MENTION:
            username = message.text[entity.offset:entity.offset + entity.length]
            if username == f"@{client.me.username}":
                await handle_tag(client, message, user_info)


async def process_no_entities(client, message, user_info):
    await handle_tag(client, message, user_info)

def getchat_button(user_id: int, message):
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
                    url=message.link
                )
            ]
        ]
    )

async def handle_tag(client, message, user_info):
    media_type, file_id = None, None
    reply_markup = None
    username_me = RENDYDEV.client_me().me.username
    if not username_me:
        return
    if message.sticker:
        media_type = "sticker"
        file_id = message.sticker.file_id
        reply_markup = getchat_button(message.from_user.id, message)
    if message.text:
        reply_markup = getchat_button(message.from_user.id, message)
    elif message.photo:
        media_type = "photo"
        file_id = (await assistant.send_photo(username_me, await message.download())).photo.file_id
        reply_markup = getchat_button(message.from_user.id, message)
    elif message.video:
        media_type = "video"
        file_id = (await assistant.send_video(username_me, await message.download())).video.file_id
        reply_markup = getchat_button(message.from_user.id, message)
    elif message.animation:
        media_type = "animation"
        file_id = (await assistant.send_animation(username_me, await message.download())).animation.file_id
        reply_markup = getchat_button(message.from_user.id, message)
    elif message.story:
        media = await message.download()
        if media.endswith(".jpg"):
            media_type = "photo"
            file_id = (await assistant.send_photo(username_me, media)).photo.file_id
            reply_markup = getchat_button(message.from_user.id, message)
        else:
            media_type = "video"
            file_id = (await assistant.send_video(username_me, media)).video.file_id
            reply_markup = getchat_button(message.from_user.id, message)

    serialized_reply_markup = (
        serialize_reply_markup(reply_markup) if reply_markup else None
    )
    tag_data = RENDYDEV.set_storage(
        file_id=file_id or "",
        message_link=message.link,
        user_id=message.from_user.id,
        caption=user_info,
        media_photo=media_type == "photo",
        is_sticker=media_type == "sticker",
        is_animation=media_type == "animation",
        media_video=media_type == "video",
        media_audio=False,
        input_text=user_info if not media_type else "",
        reply_markup=serialized_reply_markup
    )
    await db_client.set_env(f"USERAUTO2:{client.me.id}", tag_data)
    bot_username = (await assistant.get_me()).username
    try:
        oh = await client.get_inline_bot_results(bot=bot_username, query=f"userauto:{client.me.id}")
        await client.send_inline_bot_result(
            LOG_CHANNEL,
            oh.query_id,
            oh.results[0].id,
            reply_to_message_id=None
        )
    except Exception as e:
        LOGS.info(f"Failed to send inline bot result: {str(e)}")
