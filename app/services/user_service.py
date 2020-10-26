from app.models.user_model import User


class UserService:

    def __init__(self):
        self.user_table = User().user_table

    def create_user(self, user_data):
        item_response = self.user_table.get_item(Key={'user_name': user_data['user_name']})
        if 'Item' in item_response:
            return {'status': 'failed', 'message': 'User already exists'}

        user_data['password'] = User().hash_password(user_data['password'])
        self.user_table.put_item(Item=user_data)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered'
        }
        return response_object, 201
