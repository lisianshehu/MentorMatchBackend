from flask import request, current_app
from flask_restplus import Resource, Api, fields, Namespace


from app.services.user_service import UserService

api = Namespace('user')
# user = api.model('user', {
#     'username': fields.String(required=True),
#     'password': fields.String(required=True),
#     'firstname': fields.String(required=True),
#     'lastname': fields.String(required=True)
# })

user_service = UserService()


@api.route('/signup/')
class User(Resource):

    def post(self):
        print('Post request to signup')
        user_data = request.get_json()
        response = user_service.create_user(user_data=user_data)
        return response


@api.route('/login/')
class UserLogin(Resource):

    def post(self):
        print("post request to login")
        user_data = request.get_json()
        response = user_service.login_user(user_data=user_data)
        return response