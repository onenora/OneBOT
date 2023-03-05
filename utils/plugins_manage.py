'''获取插件信息和插件管理'''
import os
import re
import sys
import git
import asyncio
import requests
from pathlib import Path
from bs4 import BeautifulSoup

from utils import import_plugin
from utils.utils import Packages, PLUGINS, scheduler, oncmd
from utils.config import client, version, prefix, base_dir, plugins_dir

def get_args(mgs):
    args = {}
    for i, arg in enumerate(mgs.text.strip().split()):
        args[i] = arg
    return args

def restart():
    os.execv(sys.executable, [sys.executable] + sys.argv)

def get_url(url):
    with requests.Session() as s:
        r = s.get(url)
        if not r.ok:
            return False
        return r.text

def get_plugins():
    result = get_url('https://github.com/noreph/TMBot-Plugins/tree/4.0')
    dct = {}

    if not result:
        return False

    soup = BeautifulSoup(result, 'html.parser')
    a_tags = soup.find_all('a')
    urls = ['https://raw.githubusercontent.com' + re.sub('/blob', '', link.get('href')) 
                        for link in a_tags if '.py' in link.get('href')]

    for i in urls:
        content = re.search('(?<=(\'\'\'|\"\"\")).+(?=(\'\'\'|\"\"\"))', get_url(i))
        if content is not None:
            dct[Path(i).stem] = {'url': i, 'help': content.group(0)}

    return dct

async def install(url, plugin):
    content = get_url(url)
    packages = re.search('(?<=(Packages\((\'|\"))).+(?=(\'|\")\))', content)
    if packages:
        if not Packages(packages.group()):
            return False
    with open(f'{plugins_dir}/{plugin}.py', "w") as f:
        f.write(content)
    root = 'data/plugins'
    path = Path(root, plugin)
    module_path = '.'.join(path.parent.parts + (path.stem,))
    if import_plugin(module_path):
        return True
    else:
        return False


@oncmd(cmd='pm')
async def handler(client, message):
    '''
1、查看已安装插件列表：
`pm`
2、查看插件、指令信息：
`pm help <插件名>/<指令>`
3、升级程序：
`pm update`
4、升级已安装插件：
`pm update plugin`
5、获取可用插件列表：
`pm list`
6、安装插件：
    安装部分插件：
    `pm add <插件 1> <插件 2> <插件 3>`
    安装所有插件：
    `pm add all`
7、删除插件：
    删除已安装插件：
    `pm del <插件名>`
    删除所有已安装插件：
    `pm del all`
8、重启：
`pm restart`
    '''
    args = get_args(message)
    content = f'🤖 **TMBot v{version}**\n'
    content += f'▍ `{message.text}`\n\n'
    plugins = PLUGINS.dct()

    def plist():
        lst = []
        plugins = PLUGINS.dct()
        for plugin in plugins:
            if plugins[plugin]['type'] in ['cmd', 'sys']:
                lst.append(plugins[plugin]['cmd'])
            if plugins[plugin]['type'] != 'sys':
                lst.append(plugins[plugin]['name'])
        return lst

    async def restartd():
        await message.delete()
        restart()

    async def get_list(content):
        await message.edit(content + '获取列表中...')

        dct = get_plugins()

        if not dct:
            await message.edit(content + "插件列表获取失败~")
            return

        content += '可用插件列表:\n'
        for i in list(dct.keys()):
            content += f"`{i}`：{dct[i]['help']}\n"
        await message.edit(content)

    async def add(content):
        for i in list(args.keys())[:2]:
            del args[i]

        if not args:
            content += '缺少参数~'
            await message.edit(content)
            return

        await message.edit(content + "获取插件中...")

        dct = get_plugins()
        lst = list(dct.keys())

        if not dct:
            await message.edit(content + "插件列表获取失败~")
            return

        content += f"安装：\n"
        await message.edit(content)
        if args.get(2) == 'all':
            for i in dct:
                content += f"`{i}`...\n"
                await message.edit(content)
                await asyncio.sleep(2)
                if await install(dct[i]['url'], i):
                    content = content.replace(f"`{i}`...\n", f"`{i}`...✓ \n")
                    await message.edit(content)
                else:
                    content = content.replace(f"`{i}`...\n", f"`{i}`...✗ \n")
                    await message.edit(content)
                await asyncio.sleep(1)
            await message.edit(content + f'\n发送 `{prefix}pm` 获取帮助~')
        else:
            for i in list(args.values()):
                if i in lst:
                    content += f"`{i}`...\n"
                    await message.edit(content)
                    await asyncio.sleep(2)
                    if await install(dct[i]['url'], i):
                        content = content.replace(f"`{i}`...\n", f"`{i}`...✓ \n")
                        await message.edit(content)
                    else:
                        content = content.replace(f"`{i}`...\n", f"`{i}`...✗ \n")
                        await message.edit(content)
                else:
                    content += f"`{i}` 不存在~\n"
                    await message.edit(content)
                await asyncio.sleep(1)
            await message.edit(content + f'\n发送 `{prefix}pm` 获取帮助~')

    async def delete(content):
        if not args.get(2):
            content += '缺少参数~'
            await message.edit(content)
            return
        plugins = PLUGINS.dct()
        if args.get(2) and args.get(2) == 'all':
            content += '删除：\n'
            await message.edit(content)
            for plugin in plugins:
                if plugins[plugin]['type'] != 'sys':
                    content += f"`{plugin}`...\n"
                    await message.edit(content)
                    await asyncio.sleep(2)
                    if plugins[plugin]['type'] in ['cmd', 'msg']:
                        client.remove_handler(plugins[plugin]['handler'], plugins[plugin]['group'])
                        os.remove(plugins[plugin]['file'])
                    elif plugins[plugin]['type'] == 'sched':
                        scheduler.remove_job(str(plugins[plugin]['group']))
                        os.remove(plugins[plugin]['file'])
                    content = content.replace(f"`{plugin}`...\n", f"`{plugin}`...✓ \n")
                    await message.edit(content)
                await asyncio.sleep(1)

        elif args.get(2) and args.get(2).replace(prefix, "") in plist():
            content += '删除：\n'
            await message.edit(content)
            for plugin in plugins:
                if args.get(2) == plugins[plugin]['name'] or args.get(2) == plugins[plugin]['cmd']:
                    if plugins[plugin]['type'] == 'sys':
                        await message.edit(content + f"系统插件 {arg} 无法删除~")
                        return
                    content += f"`{plugin}`...\n"
                    await message.edit(content)
                    await asyncio.sleep(2)
                    if plugins[plugin]['type'] in ['cmd', 'msg']:
                        client.remove_handler(plugins[plugin]['handler'], plugins[plugin]['group'])
                        os.remove(plugins[plugin]['file'])
                        return
                    elif plugins[plugin]['type'] == 'sched':
                        scheduler.remove_job(str(plugins[plugin]['group']))
                        os.remove(plugins[plugin]['file'])
                        return
            content = content.replace(f"`{plugin}`...\n", f"`{plugin}`...✓ \n")
            await message.edit(content)

        else:
            content += f'`{args.get(2)}` 不存在~' 
            await message.edit(content)


    async def update(content):
        if args.get(2) and args.get(2) != 'plugin':
            content += '参数错误~'
            await message.edit(content)
            return

        if args.get(2) and args.get(2) == 'plugin':
            await message.edit(content + "获取插件中...")
            dct = get_plugins()
            lst = list(dct.keys())
            plugins = PLUGINS.dct()
            content += '升级插件：\n'
            await message.edit(content)
            for plugin in plugins:
                if plugins[plugin]['type'] != 'sys':
                    if plugin in lst:
                        content += f"`{plugin}`...\n"
                        await message.edit(content)
                        await asyncio.sleep(2)
                        if await install(dct[plugin]['url'], plugin):
                            content = content.replace(f"`{plugin}`...\n", f"`{plugin}`...✓ \n")
                            await message.edit(content)
                        else:
                            content = content.replace(f"`{plugin}`...\n", f"`{plugin}`...✗ \n")
                            await message.edit(content)
            await message.edit(content + f'\n发送 `{prefix}pm` 获取帮助~')

        else:
            content += '获取更新中...'
            try:
                update = git.cmd.Git(base_dir)
                result = update.pull()
                if result == 'Already up to date.':
                    content = content.replace('获取更新中...', '暂无更新~')
                elif result.find("Fast-forward") > -1:
                    content = content.replace('获取更新中...', f'''更新完成，即将重启：\n```{result}```''')
                    await message.edit(content)
                    restart()
                else:
                    content = content.replace('获取更新中...', f'''更新出错：\n```{result}```''')
            except Exception as e:
                content = content.replace('获取更新中...', f'''更新出错：```\n{e}```''')
            await message.edit(content)

    async def get_help(content):
        if not args.get(2):
            content += '缺少参数~'
            await message.edit(content)
            return

        plugin = args.get(2).replace(prefix,"")
        if plugin not in plist():
            content += f'`{args.get(2)}` 不存在~'
            await message.edit(content)
            return

        if not plugins.get(plugin):
            for i in plugins:
                if plugins[i]['cmd'] == plugin:
                    plugin = plugins[i]['name']
                    break

        content += f'**{args.get(2)}** 的信息：\n\n'

        if plugins[plugin]['type'] in ['sys', 'cmd']:
            content += f"命令：`{prefix}{plugins[plugin]['cmd']}`\n"

        content += f"版本：`{plugins[plugin]['ver']}`\n"
        content += f"插件名：`{plugins[plugin]['name']}`\n\n"

        content += f"{plugins[plugin]['help']}\n"

        if plugins[plugin]['doc']:
            content += f"{plugins[plugin]['doc']}\n"

        await message.edit(content)

    async def pm(content):
        sys, cmds, msgs, scheds = {}, {}, {}, {}
        for plugin in plugins:
            if plugins[plugin]['type'] == 'sys':
                sys[plugins[plugin]['cmd']] = plugins[plugin]['help']
            if plugins[plugin]['type'] == 'cmd':
                cmds[plugins[plugin]['cmd']] = plugins[plugin]['help']
            if plugins[plugin]['type'] == 'msg':
                msgs[plugins[plugin]['name']] = plugins[plugin]['help']
            if plugins[plugin]['type'] == 'sched':
                scheds[plugins[plugin]['name']] = plugins[plugin]['help']

        for i in sys:
            content += f"`{prefix}{i}`：{sys[i]}\n"

        if cmds:
            content += "\n**命令列表**\n"
            for i in cmds:
                content += f"`{prefix}{i}`：{cmds[i]}\n"

        if msgs:
            content += "\n**无命令插件**\n"
            for i in msgs:
                content += f"`{prefix}{i}`：{msgs[i]}\n"

        if scheds:
            content += "\n**定时插件**\n"
            for i in scheds:
                content += f"`{prefix}{i}`：{scheds[i]}\n"

        await message.edit(content)

        
    match args.get(1):
        case 'help':
            await get_help(content)
        case 'update':
            await update(content)
        case 'list':
            await get_list(content)
        case 'add':
            await add(content)
        case 'del':
            await delete(content)
        case 'restart':
            await restartd()
        case _:
            await pm(content)

