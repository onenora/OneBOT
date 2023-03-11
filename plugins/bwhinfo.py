'''获取搬瓦工 vps 信息'''
from utils.utils import oncmd
from utils.config import conf, config

import time
import requests
from urllib import parse

conf.read(config)
if 'BWH' not in conf:
    conf.add_section('BWH')
    conf.set('BWH', 'VEID', '123')
    conf.set('BWH', 'API_KEY', '123')
    with open(config, 'w') as configfile:
        conf.write(configfile)

VEID = conf['BWH']['VEID']
API_KEY = conf['BWH']['API_KEY']

@oncmd(cmd='bwh', ver='0.1')
async def handler(client, message):
    '''在搬瓦工后台获取 api 填入配置文件 `config.ini` 的 BWH 部分中'''
    await message.edit("获取中...")
    content = str()
    if bool(API_KEY and VEID):
        with requests.Session() as s:
            r = s.get(f'https://api.64clouds.com/v1/getLiveServiceInfo?veid={VEID}&api_key={API_KEY}')
        if r.ok:
            try:
                LiveServiceInfo = r.json()
            except Exception:
                content = "获取失败~"
            else:
                if LiveServiceInfo["error"] == 0:
                    node_datacenter = LiveServiceInfo['node_datacenter']
                    ve_status = LiveServiceInfo['ve_status']
                    load_average = LiveServiceInfo['load_average']
                    mem_available = str(LiveServiceInfo['mem_available_kb'] / 1000)
                    plan_ram = str(LiveServiceInfo['plan_ram'] / 1024 / 1024)
                    ve_used_disk_space = str(round(LiveServiceInfo['ve_used_disk_space_b'] / 1024 / 1024 / 1024,2))
                    ve_disk_quota_gb = LiveServiceInfo['ve_disk_quota_gb']
                    monthly_data_multiplier = LiveServiceInfo['monthly_data_multiplier']
                    data_counter = str(round(LiveServiceInfo['data_counter'] * monthly_data_multiplier / 1024 / 1024 / 1024,2))
                    plan_monthly_data = str(round(LiveServiceInfo['plan_monthly_data'] / 1024 / 1024 / 1024,2))
                    data_next_reset = time.strftime("%Y-%m-%d", time.localtime(LiveServiceInfo['data_next_reset']))

                    content = f'**{node_datacenter}**\n\n'
                    content += f'状态：`{ve_status},{load_average}`\n'
                    content += f'内存（可用）：`{mem_available}/{plan_ram}MB`\n'
                    content += f'硬盘（已用）：`{ve_used_disk_space}/{ve_disk_quota_gb}GB`\n'
                    content += f'流量（已用）：`{data_counter}/{plan_monthly_data}GB`\n'
                    content += f'流量重置日期：`{data_next_reset}`\n'
                else:
                    content = "获取失败~"
        else:
            content = "获取失败~"
    else:
        content = "没有获取到相关 API 值~"
    await message.edit(content)
    