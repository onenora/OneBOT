'''甲骨文保活'''
from utils.utils import Packages, onsched

import time
import math
import threading
import asyncio

if Packages('psutil'):
    from psutil import virtual_memory, cpu_percent

@onsched('* * * * *', ver='0.1')
async def handler(client):
    '''消耗 10% 的 cpu 和内存资源'''
    cpu = cpu_percent(3) < 10
    m = virtual_memory().total * 0.10
    mem = virtual_memory().used < m

    async def occupy():
        # https://stackoverflow.com/a/24016138
        cpu_time_utilisation = float(15)/100
        on_time = 0.1 * cpu_time_utilisation
        off_time = 0.1 * (1-cpu_time_utilisation)
        cpu = cpu_percent(3) < 10
        m = virtual_memory().total * 0.10

        while True:
            if cpu:
                start_time = time.process_time()
                while time.process_time() - start_time < on_time:
                    math.factorial(100)
                time.sleep(off_time)
            if virtual_memory().used < m:
                xxx = ' ' * int(m)

    def async_func():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(occupy())
        loop.close()

    if cpu or mem:
        thread = threading.Thread(target=async_func)
        thread.daemon = True
        thread.start()