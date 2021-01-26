import os
from urllib import parse


def make_url(url, local_link):
    page_url = parse.urlparse(url)
    sub_url = parse.urlparse(local_link)
    if sub_url.netloc == page_url.netloc:
        return local_link
    elif sub_url.netloc == '':
        new_sub_url = (page_url.scheme, page_url.netloc, local_link, '', '')
        return parse.urlunsplit(new_sub_url)
    return None


def make_source_name(url):
    parsed_url = parse.urlparse(url)
    source_name = parsed_url.netloc.split('.')
    path_name = list(filter(None, parsed_url.path.split('/')))
    if path_name:
        source_name.extend(path_name)
    return '-'.join(source_name)


def make_dir(user_path):
    if not os.path.exists(user_path):
        os.makedirs(user_path)
    return user_path + os.sep
