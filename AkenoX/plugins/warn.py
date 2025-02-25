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
from pyrogram.types import *

from AkenoX import *
from AkenoX.core.database import *

from . import ReplyCheck

@RENDYDEV.user(
    prefix=["warn", "dwarn"],
    filters=(
        ~filters.scheduled
        & filters.me
        & ~filters.forwarded
    ),
    is_run=False
)
async def warn_user(client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    chat_id = message.chat.id
    is_unsafe = False
    if not user_id:
        return await message.reply_text("I can't find that user.")
    if user_id == client.me.id:
        return await message.reply_text(
            "I can't warn myself, i can leave if you want."
        )
    if user_id == 6477856957:
      return await message.reply_text(
            "I can't warn myself, i can leave if you want."
        )
    if user_id in (await RENDYDEV.list_admins(client, message.chat.id)):
        return await message.reply_text("I can't ban an admin, You know the rules, so do i.")
    user = await client.get_users(user_id)
    warns = await db_client.get_env(f"USER_WARN:{user_id}")
    mention = user.mention
    if warns:
        warns = warns["warn_count"]["warns"]
    else:
        warns = 0
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if warns >= 2:
        mode = await db_client.get_env(f"SETTING_WARN:{client.me.id}")
        if mode == "ban":
            await message.chat.ban_member(user_id)
            await message.reply_text(
                f"Number of warns of {mention} exceeded, BANNED!"
            )
            await db_client.rm_env(f"USER_WARN:{user_id}")
            return
        if mode == "kick":
            await message.chat.ban_member(user_id)
            await asyncio.sleep(1.5)
            await message.chat.unban_member(user_id)
            await message.reply_text(
                f"Number of warns of {mention} exceeded, KICKED!"
            )
            await db_client.rm_env(f"USER_WARN:{user_id}")
            return
        if mode == "mute":
            await message.chat.restrict_member(user_id, permissions=ChatPermissions())
            await message.reply_text(
                f"Number of warns of {mention} exceeded, MUTED!"
            )
            await db_client.rm_env(f"USER_WARN:{user_id}")
            return
        await message.chat.ban_member(user_id)
        await message.reply_text(
            f"Number of warns of {mention} exceeded, BANNED!"
        )
    else:
        warn = {"warns": warns + 1}
        msg = f"""
**Warned User:** {mention}
**Warned By:** {message.from_user.mention if message.from_user else 'Anon'}
**Reason:** {reason or 'No Reason Provided.'}
**Warns:** {warns + 1}/3
"""
        data_warn = RENDYDEV.set_storage(
            input_text=msg,
            chat_id=chat_id,
            warn_user_id=user_id,
            warn_count=warn
        )
        await db_client.set_env(f"USER_WARN:{user_id}", data_warn)
        bot_username = (await assistant.get_me()).username
        try:
            oh = await client.get_inline_bot_results(bot=bot_username, query=f"warnpro:{user_id}")
            await client.send_inline_bot_result(
                message.chat.id,
                oh.query_id,
                oh.results[0].id,
                reply_to_message_id=ReplyCheck(message)
            )
        except Exception as e:
            await message.reply_text(f"Error : {e}")

@RENDYDEV.user(
    prefix=["rmwarns", "rmwarn"],
    filters=(
        ~filters.scheduled
        & filters.me
        & ~filters.forwarded
    ),
    is_run=False
)
async def cmd_remove_warn(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to a message to remove a user's warnings."
        )
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    warns = await db_client.get_env(f"USER_WARN:{user_id}")
    if warns:
        warns = warns["warn_count"]["warns"]
    if warns == 0 or not warns:
        await message.reply_text(f"{mention} have no warnings.")
    else:
        await db_client.rm_env(f"USER_WARN:{user_id}")
        await message.reply_text(f"Removed warnings of {mention}.")

@RENDYDEV.user(
    prefix=["warnmode"],
    filters=(
        ~filters.scheduled
        & filters.me
        & ~filters.forwarded
    ),
    is_run=False
)
async def mode_warns(client, message: Message):
    if len(message.command) < 2:
        mode = await db_client.get_env(f"SETTING_WARN:{client.me.id}")
        setting_ = mode if mode else "ban"
        return await message.reply_text(
            f"**Current Warn Mode Setting:** `{setting_}`"
        )
    
    cmd = message.command[1].lower().strip()
    if cmd in ["kick", "ban", "mute"]:
        await db_client.set_env(f"SETTING_WARN:{client.me.id}", cmd)
        await message.reply_text(f"**Warn Mode set to {cmd}!**")
    else:
        await message.reply_text("**Invalid Command**")

@RENDYDEV.user(
    prefix=["warns"],
    filters=(
        ~filters.scheduled
        & filters.me
        & ~filters.forwarded
    ),
    is_run=False
)
async def check_warns(client, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("I can't find that user.")
    warns = await db_client.get_env(f"USER_WARN:{user_id}")
    mention = (await client.get_users(user_id)).mention
    if warns:
        warns = warns["warn_count"]["warns"]
    else:
        return await message.reply_text(f"{mention} has no warnings.")
    return await message.reply_text(f"{mention} has {warns}/3 warnings.")
