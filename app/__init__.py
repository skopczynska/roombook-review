from flask import Flask

from . import db
from .bookings import bp as bookings_bp
from .search import bp as search_bp


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    if config:
        app.config.update(config)

    db.init_app(app)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(search_bp)
    return app
