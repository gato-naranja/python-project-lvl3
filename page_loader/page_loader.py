import logging
import os

import requests

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
        file_path = user_path + os.sep + page_name + '.html'
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
    with open(file_path, 'w', encoding='utf-8') as my_file:
        my_file.write(html_content)
    logging.info('Saving complete')
    if sources is not None:
        logging.info('Start sources (images, links, scripts) load')
        source_path = user_path + os.sep + page_name + '_files'
        if not os.path.exists(source_path):
            os.mkdir(source_path)
        storage.fill(user_path + os.sep, sources)
        logging.info('Sources loading complete')
    return file_path
