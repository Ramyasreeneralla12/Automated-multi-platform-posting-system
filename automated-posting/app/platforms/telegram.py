import httpx
from app.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from app.platforms.base import failed, succeeded

async def publish(message: str):
    name = "Telegram"
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return failed(name, "Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID")
    try:
        async with httpx.AsyncClient(timeout=25) as client:
            response = await client.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "link_preview_options": {"is_disabled": False}},
            )
            response.raise_for_status()
            data = response.json()
            if not data.get("ok"):
                return failed(name, data.get("description", "Telegram rejected the message"))
            result = data["result"]
            chat = result["chat"]
            username = chat.get("username")
            url = f"https://t.me/{username}/{result['message_id']}" if username else None
            return succeeded(name, url, bool(username))
    except httpx.HTTPStatusError as exc:
        return failed(name, f"API returned HTTP {exc.response.status_code}: {exc.response.text[:300]}")
    except (httpx.HTTPError, KeyError, ValueError) as exc:
        return failed(name, f"Request failed: {str(exc)[:300]}")
