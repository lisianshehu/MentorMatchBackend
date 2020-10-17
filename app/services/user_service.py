from app.models.user_model import User


class UserService:

    def __init__(self):
        self.user_table = User().user_table

    def create_user(self, user_data):
        self.user_table.put_item(Item=user_data)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered'
        }
        return response_object, 201



