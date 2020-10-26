from flask import Flask
from flask_dynamo import Dynamo
from flask_restplus import Api
from flask_cors import CORS
from flask_bcrypt import Bcrypt

from .config import config_by_name


def create_app(config_name):

    app = Flask(__name__)
    api = Api()
    bcrypt = Bcrypt()
    CORS(app)
    app.config.from_object(config_by_name[config_name])
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
        dynamo.init_app(app)

        from app.controllers.user_controller import api as user_ns
        api.add_namespace(user_ns, path='/user')

        api.init_app(app)
        bcrypt.init_app(app)
    return app
