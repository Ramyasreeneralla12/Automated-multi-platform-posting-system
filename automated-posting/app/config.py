import os
from dotenv import load_dotenv

load_dotenv()

def env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()

BLUESKY_HANDLE = env("BLUESKY_HANDLE")
BLUESKY_APP_PASSWORD = env("BLUESKY_APP_PASSWORD")

MASTODON_BASE_URL = env("MASTODON_BASE_URL").rstrip("/")
MASTODON_ACCESS_TOKEN = env("MASTODON_ACCESS_TOKEN")

TELEGRAM_BOT_TOKEN = env("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = env("TELEGRAM_CHAT_ID")

SLACK_BOT_TOKEN = env("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = env("SLACK_CHANNEL_ID")

DISCORD_WEBHOOK_URL = env("DISCORD_WEBHOOK_URL")
