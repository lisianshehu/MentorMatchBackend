from flask import Flask
from flask_dynamo import Dynamo
from flask_restplus import Api
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import ( JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies )
import os

from .config import config_by_name


def create_app(config_name):

    app = Flask(__name__)
    api = Api()
    flask_bcrypt = Bcrypt()
    CORS(app)
    jwt = JWTManager()
    app.config.from_object(config_by_name[config_name])
    app.config.from_envvar('JWT_ENV_FILE')
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_SECURE'] = False
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_ENV_FILE')
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/user/login/'

    app.config['DYNAMO_TABLES'] = [
        dict(
            TableName='Users',
            KeySchema=[dict(AttributeName='username', KeyType='HASH')],
            AttributeDefinitions=[dict(AttributeName='password', AttributeType='S'),
                                  dict(AttributeName='firstname', AttributeType='S'),
                                  dict(AttributeName='lastname', AttributeType='S')]
            # ProvisionedThroughput = dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
    )
    ]

    dynamo = Dynamo()
    with app.app_context():
        # cors.init_app(app)
        dynamo.init_app(app)

        from app.controllers.user_controller import api as user_ns
        api.add_namespace(user_ns, path='/user')

        api.init_app(app)
        flask_bcrypt.init_app(app)
        jwt.init_app(app)
    return app
