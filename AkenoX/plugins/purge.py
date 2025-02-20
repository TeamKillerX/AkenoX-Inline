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

from pyrogram import Client, filters
from pyrogram.types import Message 
from pyrogram import *
from pyrogram.types import *

from AkenoX import *

@RENDYDEV.user(
    prefix=["del"],
    filters=(
        ~filters.scheduled
        & filters.me
        & ~filters.forwarded
    ),
    is_run=False
)
async def del_user(_, message: Message):
    rep = message.reply_to_message
    await message.delete()
    await rep.delete()

@RENDYDEV.user(
    prefix=["purgeme"],
    filters=(
        ~filters.scheduled
        & filters.me
        & ~filters.forwarded
    ),
    is_run=False
)
async def purge_me_func(client: Client, message: Message):
    if len(message.command) != 2:
        return await message.delete()
    n = (
        message.reply_to_message
        if message.reply_to_message
        else message.text.split(None, 1)[1].strip()
    )
    if not n.isnumeric():
        return await message.reply_text("Invalid Bruhhh????")
    n = int(n)
    if n < 1:
        return await message.reply_text("Bruhhhh number 0?")
    chat_id = message.chat.id
    message_ids = [
        m.id
        async for m in client.search_messages(
            chat_id,
            from_user=int(message.from_user.id),
            limit=n,
        )
    ]
    if not message_ids:
        return await message.reply_text("No messages found.")
    to_delete = [message_ids[i : i + 999] for i in range(0, len(message_ids), 999)]
    for hundred_messages_or_less in to_delete:
        await client.delete_messages(
            chat_id=chat_id,
            message_ids=hundred_messages_or_less,
            revoke=True,
        )
        mmk = await message.reply_text(f"{n} Successfully fast purgeme")
        await asyncio.sleep(2)
        await mmk.delete()

@RENDYDEV.user(
    prefix=["purge"],
    filters=(
        ~filters.scheduled
        & filters.me
        & ~filters.forwarded
    ),
    is_run=False
)
async def purgefunc(client: Client, message: Message):
    await message.delete()
    if not message.reply_to_message:
        return await message.reply_text("Reply to message purge.")
    chat_id = message.chat.id
    message_ids = []
    for message_id in range(
        message.reply_to_message.id,
        message.id,
    ):
        message_ids.append(message_id)
        if len(message_ids) == 100:
            await client.delete_messages(
                chat_id=chat_id,
                message_ids=message_ids,
                revoke=True,
            )
            message_ids = []
    if len(message_ids) > 0:
        await client.delete_messages(
            chat_id=chat_id,
            message_ids=message_ids,
            revoke=True,
        )

RENDYDEV.buttons(
    "purge",
    [
        ["del", "to delete someone's message."],
        ["purge", "reply to all messages from your replied."],
        ["purgeme [count]", "to delete your messages only."],
    ],
)
