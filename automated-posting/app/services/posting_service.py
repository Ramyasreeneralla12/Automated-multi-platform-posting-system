import asyncio
from app.schemas import PlatformResult
from app.platforms import bluesky, mastodon, telegram, slack, discord

async def post_to_all_platforms(message: str) -> list[PlatformResult]:
    adapters = [
        bluesky.publish,
        mastodon.publish,
        telegram.publish,
        slack.publish,
        discord.publish,
    ]
    # Each adapter handles its own errors; gather also protects the overall request.
    outcomes = await asyncio.gather(
        *(adapter(message) for adapter in adapters),
        return_exceptions=True,
    )
    results = []
    names = ["Bluesky", "Mastodon", "Telegram", "Slack", "Discord"]
    for name, outcome in zip(names, outcomes):
        if isinstance(outcome, Exception):
            results.append(PlatformResult(
                platform=name, status="failed",
                error=f"Unexpected integration error: {str(outcome)[:300]}",
            ))
        else:
            results.append(outcome)
    return results
