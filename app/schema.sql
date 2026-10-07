DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS rooms;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id       INTEGER PRIMARY KEY,
    email    TEXT    NOT NULL UNIQUE,
    token    TEXT    NOT NULL UNIQUE,
    is_admin INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE rooms (
    id       INTEGER PRIMARY KEY,
    name     TEXT    NOT NULL,
    building TEXT    NOT NULL,
    capacity INTEGER NOT NULL
);

CREATE TABLE bookings (
    id        INTEGER PRIMARY KEY,
    room_id   INTEGER NOT NULL REFERENCES rooms(id),
    owner_id  INTEGER NOT NULL REFERENCES users(id),
    title     TEXT    NOT NULL,
    start_utc TEXT    NOT NULL,  -- ISO 8601 in UTC, e.g. 2026-11-05T09:00:00Z
    end_utc   TEXT    NOT NULL
);
