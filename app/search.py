"""Free-room search (RB-42)."""
from flask import Blueprint, jsonify, request

from .db import get_db
from .timeutil import format_utc, parse_utc

bp = Blueprint("search", __name__)


@bp.get("/rooms/free")
def free_rooms():
    """Return the rooms that are free during the whole interval [start, end) (R8)."""
    try:
        start = parse_utc(request.args["start"])
        end = parse_utc(request.args["end"])
    except (KeyError, ValueError):
        return jsonify(error="start and end are required (UTC, ISO 8601)"), 400
    if end <= start:
        return jsonify(error="end must be after start"), 400

    db = get_db()
    s, e = format_utc(start), format_utc(end)

    # A room is busy if one of its bookings starts or ends inside the window
    busy = db.execute(
        "SELECT DISTINCT room_id FROM bookings "
        "WHERE (start_utc >= ? AND start_utc < ?) "
        "   OR (end_utc > ? AND end_utc <= ?)",
        (s, e, s, e),
    ).fetchall()
    busy_ids = [row["room_id"] for row in busy]

    sql = "SELECT id, name, building, capacity FROM rooms"
    conditions, params = [], []
    if busy_ids:
        placeholders = ",".join("?" * len(busy_ids))
        conditions.append(f"id NOT IN ({placeholders})")
        params.extend(busy_ids)

    building = request.args.get("building")
    if building:
        conditions.append(f"building = '{building}'")

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    rows = db.execute(sql + " ORDER BY name", params).fetchall()
    return jsonify([dict(r) for r in rows])
