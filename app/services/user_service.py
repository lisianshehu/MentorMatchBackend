from app.models.user_model import User
from flask_jwt_extended import create_access_token
import datetime


class UserService:

    def __init__(self):
        self.user_model = User()
        self.user_table = self.user_model.user_table

    def get_user_password(self, user_name):
        item_response = self.user_table.get_item(Key={'user_name': user_name})
        if 'Item' in item_response:
            stored_hashed_password = item_response['Item']['password']
            return stored_hashed_password

        return None

    def create_user(self, user_data):
        item_response = self.user_table.get_item(Key={'user_name': user_data['user_name']})
        if 'Item' in item_response:
            return {'status': 'failed', 'message': 'User already exists'}

        user_data['password'] = self.user_model.hash_password(user_data['password'])
        self.user_table.put_item(Item=user_data)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered'
        }
        return response_object, 201

    def login_user(self, user_data):
        user_name = user_data['user_name']
        password = user_data['password']
        item_response = self.user_table.get_item(Key={'user_name': user_data['user_name']})
        print(type(password))
        try:
            if 'Item' in item_response and self.user_model.check_password_hash(self.get_user_password(user_name), str(password)):
                expires = datetime.timedelta(days=7)
                auth_token = create_access_token(identity=str(user_name), expires_delta=expires)
                if auth_token:
                    return {'status': 'success', 'message': 'Successfully logged-in'}, 200

            return {'status': 'failed', 'message': 'Failed logged-in'}
        except Exception as e:
            return {'status': 'failed', 'message': 'Failed logged-in: '.format(e)}

