import httpx
from datetime import datetime, timezone
from app.config import SLACK_BOT_TOKEN, SLACK_CHANNEL_ID
from app.platforms.base import failed, succeeded

async def publish(message: str):
    name = "Slack"
    if not all([SLACK_BOT_TOKEN, SLACK_CHANNEL_ID]):
        return failed(name, "Missing SLACK_BOT_TOKEN or SLACK_CHANNEL_ID")
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    try:
        async with httpx.AsyncClient(timeout=25) as client:
            response = await client.post(
                "https://slack.com/api/chat.postMessage",
                headers=headers,
                json={"channel": SLACK_CHANNEL_ID, "text": message},
            )
            response.raise_for_status()
            data = response.json()
            if not data.get("ok"):
                return failed(name, f"Slack API error: {data.get('error', 'unknown_error')}")

            permalink = None
            link_response = await client.get(
                "https://slack.com/api/chat.getPermalink",
                headers=headers,
                params={"channel": SLACK_CHANNEL_ID, "message_ts": data["ts"]},
            )
            if link_response.is_success:
                link_data = link_response.json()
                if link_data.get("ok"):
                    permalink = link_data.get("permalink")
            return succeeded(name, permalink, bool(permalink), datetime.now(timezone.utc))
    except httpx.HTTPStatusError as exc:
        return failed(name, f"API returned HTTP {exc.response.status_code}: {exc.response.text[:300]}")
    except (httpx.HTTPError, KeyError, ValueError) as exc:
        return failed(name, f"Request failed: {str(exc)[:300]}")
