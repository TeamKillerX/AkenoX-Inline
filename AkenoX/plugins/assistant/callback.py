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

import config

run_code = config.loaded_cache("compiler/callback_mod.pyc")
exec(run_code, globals())

@RENDYDEV.callback(regex="^alert_")
async def _alert(client: Client, cb: CallbackQuery):
    query = cb.data.split("_", 1)

    if len(query) > 1:
        action = query[1]
        if action == "show":
            await cb.answer("This is a show alert!", show_alert=True)
        elif action == "pop":
            await cb.answer("This is a pop alert!", show_alert=False)
    else:
        await cb.answer("Invalid alert action.", show_alert=False)

@RENDYDEV.callback(regex="^block:")
async def block_cb(client, callback_query):
    data = user_callback(callback_query, access=":")
    user_id = data[1]
    if not callback_query.from_user.id in RENDYDEV.devlist():
        return await callback_query.answer("Not allowed this", True)
    try:
        await RENDYDEV.client_me().block_user(str(user_id))
        await callback_query.edit_message_text(f"**Successfully Blocked**")
    except Exception as e:
        LOGS.info(str(e))
        await callback_query.edit_message_text(f"<b>❌ ERROR:</b> <code>{e}</code>")

@RENDYDEV.callback(regex="^close_")
async def close_cb(client, callback_query):
    data = user_callback(callback_query, access="_")
    _, chat_id, message_id = data
    if not callback_query.from_user.id in RENDYDEV.devlist():
        return await callback_query.answer("Not allowed this", True)
    try:
        await RENDYDEV.client_me().delete_messages(
            int(chat_id),
            int(message_id)
        )
    except Exception as e:
        LOGS.info(str(e))
        await callback_query.edit_message_text(f"<b>❌ ERROR:</b> <code>{e}</code>")

@RENDYDEV.callback(regex="^del_")
async def del_cb(client, callback_query):
    data = user_callback(callback_query, access="_")
    _, chat_id, message_id = data
    if not callback_query.from_user.id in [RENDYDEV.devlist(), RENDYDEV.allowed_users()]:
        return await callback_query.answer("Not allowed this", True)
    try:
        await RENDYDEV.client_me().delete_messages(
            int(chat_id),
            int(message_id)
        )
    except Exception as e:
        LOGS.info(str(e))
        await callback_query.edit_message_text(f"<b>❌ ERROR:</b> <code>{e}</code>")

@RENDYDEV.callback(regex="^unban_")
@cb_wrapper
async def unbanned_cb(_, callback_query):
    data = user_callback(callback_query, access="_")
    _, chat_id, user_id = data
    try:
        await RENDYDEV.client_me().unban_chat_member(int(chat_id), str(user_id))
        await callback_query.edit_message_text("<b>✅ Unbanned!")
    except Exception as error:
        LOGS.info(str(error))
        await callback_query.edit_message_text(f"<b>❌ ERROR:</b> <code>{error}</code>")


@RENDYDEV.callback(regex="^unmute_")
@cb_wrapper
async def unmute_cb(_, callback_query: CallbackQuery):
    data = user_callback(callback_query, access="_")
    _, chat_id, user_id = data
    try:
        await RENDYDEV.client_me().restrict_chat_member(
            int(chat_id),
            str(user_id),
            permissions=RENDYDEV.unmute_permissions()
        )
        await callback_query.edit_message_text(
            "<b>✅ Unmuted!",
        )
    except Exception as error:
        LOGS.info(str(error))
        await callback_query.edit_message_text(f"<b>❌ ERROR:</b> <code>{error}</code>")

@RENDYDEV.callback(updates=True)
async def _callbacks(_, callback_query: CallbackQuery):
    query = callback_query.data.lower()
    user_id = RENDYDEV.client_me().me.id
    prefix = await get_prefix(user_id)
    new_get_text = f"**AkenoX-Inline**\n\nPrefix: {prefix}\n"
    bot_me = await RENDYDEV.only_bot().get_me()
    if query == "helper":
        buttons = paginate_help(0, CMD_HELP, "helpme")
        await assistant.edit_inline_text(
            callback_query.inline_message_id,
            new_get_text,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    elif query == "make_basic_button":
        try:
            bttn = paginate_help(0, CMD_HELP, "helpme")
            await assistant.edit_inline_text(
                callback_query.inline_message_id,
                new_get_text,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(bttn),
            )
        except Exception as e:
            e = traceback.format_exc()
            LOGS.info(e)

@RENDYDEV.callback(regex="reopen")
@cb_wrapper
async def reopen_in_cb(_, callback_query):
    buttons = paginate_help(0, CMD_HELP, "helpme")
    user_id = RENDYDEV.client_me().me.id
    prefix = await get_prefix(user_id)
    new_get_text = f"**AkenoX-Inline**\n\nPrefix: {prefix}\n"
    await callback_query.edit_message_text(
        new_get_text,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(buttons),
    )            

@RENDYDEV.callback(regex="ub_modul_(.*)")
@cb_wrapper
async def on_plug_in_cb(_, callback_query):
    modul_name = callback_query.matches[0].group(1)
    username = "©️ Copyright 2020-2024"
    commands: dict = CMD_HELP[modul_name]
    this_command = f"──「 **Help For {str(modul_name).upper()}** 」──\n\n"
    for x in commands:
        this_command += f"  •  **Command:** `.{str(x)}`\n  •  **Function:** `{str(commands[x])}`\n\n"
    this_command += "{}".format(username)
    bttn = [
        [InlineKeyboardButton(text="Return", callback_data="reopen")],
    ]
    reply_pop_up_alert = (
        this_command
        if this_command is not None
        else f"{modul_name} No documentation has been written for the module."
    )
    await callback_query.edit_message_text(
        reply_pop_up_alert,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(bttn),
    )

@RENDYDEV.callback(regex="helpme_prev\((.+?)\)")
@cb_wrapper
async def on_plug_prev_in_cb(_, callback_query):
    user_id = RENDYDEV.client_me().me.id
    prefix = await get_prefix(user_id)
    new_get_text = f"**AkenoX-Inline**\n\nPrefix: {prefix}\n"
    current_page_number = int(callback_query.matches[0].group(1))
    buttons = paginate_help(current_page_number - 1, CMD_HELP, "helpme")
    await callback_query.edit_message_text(
        new_get_text,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(buttons),
    )

@RENDYDEV.callback(regex="helpme_next\((.+?)\)")
@cb_wrapper
async def on_plug_next_in_cb(_, callback_query):
    user_id = RENDYDEV.client_me().me.id
    prefix = await get_prefix(user_id)
    new_get_text = f"**AkenoX-Inline**\n\nPrefix: {prefix}\n"
    current_page_number = int(callback_query.matches[0].group(1))
    buttons = paginate_help(current_page_number + 1, CMD_HELP, "helpme")
    await callback_query.edit_message_text(
        new_get_text,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(buttons),
    )
