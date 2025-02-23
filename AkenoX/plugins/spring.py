import asyncio
import time
from datetime import datetime

from pyrogram import *
from pyrogram.types import *

from AkenoX import *
from AkenoX.plugins.libso.ping import custom_ping

from . import *


@RENDYDEV.user(
    prefix=["ping"],
    filters=(
        ~filters.scheduled
        & filters.me
        & ~filters.forwarded
    ),
    is_run=False,
    limit=3,
    time_frame=10
)
async def sping_handler(client, message):
    await custom_ping(client, message)
