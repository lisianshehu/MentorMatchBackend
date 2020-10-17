from app.models.DynamoDB import DynamoDB


class User(DynamoDB):

    def __init__(self):
        super().__init__()
        self.user_table = self.tables['Users']

