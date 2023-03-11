from pyrogram import Client, idle

from core import app
from tools.initializer import init_logger
from tools.sessions import session


async def main():
    init_logger()
    await app.start()
    await idle()
    await session.close()
    await app.stop()


if __name__ == '__main__':
    app.run(main())


app = Client(
    session_name=session,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workdir="./",
    config={
        'run_workers': True,
        'workers': 4,
        'app_version': '1.2.0',
        'lang_code': 'en'
    },
)

async def main():
    init_logger()
    await app.start()
    await idle()
    await app.stop()
    await session.close()

if __name__ == '__main__':
    app.run(main())