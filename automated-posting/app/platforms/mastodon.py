from datetime import datetime
import httpx
from app.config import MASTODON_BASE_URL, MASTODON_ACCESS_TOKEN
from app.platforms.base import failed, succeeded

async def publish(message: str):
    name = "Mastodon"
    if not MASTODON_BASE_URL or not MASTODON_ACCESS_TOKEN:
        return failed(name, "Missing MASTODON_BASE_URL or MASTODON_ACCESS_TOKEN")
    try:
        async with httpx.AsyncClient(timeout=25) as client:
            response = await client.post(
                f"{MASTODON_BASE_URL}/api/v1/statuses",
                headers={"Authorization": f"Bearer {MASTODON_ACCESS_TOKEN}"},
                data={"status": message, "visibility": "public"},
            )
            response.raise_for_status()
            data = response.json()
            return succeeded(name, data.get("url"), True)
    except httpx.HTTPStatusError as exc:
        return failed(name, f"API returned HTTP {exc.response.status_code}: {exc.response.text[:300]}")
    except (httpx.HTTPError, ValueError) as exc:
        return failed(name, f"Request failed: {str(exc)[:300]}")
