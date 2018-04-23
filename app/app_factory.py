from flask import Flask


def create_app(config_filename):
    """
    Factory to create the application using a file

    :param config_filename: The name of the file that will be used for configuration.
    :return: The created application
    """
    print("Creating flask app")
    app = Flask(__name__)
    app.config.from_object(config_filename)

    @app.route("/")
    def hello():
        return "Hello World!: DEBUG: {}".format(app.config["DEBUG"])

    return app
