from helpers import at, auth, book


def test_list_rooms(client):
    names = [r["name"] for r in client.get("/rooms").get_json()]
    assert names == ["A1", "A2", "L1"]


def test_create_booking(client):
    resp = book(client)
    assert resp.status_code == 201
    mine = client.get("/bookings/mine", headers=auth("alice")).get_json()
    assert len(mine) == 1 and mine[0]["title"] == "Seminar"


def test_create_requires_login(client):
    resp = client.post("/bookings", json={"room_id": 1})
    assert resp.status_code == 401


def test_rejects_end_before_start(client):
    resp = book(client, start=at(days=2, hours=2), end=at(days=2, hours=1))
    assert resp.status_code == 400


def test_rejects_booking_in_the_past(client):
    resp = book(client, start=at(days=-1), end=at(days=-1, hours=1))
    assert resp.status_code == 400


def test_rejects_too_long_booking(client):
    resp = book(client, start=at(days=2), end=at(days=2, hours=4))
    assert resp.status_code == 400


def test_overlapping_booking_is_rejected(client):
    book(client, start=at(days=2), end=at(days=2, hours=2))
    resp = book(client, user="bob", start=at(days=2, hours=1), end=at(days=2, hours=3))
    assert resp.status_code == 409


def test_back_to_back_bookings_are_allowed(client):
    book(client, start=at(days=2), end=at(days=2, hours=1))
    resp = book(client, user="bob", start=at(days=2, hours=1), end=at(days=2, hours=2))
    assert resp.status_code == 201


def test_public_schedule_has_no_personal_data(client):
    book(client)
    rows = client.get("/rooms/1/bookings").get_json()
    assert set(rows[0]) == {"id", "title", "start_utc", "end_utc"}
