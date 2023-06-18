from model.builder_model import BuilderTypeModel, BuilderValueModel
from service.base_service import BaseService
from util.s3_util import S3


class BuilderTypeService(BaseService):
    def __init__(self):
        super().__init__(BuilderTypeModel())


class BuilderValueService(BaseService):
    def __init__(self):
        super().__init__(BuilderValueModel())
        self.s3_photo = S3(bucket_name='image')

    def build_item(self, item):
        parent = item.get('parent', '')
        name = item.get('name', '')
        list_parent, _, _, _ = BuilderTypeService().get_list({'name': parent}, page=0, size=1000)
        if len(list_parent) == 0:
            return None, -1, 'parent name not exist'

        image = item.pop('image', None)
        if image is None:
            return None, -1, 'invalid image'
        self.s3_photo.put_object(image.file, f'builder/{parent}/{name}')

        item['image_src'] = f'{self.s3_photo.bucket_name}.s3.{self.s3_photo.region_name}.amazonaws.com/builder/{parent}/{name}'

        return super().build_item(item)

    def build_update_item(self, update_item):
        item = {}
        item['name'] = update_item.get('name', '')

        return item, 0, 'item valid'
