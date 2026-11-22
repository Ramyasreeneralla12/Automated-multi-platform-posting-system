import httpx
from app.config import DISCORD_WEBHOOK_URL
from app.platforms.base import failed, succeeded

async def publish(message: str):
    name = "Discord"
    if not DISCORD_WEBHOOK_URL:
        return failed(name, "Missing DISCORD_WEBHOOK_URL")
    try:
        async with httpx.AsyncClient(timeout=25) as client:
            response = await client.post(
                DISCORD_WEBHOOK_URL,
                params={"wait": "true"},
                json={"content": message},
            )
            response.raise_for_status()
            data = response.json()
            guild_id = data.get("guild_id")
            channel_id = data.get("channel_id")
            message_id = data.get("id")
            url = (
                f"https://discord.com/channels/{guild_id}/{channel_id}/{message_id}"
                if guild_id and channel_id and message_id else None
            )
            # A Discord message's visibility depends on channel/server permissions.
            return succeeded(name, url, False)
    except httpx.HTTPStatusError as exc:
        return failed(name, f"API returned HTTP {exc.response.status_code}: {exc.response.text[:300]}")
    except (httpx.HTTPError, ValueError) as exc:
        return failed(name, f"Request failed: {str(exc)[:300]}")
