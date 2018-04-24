import os
from flask import Flask
from flask_migrate import Migrate

from app.extensions import db


def create_app(config_filename):
    """
    Factory to create the application using a file

    :param config_filename: The name of the file that will be used for configuration.
    :return: The created application
    """
    print("Creating flask app")
    app = Flask(__name__)
    app.config.from_object(config_filename)

    setup_db(app)

    @app.route("/")
    def hello():
        return "Hello World!: DEBUG: {}".format(app.config["DEBUG"])

    return app


def setup_db(app):
    if os.environ.get("APP_DB_ENGINE", None) == "postgresql":
        app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
            app.config["DB_USER"],
            app.config["DB_PASSWORD"],
            app.config["DB_SERVICE_NAME"],
            app.config["DB_PORT"],
            app.config["DB_NAME"]
        )
    else:
        _basedir = os.path.abspath(os.path.dirname(__file__))
        app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(_basedir, 'webapp.db')

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    Migrate(app, db)
    db.app = app
