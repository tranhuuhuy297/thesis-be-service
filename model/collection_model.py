from pydantic import BaseModel
from model.base_mongodb import BaseMongoModel


class Collection(BaseModel):
    user_id: str
    collection_name: str


class CollectionModel(BaseMongoModel):
    def __init__(self):
        super().__init__('thesis', 'COLLECTION')
