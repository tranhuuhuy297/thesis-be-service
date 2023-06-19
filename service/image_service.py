from model.image_model import ImageModel
from model.upvote_model import UpvoteModel
from service.base_service import BaseService
from service.prompt_service import PromptService
from service.upvote_service import UpvoteService
from service.user_service import UserService
from util import s3_image, sqs
from util.time_util import get_time_string
from util.logger_util import logger
from util.error_util import Error


class ImageService(BaseService):
    def __init__(self):
        super().__init__(ImageModel())

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
        s3_image.put_object(image.file, file_name)

        image_src = f'{s3_image.bucket_name}.s3.{s3_image.region_name}.amazonaws.com/{file_name}'

        return {
            'user_id': user_id,
            'prompt_id': prompt_id,
            'image_src': image_src,
        }, 0, 'valid'

    def create(self, data):
        try:
            item, code, msg = self.build_item(data)
            if item is None:
                return None, code, msg
            logger.info(f'Build item: {msg}\n{item}')
            created_item, code, msg = self.model.create(item)

            # add to sqs
            prompt, _, _ = PromptService().get(created_item['prompt_id'], _filter={'user_id': created_item['user_id']})
            sqs.send_message({'id': created_item['id'],
                              'prompt_id': prompt['id'],
                              'user_id': prompt['user_id'],
                              'image_src': item['image_src'],
                              'prompt': prompt['prompt'],
                              'negative_prompt': prompt.get('negative_prompt', '')})
            return created_item, code, msg
        except Exception as e:
            logger.error(e, exc_info=True)
            return None, Error.ERROR_CODE_GOT_EXCEPTION, e

    def get_extra_info(self, item):
        prompt_id = item.get('prompt_id', '')
        user_id = item.get('user_id', '')
        prompt, _, _ = PromptService().get(prompt_id, _filter={'user_id': user_id})
        user, _, _ = UserService().get(user_id)

        upvote, _, _ = UpvoteService().get(None, {'user_id': user_id, 'prompt_id': prompt_id})
        count_upvote = UpvoteModel().count({'prompt_id': prompt_id})

        return {**item,
                'is_upvote': bool(upvote),
                'count_upvote': count_upvote,
                'user_gmail': user.get('gmail', ''),
                'prompt_id': prompt.get('id', ''),
                'prompt': prompt.get('prompt', ''),
                'negative_prompt': prompt.get('negative_prompt', '')}
