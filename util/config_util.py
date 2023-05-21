import configparser

import pymongo

config_parser = configparser.ConfigParser()
config_parser.read('config.ini')

config = config_parser._sections

# mongoDB
mongodb_config = config['MongoDB']
MONGO = pymongo.MongoClient(mongodb_config['url'])

# jwt
jwt_config = config['jwt']
