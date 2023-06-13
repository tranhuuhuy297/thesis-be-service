from fastapi import APIRouter, Depends
from pydantic import BaseModel

from service.upvote_service import UpvoteService
from util.token_util import JWTBearer
from util.wrap_util import wrap_response

api = APIRouter()
upvote_service = UpvoteService()


class Upvote(BaseModel):
    user_id: str
    prompt_id: str


@api.get('/upvote')
def get_upvote(user_id: str, prompt_id: str):
    result, code, msg = upvote_service.get(None, {'user_id': user_id, 'prompt_id': prompt_id})
    return result, code, msg


@api.post('/upvote', dependencies=[Depends(JWTBearer())])
@wrap_response
def create_upvote(upvote: Upvote):
    result, code, msg = upvote_service.create(data=upvote.dict())
    return result, code, msg


@api.delete('/upvote', dependencies=[Depends(JWTBearer())])
@wrap_response
def delete_upvote(upvote: Upvote):
    upvote, _, _ = upvote_service.get(None, upvote.dict())
    if upvote is None:
        return None, -1, 'not exist'
    result, code, msg = upvote_service.delete(upvote.get('id', ''))

    return result, code, msg
