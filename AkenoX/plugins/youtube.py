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

import os
from typing import TYPE_CHECKING

import requests
from pyrogram.errors import *
from pyrogram.types import *

from AkenoX import *
from AkenoX.core.helper_button import *
from AkenoX.core.logger import LOGS
from AkenoX.core.scripts import progress
from AkenoX.plugins.libso.cybersecurity_hdr import *

from . import ReplyCheck

if TYPE_CHECKING:
    from AkenoX import assistant

from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL


def secs_to_mins(secs: int) -> str:
    mins, secs = divmod(secs, 60)
    return f"{mins}:{secs}"

async def input_user(message) -> str:
    if len(message.command) < 2:
        output = ""
    else:
        try:
            output = message.text.split(" ", 1)[1].strip() or ""
        except IndexError:
            output = ""
    return output

def button_inline(user_id: int, url: str):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🔗 Link YouTube",
                    url=url
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🥶 Owner",
                    user_id=user_id
                )
            ]
        ]
    )

@RENDYDEV.user(
    prefix=["ytv"],
    filters=(
        ~filters.scheduled
        & filters.me
        & ~filters.forwarded
    ),
    is_run=False,
    limit=3,
    time_frame=10
)
async def ytvideo(client: assistant, message):
    reply_markup = None
    if len(message.command) < 2:
        return await message.reply_text(
            "Give a valid youtube link to download video."
        )
    query = await input_user(message)
    pro = await message.reply_text("Checking ...")
    username_me = RENDYDEV.client_me().me.username
    if not username_me:
        return await message.reply_text("?")
    status, url = YoutubeDriver.check_url(query)
    if not status:
        return await pro.edit_text(url)
    await pro.edit_text(f"__Downloading video ...__")
    try:
        with YoutubeDL(YoutubeDriver.video_options()) as ytdl:
            yt_data = ytdl.extract_info(url, True)
            yt_file = yt_data["id"]

        upload_text = f"**𝖴𝗉𝗅𝗈𝖺𝖽𝗂𝗇𝗀 Video ...** \n\n**𝖳𝗂𝗍𝗅𝖾:** `{yt_data['title'][:50]}`\n**𝖢𝗁𝖺𝗇𝗇𝖾𝗅:** `{yt_data['channel']}`"
        await pro.edit_text(upload_text)
        response = requests.get(f"https://i.ytimg.com/vi/{yt_data['id']}/hqdefault.jpg")
        with open(f"{yt_file}.jpg", "wb") as f:
            f.write(response.content)
        results = await assistant.send_video(
            username_me,
            f"{yt_file}.mp4",
            caption=f"**🎧 𝖳𝗂𝗍𝗅𝖾:** {yt_data['title']} \n\n**👀 𝖵𝗂𝖾𝗐𝗌:** `{yt_data['view_count']}` \n**⌛ 𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇:** `{secs_to_mins(int(yt_data['duration']))}`",
            duration=int(yt_data["duration"]),
            thumb=f"{yt_file}.jpg",
            progress=progress,
            progress_args=(
                pro,
                time.time(),
                upload_text,
            ),
        )
        file_id = results.video.file_id
        reply_markup = button_inline(RENDYDEV.client_me().me.id, query)
        serialized_reply_markup = (
            serialize_reply_markup(reply_markup) if reply_markup else None
        )
        save_data = RENDYDEV.set_storage(
            file_id=file_id or "",
            caption=f"**🎧 𝖳𝗂𝗍𝗅𝖾:** {yt_data['title']} \n\n**👀 𝖵𝗂𝖾𝗐𝗌:** `{yt_data['view_count']}` \n**⌛ 𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇:** `{secs_to_mins(int(yt_data['duration']))}`",
            media_photo=False,
            is_sticker=False,
            is_animation=False,
            media_video=True,
            media_audio=False,
            input_text="",
            reply_markup=serialized_reply_markup,
        )
        await db_client.set_env(f"USERAUTO2:{client.me.id}", save_data)
        bot_username = (await assistant.get_me()).username
        oh = await client.get_inline_bot_results(bot=bot_username, query=f"userauto:{client.me.id}")
        await client.send_inline_bot_result(
            message.chat.id,
            oh.query_id,
            oh.results[0].id,
            reply_to_message_id=ReplyCheck(message)
        )
        await pro.delete()
    except Exception as e:
        return await pro.edit_text(f"**🍀 Video not Downloaded:** `{e}`")
    try:
        os.remove(f"{yt_file}.jpg")
        os.remove(f"{yt_file}.mp4")
    except:
        pass
