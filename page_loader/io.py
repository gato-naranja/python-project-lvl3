import os
from urllib import parse


def make_dir(user_path):
    if not os.path.exists(user_path):
        os.makedirs(user_path)
    return user_path + os.sep


def make_source_name(url):
    splitted_url = parse.urlsplit(url)
    source_name = splitted_url.netloc.split('.')
    path_name = list(filter(None, splitted_url.path.split('/')))
    if path_name:
        source_name.extend(path_name)
    return '-'.join(source_name)


def have_not_netloc(url):
    parsed = parse.urlsplit(url)
    return True if parsed.netloc == '' else False
