import os
from flask_testing import TestCase
from app.app_factory import create_app
from app.extensions import db
from app.settings import FileConfiguration
from tests import config_test

_basedir = os.path.abspath(os.path.dirname(__file__))


def create_test_app():

    config = FileConfiguration(config_test)
    application = create_app(config)
    application.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(_basedir, 'test_app.db')

    return application


class BaseTestCase(TestCase):

    def create_app(self):
        return create_test_app()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        try:
            os.remove(os.path.join(_basedir, 'test_app.db'))
        except OSError:
            pass
