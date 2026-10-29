from helpers import at, auth, book


def make_booking(client, user="alice", days=3):
    resp = book(client, user=user, start=at(days=days), end=at(days=days, hours=2))
    assert resp.status_code == 201
    return resp.get_json()["id"]


def test_owner_can_cancel(client):
    booking_id = make_booking(client)
    resp = client.delete(f"/bookings/{booking_id}", headers=auth("alice"))
    assert resp.status_code == 204
    assert client.get("/bookings/mine", headers=auth("alice")).get_json() == []


def test_admin_can_cancel(client):
    booking_id = make_booking(client)
    resp = client.delete(f"/bookings/{booking_id}", headers=auth("admin"))
    assert resp.status_code == 204


def test_other_user_cannot_cancel(client):
    booking_id = make_booking(client)
    resp = client.delete(f"/bookings/{booking_id}", headers=auth("bob"))
    assert resp.status_code == 403


def test_cancel_unknown_booking(client):
    resp = client.delete("/bookings/999", headers=auth("alice"))
    assert resp.status_code == 404


def test_cancel_requires_login(client):
    booking_id = make_booking(client)
    assert client.delete(f"/bookings/{booking_id}").status_code == 401
