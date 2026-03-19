from flask import Flask

from app.db import close_db
from app.routes.pages import pages_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    app.teardown_appcontext(close_db)

    app.register_blueprint(pages_bp)

    return app
