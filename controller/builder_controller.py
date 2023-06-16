from typing import Literal

from fastapi import APIRouter, Depends, UploadFile, Form
from pydantic import BaseModel

from service.builder_service import BuilderTypeService, BuilderValueService
from util.token_util import JWTBearer
from util.wrap_util import wrap_response

api = APIRouter()
builder_type_service = BuilderTypeService()
builder_value_service = BuilderValueService()


class BuilderType(BaseModel):
    parent: Literal['Text', 'Style', 'Param']
    name: str
    short_name: str


@api.get('/builder_type')
@wrap_response
def get_list_builder_type(page: int = 0, size: int = 100, parent: str = 'Style'):
    result, code, msg = BuilderTypeService().get_list({'parent': parent}, page, size)
    return result, code, msg


@api.post('/builder_type')
@wrap_response
def create_builder_type(builder_type: BuilderType):
    item = {key: value.title() for (key, value) in builder_type.dict().items()}
    if 'short_name' in builder_type.dict():
        item['short_name'] = builder_type.dict()['short_name']
    result, code, msg = BuilderTypeService().create(item)
    return result, code, msg


@api.delete('/builder_type/{builder_type_id}')
@wrap_response
def delete_builder_type(builder_type_id: str):
    result, code, msg = BuilderTypeService().delete(builder_type_id)
    return result, code, msg


# Builder Value ------------------------------------------------------------------------------------------

@api.get('/builder_value')
@wrap_response
def get_list_builder_value(builder_type: str = 'Layouts', page: int = 0, size: int = 100):
    _filter = {'parent': builder_type}
    result, code, msg = BuilderValueService().get_list(_filter, page, size)
    return result, code, msg


@api.post('/builder_value')
@wrap_response
def create_builder_value(image: UploadFile = Form(...), parent: str = Form(...), name: str = Form(...)):
    result, code, msg = BuilderValueService().create({'parent': parent.title(), 'name': name.title(), 'image': image})
    return result, code, msg


@api.delete('/builder_value/{builder_value_id}')
@wrap_response
def delete_builder_value(builder_value_id: str):
    result, code, msg = BuilderValueService().delete(builder_value_id)
    return result, code, msg
