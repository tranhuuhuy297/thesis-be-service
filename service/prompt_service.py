from model.prompt_model import PromptModel
from model.upvote_model import UpvoteModel
from service.base_service import BaseService
from service.user_service import UserService
from util.s3_util import S3
from util.time_util import get_time_string


class PromptService(BaseService):
    def __init__(self):
        super().__init__(PromptModel())
        self.s3_photo = S3(bucket_name='image')

    def build_item(self, item):
        user_id = item.get('user_id', '')
        user, _, _ = UserService().get(user_id)
        if user is None:
            return None, -1, 'invalid user'

        prompt = item.get('prompt', '')
        negative_prompt = item.get('negative_prompt', '')

        return {
            'user_id': user_id,
            'prompt': prompt,
            'negative_prompt': negative_prompt,
        }, 0, 'valid'

    def get_extra_info(self, id, item):
        count_upvote = UpvoteModel().count({'prompt_id': id})

        return {**item, 'count_upvote': count_upvote}
