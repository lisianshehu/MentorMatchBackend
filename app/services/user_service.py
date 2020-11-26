from app.models.user_model import User
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies
import datetime


class UserService:

    def __init__(self):
        self.user_model = User()
        self.user_table = self.user_model.user_table

    def get_user_password(self, user_name):
        item_response = self.user_table.get_item(Key={'user_name': user_name})
        if 'Item' in item_response:
            stored_hashed_password = item_response['Item']['password']
            print(stored_hashed_password)
            return stored_hashed_password

        raise Exception("User does not exist")

    def create_user(self, user_data):
        item_response = self.user_table.get_item(Key={'user_name': user_data['user_name']})
        if 'Item' in item_response:
            return {'status': 'failed', 'message': 'User already exists'}
        user_data['loginStatus'] = False
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
        item_response = self.user_table.get_item(Key={'user_name': user_name})
        print(item_response)
        if 'Item' in item_response and self.user_model.check_password(self.get_user_password(user_name), password):
            expires = datetime.timedelta(days=7)
            auth_token = create_access_token(identity=str(user_name), expires_delta=expires)
            print("here: ", auth_token)
            if auth_token is not None:
                self.user_table.update_item(
                    Key={
                        'user_name': user_name,
                    },
                    UpdateExpression="set loginStatus = :updated",
                    ExpressionAttributeValues={
                        ':updated': True,
                    }
                )
                response = {'status': 'success', 'message': 'Successfully logged-in', 'token': auth_token}
                print(response)
                return response, 200

        return {'status': 'failed', 'message': 'Failed logged-in'}

    def logout_user(self, user_data):
        user_name = user_data['user_name']
        table_response = self.user_table.update_item(
            Key={
                'user_name': user_name,
            },
            UpdateExpression="set loginStatus = :updated",
            ExpressionAttributeValues={
                ':updated': False,
            }
        )
        print(table_response)
        response = {'status': 'success', 'message': 'Logged-out!'}
        return response

    def get_online_status(self, user_to_search):
        table_response = self.user_table.get_item(Key={'user_name': user_to_search})
        if table_response['Item']['loginStatus'] == True:
            print('Online {}'.format(table_response['Item']['loginStatus']))
            return True

        return False

    def search_user(self, user_to_search):
        item_response = self.user_table.get_item(Key={'user_name': user_to_search})
        if 'Item' in item_response:
            response = {'status': 'success', 'message': 'Search successful', 'username': item_response['Item']['user_name']}
            if self.get_online_status(user_to_search):
                response['loginStatus'] = True
                return response
        else:
            return {'status': 'failed', 'message': 'User does not exist', 'loginStatus': True}


