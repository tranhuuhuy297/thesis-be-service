import bson
import threading

from util.logger_util import logger
from util.error_util import Error
from model.base_mongodb import BaseMongoModel


class Singleton(type):
    _lock = threading.Lock()
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super(
                        Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class BaseService(object, metaclass=Singleton):
    def __init__(self, model: BaseMongoModel):
        self.model = model

    def build_item(self, item):
        return item, 0, 'Item is validated'

    def create(self, data):
        try:
            item, code, msg = self.build_item(data)
            logger.debug(f'Build item: {msg}\n{item}')
            build_item, code, msg = self.model.create(item)
            return build_item, code, msg
        except Exception as e:
            logger.error(e, exc_info=True)
            return None, Error.ERROR_CODE_GOT_EXCEPTION, e

    def get_paging_data(self, _filter={}):
        size = int(_filter.get("size", 10))
        page = int(_filter.get("page", 0))
        skip = page * size

        return size, skip

    def get_extra_info(self, id, item):
        return item

    def get(self, id, deep=False):
        try:
            item, code, msg = self.model.get(id)
            if not item:
                return None, Error.ERROR_CODE_GET_NO_SUCH_ITEM, Error.ERROR_MESSAGE_GET_NO_SUCH_ITEM
            if deep:
                item = self.get_extra_info(id, item)
            return item, code, msg
        except Exception as e:
            logger.error(e, exc_info=True)
            return None, Error.ERROR_CODE_GOT_EXCEPTION, e

    def get_list(self, _filter):
        pass

    def build_update_item(self, id, update_item):
        return update_item, 0, 'Item is validated'

    def update(self, id, data):
        try:
            data.pop('create_time', None)
            data.pop('update_time', None)
            item, code, msg = self.build_update_item(id, data)
            if not item:
                return None, code, msg
            item = {k: v for k, v in item.items() if v is not None}

            update_count, code, msg = self.model.update(id, item=item)
            if update_count:
                item, _, _ = self.get(id)
                return item, code, msg
            return None, -1, 'None of item was updated'
        except Exception as e:
            logger.error(e, exc_info=True)
            return None, Error.ERROR_CODE_GOT_EXCEPTION, e

    def delete(self, id):
        try:
            delete_count, code, msg = self.model.delete(id)
            if delete_count:
                item, _, _ = self.get(id)
                return item, code, msg
            return None, -1, 'None of item was deleted'
        except Exception as e:
            logger.error(e, exc_info=True)
            return None, Error.ERROR_CODE_GOT_EXCEPTION, e
