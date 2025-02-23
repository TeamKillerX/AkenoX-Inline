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
import os
import time
from typing import TYPE_CHECKING

from pyrogram import *
from pyrogram.errors import *
from pyrogram.types import *

from AkenoX import *
from AkenoX.core.database import *
from AkenoX.core.helper_button import *
from AkenoX.core.logger import LOGS
from AkenoX.core.upload_file import *

from . import ReplyCheck

if TYPE_CHECKING:
    from AkenoX import assistant

@RENDYDEV.user(prefix=["rmbutton"], filters=(filters.me & ~filters.forwarded))
async def clear_button_from_db(client, message):
    try:
        me_user_id = RENDYDEV.client_me().me.id
        await db_client.set_env(f"USERAUTO2:{me_user_id}", None)
        await message.reply_text("Successfully delete button from database")
    except Exception as e:
        await message.reply_text(str(e))
    
@RENDYDEV.user(prefix=["send"], filters=(filters.me & ~filters.forwarded))
async def _save_message(client: assistant, message: Message):
    args = message.text.split("\n", 1)
    text = args[0].split(None, 1)[1] if len(args[0].split()) > 1 else None
    button_text = args[1].strip() if len(args) > 1 else None

    if not RENDYDEV.client_me().me.username:
        return await message.reply_text("Username required")

    reply_message = message.reply_to_message
    if reply_message:
        text = reply_message.text.html if reply_message.text else reply_message.caption.html if reply_message.caption else ""
    else:
        text = text or ""

    chat_id = None
    if button_text.startswith("@"):
        chat_id = button_text
    else:
        chat_id = message.chat.id

    reply_markup = None
    if message.reply_to_message and message.reply_to_message.reply_markup:
        reply_markup = message.reply_to_message.reply_markup
    else:
        try:
            reply_markup = parse_buttons(button_text)
        except AttributeError:
            reply_markup = None

    serialized_reply_markup = (
        serialize_reply_markup(reply_markup) if reply_markup else None
    )
    me_user_id = RENDYDEV.client_me().me.id
    media_type, file_id = None, None
    if reply_message:
        if reply_message.sticker:
            media_type = "sticker"
            file_id = reply_message.sticker.file_id
        elif reply_message.photo:
            media_type = "photo"
            file_id = (await assistant.send_photo(RENDYDEV.client_me().me.username, await reply_message.download())).photo.file_id
        elif reply_message.video:
            media_type = "video"
            file_id = (await assistant.send_video(RENDYDEV.client_me().me.username, await reply_message.download())).video.file_id
        elif reply_message.animation:
            media_type = "animation"
            file_id = (await assistant.send_animation(RENDYDEV.client_me().me.username, await reply_message.download())).animation.file_id
        elif reply_message.story:
            media = await reply_message.download()
            if media.endswith(".jpg"):
                media_type = "photo"
                file_id = (await assistant.send_photo(RENDYDEV.client_me().me.username, media)).photo.file_id
            else:
                media_type = "video"
                file_id = (await assistant.send_video(RENDYDEV.client_me().me.username, media)).video.file_id

    save_data = RENDYDEV.set_storage(
        file_id=file_id or "",
        caption=text,
        media_photo=media_type == "photo",
        is_sticker=media_type == "sticker",
        is_animation=media_type == "animation",
        media_video=media_type == "video",
        media_audio=False,
        input_text=text if not media_type else "",
        reply_markup=serialized_reply_markup,
    )
    await db_client.set_env(f"USERAUTO2:{me_user_id}", save_data)
    try:
        bot_username = (await assistant.get_me()).username
        inline = await RENDYDEV.client_me().get_inline_bot_results(
            bot=bot_username, query=f"userauto:{me_user_id}"
        )
        await RENDYDEV.client_me().send_inline_bot_result(
            chat_id,
            inline.query_id,
            inline.results[0].id,
            reply_to_message_id=ReplyCheck(message),
        )
    except Exception as e:
        LOGS.info(str(e))
