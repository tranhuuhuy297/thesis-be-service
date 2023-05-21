import pymongo
from pydantic import BaseModel

from model.base_mongodb import BaseMongoModel
from util.config_util import mongodb_config


class Upvote(BaseModel):
    user_id: str
    prompt_id: str


class UpvoteModel(BaseMongoModel):
    def __init__(self):
        super().__init__(mongodb_config['db_name'], mongodb_config['upvote_collection'])
        self.collection.create_index([('user_id', pymongo.ASCENDING),
                                      ('prompt_id', pymongo.ASCENDING)],
                                     name='user_prompt', unique=True)
