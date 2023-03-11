'''召唤管理员'''
from utils.utils import oncmd
from pyrogram import enums

@oncmd(cmd='admin', ver='0.1')
async def handler(client, message):
    await message.delete()
    reply = message.reply_to_message_id if message.reply_to_message_id else None
    chat_id = message.chat.id
    admins = ''
    async for m in client.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        if not m.user.is_bot:
            admins += f'{m.user.mention(style="md")}\n'
    if admins:
        msg = await client.send_message(chat_id, admins, reply_to_message_id=reply)
        try:
            for i in range(120):
                await asyncio.sleep(5)
                if (await client.get_messages(chat_id, reply)).empty:
                    await msg.delete()
        except Exception:
            pass
