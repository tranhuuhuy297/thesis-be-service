from model.prompt_model import PromptModel
from model.upvote_model import UpvoteModel
from service.base_service import BaseService
from service.user_service import UserService
from util.logger_util import logger
from util.error_util import Error


class PromptService(BaseService):
    def __init__(self):
        super().__init__(PromptModel())

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
