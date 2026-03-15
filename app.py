from flask import Flask
import os
import asyncio
import threading
import importlib
import logging

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)

# --- Flask health-check app (Render needs a listening port) ---
flask_app = Flask(__name__)

# For gunicorn compatibility: expose as 'app'
app = flask_app


@flask_app.route("/")
def health():
    return "Bot is running!", 200


@flask_app.route("/health")
def health_check():
    return "OK", 200


# --- Pyrogram bot startup (runs in a background thread) ---
def start_bot():
    """Start the Pyrogram bot in its own asyncio event loop."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def _boot():
        from pyrogram import idle
        from Extractor.modules import ALL_MODULES
        import Extractor

        await Extractor.app.start()
        getme = await Extractor.app.get_me()
        Extractor.BOT_ID = getme.id
        Extractor.BOT_USERNAME = getme.username
        if getme.last_name:
            Extractor.BOT_NAME = getme.first_name + " " + getme.last_name
        else:
            Extractor.BOT_NAME = getme.first_name

        for module in ALL_MODULES:
            importlib.import_module("Extractor.modules." + module)

        print("» Bot deployed successfully!")
        await idle()

    try:
        loop.run_until_complete(_boot())
    except Exception as e:
        print(f"Bot error: {e}")
    finally:
        loop.close()


# Auto-start the bot when this module is loaded (by gunicorn or directly)
_bot_thread = threading.Thread(target=start_bot, daemon=True)
_bot_thread.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    flask_app.run(host="0.0.0.0", port=port)
