import logging


def setup(log_level='INFO'):
    logging.basicConfig(
        format='[%(asctime)s] [%(levelname)s] [%(name)s] %(filename)s => %(message)s',  # noqa: E501
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.getLevelName(log_level),
        filename='loader.log',
    )
