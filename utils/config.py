import sys
import uvloop
import logging
import pathlib
import configparser
from os import path, mkdir, getenv

from pyrogram import Client
from utils.convopyro import Conversation
version = "4.5.4"
# 创建文件夹的函数，如果不存在则创建
def check_dir(directory):
    if not path.exists(directory):
        mkdir(directory)
# 从环境变量中获取API ID和API HASH的值
api_id = getenv("API_ID")
api_hash = getenv("API_HASH")
# 设置工作目录
base_dir = pathlib.Path.cwd()
data_dir = path.join(base_dir, 'data')
plugins_dir = path.join(data_dir, 'plugins')
session_dir = path.join(data_dir, 'session')
tmp_dir = path.join(data_dir, 'tmp')
config = path.join(data_dir, 'config.ini')
check_dir(data_dir)
check_dir(plugins_dir)
check_dir(session_dir)
check_dir(tmp_dir)
# 创建配置文件对象
conf = configparser.ConfigParser()
# 如果配置文件不存在，创建默认配置文件
if path.exists(config):
    with open(config, 'r', encoding='utf-8') as f:
            text = f.read()

    text = text.replace("[DEFAULT]", "[TMBot]")
    with open(config, 'w', encoding='UTF-8') as f:
        f.write(text)

if not path.exists(config):
    conf['TMBot'] = {'desc': 'TMBot 的配置',
                        'name': 'TMBot',
                        'prefix': '#',
                        'loglevel': 'INFO',
                        'pyrogram_log_level': 'WARNING',
                        'apscheduler_log_level': 'WARNING'}

    with open(config, 'w') as configfile:
        conf.write(configfile)
 # 读取配置文件
conf.read(config)

SESSN = conf['TMBot']['name']
prefix = conf['TMBot']['prefix']
log_level = conf['TMBot']['loglevel']
pyrogram_log_level = conf['TMBot']['pyrogram_log_level']
apscheduler_log_level = conf['TMBot']['apscheduler_log_level']

uvloop.install()

client = Client(
    SESSN, 
    api_id=api_id,
    api_hash=api_hash,
    workdir=session_dir
)

Conversation(client)

def loglevel(level):
    if level == 'WARNING':
        return logging.WARNING
    elif level == 'INFO':
        return logging.INFO
    elif level == 'DEBUG':
        return logging.DEBUG
    else:
        return logging.INFO

logging.basicConfig(level=loglevel(log_level),
                    format='[%(name)s - %(asctime)s] - [%(levelname)s]: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger("pyrogram").setLevel(loglevel(pyrogram_log_level))
logging.getLogger("apscheduler").setLevel(loglevel(apscheduler_log_level))
logger = logging.getLogger(SESSN)
