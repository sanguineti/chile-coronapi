from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler


from coronapi.helpers.get_national_data import get_national_data
from coronapi.helpers.get_regional_data import get_regional_data
from . import api


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY="dev")

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
    app.register_blueprint(api.bp)

    get_regional_data()
    get_national_data()
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(get_regional_data, "interval", minutes=60)
    sched.add_job(get_national_data, "interval", minutes=60)
    sched.start()

    return app


app = create_app()
