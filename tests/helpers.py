from datetime import timedelta

from app.timeutil import format_utc, now_utc

# name -> (email, token, is_admin)
USERS = {
    "alice": ("alice@example.edu", "token-alice", 0),
    "bob": ("bob@example.edu", "token-bob", 0),
    "admin": ("admin@example.edu", "token-admin", 1),
}


def auth(user):
    return {"Authorization": f"Bearer {USERS[user][1]}"}


def at(days=0, hours=0):
    """A future point in time, rounded down to the full hour, as an ISO UTC string."""
    base = now_utc().replace(minute=0, second=0, microsecond=0)
    return format_utc(base + timedelta(days=days, hours=hours))


def book(client, user="alice", room_id=1, start=None, end=None, title="Seminar"):
    return client.post(
        "/bookings",
        headers=auth(user),
        json={
            "room_id": room_id,
            "title": title,
            "start": start or at(days=2),
            "end": end or at(days=2, hours=1),
        },
    )
