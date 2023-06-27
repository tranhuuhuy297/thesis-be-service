import configparser

import pymongo

from util.const_util import MONGO_URL

config_parser = configparser.ConfigParser()
config_parser.read('config.ini')

config = config_parser._sections

# mongoDB
mongodb_config = config['MongoDB']
MONGO = pymongo.MongoClient(MONGO_URL)
