'''获取群、对话或群员信息'''
from utils.utils import oncmd
from pyrogram import enums
import datetime

@oncmd(cmd='info', ver='0.1')
async def handler(client, message):
    await message.edit("获取中...")
    
    user = None
    channel_id = None
    sender_chat_id = None
    get_chat_member = None

    reply = message.reply_to_message_id if message.reply_to_message_id else None

    def GetInfo(dicts):
        text = str()
        for i in dicts:
            if not isinstance(dicts[i], bool):
                if isinstance(dicts[i], (str, int, datetime.datetime, enums.ChatMemberStatus, enums.ChatType)):
                    if i != "phone_number":
                        if isinstance(dicts[i], (enums.ChatMemberStatus, enums.ChatType)):
                            text += f"**{i}**: `{dicts[i].value}`\n"
                        else:
                            text += f"**{i}**: `{dicts[i]}`\n"
        return text

    if bool(message.chat and message.chat.type in {enums.ChatType.GROUP, enums.ChatType.SUPERGROUP}):
        channel_id = message.chat.id
        if reply:
            if message.reply_to_message.sender_chat:
                sender_chat_id = message.reply_to_message.sender_chat.id
                get_sender_chat = (await client.get_chat(sender_chat_id)).__dict__
            else:
                user = message.reply_to_message.from_user.id
                get_chat_member = (await client.get_chat_member(channel_id, user)).__dict__
        else:
            get_chat = (await client.get_chat(channel_id)).__dict__
    else:
        channel_id = message.chat.id
        get_chat = (await client.get_chat(channel_id)).__dict__

    if user:
        get_user = (await client.get_users(user)).__dict__
        text = GetInfo(get_user)

    if channel_id and reply:
        if sender_chat_id:
            text = GetInfo(get_sender_chat)
        else:
            text += GetInfo(get_chat_member)
            messages_count = await client.search_messages_count(channel_id, from_user=user)
            text += f"**messages_count**: `{messages_count}`\n"
    elif channel_id and not reply:
        text = GetInfo(get_chat)
    else:
        text = "获取失败~"

    await message.edit(text)
