import logging

DATE_FORMAT = "%d-%m-%y %H:%M:%S"
MESSAGE_FORMAT = "%(asctime)s - %(levelname)s | %(message)s"

logging.basicConfig(level=logging.INFO, format=MESSAGE_FORMAT, datefmt=DATE_FORMAT)
logger = logging.getLogger('thesis-be-service')
