from app.models.DynamoDB import DynamoDB
from flask_bcrypt import generate_password_hash, check_password_hash


class User(DynamoDB):

    def __init__(self):
        super().__init__()
        self.user_table = self.tables['Users']
        self.password_hashed = None

    def hash_password(self, password):
        self.password_hashed = generate_password_hash(password).decode()

    def check_password_hash(self, password):
        return check_password_hash(self.password_hashed, password)
