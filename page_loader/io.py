import os
from urllib import parse


def construct(user_dir, url):
    return make_dir(user_dir) + os.sep + get_filename(url)


def get_filename(url):
    from_url = parse.urlsplit(url)
    netloc_name = '-'.join(from_url.netloc.split('.'))
    path_name = ''.join(from_url.path.split('/'))
    return netloc_name + path_name + '.html'


def make_dir(user_path):
    try:
        os.makedirs(user_path)
    except FileExistsError:
        pass
    return os.path.join(os.getcwd(), user_path)
