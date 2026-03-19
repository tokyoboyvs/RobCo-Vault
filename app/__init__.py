from flask import Flask

from app.db import init_app
from app.routes.pages import pages_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    init_app(app)

    app.register_blueprint(pages_bp)

    return app
