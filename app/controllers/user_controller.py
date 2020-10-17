from flask import request
from flask_restplus import Resource, Api, fields, Namespace

from app.services.user_service import UserService

api = Namespace('user')
user = api.model('user', {
    'user_id': fields.String(required=True),
    'user_pass': fields.String(required=True),
    'user_first_name': fields.String(required=True),
    'user_last_name': fields.String(required=True)
})

user_service = UserService()

@api.route('/')
class User(Resource):
    def post(self):
        # user_data = request.get_json()
        user_service.create_user()

