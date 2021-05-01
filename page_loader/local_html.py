import logging
import os

from bs4 import BeautifulSoup

from page_loader import urls


TAGS = [('img', 'src'), ('link', 'href'), ('script', 'src')]


def prepare(page_url, page_name, content):
    """
    prepare(url, page_name, downloaded_page):
    Search on the downloaded page for internal links (images, css, js-scripts)
    and form lists of internal links for loading.
    """
    logging.info('Start page localization')
    soup = BeautifulSoup(content, 'html.parser')
    storage_prefix = f'{page_name}_files{os.sep}'
    sources = []
    for tag, field in TAGS:
        links = soup.find_all(tag)
        if links is None:
            logging.info(f'Sources -{tag}- not found')
            continue
        for link in links:
            if not link.get(field):
                continue
            value = urls.absolutize(page_url, link.get(field))
            if value is not None:
                link[field] = storage_prefix + urls.to_name(value, ext=True)
                sources.append((link[field], value))
        logging.info(f'Sources -{tag}- was localized')
    logging.info('Finish page localization')
    return soup.prettify(formatter='html5'), sources
