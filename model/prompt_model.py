from pydantic import BaseModel
from model.base_mongodb import BaseMongoModel


class Prompt(BaseModel):
    user_id: str
    collection_id: str
    prompt_content: str
    model: str


class PromptModel(BaseMongoModel):
    def __init__(self):
        super().__init__('thesis', 'PROMPT')
