import os
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
    if not os.path.exists(user_path):
        logger.error(f'Directory {user_path} not exist')
        raise Exception(f'Directory {user_path} not exist')
    try:
        page_content = load(url)
    except Exception:
        raise
    source_name = make.current_name(url)
    try:
        localized_page, sub_sources = localize(
            url,
            page_content,
            source_name,
            user_path,
            )
        path_to_file = user_path + os.sep + source_name + '.html'
        save_page(localized_page, path_to_file, 'w', 'utf-8')
    except Exception:
        raise
    logger.info('Start images, links and scripts load')
    for tag in ('imgs', 'links', 'scripts'):
        if sub_sources.get(tag) is not None:
            count_sources = 0
            bar_limit = len(sub_sources[tag])
            bar = Bar(f'Loading {tag}', suffix='%(percent)d%%', max=bar_limit)
            for source_url, source_file in sub_sources[tag]:
                try:
                    source_content = load(source_url)
                except Exception:
                    logger.error(f'{source_url} not loaded')
                    continue
                try:
                    save_page(source_content, source_file, 'wb', None)
                    count_sources += 1
                    bar.next()
                except Exception:
                    logger.error(f'{source_url} not saved')
                    continue
            bar.finish()
            logger.info(f'-{tag}- loaded {count_sources} files')
        else:
            logger.info(f'Sources -{tag}- not found')
    logger.info('Finish images, links and scripts load')
    return path_to_file


def load(url):
    """
    load(loading_url):
    Downloads resources from the url.
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
    return response.content


def save_page(content, path, save_type, enc):
    """
    save_page(content, path_to_local_file, type_of_file_open, encoding):
    Saves sources to the local file.
    """
    logger = logging.getLogger('main.page_loader.save')
    logger.info(f'Saving {path}')
    try:
        with open(path, save_type, encoding=enc) as source_file:
            try:
                source_file.write(content)
                print('Saving complete')
                logger.info(f'File {path} was wrote')
            except Exception as err:
                logger.error(f'File "{path}" not wrote:\n{err.__str__()}')
                raise Exception
    except Exception:
        logger.error(f'File "{path}" not open')
        raise
