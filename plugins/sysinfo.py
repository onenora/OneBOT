'''获取系统信息'''
from utils.utils import Packages, oncmd

import time
import platform

if Packages('psutil py-cpuinfo uptime'):
    import psutil
    import cpuinfo
    from uptime import uptime

@oncmd(cmd='sysinfo', ver='0.1')
async def handler(client, message):
    await message.edit("获取中...")

    def get_size(bytes, suffix="B"):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

    uname = platform.uname()
    svmem = psutil.virtual_memory()
    sdiskusage = psutil.disk_usage('/')
    load1, load5, load15 = psutil.getloadavg()

    up = uptime()
    parts = []
    days, up = up // 86400, up % 86400
    if days:
        parts.append('%d day%s' % (days, 's' if days != 1 else ''))
    hours, up = up // 3600, up % 3600
    if hours:
        parts.append('%d hour%s' % (hours, 's' if hours != 1 else ''))
    minutes, up = up // 60, up % 60
    if minutes:
        parts.append('%d minute%s' % (minutes, 's' if minutes != 1 else ''))

    text = "**系统信息**\n\n"
    text += f"**系统**: `{uname.system} {uname.release}, {uname.version}`\n"
    if cpuinfo.get_cpu_info()['arch'] == "X86_64":
        text += f"**CPU**: `{cpuinfo.get_cpu_info()['brand_raw']}`\n"
    else:
        text += f"**CPU**: `{cpuinfo.get_cpu_info()['arch']} ({cpuinfo.get_cpu_info()['count']}) `\n"
    text += f"**内存**: `{get_size(svmem.used)} / {get_size(svmem.total)}`\n"
    text += f"**硬盘**: `{get_size(sdiskusage.used)} / {get_size(sdiskusage.total)}`\n"
    text += f"**负载**: `{psutil.cpu_percent()}%, {'%.2f' %load1}, {'%.2f' %load5}, {'%.2f' %load15}`\n"
    text += f"**运行时间**: `{', '.join(parts)}`\n"

    await message.edit(text)