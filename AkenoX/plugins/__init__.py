from pyrogram.types import Message

custom_blue = "<emoji id=5328317370647715629>✅</emoji>"
custom_cat = "<emoji id=5352865784508980799>🗿</emoji>"
custom_pong = "<emoji id=5269563867305879894>🗿</emoji>"
custom_balon = "<emoji id=5407064810040864883>🗿</emoji>"
custom_owner = "<emoji id=5467406098367521267>🗿</emoji>"

def ReplyCheck(message: Message):
    reply_id = None
    if message.reply_to_message:
        reply_id = message.reply_to_message.id if message.reply_to_message else None
    elif not message.from_user.is_self if message.from_user else None:
        reply_id = message.id
    return reply_id
