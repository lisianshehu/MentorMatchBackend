from flask import current_app


class DynamoDB:

    def __init__(self):
        self.tables = current_app.extensions['dynamo'].tables
        print(self.tables)

