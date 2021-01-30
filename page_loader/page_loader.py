import requests
import logging
from page_loader.localization import localize
from page_loader import make


def download(url, user_path):
    """
    download(url, path_to_user_directory):
    Downloads the page at the specified url
    and saves it to a html-file in the user folder.
    And return the path to the saved local file.
    """
    logger = logging.getLogger('main.page_loader')
    page = make_page_meta(url, user_path)
    path_to_file = page['dir'] + page['file']
    load([(page['url'], path_to_file)])
    localize(page)
    logger.info('Start images, links and scripts load')
    for tag in ('img_links', 'link_links', 'script_links'):
        if page.get(tag) is not None:
            load(page[tag])
    logger.info('Finish images, links and scripts load')
    return path_to_file


def make_page_meta(url, user_path):
    name = make.current_name(url)
    return {
        'name': name,
        'url': url,
        'dir': make.directory(user_path),
        'file': name + '.html',
    }


def load(data_loading):
    """
    load(pare_of_url_and_local_source):
    Downloads resources to the url and saves them to the file.
    """
    logger = logging.getLogger('main.page_loader.load')
    with requests.session() as session:
        for url, filename in data_loading:
            logger.info(f'Load {url}')
            response = session.get(url)
            if response.status_code == 200:
                logger.info(f'Loading complete, code {response.status_code}')
            else:
                logger.info(f'Response code: {response.status_code}')
            with open(filename, 'wb') as source_file:
                source_file.write(response.content)
