import pytest

from app import create_app
from app.db import get_db, init_db
from helpers import USERS


@pytest.fixture
def app(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.sqlite")})
    with app.app_context():
        init_db()
        db = get_db()
        db.executemany(
            "INSERT INTO users (email, token, is_admin) VALUES (?, ?, ?)",
            USERS.values(),
        )
        db.executemany(
            "INSERT INTO rooms (name, building, capacity) VALUES (?, ?, ?)",
            [("A1", "CW", 30), ("A2", "CW", 60), ("L1", "BT", 120)],
        )
        db.commit()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()
