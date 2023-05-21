from model.image_model import ImageModel
from service.base_service import BaseService
from service.prompt_service import PromptService
from service.user_service import UserService
from util.s3_util import S3
from util.time_util import get_time_string


class ImageService(BaseService):
    def __init__(self):
        super().__init__(ImageModel())
        self.s3_photo = S3(bucket_name='image')

    def build_item(self, item):
        user_id = item.get('user_id', '')
        user, _, _ = UserService().get(user_id)
        if user is None:
            return None, -1, 'invalid user'

        prompt_id = item.get('prompt_id', '')
        prompt, _, _ = PromptService().get(prompt_id)
        if prompt is None:
            return None, -1, 'invalid prompt'

        image = item.get('image', None)
        if image is None:
            return None, -1, 'invalid image'
        file_name = f'user/{user["gmail"]}/{get_time_string()}/{image.filename}'
        self.s3_photo.put_object(image.file, file_name)

        image_src = f'{self.s3_photo.bucket_name}.s3.{self.s3_photo.region_name}.amazonaws.com/{file_name}'

        return {
            'user_id': user_id,
            'prompt_id': prompt_id,
            'image_src': image_src,
        }, 0, 'valid'
