import sys
import uvloop
import logging
import pathlib
import configparser
from os import path, mkdir, getenv

from pyrogram import Client

version = "4.1"

def check_dir(directory):
    if not path.exists(directory):
        mkdir(directory)

api_id = getenv("API_ID")
api_hash = getenv("API_HASH")

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

conf = configparser.ConfigParser()

if not path.exists(config):
    conf['DEFAULT'] = {'name': 'TMBot',
                        'prefix': '#',
                        'loglevel': 'INFO',
                        'pyrogram_log_level': 'WARNING',
                        'apscheduler_log_level': 'WARNING'}

    with open(config, 'w') as configfile:
        conf.write(configfile)

conf.read(config)

SESSN = conf['DEFAULT']['name']
prefix = conf['DEFAULT']['prefix']
log_level = conf['DEFAULT']['loglevel']
pyrogram_log_level = conf['DEFAULT']['pyrogram_log_level']
apscheduler_log_level = conf['DEFAULT']['apscheduler_log_level']

uvloop.install()

client = Client(
    SESSN, 
    api_id=api_id,
    api_hash=api_hash,
    workdir=session_dir
)

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
