import os
import sys
import inspect
import subprocess
import pkg_resources
from typing import Callable
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pyrogram import handlers, filters

from utils.config import version, prefix, client, logger

scheduler = AsyncIOScheduler()

class PLUGINS:
    def init():
        global group, plugins
        group = 0
        plugins = {}

    def reg(func, types, cmd, ver):
        global plugins, group
        group += 1

        file = inspect.getfile(func)
        name = inspect.getmodulename(file)

        if name == 'plugins_manage':
            types = 'sys'
            ver = version

        if types in ['sys', 'cmd', 'msg']:
            if types in ['sys', 'cmd']:
                Filter =  filters.me & ~filters.forwarded & filters.command(cmd, prefixes=prefix)
            elif types in ['msg']:
                Filter = cmd
            handler = handlers.MessageHandler(func, Filter)
            client.add_handler(handler, group) 
        elif types in ['sched']:
            group -= -1000
            handler = scheduler.add_job(func, CronTrigger.from_crontab(cmd, 'UTC'), kwargs={'client': client}, id=str(group))
        logger.info(f'loaded: {name}')

        plugins[name] = {
            'handler': handler,
            'file': file,
            'name': name,
            'type': types,
            'help': inspect.getmodule(func).__doc__,
            'group': group,
            'cmd': cmd,
            'doc': func.__doc__,
            'ver': ver
        }

    def dct():
        return plugins

def oncmd(cmd, ver: str = '0.0') -> Callable:
    def decorator(func: Callable) -> Callable:
        PLUGINS.reg(func, 'cmd', cmd, ver)
        return func
    return decorator

def onmsg(Filter, ver: str = '0.0') -> Callable:
    def decorator(func: Callable) -> Callable:
        PLUGINS.reg(func, 'msg', Filter, ver)
        return func
    return decorator

def onsched(cron, ver: str = '0.0') -> Callable:
    def decorator(func: Callable) -> Callable:
        PLUGINS.reg(func, 'sched', cron, ver)
        return func
    return decorator

def Packages(p):
    required = set(p.split())
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed
    if not missing:
        return True
    try:
        if subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--root-user-action=ignore', *missing]) == 0:
            return True
    except Exception as e:
        logger.error(f'failed to install required: {e}')
        return False
