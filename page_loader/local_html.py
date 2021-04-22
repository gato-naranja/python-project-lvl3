import logging
import os

from bs4 import BeautifulSoup

from page_loader import urls


TAGS = [('img', 'src'), ('link', 'href'), ('script', 'src')]


def prepare(page_url, page_name, content):
    """
    localize(url, downloaded_page, page_name, path_to_load):
    Search on the downloaded page for internal links (images, css, js-scripts),
    form lists of internal links for loading.
    """
    logging.info('Start page localization')
    soup = BeautifulSoup(content, 'html.parser')
    prefix = page_name + '_files' + os.sep
    sources = []
    for tag, field in TAGS:
        links = soup.find_all(tag)
        if links is not None:
            for link in links:
                value = urls.transform(page_url, link.get(field))
                link[field] = (
                    link[field] if value is None else
                    prefix + urls.to_name(value, ext=True)
                )
                if value is None:
                    continue
                else:
                    sources.append((link[field], value))
            logging.info(f'Sources -{tag}- was localized')
        else:
            logging.info(f'Sources -{tag}- not found')

    logging.info('Finish page localization')
    return soup.prettify(formatter='html5'), sources
