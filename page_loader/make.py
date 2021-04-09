import os
import sys
import logging
from urllib import parse


def current_url(url, local_link):
    page_url = parse.urlparse(url)
    sub_url = parse.urlparse(local_link)
    if sub_url.netloc == page_url.netloc:
        return local_link
    elif sub_url.netloc == '':
        new_sub_url = (page_url.scheme, page_url.netloc, local_link, '', '')
        return parse.urlunsplit(new_sub_url)
    return None


def current_name(url):
    parsed_url = parse.urlparse(url)
    source_name = parsed_url.netloc.split('.')
    path_name = list(filter(None, parsed_url.path.split('/')))
    if path_name:
        source_name.extend(path_name)
    return '-'.join(source_name)


def directory(user_path, log_level='main'):
    logger = logging.getLogger(log_level + '.make_dir')
    if not os.path.exists(user_path):
        try:
            os.makedirs(user_path)
        except OSError:
            err_msg = f'Impossible to create a directory -> {user_path}'
            logger.error(err_msg)
            sys.stderr.write(err_msg + '\n')
            raise Exception('Directory make error')
        logger.info(f'Creating dir {user_path}')
    else:
        logger.info(f'Dir "{user_path}" already exists')
