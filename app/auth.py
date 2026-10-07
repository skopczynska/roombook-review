from functools import wraps

from flask import abort, g, request

from .db import query


def current_user():
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return None
    token = header.removeprefix("Bearer ")
    return query("SELECT * FROM users WHERE token = ?", (token,), one=True)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user = current_user()
        if user is None:
            abort(401)
        g.user = user
        return view(*args, **kwargs)

    return wrapped
