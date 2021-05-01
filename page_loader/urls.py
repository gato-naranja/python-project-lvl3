from urllib import parse


def to_name(url, ext=False):
    parsed_url = parse.urlparse(url)
    source_name = parsed_url.netloc.split('.')
    path_name = list(filter(None, parsed_url.path.split('/')))
    if path_name:
        source_name.extend(path_name)
    name = '-'.join(source_name)
    if ext:
        name = (name + '.html' if len(name.split('.')) == 1 else name)
    return name


def absolutize(url, internal_link):
    page_url = parse.urlparse(url)
    sub_url = parse.urlparse(internal_link)
    if sub_url.netloc == page_url.netloc:
        return internal_link
    elif sub_url.netloc == '':
        new_sub_url = (page_url.scheme, page_url.netloc, internal_link, '', '')
        return parse.urlunsplit(new_sub_url)
    return None
