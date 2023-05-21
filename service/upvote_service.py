from model.upvote_model import UpvoteModel
from service.base_service import BaseService
from util.logger_util import logger


class UpvoteService(BaseService):
    def __init__(self):
        super().__init__(UpvoteModel())
