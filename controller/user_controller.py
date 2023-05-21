from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import BaseModel

from service.prompt_service import PromptService
from service.user_service import UserService
from util.token_util import JWTBearer, encode_token
from util.wrap_util import wrap_response

api = APIRouter()
user_service = UserService()


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
                username: str = Form(''),
                image: UploadFile = File(None)):
    update_item = {'username': username}
    if image is not None:
        update_item['image'] = image
    result, code, msg = user_service.update(user_id, update_item)
    return result, code, msg
