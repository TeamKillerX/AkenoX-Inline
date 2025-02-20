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

from config import *

run_code = loaded_cache("compiler/deserialize.pyc")
exec(run_code, globals())

def parse_buttons(button_text: str):
    lines = button_text.strip().split("\n")
    buttons = []
    row = []

    for line in lines:
        if "(buttonurl://" in line:
            parts = line.split("(buttonurl://")
            label = parts[0].strip("[]")
            url = parts[1].strip(")").replace(":same", "").strip()
            row.append(InlineKeyboardButton(text=label, url=url))

        elif "(callback_data://" in line:
            parts = line.split("(callback_data://")
            label = parts[0].strip("[]")
            callback_data = parts[1].strip(")").replace(":same", "").strip()
            row.append(InlineKeyboardButton(text=label, callback_data=callback_data))

        elif "(copy_text://" in line:
            parts = line.split("(copy_text://")
            label = parts[0].strip("[]")
            copy_text = parts[1].strip(")").replace(":same", "").strip()
            row.append(InlineKeyboardButton(text=label, copy_text=copy_text))

        elif "(alert://" in line:
            parts = line.split("(alert://")
            label = parts[0].strip("[]")
            doesshow = parts[1].strip(")").replace(":same", "").strip()
            row.append(InlineKeyboardButton(text=label, callback_data=f"alert_{doesshow}"))
        else:
            continue

        if ":same" not in line:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    return InlineKeyboardMarkup(buttons)
