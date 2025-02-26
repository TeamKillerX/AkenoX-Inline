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
import inspect
import io
import logging
import os
import re
import subprocess
import sys
import traceback
import uuid
from asyncio import sleep
from contextlib import suppress
from io import BytesIO, StringIO
from random import randint
from typing import Optional

import aiohttp
import akenoai as at
import pyrogram
import requests
from box import Box
from meval import meval
from pyrogram import *
from pyrogram.enums import *
from pyrogram.raw import *
from pyrogram.raw.types import *
from pyrogram.types import *

from AkenoX import *
from AkenoX import running_tasks
from AkenoX.core.database import *
from AkenoX.core.logger import *


@RENDYDEV.user(
    prefix=["ev"],
    filters=(
        ~filters.scheduled
        & filters.me
        & ~filters.forwarded
    ),
    is_run=False
)
async def evaluation_cmd(client, message):
    global running_tasks
    user_id = message.from_user.id if message.from_user else None
    task_id = uuid.uuid4().hex[:8]
    status_message = await message.reply("__Processing eval pyrogram...__")
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await status_message.edit("__No evaluate message!__")

    async def execute_eval():
        old_stderr = sys.stderr
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()
        redirected_error = sys.stderr = io.StringIO()
        stdout, stderr, exc = None, None, None
        variables = {
            "client": client,
            "pyrogram": pyrogram,
            "c": client,
            "m": message,
            "message": message,
            "r": message.reply_to_message,
            "chat": message.chat.id if message.chat else None,
            "user": message.from_user,
            "to_video": message.reply_video,
            "to_photo": message.reply_photo,
            "to_text": message.reply_text,
            "types": pyrogram.types,
            "raw_types": pyrogram.raw.types,
            "raw": pyrogram.raw,
            "assistant": assistant,
            "rendydev": RENDYDEV,
            "libso": inspect.getsource,
            "uhelp": help,
            "to_obj": Box,
            "db_client": db_client,
            "os": os,
            "lsopen": os.popen,
            "fasthttp": requests
        }
        try:
            result = await meval(cmd, globals(), **variables)
        except asyncio.CancelledError:
            await status_message.edit("__Task was cancelled!__")
            return
        except Exception:
            exc = traceback.format_exc()
        finally:
            stdout = redirected_output.getvalue().strip()
            stderr = redirected_error.getvalue().strip()
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        evaluation = exc or stderr or str(result) or "Success"
        final_output = f"**OUTPUT**:\n<pre language=''>{evaluation.strip()}</pre>"
        eval_data = {
            "input_text": evaluation.strip(),
            "chat_id": message.chat.id if message.chat else None,
            "message_id": message.id + 2,
        }
        await db_client.set_env(f"EVAL:{client.me.id}", eval_data)
        if len(final_output) > 4096:
            with open("eval.txt", "w+", encoding="utf8") as out_file:
                out_file.write(final_output)
            await status_message.reply_document(
                document="eval.txt",
                disable_notification=True,
            )
            os.remove("eval.txt")
        else:
            bot_username = (await assistant.get_me()).username
            try:
                inline = await client.get_inline_bot_results(bot=bot_username, query=f"eval_{client.me.id}")
                await asyncio.gather(
                    status_message.delete(),
                    client.send_inline_bot_result(
                        message.chat.id,
                        inline.query_id,
                        inline.results[0].id,
                        reply_to_message_id=ReplyCheck(message)
                    )
                )
            except Exception as e:
                await status_message.edit_text(str(e))

    task = asyncio.create_task(execute_eval())
    running_tasks[task_id] = task
    await status_message.edit_text(f" Task Started \nTask ID: `{task_id}`")
    try:
        await task
    finally:
        running_tasks.pop(task_id, None)

@RENDYDEV.user(
    prefix=["sh"],
    filters=(
        ~filters.scheduled
        & filters.me
        & ~filters.forwarded
    ),
    is_run=False
)
async def shell_cmd(client, message):
    global running_tasks
    user_id = message.from_user.id if message.from_user else None
    task_id = uuid.uuid4().hex[:8]
    status_message = await message.reply("__Processing shell command...__")

    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await status_message.edit("__No command provided!__")

    async def execute_shell():
        process = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        output = (stdout.decode().strip() or stderr.decode().strip() or "Success")

        final_output = f"**OUTPUT**:\n<pre language=''>{output}</pre>"

        await db_client.set_env(f"SH:{client.me.id}", {
            "input_text": output,
            "chat_id": message.chat.id,
            "message_id": message.id + 2,
        })

        if len(final_output) > 4096:
            with open("shell_output.txt", "w+", encoding="utf8") as out_file:
                out_file.write(final_output)
            await status_message.reply_document(
                document="shell_output.txt",
                disable_notification=True,
            )
            os.remove("shell_output.txt")
        else:
            bot_username = (await assistant.get_me()).username
            try:
                inline = await client.get_inline_bot_results(bot=bot_username, query=f"sh_{client.me.id}")
                await asyncio.gather(
                    status_message.delete(),
                    client.send_inline_bot_result(
                        message.chat.id,
                        inline.query_id,
                        inline.results[0].id,
                        reply_to_message_id=ReplyCheck(message)
                    )
                )
            except Exception as e:
                await status_message.edit_text(str(e))

    task = asyncio.create_task(execute_shell())
    running_tasks[task_id] = task
    await status_message.edit_text(f"**Task Started**\nTask ID: `{task_id}`")
    try:
        await task
    finally:
        running_tasks.pop(task_id, None)
