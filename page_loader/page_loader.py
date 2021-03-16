import requests
import logging
from progress.bar import Bar
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
    try:
        page = make_page_meta(url, user_path)
    except Exception:
        logger.error(f'Bad user path: {user_path}')
        raise
    path_to_file = page['dir'] + page['file']
    try:
        load(page['url'], path_to_file)
    except Exception:
        raise
    try:
        localize(page)
    except Exception:
        raise
    logger.info('Start images, links and scripts load')
    for tag in ('imgs', 'links', 'scripts'):
        if page.get(tag) is not None:
            count_sources = 0
            bar_limit = len(page[tag])
            bar = Bar(f'Loading {tag}', suffix='%(percent)d%%', max=bar_limit)
            for source_url, source_file in page[tag]:
                try:
                    load(source_url, source_file)
                    count_sources += 1
                    bar.next()
                except Exception:
                    logger.error(f'{source_url} not loaded')
                    continue
            bar.finish()
            logger.info(f'-{tag}- loaded {count_sources} files')
        else:
            logger.info(f'Sources -{tag}- not found')
    logger.info('Finish images, links and scripts load')
    return path_to_file


def make_page_meta(url, user_path):
    name = make.current_name(url)
    try:
        work_dir = make.directory(user_path)
    except Exception:
        raise
    return {
        'name': name,
        'url': url,
        'dir': work_dir,
        'file': name + '.html',
    }


def load(url, path):
    """
    load(loading_url, path_to_local_file):
    Downloads resources from the url and saves them to the file.
    """
    logger = logging.getLogger('main.page_loader.load')
    with requests.session() as session:
        logger.info(f'Load {url}')
        try:
            response = session.get(url)
        except Exception as err:
            logger.error(f'GET-request for {url} failed. Details:\n{err}')
            raise Exception(f'loading error -> GET-request for {url} failed')
        if response.status_code == 200:
            logger.info(f'Loading complete, code {response.status_code}')
        elif response.status_code in range(201, 400):
            logger.info(f'Response code: {response.status_code}')
        else:
            logger.error(f'Page not loaded. Code {response.status_code}')
            raise Exception(response.status_code)
        try:
            with open(path, 'wb') as source_file:
                source_file.write(response.content)
                logger.info(f'File {path} was wrote')
        except IOError:
            logger.error(f'File "{path}" not wrote')
            raise
