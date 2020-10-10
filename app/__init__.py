from flask import Flask
from boto3 import dynamodb

from .config import config_by_name


def create_app(config_name):
    # other configurations such as DB(Dynamo)

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    return app
