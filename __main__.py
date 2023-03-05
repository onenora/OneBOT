#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# 现学现卖、东拼西凑的玩意
#

from pyrogram import idle
from utils import load_plugin
from utils.config import client, logger, prefix

if __name__ == "__main__":
    load_plugin()
    client.start()
    me = client.get_me()
    logger.info(f"嗨~ {me.first_name}{me.last_name}，请在任意对话框发送 {prefix}pm help pm 获取帮助~")
    idle()
