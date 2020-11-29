from flask import Flask
from flask_dynamo import Dynamo
from flask_restplus import Api
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import ( JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies )
from flask_socketio import SocketIO, join_room, leave_room
import os

from .config import config_by_name

socket = SocketIO()

@socket.on('connect')
def on_connect():
    print("connected to socket!")

@socket.on('disconnect')
def on_disconnect():
    print("disconnected to socket!")

@socket.on('join')
def on_join(data):
    print("joining private room")
    user_list = []
    print(data['target_user'])
    initiated_chat_user = data['current_user']
    target_user = data['target_user']
    user_list.append(initiated_chat_user)
    user_list.append(target_user)
    user_list = sorted(user_list)
    print(user_list)
    room_based_off_users = ''.join(user_list)
    print(room_based_off_users)
    join_room(room_based_off_users)


@socket.on('send_message')
def on_message(data):
    user_list = sorted([data['current_user'], data['target_user']])
    target_room = ''.join(user_list)
    message = data['message']
    print('sending message: {}'.format(message))
    print(target_room)
    socket.emit('message', {'message': message, 'user': data['current_user']}, room=target_room)


def create_app(config_name):

    app = Flask(__name__)
    app.host = 'localhost'
    api = Api()
    flask_bcrypt = Bcrypt()
    CORS(app)
    jwt = JWTManager()
    app.config.from_object(config_by_name[config_name])
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
        socket.init_app(app, cors_allowed_origins="*")

    return app
