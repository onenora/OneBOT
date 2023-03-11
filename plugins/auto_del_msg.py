'''自动删除消息'''

from utils.utils import onsched
from utils.config import conf, config

import asyncio
from pyrogram import enums
from datetime import datetime 

conf.read(config)
if 'AUTODELMSG' not in conf:
    conf.add_section('AUTODELMSG')
    conf.set('AUTODELMSG', 'cron', '*/30 * * * *')
    conf.set('AUTODELMSG', 'intervals', '1')
    conf.set('AUTODELMSG', 'types', 'BOT, GROUP, SUPERGROUP, Discussion')
    with open(config, 'w') as configfile:
        conf.write(configfile)

cron = conf['AUTODELMSG']['cron']
intervals = int(conf['AUTODELMSG']['intervals'])
types = conf['AUTODELMSG']['types'].replace(' ','').split(',')
ChatType = []
for i in types:
    if i == "BOT":
        ChatType.append(enums.ChatType.BOT)
    elif i == "GROUP":
        ChatType.append(enums.ChatType.GROUP)
    elif i == "SUPERGROUP":
        ChatType.append(enums.ChatType.SUPERGROUP)
    elif i == "CHANNEL":
        ChatType.append(enums.ChatType.CHANNEL)
    elif i == "PRIVATE":
        ChatType.append(enums.ChatType.PRIVATE)
    elif i == "Discussion":
        ChatType.append('Discussion')

@onsched(cron)
async def handler(client):
    """默认每 30 分钟进行检查一次 1 天以上在机器人、群组发过的消息并删除。
如需更改默认设定，请修改配置文件 `config.ini` 里的 `AUTODELMSG` 部分。
配置文件参数说明：
    `cron`：定时检查
    `intervals`：消息间隔时间，单位为天
    `types`：对话框类型，类型有机器人 `BOT`、群组 `GROUP`、超级群组 `SUPERGROUP`、频道 `CHANNEL`、私聊 `PRIVATE`、频道评论区 `Discussion`

为避免触发 telegram 限制，每次最多只删除一百条信息。
    """
    global count
    count = 100
    async def delmsg(chat_id):
        global count
        count -= 1
        async for message in client.search_messages(chat_id, from_user="me"):
            if (datetime.now() - message.date).days >= intervals:
                if not message.service:
                    try:
                        if message.text or message.caption:
                            await message.edit_text('ㅤ')
                    except Exception:
                        pass
                    await message.delete()
            await asyncio.sleep(3)

    async for dialog in client.get_dialogs():
        if 'Discussion' in ChatType:
            if dialog.chat.type == enums.ChatType.CHANNEL:
                chat = await client.get_chat(dialog.chat.id)
                if chat.linked_chat:
                    await delmsg(chat.linked_chat.id)

        if dialog.chat.type in ChatType:
            await delmsg(dialog.chat.id)

        if count == 0:
            break
