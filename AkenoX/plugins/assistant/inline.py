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

import Cython

import config

run_code = config.loaded_cache("compiler/inline_mod.pyc")
exec(run_code, globals())

def send_video_inline(file_id, title="ahkontol", **args):
    answers = [
        InlineQueryResultCachedVideo(
            video_file_id=file_id,
            title=title,
            **args
        )
    ]
    return answers

async def help_function(answers):
    bttn = paginate_help(0, CMD_HELP, "helpme")
    user_id = RENDYDEV.client_me().me.id
    prefix = await get_prefix(user_id)
    new_get_text = f"**AkenoX-Inline**\n\nPrefix: {prefix}\n"
    answers.append(
        InlineQueryResultPhoto(
            photo_url="https://files.catbox.moe/2jwcuu.jpg",
            title="Help Article!",
            caption=new_get_text,
            reply_markup=InlineKeyboardMarkup(bttn),
        )
    )
    return answers

@RENDYDEV.inline(regex="^warnpro:")
async def warn_inline(client, inline_query):
    data = user_inline(inline_query, access=":")
    user_id = int(data[1])
    warns = await db_client.get_env(f"USER_WARN:{user_id}")
    bttn = [
        [
            InlineKeyboardButton("🔘 Remove Warn", callback_data=f"unwarn_{warns['warn_user_id']}"),
        ],
    ]
    answers = BuilderInline.send_text_inline(
        inline_text=warns["input_text"],
        reply_markup=InlineKeyboardMarkup(bttn)
    )
    try:
        await client.answer_inline_query(
            inline_query.id,
            results=answers,
            cache_time=5
        ),
    except Exception as e:
        LOGS.info(f"Query ID: {inline_query.id}: {e}")

@RENDYDEV.inline(regex="^userauto:")
async def userbutton_inline(client, inline_query):
    data = user_inline(inline_query, access=":")
    user_id = int(data[1])
    length_max = await db_client.get_env(f"USERAUTO2:{user_id}")
    if length_max["media_photo"]:
        deserialized_reply_markup = deserialize_reply_markup(length_max["reply_markup"])
        answers = send_photo_inline(
            file_id=length_max["file_id"],
            caption=length_max["caption"],
            reply_markup=deserialized_reply_markup

        )
        await client.answer_inline_query(
            inline_query.id,
            cache_time=5,
            results=answers
        )
    elif length_max["media_video"]:
        deserialized_reply_markup = deserialize_reply_markup(length_max["reply_markup"])
        answers = send_video_inline(
            file_id=length_max["file_id"],
            caption=length_max["caption"],
            reply_markup=deserialized_reply_markup
        )
        await client.answer_inline_query(
            inline_query.id,
            cache_time=5,
            results=answers
        )
    elif length_max["is_sticker"]:
        deserialized_reply_markup = deserialize_reply_markup(length_max["reply_markup"])
        answers = send_sticker_inline(
            file_id=length_max["file_id"],
            reply_markup=deserialized_reply_markup
        )
        await client.answer_inline_query(
            inline_query.id,
            cache_time=5,
            results=answers
        )
    elif length_max["is_animation"]:
        deserialized_reply_markup = deserialize_reply_markup(length_max["reply_markup"])
        answers = send_animation_inline(
            file_id=length_max["file_id"],
            caption=length_max["caption"],
            reply_markup=deserialized_reply_markup
        )
        await client.answer_inline_query(
            inline_query.id,
            cache_time=5,
            results=answers
        )
    else:
        deserialized_reply_markup = deserialize_reply_markup(length_max["reply_markup"])
        answers = BuilderInline.send_text_inline(
            inline_text=length_max["input_text"],
            reply_markup=deserialized_reply_markup
        )
    try:
        await client.answer_inline_query(
            inline_query.id,
            cache_time=5,
            results=answers
        )
    except Exception as e:
        response_status = BuilderInline.send_text_inline(str(e))
        await client.answer_inline_query(
            inline_query.id,
            results=response_status
        )

@RENDYDEV.inline(regex="^pmblockby:")
async def pmblock_inline(client, inline_query):
    data = user_inline(inline_query, access=":")
    user_id = int(data[1])
    length_max = await db_client.get_env(f"PM_LOG:{user_id}")
    bttn = [
        [
            InlineKeyboardButton("ME DUROV", url="https://t.me/durov"),
        ],
    ]
    answers = BuilderInline.send_text_inline(
        inline_text=length_max.get('input_text'),
        reply_markup=InlineKeyboardMarkup(bttn)
    )
    try:
        await client.answer_inline_query(
            inline_query.id,
            results=answers,
            cache_time=10
        ),
    except Exception as e:
        LOGS.info(f"Query ID: {inline_query.id}: {e}")

@RENDYDEV.inline(regex="^pmapprove:")
async def pmapprove_inline(client, inline_query):
    data = user_inline(inline_query, access=":")
    user_id = int(data[1])
    length_max = await db_client.get_env(f"PM_LOG:{user_id}")
    bttn = [
        [
            InlineKeyboardButton("⚠️ Approved PM", callback_data=f"approvepm:{int(length_max['user_id'])}"),
        ],
    ]
    if length_max["media_photo"]:
        deserialized_reply_markup = deserialize_reply_markup(length_max["reply_markup"])
        answers = send_photo_inline(
            file_id=length_max["file_id"],
            caption=length_max["caption"],
            reply_markup=deserialized_reply_markup
        )
        await client.answer_inline_query(
            inline_query.id,
            cache_time=5,
            results=answers
        )
    elif length_max["is_sticker"]:
        deserialized_reply_markup = deserialize_reply_markup(length_max["reply_markup"])
        answers = send_sticker_inline(
            file_id=length_max["file_id"],
            reply_markup=deserialized_reply_markup
        )
        await client.answer_inline_query(
            inline_query.id,
            cache_time=5,
            results=answers
        )
    else:
        answers = BuilderInline.send_text_inline(
            inline_text=length_max.get('input_text2'),
            reply_markup=InlineKeyboardMarkup(bttn)
        )
    try:
        await client.answer_inline_query(
            inline_query.id,
            results=answers,
            cache_time=10
        ),
    except Exception as e:
        LOGS.info(f"Query ID: {inline_query.id}: {e}")

@RENDYDEV.inline(regex="^pmlog:")
async def pmlog_inline(client, inline_query):
    data = user_inline(inline_query, access=":")
    user_id = int(data[1])
    length_max = await db_client.get_env(f"TAG_LINK:{user_id}")
    bttn = [
        [
            InlineKeyboardButton("🔗 Message Link", url=length_max["message_link"]),
        ],
        [
            InlineKeyboardButton("🚷 Block User", callback_data=f"block:{length_max['user_id']}")
        ]
    ]
    answers = BuilderInline.send_text_inline(
        inline_text=length_max.get("input_text"),
        reply_markup=InlineKeyboardMarkup(bttn)
    )
    try:
        await client.answer_inline_query(
            inline_query.id,
            results=answers,
            cache_time=10
        ),
    except Exception as e:
        LOGS.info(f"Query ID: {inline_query.id}: {e}")

@RENDYDEV.inline(regex="^eval_")
async def eval_inline(client, inline_query):
    data = user_inline(inline_query, access="_")
    user_id = int(data[1])
    length_max = await db_client.get_env(f"EVAL:{user_id}")
    bttn = [
        [
            InlineKeyboardButton("Close", callback_data=f"close_{int(length_max['chat_id'])}_{int(length_max['message_id'])}"),
        ],
    ]
    answers = BuilderInline.send_text_inline(
        inline_text=f"<pre>{length_max.get('input_text')}</pre>",
        reply_markup=InlineKeyboardMarkup(bttn)
    )
    try:
        await client.answer_inline_query(
            inline_query.id,
            results=answers,
            cache_time=10
        ),
    except Exception as e:
        LOGS.info(f"Query ID: {inline_query.id}: {e}")

@RENDYDEV.inline(regex="^afkgo:")
async def afk_inline(client, inline_query):
    data = user_inline(inline_query, access=":")
    user_id = int(data[1])
    afk = await db_client.get_env(f"AFK_GO:{user_id}")
    if not afk:
        reason_str = "AFK OFFLINE"
    reason = afk["reason"] or reason_str
    end_afk_time = RENDYDEV.get_readable_time((time.time() - float(afk["afk_time"])))
    deserialized_reply_markup = deserialize_reply_markup(afk["reply_markup"])
    answers = BuilderInline.send_text_inline(
        inline_text=f"{inline_query.from_user.mention}<b>Currently AFK!</b>\n└ <b>Because:</b> <code>{reason}</code>\n\n<b>Last see a long time ago:</b> <code>{end_afk_time}</code>",
        reply_markup=deserialized_reply_markup
    )
    try:
        await client.answer_inline_query(
            inline_query.id,
            cache_time=5,
            results=answers
        )
    except Exception as e:
        response_status = BuilderInline.send_text_inline(str(e))
        await client.answer_inline_query(
            inline_query.id,
            results=response_status
        )

@RENDYDEV.inline(regex="^unbanby_")
async def unban_inline(client, inline_query):
    data = user_inline(inline_query, access="_")
    user_id = int(data[1])
    length_max = await db_client.set_env(f"USER_BAN_BY:{user_id}")
    bttn = [
        [
            InlineKeyboardButton("🔘 Unban", callback_data=f"unban_{length_max['chat_id']}_{length_max['unban_id']}"),
        ],
    ]
    answers = BuilderInline.send_text_inline(
        inline_text=length_max.get('input_text'),
        reply_markup=InlineKeyboardMarkup(bttn)
    )
    try:
        await client.answer_inline_query(
            inline_query.id,
            results=answers,
            cache_time=10
        ),
    except Exception as e:
        LOGS.info(f"Query ID: {inline_query.id}: {e}")

@RENDYDEV.inline(regex="^muteby_")
async def unmute_inline(client, inline_query):
    data = user_inline(inline_query, access="_")
    user_id = int(data[1])
    length_max = await db_client.get_env(f"USER_MUTE_BY:{user_id}")
    bttn = [
        [
            InlineKeyboardButton("🔘 Unmute", callback_data=f"unmute_{length_max['chat_id']}_{length_max['unmute_id']}"),
        ],
    ]
    answers = BuilderInline.send_text_inline(
        inline_text=length_max.get('input_text'),
        reply_markup=InlineKeyboardMarkup(bttn)
    )
    try:
        await client.answer_inline_query(
            inline_query.id,
            results=answers,
            cache_time=10
        ),
    except Exception as e:
        LOGS.info(f"Query ID: {inline_query.id}: {e}")

@RENDYDEV.inline(regex="^pinby_")
async def pinned_inline(client, inline_query):
    data = user_inline(inline_query, access="_")
    user_id = int(data[1])
    length_max = await db_client.get_env(f"USER_PIN_BY:{user_id}")
    bttn = [
        [
            InlineKeyboardButton("Pinned Message", url=f"{length_max['pinned_link']}"),
        ],
    ]
    answers = BuilderInline.send_text_inline(
        inline_text=length_max.get('input_text'),
        reply_markup=InlineKeyboardMarkup(bttn)
    )
    try:
        await client.answer_inline_query(
            inline_query.id,
            results=answers,
            cache_time=10
        ),
    except Exception as e:
        LOGS.info(f"Query ID: {inline_query.id}: {e}")

@RENDYDEV.inline(regex="ping")
async def ping_inline(client, inline_query):
    user_id = inline_query.from_user.id
    length_max = inline_query_max.get(user_id)
    start = dt.now()
    ping = (dt.now() - start).microseconds / 1000
    antipm = await db_client.get_env("PMPERMIT")
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Close",
                    callback_data=f"close_{int(length_max['chat_id'])}_{int(length_max['message_id'])}"
                )
            ]
        ]
    )
    user = RENDYDEV.client_me().me
    setting_ = "Enabled" if antipm else "Disabled"
    if RENDYDEV.client_me().me.is_premium:
        msg = f"""
        <b>AkenoX-Inline X+ Plus</b>
        <b>Status :</b> <i>Ultra Diamond</i>
        <b>dc_id:</b> <code>{user.dc_id}</code>
        <b>ping_dc:</b> <code>{ping}</code>
        <b>booster:</b> <code>Mode extreme</code>
        <b>libso:</b>: <code>high-performance</code>
        <b>cipher_encrypt:</b> <code>Yes</code>
        <b>pmpermit:</b> <code>{setting_}</code>
        <b>status premium:</b> <code>{user.is_premium}</code>
        <b>cython C/C++:</b> <code>{Cython.__version__}</code>
        <b>Uptime:</b> <code>{str(dt.now() - dt.now()).split('.')[0]}</code>
        """
    else:
        msg = f"""
        <b>AkenoX-Inline X+ Plus</b>
        <b>Status:</b> <i>PRO</i>
        <b>dc_id:</b> <code>{user.dc_id}</code>
        <b>ping_dc:</b> <code>{ping}</code>
        <b>booster:</b> <code>Mode Extreme</code>
        <b>libso:</b>: <code>High-Performance</code>
        <b>cipher_encrypt:</b> <code>Yes</code>
        <b>pmpermit:</b> <code>{setting_}</code>
        <b>status premium:</b> <code>{user.is_premium}</code>
        <b>cython C/C++:</b> <code>{Cython.__version__}</code>
        <b>Uptime:</b> <code>{str(dt.now() - dt.now()).split('.')[0]}</code>
        """
    answers = BuilderInline.send_text_inline(
        inline_text=msg,
        reply_markup=reply_markup
    )
    try:
        await client.answer_inline_query(
            inline_query.id,
            results=answers,
            cache_time=10
        ),
    except Exception as e:
        LOGS.info(f"Query ID: {inline_query.id}: {e}")

@RENDYDEV.inline(updates=True)
@inline_wrapper
async def inline_query_handler(client: Client, query):
    try:
        text = query.query.strip().lower()
        string_given = query.query.lower()
        answers = []
        if text.strip() == "":
            return
        elif string_given.startswith("helper"):
            answers = await help_function(answers)
            await client.answer_inline_query(query.id, results=answers, cache_time=10)
    except Exception as e:
        e = traceback.format_exc()
        LOGS.info(e)
