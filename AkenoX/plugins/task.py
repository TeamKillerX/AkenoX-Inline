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
from pyrogram.types import *

from AkenoX import *
from AkenoX import running_tasks


@RENDYDEV.user(prefix="stop_task", filters=(filters.me & ~filters.forwarded))
async def stop_task(client, message):
    global running_tasks
    try:
        command = message.text.split(" ", maxsplit=1)
        if len(command) < 2:
            return await message.reply("❗ Please provide a valid task ID to stop.")

        task_id = command[1].strip()
        if task_id in running_tasks:
            task = running_tasks.pop(task_id)
            task.cancel()
            await message.reply(f"✅ Task `{task_id}` has been stopped successfully.")
        else:
            await message.reply(f"❌ No active task found with ID `{task_id}`.")
    except Exception as e:
        await message.reply(f"❗ Error: {str(e)}")

@RENDYDEV.user(prefix="tasklist", filters=(filters.me & ~filters.forwarded))
async def tasklist_handler(client, message):
    global running_tasks
    if not running_tasks:
        return await message.reply_text("✅ No active tasks.")
    tasks_info = "\n".join(
        [f"• Task ID: `{task_id}`" for task_id in running_tasks]
    )
    await message.reply_text(f"**Active Tasks:**\n{tasks_info}")
