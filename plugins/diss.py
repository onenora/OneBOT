'''怼人'''
from utils.utils import oncmd
import requests

@oncmd(cmd='diss', ver='0.1')
async def handler(client, message):
    await message.delete()
    reply = message.reply_to_message_id if message.reply_to_message_id else None

    with requests.Session() as s:
        r = s.get('https://zuan.shabi.workers.dev')

    if r.ok:
        content = f'**{r.text}**'
        if reply:
            content += f' [😘](tg://user?id={message.reply_to_message.from_user.id})'

        await client.send_message(message.chat.id, content, reply_to_message_id=reply)
