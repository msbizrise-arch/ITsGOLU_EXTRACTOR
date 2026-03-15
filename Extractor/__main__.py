import asyncio
import importlib
import signal
from pyrogram import idle
from Extractor.modules import ALL_MODULES
import Extractor

loop = asyncio.get_event_loop()

# Graceful shutdown
should_exit = asyncio.Event()

def shutdown():
    print("Shutting down gracefully...")
    should_exit.set()

signal.signal(signal.SIGTERM, lambda s, f: loop.create_task(should_exit.set()))
signal.signal(signal.SIGINT,  lambda s, f: loop.create_task(should_exit.set()))

async def sumit_boot():
    # Start the bot and fetch info HERE (not at import time)
    await Extractor.app.start()
    getme = await Extractor.app.get_me()
    Extractor.BOT_ID       = getme.id
    Extractor.BOT_USERNAME = getme.username
    if getme.last_name:
        Extractor.BOT_NAME = getme.first_name + " " + getme.last_name
    else:
        Extractor.BOT_NAME = getme.first_name

    # Load all modules after bot is ready
    for module in ALL_MODULES:
        importlib.import_module("Extractor.modules." + module)

    print("» ʙᴏᴛ ᴅᴇᴘʟᴏʏ sᴜᴄᴄᴇssғᴜʟʟʏ ✨ 🎉")
    await idle()  # keeps the bot alive

    print("» ɢᴏᴏᴅ ʙʏᴇ ! sᴛᴏᴘᴘɪɴɢ ʙᴏᴛ.")

if __name__ == "__main__":
    try:
        loop.run_until_complete(sumit_boot())
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        pending = asyncio.all_tasks(loop)
        for task in pending:
            task.cancel()
        loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        loop.close()
        print("Loop closed.")
