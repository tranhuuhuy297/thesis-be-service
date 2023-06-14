from pydantic import BaseModel

from model.base_mongodb import BaseMongoModel
from util.config_util import mongodb_config


class Generate(BaseModel):
    user_id: str
    hint_text: str
    result: list


class GenerateModel(BaseMongoModel):
    def __init__(self):
        super().__init__(mongodb_config['db_name'], mongodb_config['generate_collection'])
