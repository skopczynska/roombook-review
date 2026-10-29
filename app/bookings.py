from datetime import datetime, timedelta

from flask import Blueprint, current_app, g, jsonify, request

from .auth import login_required
from .db import execute_write, query
from .notify import notify_cancellation
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
        "SELECT b.id, b.title, b.start_utc, b.end_utc, u.email AS owner_email "
        "FROM bookings b JOIN users u ON u.id = b.owner_id "
        "WHERE b.room_id = ? ORDER BY b.start_utc",
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


@bp.delete("/bookings/<int:booking_id>")
@login_required
def cancel_booking(booking_id):
    """Cancel a booking (R4, R5) and notify its owner (R7)."""
    booking = query(
        "SELECT b.*, u.email AS owner_email FROM bookings b "
        "JOIN users u ON u.id = b.owner_id WHERE b.id = ?",
        (booking_id,),
        one=True,
    )
    if booking is None:
        return jsonify(error="booking not found"), 404

    start = datetime.fromisoformat(booking["start_utc"].rstrip("Z"))
    if start <= datetime.now():
        return jsonify(error="booking has already started"), 400

    execute_write("DELETE FROM bookings WHERE id = ?", (booking_id,))

    if booking["owner_id"] != g.user["id"] and not g.user["is_admin"]:
        return jsonify(error="only the owner or an admin can cancel"), 403

    notify_cancellation(booking, booking["owner_email"])
    return "", 204
