from pydantic import BaseModel
from model.base_mongodb import BaseMongoModel


class Upvote(BaseModel):
    user_id: str
    collection_id: str


class UpvoteModel(BaseMongoModel):
    def __init__(self):
        super().__init__('thesis', 'UPVOTE')
