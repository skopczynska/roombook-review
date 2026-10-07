import sqlite3
from pathlib import Path

from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_exc=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def query(sql, params=(), one=False):
    rows = get_db().execute(sql, params).fetchall()
    if one:
        return rows[0] if rows else None
    return rows


def execute_write(sql, params=()):
    """Run a single INSERT/UPDATE/DELETE and commit it immediately."""
    db = get_db()
    cur = db.execute(sql, params)
    db.commit()
    return cur


def init_db():
    schema = Path(__file__).with_name("schema.sql").read_text()
    get_db().executescript(schema)


def init_app(app):
    app.teardown_appcontext(close_db)
