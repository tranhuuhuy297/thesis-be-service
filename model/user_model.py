from pydantic import BaseModel
from model.base_mongodb import BaseMongoModel


class User(BaseModel):
    user_name: str
    gmail: str
    password: str


class UserModel(BaseMongoModel):
    def __init__(self):
        super().__init__('thesis', 'USER')
