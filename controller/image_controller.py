import os
from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from util import pinecone_user_prompt
from PIL import Image as PILImage


from model.image_model import Image

from service.image_service import ImageService
from util.image_util import compress_image
from util.token_util import JWTBearer
from util.wrap_util import wrap_authorization, wrap_get_list_response, wrap_response

api = APIRouter()
image_service = ImageService()

MAX_IMAGE = 1


@api.get('/image')
@wrap_get_list_response
def get_list_image(user_id: str = None, page: int = 0, size: int = 20):
    _filter = {}
    if user_id != None:
        _filter['user_id'] = user_id
    result, count, code, msg = image_service.get_list(_filter, page, size, deep=False)
    result = [image_service.get_extra_info({**item}) for item in result]
    return result, count, code, msg


@api.delete('/image/{image_id}', dependencies=[Depends(JWTBearer())])
@wrap_response
@wrap_authorization
def delete_image(req: Request,  image_id: str, user_id: str):
    _id, code, msg = image_service.delete(image_id)
    if _id is not None:
        pinecone_user_prompt.delete([_id])
    return _id, code, msg


@api.post('/image', dependencies=[Depends(JWTBearer())])
@wrap_response
@wrap_authorization
def create_image(
        req: Request,
        user_id: str = Form(...),
        prompt: str = Form(...),
        negative_prompt: str = Form(None),
        image: UploadFile = File(...)):
    result, code, msg = image_service.create({
        'user_id': user_id,
        'prompt': prompt,
        'negative_prompt': negative_prompt,
        'image': image
    })
    return result, code, msg


@api.get('/image/{image_id}')
@wrap_response
def get_image(image_id: str):
    result, code, msg = image_service.get(image_id)
    return result, code, msg


@api.get('/image/search/semantic-search')
@wrap_response
def search_semantic(query: str):
    user_prompt = pinecone_user_prompt.query(query=query)
    user_prompt = [{**item, **item['metadata']} for item in user_prompt]

    # only get result which has score > 0.5
    result = [image_service.get_extra_info({**item}) for item in user_prompt if item.get('score', 0) > 0.5]

    return result, 0, 'success'


@api.post('/upsert_after_generate')
@wrap_response
def upsert_after_generate(user_id: str = Form(...), prompt: str = Form(...), image_src: str = Form(...)):
    file_name = compress_image(image_src)
    if file_name is None:
        return None, -1, 'error compress image'

    result, code, msg = image_service.create({
        'user_id': user_id,
        'prompt': prompt,
        'image': {
            'file': PILImage.open(file_name),
            'filename': file_name
        }
    })

    os.remove(file_name)
    return result, code, msg
