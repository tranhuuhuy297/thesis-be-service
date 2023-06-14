from model.generate_model import GenerateModel
from service.base_service import BaseService
from service.user_service import UserService
from util.logger_util import logger


class GenerateService(BaseService):
    def __init__(self):
        super().__init__(GenerateModel())

    def generate(self, payload):
        user_id = payload.get('user_id', '')
        hint_text = payload.get('hint_text', '')
        user, _, _ = UserService().get(user_id)
        if user is None:
            return None, -1, 'user not exists'
