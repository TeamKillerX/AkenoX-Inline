from AkenoX.plugins.libso.funcs_afk import *

from AkenoX import *

@RENDYDEV.user(
    prefix=["afk"],
    filters=(
        ~filters.scheduled
        & filters.me
        & ~filters.forwarded
    ),
    is_run=False
)
async def afkok_handler(client, message):
    await afkok(client, message)

@RENDYDEV.user(is_afk=True)
async def afk_mentioned_handler(client, message):
    await afk_mentioned(client, message)

@RENDYDEV.user(
    prefix=["unafk"],
    filters=(
        ~filters.scheduled
        & filters.me
        & ~filters.forwarded
    ),
    is_run=False
)
async def no_longer_afk_handler(client, message):
    await no_longer_afk(client, message)

RENDYDEV.buttons(
    "afk",
    [
        ["afk <Because>", "Notifies people who tag or reply to one of your messages or dm that you are afk"],
    ],
)
