import pymongo
import datetime
import threading

from copy import deepcopy
from bson.errors import InvalidId
from bson.objectid import ObjectId


from endpoint import mongo
from util.logger_util import logger
from util.time_util import now
from util.error_util import Error


class Singleton(type):
    _lock = threading.Lock()
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if not cls in cls._instances:
            with cls._lock:
                if not cls in cls._instances:
                    cls._instances[cls] = super(
                        Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class BaseMongoModel(object, metaclass=Singleton):
    def __init__(self, db, collection):
        self.db = mongo[db]
        self.collection = self.db[collection]

    def convert_fields(self, item):
        _id = item.pop('_id', None)
        if _id:
            item['id'] = str(_id)

        if 'create_time' in item:
            item['create_time'] = int(item['create_time'].replace(
                tzinfo=datetime.timezone.utc).timestamp())

        if 'update_time' in item:
            item['update_time'] = int(item['update_time'].replace(
                tzinfo=datetime.timezone.utc).timestamp())

        return item

    def create(self, item):
        try:
            time = now()
            item['create_time'] = time
            item['update_time'] = time

            return_id = str(self.collection.insert_one(item).inserted_id)
            if return_id:
                item = self.convert_fields(item)
                return item, 0, 'Create item successfully'
            else:
                return None, Error.ERROR_CODE_CREATED_FAILED, Error.ERROR_MESSAGE_CREATED_FAILED
        except Exception as e:
            logger.error(e, exc_info=True)
            return None, Error.ERROR_CODE_CREATED_FAILED, e

    def get(self, id):
        try:
            _filter = {'_id': ObjectId(id)}

            item = self.collection.find_one(_filter)
            if item:
                item = self.convert_fields(item)
                return item, 0, 'Get item successfully'
            else:
                return None, Error.ERROR_CODE_GOT_FAILED, Error.ERROR_MESSAGE_GOT_FAILED
        except InvalidId as invalid_id_err:
            logger.error(invalid_id_err, exc_info=True)
            return None, Error.ERROR_CODE_GOT_FAILED, Error.ERROR_MESSAGE_GOT_FAILED
        except Exception as e:
            logger.error(e, exc_info=True)
            return None, Error.ERROR_CODE_GOT_FAILED, e

    def update(self, id, item):
        try:
            _filter = {'_id': ObjectId(id)}
            update_data = {"$set": item}
            result = self.collection.update_one(_filter, update_data)

            update_count = result.modified_count
            if update_count:
                return update_count, 0, 'Update item successfully'
            return None, Error.ERROR_CODE_UPDATED_FAILED, Error.ERROR_MESSAGE_UPDATED_FAILED
        except Exception as e:
            logger.error(e, exc_info=True)
            return None, Error.ERROR_CODE_UPDATED_FAILED, e

    def delete(self, id):
        try:
            _filter = {'_id': ObjectId(id)}
            result = self.collection.delete_one(_filter)

            if result:
                return result.deleted_count, 0, 'Delete item successfully'
            return None, Error.ERROR_CODE_DELETED_FAILED, Error.ERROR_MESSAGE_DELETED_FAILED
        except InvalidId as invalid_id_err:
            logger.error(invalid_id_err, exc_info=True)
            return None, Error.ERROR_CODE_DELETED_FAILED, str(invalid_id_err)
        except Exception as e:
            logger.error(e, exc_info=True)
            return None, Error.ERROR_CODE_DELETED_FAILED, e
