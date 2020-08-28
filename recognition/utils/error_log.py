import logging


error_logger = logging.getLogger(__name__)
error_logger.setLevel(logging.ERROR)
formatter = logging.Formatter('%(name)s:%(asctime)s:%(message)s')
file_handler = logging.FileHandler('error.log')
file_handler.setFormatter(formatter)
error_logger.addHandler(file_handler)
