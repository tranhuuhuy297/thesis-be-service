from model.user_model import UserModel
from service.base_service import BaseService
from util.logger_util import logger
from util.s3_util import S3
from util.token_util import encode_sha256


class UserService(BaseService):
    def __init__(self):
        super().__init__(UserModel())
        self.s3_photo = S3(bucket_name='image')

    def build_update_item(self, update_item):
        # password = update_item.get('password', '')
        # password = encode_sha256(password)

        # return {**update_item, 'password': password}, 0, 'validate'
        username = update_item.get('username', '')
        if 'image' in update_item:
            image = update_item.pop('image', None)
            if image is None:
                return None, -1, 'invalid image'
            file_name = f'user/{username}/{image.filename}'
            if not self.s3_photo.put_object(image.file, file_name):
                return None, -1, 'upload image fail'
            image_src = f'{self.s3_photo.bucket_name}.s3.{self.s3_photo.region}.amazonaws.com/{file_name}'
            update_item['image_src'] = image_src

        return update_item, 0, 'valid'
