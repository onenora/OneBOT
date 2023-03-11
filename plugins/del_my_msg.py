'''删除自己消息'''
from utils.utils import oncmd

import asyncio
from pyrogram import enums

@oncmd(cmd='dme', ver='0.1')
async def handler(client, message):
    """
1、默认删除十条消息：`dme`
2、删除 N 条消息：`dme N`
3、删除所有群的消息：`dme all`
"""
    await message.delete()

    chat_id = message.chat.id

    args = message.text.strip().split()
    arg = args[1] if len(args) > 1 else None

    def is_number(s):
        try:
            val = int(s)
            if val > 0:
                return True
        except:
            return False 

    async def dmlmsg(msg):
        if not msg.service:
            try:
                if msg.text or msg.caption:
                    await msg.edit_text('ㅤ')
            except:
                pass
            try:
                await msg.delete()
            except:
                pass

    if arg == "all":
        async for dialog in client.get_dialogs():
            if dialog.chat.type in {enums.ChatType.GROUP, enums.ChatType.SUPERGROUP}:
                async for msg in client.search_messages(dialog.chat.id, from_user="me"):
                    await dmlmsg(msg)
            await asyncio.sleep(3)
    else:
        if is_number(arg):
            limit = int(arg)
        else:
            limit = 10
        async for msg in client.search_messages(chat_id, from_user="me", limit=limit):
            await dmlmsg(msg)
                