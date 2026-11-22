from datetime import datetime
import httpx
from app.config import BLUESKY_HANDLE, BLUESKY_APP_PASSWORD
from app.platforms.base import failed, succeeded

async def publish(message: str):
    name = "Bluesky"
    if not BLUESKY_HANDLE or not BLUESKY_APP_PASSWORD:
        return failed(name, "Missing BLUESKY_HANDLE or BLUESKY_APP_PASSWORD")
    base = "https://bsky.social/xrpc"
    try:
        async with httpx.AsyncClient(timeout=25) as client:
            login = await client.post(
                f"{base}/com.atproto.server.createSession",
                json={"identifier": BLUESKY_HANDLE, "password": BLUESKY_APP_PASSWORD},
            )
            login.raise_for_status()
            session = login.json()
            headers = {"Authorization": f"Bearer {session['accessJwt']}"}
            now = datetime.now().astimezone().isoformat()
            response = await client.post(
                f"{base}/com.atproto.repo.createRecord",
                headers=headers,
                json={
                    "repo": session["did"],
                    "collection": "app.bsky.feed.post",
                    "record": {"$type": "app.bsky.feed.post", "text": message, "createdAt": now},
                },
            )
            response.raise_for_status()
            data = response.json()
            rkey = data["uri"].rsplit("/", 1)[-1]
            url = f"https://bsky.app/profile/{session['did']}/post/{rkey}"
            return succeeded(name, url, True)
    except httpx.HTTPStatusError as exc:
        return failed(name, f"API returned HTTP {exc.response.status_code}: {exc.response.text[:300]}")
    except (httpx.HTTPError, KeyError, ValueError) as exc:
        return failed(name, f"Request failed: {str(exc)[:300]}")
