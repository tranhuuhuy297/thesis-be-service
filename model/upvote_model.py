import pymongo
from pydantic import BaseModel

from model.base_mongodb import BaseMongoModel
from util.config_util import mongodb_config


class Upvote(BaseModel):
    user_sender_id: str
    user_receiver_id: str
    prompt_id: str


class UpvoteModel(BaseMongoModel):
    def __init__(self):
        super().__init__(mongodb_config['db_name'], mongodb_config['upvote_collection'])
        self.collection.create_index([('user_sender_id', pymongo.ASCENDING),
                                      ('user_receiver_id', pymongo.ASCENDING),
                                      ('prompt_id', pymongo.ASCENDING)],
                                     name='sender_receiver_prompt', unique=True)
