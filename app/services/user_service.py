from app.models.user_model import User


class UserService:

    def __init__(self):
        self.user_table = User().user_table

    def create_user(self):
        self.user_table['users'].put_item(data={
            'user_id' : 'lisi98',
            'user_pass': 'cool',
            'first_name': 'Lisian',
            'last_name': 'Shehu'
        })

