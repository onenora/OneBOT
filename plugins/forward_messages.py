'''复读机'''
from utils.utils import oncmd

@oncmd(cmd='re', ver='0.1')
async def handler(client, message):
    '''
`re`：复读机
`re save`：转发到 Saved Messages
    '''
    await message.delete()
    args = message.text.strip().split()
    arg = args[1] if len(args) > 1 else None
    reply = message.reply_to_message_id if message.reply_to_message_id else None
    from_chat_id = message.chat.id
    
    chat_id = "me" if arg == "save" else from_chat_id

    if reply:
        try:
            await client.forward_messages(chat_id, from_chat_id, message.reply_to_message_id)
        except Exception:
            try:
                await client.copy_message(chat_id, from_chat_id, message.reply_to_message_id)
            except Exception:
                pass
