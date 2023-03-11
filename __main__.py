#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# 现学现卖、东拼西凑的玩意
# This is a Python script for running a Pyrogram bot. Created by [author]
# 2023.03.12

from pyrogram import idle
from utils import import_plugin
from utils.config import client, logger, prefix

def get_bot_greeting():
    me = client.get_me()
    return f"Hi~ {me.first_name} {me.last_name}"

def start_bot():
    import_plugin()
    client.start()
    logger.info(f"{get_bot_greeting()}, please send '{prefix}pm help pm' to any chat to get help.")

if __name__ == "__main__":
    with client:
        start_bot()
