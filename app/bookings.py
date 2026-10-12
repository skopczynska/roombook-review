from datetime import timedelta

from flask import Blueprint, current_app, g, jsonify, request

from .auth import login_required
from .db import execute_write, query
from .timeutil import format_utc, now_utc, parse_utc

bp = Blueprint("bookings", __name__)


def has_conflict(room_id, start, end):
    """True if [start, end) overlaps any booking of the room (half-open, R2)."""
    row = query(
        "SELECT 1 FROM bookings WHERE room_id = ? AND start_utc < ? AND end_utc > ?",
        (room_id, format_utc(end), format_utc(start)),
        one=True,
    )
    return row is not None


@bp.get("/rooms")
def list_rooms():
    rows = query("SELECT id, name, building, capacity FROM rooms ORDER BY name")
    return jsonify([dict(r) for r in rows])


@bp.get("/rooms/<int:room_id>/bookings")
def room_bookings(room_id):
    rows = query(
        "SELECT id, title, start_utc, end_utc FROM bookings "
        "WHERE room_id = ? ORDER BY start_utc",
        (room_id,),
    )
    return jsonify([dict(r) for r in rows])


@bp.post("/bookings")
@login_required
def create_booking():
    data = request.get_json(silent=True) or {}
    try:
        room_id = int(data["room_id"])
        title = str(data["title"]).strip()
        start = parse_utc(data["start"])
        end = parse_utc(data["end"])
    except (KeyError, TypeError, ValueError):
        return jsonify(error="room_id, title, start and end are required"), 400

    if not title:
        return jsonify(error="title must not be empty"), 400
    if end <= start:
        return jsonify(error="end must be after start"), 400
    if start <= now_utc():
        return jsonify(error="cannot book in the past"), 400
    if end - start > timedelta(hours=current_app.config["MAX_BOOKING_HOURS"]):
        return jsonify(error="booking too long"), 400
    if query("SELECT 1 FROM rooms WHERE id = ?", (room_id,), one=True) is None:
        return jsonify(error="room not found"), 404
    if has_conflict(room_id, start, end):
        return jsonify(error="room already booked"), 409

    cur = execute_write(
        "INSERT INTO bookings (room_id, owner_id, title, start_utc, end_utc) "
        "VALUES (?, ?, ?, ?, ?)",
        (room_id, g.user["id"], title, format_utc(start), format_utc(end)),
    )
    return jsonify(id=cur.lastrowid), 201


@bp.get("/bookings/mine")
@login_required
def my_bookings():
    rows = query(
        "SELECT id, room_id, title, start_utc, end_utc FROM bookings "
        "WHERE owner_id = ? ORDER BY start_utc",
        (g.user["id"],),
    )
    return jsonify([dict(r) for r in rows])
