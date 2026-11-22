from datetime import datetime, timezone
from app.schemas import PlatformResult

def failed(platform: str, message: str) -> PlatformResult:
    return PlatformResult(platform=platform, status="failed", error=message)

def succeeded(platform: str, url: str | None, public: bool,
              created_at: datetime | None = None) -> PlatformResult:
    created_at = created_at or datetime.now(timezone.utc)
    return PlatformResult(
        platform=platform,
        status="success",
        posted_url=url,
        public_access=public,
        date=created_at.date().isoformat(),
        time=created_at.time().replace(microsecond=0).isoformat(),
    )
