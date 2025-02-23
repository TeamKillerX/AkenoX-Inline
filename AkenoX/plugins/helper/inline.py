from math import ceil
from traceback import format_exc

from pyrogram.errors import MessageNotModified
from pyrogram.types import *

from AkenoX import ids as list_users

looters = None


def paginate_help(page_number, loaded_modules, prefix):
    number_of_rows = 5
    number_of_cols = 3
    global looters
    looters = page_number
    helpable_modules = [p for p in loaded_modules if not p.startswith("_")]
    helpable_modules = sorted(helpable_modules)
    modules = [
        InlineKeyboardButton(
            text="{}".format(x),
            callback_data=f"ub_modul_{x}",
        )
        for x in helpable_modules
    ]
    pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols]))
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    max_num_pages = ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if len(pairs) > number_of_rows:
        pairs = pairs[
            modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)
        ] + [
            (
                InlineKeyboardButton(
                    text="《",
                    callback_data=f"{prefix}_prev({modulo_page})"
                ),
                InlineKeyboardButton(
                    text="》",
                    callback_data=f"{prefix}_next({modulo_page})"
                ),
            )
        ]
    return pairs


def cb_wrapper(func):
    async def wrapper(client, cb):
        user_id = cb.from_user.id
        users = list_users
        if user_id not in users:
            await cb.answer(
                "gak bisa developer!",
                cache_time=0,
                show_alert=True,
            )
        else:
            try:
                await func(client, cb)
            except MessageNotModified:
                await cb.answer("LU GOBLOK")
            except Exception:
                print(format_exc())
                await cb.answer(
                    f"Oh No, SomeThing Isn't Right. Please Check Logs!",
                    cache_time=0,
                    show_alert=True,
                )

    return wrapper

ok_inline_text = """
**AkenoX-Inline** is an ultra-fast bot optimized for inline 🚀
"""

def inline_wrapper(func):
    async def wrapper(client, inline_query):
        users = list_users
        bttn = [
            [InlineKeyboardButton("🗿 Source code", url=f"https://github.com/TeamKillerX/AkenoX-Inline/")]
        ]
        if inline_query.from_user.id not in users:
            await client.answer_inline_query(
                inline_query.id,
                cache_time=1,
                results=[
                    (
                        InlineQueryResultArticle(
                            title="Sorry, You can get source code here",
                            input_message_content=InputTextMessageContent(
                                ok_inline_text
                            ),
                            reply_markup=InlineKeyboardMarkup(bttn)
                        )
                    )
                ],
            )
        else:
            await func(client, inline_query)
    return wrapper
