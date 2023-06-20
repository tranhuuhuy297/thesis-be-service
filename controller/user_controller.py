from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import BaseModel

from service.prompt_service import PromptService
from service.image_service import ImageService
from service.user_service import UserService
from service.upvote_service import UpvoteService
from util.token_util import JWTBearer, encode_token
from util.wrap_util import wrap_response

api = APIRouter()
user_service = UserService()


class UserUpdate(BaseModel):
    username: str


class UserLogin(BaseModel):
    gmail: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "gmail": 'tranhuuhuy297@gmail.com',
                "password": '4db17c4a8175908bbcbe21dec3cc008e0ff6d7817a5d9e9bff6e0d99f2b6d352',
            }
        }


@api.post('/user/login')
@wrap_response
def login(user: UserLogin):
    gmail = user.dict()['gmail']
    password = user.dict()['password']
    result, code, msg = user_service.get(None, {'gmail': gmail})

    if result is not None and password == result['password']:
        access_token, expire_time = encode_token(result)
        return {'access_token': access_token, 'expire_time': expire_time, **result}, code, msg

    return None, -1, 'fail'


@api.post('/user/logout')
def logout():
    pass


@api.put('/user/{user_id}', dependencies=[Depends(JWTBearer())])
@wrap_response
def update_user(user_id: str,
                user: UserUpdate,
                ):
    update_item = user.dict()
    result, code, msg = user_service.update_user(user_id, update_item)
    return result, code, msg


@api.get('/user/{user_id}/statistics')
@wrap_response
def get_statistics(user_id: str):
    # count_prompt = PromptService().count({'user_id': user_id})
    count_image = ImageService().count({'user_id': user_id})
    count_upvote = UpvoteService().count({'user_receiver_id': user_id})

    return {'count_image': count_image, 'count_upvote': count_upvote}, 0, 'success'
