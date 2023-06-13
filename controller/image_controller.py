from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import BaseModel

from service.image_service import ImageService
from util.token_util import JWTBearer
from util.wrap_util import wrap_response

api = APIRouter()
image_service = ImageService()

MAX_IMAGE = 1


@api.get('/image')
@wrap_response
def get_list_image(page: int = 0, size: int = 20):
    result, code, msg = image_service.get_list({}, page, size, deep=True)
    return result, code, msg


@api.delete('/image/{image_id}')
@wrap_response
def delete_image(image_id: str):
    result, code, msg = image_service.delete(image_id)
    return result, code, msg


@api.post('/image')
@wrap_response
def create_image(user_id: str = Form(...),
                 prompt_id: str = Form(...),
                 image: UploadFile = File(...)):
    result, code, msg = image_service.create({
        'user_id': user_id, 'prompt_id': prompt_id, 'image': image
    })

    return result, code, msg


@api.get('/image/user/{user_id}')
@wrap_response
def get_list_image_by_user(user_id: str, page: int = 0, size: int = 20):
    result, code, msg = image_service.get_list({'user_id': user_id}, page, size, deep=True)
    return result, code, msg
