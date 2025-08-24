import logging
import os
import sys

from flask import Flask

from app import api, root, probe, auth


def configure_logging():
    file_handler = logging.FileHandler(filename='flask-app.log')
    stdout_handler = logging.StreamHandler(sys.stdout)
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - '
               '%(message)s',
        handlers=[stdout_handler, file_handler])


def create_app():
    configure_logging()
    app = Flask(__name__, instance_relative_config=True)

    # Configure session with a more secure secret key
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', os.urandom(16))
    )
    app.config.from_pyfile('config.py', silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(auth.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(root.bp)
    app.register_blueprint(probe.bp)
    return app
