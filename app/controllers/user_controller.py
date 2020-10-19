from flask import request, current_app
from flask_restplus import Resource, Api, fields, Namespace
from flask_cors import cross_origin


from app.services.user_service import UserService

api = Namespace('user')
user = api.model('user', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
    'firstname': fields.String(required=True),
    'lastname': fields.String(required=True)
})

user_service = UserService()

@api.route('/')
class User(Resource):

    def post(self):
        user_data = request.get_json()
        response = user_service.create_user(user_data=user_data)
        return response
