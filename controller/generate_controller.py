from fastapi import APIRouter
from pydantic import BaseModel

from service.generate_service import GenerateService
from util.token_util import JWTBearer
from util.wrap_util import wrap_response

api = APIRouter()
generate_service = GenerateService()


class Payload(BaseModel):
    user_id: str
    hint_text: str


@api.post('/generate')
@wrap_response
def create_prompt(payload: Payload):
    result, code, msg = generate_service.generate(payload.dict())
    return result, code, msg
