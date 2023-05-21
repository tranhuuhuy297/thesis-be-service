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


@api.post('/upvote', dependencies=[Depends(JWTBearer())])
@wrap_response
def create_upvote(upvote: Upvote):
    result, code, msg = upvote_service.create(data=upvote.dict())
    return result, code, msg


@api.delete('/upvote/{upvote_id}', dependencies=[Depends(JWTBearer())])
@wrap_response
def delete_upvote(upvote_id: str):
    result, code, msg = upvote_service.delete(upvote_id)
    return result, code, msg
