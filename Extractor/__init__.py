import asyncio
import logging
import os
import sys
from pyromod import listen
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

# Create sessions directory if it doesn't exist
if not os.path.exists("sessions"):
    os.makedirs("sessions")

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)

# Validate credentials before creating the client
if not API_ID or not API_HASH or not BOT_TOKEN:
    print("FATAL: API_ID, API_HASH, and BOT_TOKEN environment variables are required.")
    print(f"  API_ID set: {bool(API_ID)}")
    print(f"  API_HASH set: {bool(API_HASH)}")
    print(f"  BOT_TOKEN set: {bool(BOT_TOKEN)}")
    sys.exit(1)

app = Client(
    "Extractor",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workdir="sessions",
    workers=200,
    in_memory=True,
)

# Initialize pyromod attributes
app.listening = {}
app.listening_cb = {}
app.waiting_input = {}

# Global bot info — populated during startup in __main__.py
BOT_ID = None
BOT_NAME = None
BOT_USERNAME = None
