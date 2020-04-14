from flask import Flask
from . import api


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(test_config)
    app.register_blueprint(api.bp)

    return app


app = create_app()
