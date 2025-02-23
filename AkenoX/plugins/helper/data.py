from pyrogram.types import InlineKeyboardButton, WebAppInfo


class Data:
    text_help_menu = (
        "**Command List & Help**"
        .replace(",", "")
        .replace("[", "")
        .replace("]", "")
        .replace("'", "")
    )
    reopen = [[InlineKeyboardButton("Re-Open", callback_data="reopen")]]
