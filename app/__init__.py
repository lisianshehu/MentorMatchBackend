from flask import Flask
from flask_dynamo import Dynamo
from flask_restplus import Api

from .config import config_by_name


def create_app(config_name):

    app = Flask(__name__)
    api = Api()
    app.config.from_object(config_by_name[config_name])
    app.config['DYNAMO_TABLES'] = [
        dict(
            TableName='Users',
            KeySchema=[dict(AttributeName='user_name', KeyType='HASH')],
            AttributeDefinitions=[dict(AttributeName='user_pass', AttributeType='S'),
                                  dict(AttributeName='user_first_name', AttributeType='S'),
                                  dict(AttributeName='user_last_name', AttributeType='S')]
            # ProvisionedThroughput = dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
    )
    ]

    dynamo = Dynamo()
    with app.app_context():
        dynamo.init_app(app)

        from app.controllers.user_controller import api as user_ns
        api.add_namespace(user_ns, path='/user')

        api.init_app(app)

    return app
