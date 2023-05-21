from pydantic import BaseModel

from model.base_mongodb import BaseMongoModel
from util.config_util import mongodb_config


class Image(BaseModel):
    user_id: str
    prompt_id: str
    image_src: str


class ImageModel(BaseMongoModel):
    def __init__(self):
        super().__init__(mongodb_config['db_name'], mongodb_config['image_collection'])
