import logging
import os

import requests
from progress.bar import Bar

from page_loader import local_html
from page_loader import storage
from page_loader import urls


def download(url, user_path):
    """
    download(url, path_to_user_directory):
    Downloads the page at the specified url
    and saves it to a html-file in the user folder.
    And return the path to the saved local file.
    """
    page_name = urls.to_name(url)
    if os.path.exists(user_path):
        file_path = f'{user_path}{os.sep}{page_name}.html'
    else:
        logging.error(f'Directory {user_path} not exist')
        raise Exception(
            f'folder "{user_path}" not found, loading {url} aborted',
        )
    response = requests.get(url)
    if not response.ok:
        logging.error(
            f'GET-request for {url} failed. Code: {response.status_code}',
        )
        response.raise_for_status()
    html_content, sources = local_html.prepare(
        url,
        page_name,
        response.content,
    )
    logging.info(f'Saving page to {file_path}')
    storage.save(html_content, file_path)
    if sources is not None:
        logging.info('Start sources (images, links, scripts) load')
        storage.create(user_path, f'{page_name}_files')
        download_sources(user_path + os.sep, sources)
        logging.info('Sources loading complete')
    return file_path


def download_sources(main_path, paths_and_links):
    bar_limit = len(paths_and_links)
    bar = Bar('Loading', suffix='%(percent)d%%', max=bar_limit)
    for path, link in paths_and_links:
        path_for_save = main_path + path
        source = requests.get(link)
        if source.ok:
            logging.info(f'Source {link} was load')
            storage.save(source.content, path_for_save)
            logging.info(f'It was save to {path_for_save}')
        else:
            logging.warning(
                f'Source {link} not load. Code: {source.status_code}',
            )
        bar.next()
