from flask import Flask
from . import api
from flask_cors import CORS


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY="dev")
    CORS(app)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
    app.register_blueprint(api.bp)

    return app


app = create_app()
