from model.builder_model import BuilderTypeModel, BuilderValueModel
from service.base_service import BaseService
from util import s3_image
from util.const_util import AWS_CDN


class BuilderTypeService(BaseService):
    def __init__(self):
        super().__init__(BuilderTypeModel())


class BuilderValueService(BaseService):
    def __init__(self):
        super().__init__(BuilderValueModel())

    def build_item(self, item):
        parent = item.get('parent', '')
        name = item.get('name', '')
        list_parent, _, _, _ = BuilderTypeService().get_list({'name': parent}, page=0, size=1000)
        if len(list_parent) == 0:
            return None, -1, 'parent name not exist'

        image = item.pop('image', None)
        if image is None:
            return None, -1, 'invalid image'
        s3_image.put_object(image.file, f'builder/{parent}/{name}')

        item['image_src'] = f'/builder/{parent}/{name}'

        return super().build_item(item)

    def build_update_item(self, update_item):
        item = {}
        item['name'] = update_item.get('name', '')

        return item, 0, 'item valid'

    def get_extra_info(self, item):
        return {
            **item,
            'image_src': AWS_CDN + item['image_src']
        }
