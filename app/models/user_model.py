from app.models.DynamoDB import DynamoDB
from flask_bcrypt import generate_password_hash, check_password_hash


class User(DynamoDB):

    def __init__(self):
        super().__init__()
        self.user_table = self.tables['Users']

    def hash_password(self, password):
        return generate_password_hash(password).decode()

    def check_password(self, hashed_password, password):
        print(check_password_hash(hashed_password, password))
        return check_password_hash(hashed_password, password)
