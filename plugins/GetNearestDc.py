'''获取 dc 方位'''
from utils.utils import oncmd

from pyrogram.raw.functions.help import GetNearestDc
from  pyrogram.enums import ParseMode

@oncmd(cmd='dc', ver='0.1')
async def handler(client, message):
    dc = await client.invoke(GetNearestDc())
    await message.edit(f"<code>{dc}</code>", parse_mode=ParseMode.HTML)