import logging

from utils.const import Paths


def _create_logger():
    logger = logging.Logger('test_api')
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(Paths.TEST_LOG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


log = _create_logger()
