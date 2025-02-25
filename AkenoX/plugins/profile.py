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
import time

from pyrogram import *
from pyrogram.types import *

from AkenoX import *

from . import ReplyCheck


@RENDYDEV.user(
    prefix=["block"],
    filters=(
        ~filters.scheduled
        & filters.me
        & ~filters.forwarded
    ),
    is_run=False
)
async def block_user_func(client, message):
    try:
        user_id = await extract_user(message)
    except AttributeError:
        return
    u = await message.reply_text("`Processing . . .`")
    if not user_id:
        return await u.edit_text(
            "Provide User ID/Username or reply to user message to block."
        )
    if user_id == client.me.id:
        return await u.edit_text("i can't block.")
    if user_id == 6477856957:
        return await u.edit_text("i can't block.")
    await client.block_user(user_id)
    umention = (await client.get_users(user_id)).mention
    await u.edit_text(f"**Successfully Blocked** {umention}")

@RENDYDEV.user(
    prefix=["unblock"],
    filters=(
        ~filters.scheduled
        & filters.me
        & ~filters.forwarded
    ),
    is_run=False
)
async def unblock_user_func(client: Client, message: Message):
    user_id = await extract_user(message)
    u = await message.reply_text("`Processing . . .`")
    if not user_id:
        return await u.edit_text(
            "Provide User ID/Username or reply to user's message to unblock.."
        )
    if user_id == client.me.id:
        return await u.edit_text("i can't block.")
    await client.unblock_user(user_id)
    umention = (await client.get_users(user_id)).mention
    await message.edit(f"**Successfully Unblocked** {umention}")

@RENDYDEV.user(
    prefix=["setname"],
    filters=(
        ~filters.scheduled
        & filters.me
        & ~filters.forwarded
    ),
    is_run=False
)
async def setname(client, message):
    u = await message.reply_text("`Processing . . .`")
    if len(message.command) == 1:
        return await u.edit_text(
            "Provide text to set as your telegram name"
        )
    elif len(message.command) > 1:
        name = message.text.split(None, 1)[1]
        try:
            await client.update_profile(first_name=name)
            await u.edit_text(f"**Successfully Changed Your Telegram Name To** `{name}`")
        except Exception as e:
            await u.edit_text(f"**ERROR:** `{e}`")
    else:
        return await u.edit_text(
            "Provide text to set as your telegram name."
        )

@RENDYDEV.user(
    prefix=["setbio"],
    filters=(
        ~filters.scheduled
        & filters.me
        & ~filters.forwarded
    ),
    is_run=False
)
async def set_bio(client, message):
    u = await message.reply_text("`Processing . . .`")
    if len(message.command) == 1:
        return await u.edit_text("Berikan teks untuk ditetapkan sebagai bio.")
    elif len(message.command) > 1:
        bio = message.text.split(None, 1)[1]
        try:
            await client.update_profile(bio=bio)
            await u.edit_text(f"**Successfully Changed your BIO to** `{bio}`")
        except Exception as e:
            await u.edit_text(f"**ERROR:** `{e}`")
    else:
        return await u.edit_text("Provide text to set as bio.")

@RENDYDEV.user(
    prefix=["setpfp"],
    filters=(
        ~filters.scheduled
        & filters.me
        & ~filters.forwarded
    ),
    is_run=False
)
async def set_pfp(client, message):
    replied = message.reply_to_message
    if (
        replied
        and replied.media
        and (
            replied.photo
            or (replied.document and "image" in replied.document.mime_type)
        )
    ):
        profile_photo = await client.download_media(message=replied)
        await client.set_profile_photo(profile_photo)
        await message.edit_text("**Your Profile Photo Has Been Changed Successfully.**")
    else:
        await message.edit_text(
            "`Reply to any photo to set as profile picture`"
        )
        await asyncio.sleep(3)
        await message.delete()
