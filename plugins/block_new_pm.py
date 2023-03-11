'''自动 block 无私聊记录的对话'''
from utils.utils import onmsg

from pyrogram import filters
from pyrogram.raw.functions.messages import DeleteHistory

@onmsg(filters.private & ~filters.me, ver='0.1')
async def handler(client, message):
    if await client.search_messages_count(message.chat.id) <= 1:
        await client.read_chat_history(message.chat.id)
        await client.invoke(
            DeleteHistory(
                max_id=0, 
                revoke=True, 
                peer=(await client.resolve_peer(message.from_user.id))
            )
        )
        await client.block_user(message.from_user.id)