'''谷歌搜索'''
from utils.utils import Packages, oncmd

import requests
from urllib import parse

if Packages('googlesearch-python'):
    from googlesearch import search

@oncmd(cmd='google', ver='0.1')
async def handler(client, message):
    title = None
    result = {}
    args = message.text.strip().split()
    arg = args[1:] if len(args) > 1 else None
    reply = message.reply_to_message_id if message.reply_to_message_id else None

    if arg:
        query = ' '.join(arg)
    elif reply:
        query = message.reply_to_message.text if message.reply_to_message.text else message.reply_to_message.caption
    else:
        await message.edit("请加入搜索内容~")

    if query:
        await message.edit(f"正在搜索...\n\n{query}")
        for i in search(query, advanced=True):
            result[i.title] = i.url
            if len(result) > 10:
                break
        if result:
            links = '\n\n'.join(f"{i+1}、 [{item[0]}]({item[1]})" for i, item in enumerate(result.items()))
            content = f"🔎 | **Google** | [{query}](https://www.google.com/search?q={parse.quote(query)})\n\n{links}"
            await message.edit(text=content, disable_web_page_preview=True)
        else:
            await message.edit(f"搜索失败~\n建议手动搜索：[{query}](https://www.google.com/search?q={parse.quote(query)})")