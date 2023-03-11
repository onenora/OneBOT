'''speedtest 测速'''
from utils.utils import oncmd
from utils.config import tmp_dir

import os
import json
import tarfile
import requests
import platform
import subprocess

@oncmd(cmd='speedtest', ver='0.1')
async def handler(client, message):
    """
使用示例：
1、测速：`speedtest`
2、获取服务器：`speedtest L`
3、指定服务器测速：`speedtest <服务器 id>`
"""
    def convert_size(b, suffix="B", factor=1024):
        for unit in ["", "K", "M", "G", "T", "P"]:
            if b < factor:
                return f'{b:.2f}{unit}{suffix}'
            b /= factor

    def is_json(content):
        try:
            json.loads(content)
        except:
            return False
        return True

    await message.edit(f'运行中...')

    chat_id = message.chat.id
    speedtest = f'{tmp_dir}/speedtest'
    
    args = message.text.strip().split()
    arg = args[1] if len(args) > 1 else None

    async def sptest():
        await message.edit(f'测速中...')
        cmd = [speedtest, "--format=json-pretty", "--progress=no", "--accept-license", "--accept-gdpr"]
        cmd.append(f"--server-id={arg}")
        try:
            output = subprocess.check_output(cmd)
        except Exception as e:
            output = e
        return output

    if not os.path.exists(speedtest):
        await message.edit("下载 speedtest 中...")
        arch = platform.machine()
        url = f'https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-{arch}.tgz'
        try:
            with requests.Session() as s:
                r = s.get(url)
            if r.ok:
                with open(f'{speedtest}.tgz', "wb") as f:
                    f.write(r.content)
                tar = tarfile.open(f'{speedtest}.tgz', "r:*")
                tar.extract("speedtest", path=tmp_dir)
        except:
            await message.edit("下载 speedtest 失败~")

    if os.path.exists(speedtest):
        if arg == 'L':
            await message.edit(f'获取服务器中...')
            cmd = [speedtest, "-L", "--format=json-pretty", "--accept-license", "--accept-gdpr"]
            try:
                output = subprocess.check_output(cmd)
            except Exception as e:
                await message.edit(f'获取服务器失败...')
            else:
                content = "**SPEEDTEST 服务器列表**\n\n"
                servers = json.loads(output)["servers"]
                for s in servers:
                    content += f"▪️ `{s['id']}`： `{s['name']} - {s['location']} {s['country']}`\n"
                await message.edit(content)
        else:
            output = await sptest()
            if is_json(output):
                await message.delete()
                data = json.loads(output)
                content = "**🕸 打咩-Speedtest-测速结果**\n\n"
                content += f'下载：`{convert_size(data["download"]["bandwidth"], suffix="B/s")} - {convert_size(data["download"]["bytes"], suffix="B", factor=1000)}`\n'
                content += f'上传：`{convert_size(data["upload"]["bandwidth"], suffix="B/s")} - {convert_size(data["upload"]["bytes"], suffix="B", factor=1000)}`\n'
                content += f'Ping：`{data["ping"]["latency"]}ms - {data["ping"]["jitter"]}`\n'
                content += f'测速点：`{data["isp"]}`\n'
                content += f'服务商：`{data["server"]["name"]} - {data["server"]["location"]} {data["server"]["country"]}`\n'
                await client.send_photo(chat_id, photo=f'{data["result"]["url"]}.png', caption=content)
            else:
                await message.edit(f'测速失败...\n{output}')