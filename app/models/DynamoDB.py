import boto3
from flask import current_app


class DynamoDB:

    def __init__(self):
        self.tables = current_app.extensions['dynamodb']

