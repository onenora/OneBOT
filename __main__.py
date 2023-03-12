#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# 现学现卖、东拼西凑的玩意
# This is a Python script for running a Pyrogram bot. Created by [author]
# 2023.03.13
# 导入“pyrogram”库中的“idle”函数
# 导入自定义函数“load_plugin”
# 导入自定义配置变量“client”，“logger”和“prefix”
from pyrogram import idle
from utils import load_plugin
from utils.config import client, logger, prefix

# 定义一个名为“main”的函数
def main():
    # 调用自定义函数“load_plugin”，加载插件/命令
    load_plugin()
    # 使用“client”创建一个会话
    with client:
        # 获取当前“client”所属账号信息
        me = client.get_me()
        # 在日志中输出欢迎词
        logger.info(f"嗨~ {me.first_name}{me.last_name}，请在任意对话框发送 {prefix}pm help pm 获取帮助~")
        # 让会话保持运行状态
        idle()
        
# 在运行当前脚本时，执行“main”函数
if __name__ == '__main__':
    main()
