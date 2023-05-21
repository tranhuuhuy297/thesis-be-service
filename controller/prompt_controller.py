import re

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import BaseModel

from service.prompt_service import PromptService
from util.token_util import JWTBearer
from util.wrap_util import wrap_response

api = APIRouter()
prompt_service = PromptService()


class Prompt(BaseModel):
    user_id: str
    prompt: str
    negative_prompt: str


@api.get('/prompt')
@wrap_response
def get_list_prompt(search: str = '', page: int = 0, size: int = 10):
    _filter = {'prompt': re.compile(search, re.IGNORECASE)}
    result, code, msg = prompt_service.get_list(_filter, page, size)
    return result, code, msg


@api.get('/prompt/user/{user_id}')
@wrap_response
def get_list_prompt_by_user(user_id: str, search: str = '', page: int = 0, size: int = 10):
    _filter = {'prompt': re.compile(search, re.IGNORECASE), 'user_id': user_id}
    result, code, msg = prompt_service.get_list(_filter, page, size)
    return result, code, msg


@api.get('/prompt/{prompt_id}')
@wrap_response
def get_prompt(prompt_id: str):
    result, code, msg = prompt_service.get(prompt_id, {}, deep=True)
    return result, code, msg


@api.delete('/prompt/{prompt_id}', dependencies=[Depends(JWTBearer())])
@wrap_response
def delete_prompt(prompt_id: str):
    result, code, msg = prompt_service.delete(prompt_id)
    return result, code, msg


@api.post('/prompt', dependencies=[Depends(JWTBearer())])
@wrap_response
def create_prompt(prompt: Prompt):
    result, code, msg = prompt_service.create(prompt.dict())
    return result, code, msg
