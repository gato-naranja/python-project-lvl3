import requests
from page_loader.localization import localize
from page_loader.io import make_dir, make_source_name


def download(url, user_path):
    page = make_page_meta(url, user_path)
    path_to_file = page['dir'] + page['file']
    load([(page['url'], path_to_file)])
    localize(page)
    for tag in ('img_links', 'link_links', 'script_links'):
        if page.get(tag) is not None:
            load(page[tag])
    return path_to_file


def make_page_meta(url, user_path):
    name = make_source_name(url)
    return {
        'name': name,
        'url': url,
        'dir': make_dir(user_path),
        'file': name + '.html',
    }


def load(data_loading):
    with requests.session() as session:
        for url, filename in data_loading:
            response = session.get(url)
            with open(filename, 'wb') as source_file:
                source_file.write(response.content)
