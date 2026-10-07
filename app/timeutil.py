from datetime import datetime, timezone

ISO_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def now_utc():
    """Current time as a timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


def parse_utc(value):
    """Parse '2026-11-05T09:00:00Z' into an aware UTC datetime. Raises ValueError."""
    return datetime.strptime(value, ISO_FORMAT).replace(tzinfo=timezone.utc)


def format_utc(dt):
    """Format an aware datetime as an ISO 8601 UTC string (R3)."""
    return dt.astimezone(timezone.utc).strftime(ISO_FORMAT)
