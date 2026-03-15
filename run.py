#!/usr/bin/env python3
"""
Unified entry point for running locally or on Render / Heroku.
On cloud platforms, use gunicorn with app:app instead (see Procfile / Dockerfile).
This script is handy for local development.
"""
import os
import sys
from dotenv import load_dotenv

if __name__ == "__main__":
    # 1) Load .env locally; on Render/Heroku env vars are already set
    load_dotenv()

    # 2) Verify we have the creds we need
    from config import API_ID, API_HASH, BOT_TOKEN
    if not all([API_ID, API_HASH, BOT_TOKEN]):
        sys.exit("Missing API_ID, API_HASH, or BOT_TOKEN in the environment")

    # 3) Import app.py which starts both Flask + Bot
    #    Running app.py directly starts Flask dev server on PORT
    os.makedirs("sessions", exist_ok=True)

    from app import flask_app
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Flask dev server on port {port}...")
    flask_app.run(host="0.0.0.0", port=port)
