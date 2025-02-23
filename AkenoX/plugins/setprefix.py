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

from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *

from AkenoX import *
from AkenoX.core.sqlite_prefix import *


@RENDYDEV.user(
    prefix=["setprefix"],
    filters=(
        ~filters.scheduled
        & filters.me
        & ~filters.forwarded
    ),
    is_run=False
)
async def set_prefix(client: Client, message: Message):
    user_id = message.from_user.id
    if not message.text or len(message.text.split()) < 2:
        await message.reply_text("Usage: $setprefix custom emoji or None")
        return

    new_prefix_text = message.text.split(maxsplit=1)[1]

    if client.me.is_premium:
        if message.entities:
            for entity in message.entities:
                if entity.type == MessageEntityType.CUSTOM_EMOJI and entity.offset >= len(message.text.split()[0]) + 1:
                    custom_emoji_id = entity.custom_emoji_id
                    await set_prefix_in_db(user_id, custom_emoji_id)
                    await message.reply_text(f"Custom emoji prefix set to: <emoji id={custom_emoji_id}>🗿</emoji>")
                    return

    if new_prefix_text.lower() == "none":
        await set_prefix_in_db(user_id, "None")
        await message.reply_text("Prefix removed.")
        return
    try:
        emoji_or_symbol = new_prefix_text.encode("utf-8").decode("utf-8")
        await set_prefix_in_db(user_id, emoji_or_symbol)
        await message.reply_text(f"Prefix set to: {emoji_or_symbol}")
    except UnicodeDecodeError:
        await message.reply_text("Invalid emoji or symbol. Please try again.")
