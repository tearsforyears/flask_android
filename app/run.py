# coding=utf-8
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.secret_key = "adsgidasjfdsaodsa"

    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
