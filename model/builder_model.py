import pymongo
from pydantic import BaseModel

from model.base_mongodb import BaseMongoModel
from util.config_util import mongodb_config


class BuilderType(BaseModel):
    parent: str
    name: str
    short_name: str


class BuilderValue(BaseModel):
    parent: str
    name: str
    image_src: str


class BuilderTypeModel(BaseMongoModel):
    def __init__(self):
        super().__init__(mongodb_config['db_name'], mongodb_config['builder_type_collection'])


class BuilderValueModel(BaseMongoModel):
    def __init__(self):
        super().__init__(mongodb_config['db_name'], mongodb_config['builder_value_collection'])
        self.collection.create_index([('parent', pymongo.ASCENDING),
                                      ('name', pymongo.ASCENDING)],
                                     name='parent_name', unique=True)
