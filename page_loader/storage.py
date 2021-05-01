import os
import logging


def save(content, path):
    file_mode = 'wb' if isinstance(content, bytes) else 'w'
    enc = 'utf-8' if file_mode == 'w' else None
    with open(path, file_mode, encoding=enc) as file:
        file.write(content)
    logging.info('Saved')


def create(*args):
    parts_of_path = list(args)
    path = os.sep.join(parts_of_path)
    if not os.path.exists(path):
        os.mkdir(path)
        logging.info(f'Created {path}')
