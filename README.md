# RoomBook

A small REST API for booking university seminar rooms (Flask + SQLite).
Business rules are listed in [REQUIREMENTS.md](REQUIREMENTS.md).

## Run the tests

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -q
```

## Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/rooms` | – | list rooms |
| GET | `/rooms/<id>/bookings` | – | public schedule of a room |
| POST | `/bookings` | user | create a booking |
| GET | `/bookings/mine` | user | bookings of the current user |

Authentication: `Authorization: Bearer <token>` (tokens are stored in the `users` table).
