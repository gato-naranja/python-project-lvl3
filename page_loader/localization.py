import os
import sys
import logging
import functools
from bs4 import BeautifulSoup
from page_loader import make


LOGGER = logging.getLogger('main.page_loader.localization')


def logging_localization(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        LOGGER.info('Start page localization')
        func(*args, **kwargs)
        LOGGER.info('Finish page localization')

    return wrapper


@logging_localization
def localize(source):
    """
    localize(page_metadata):
    Search on the downloaded page for internal links (images, css, js-scripts),
    form lists of internal links for loading.
    """
    html_filename = source['dir'] + source['file']
    try:
        with open(html_filename, 'rb') as content:
            soup = BeautifulSoup(content, 'lxml')
    except IOError:
        LOGGER.error(f'File {html_filename} not open /not found')
        sys.stderr.write(f'File {html_filename} not open / not found\n')
        raise
    source['sub_dir_name'] = source['name'] + '_files'
    source['sub_dir_path'] = make.directory(
        source['dir'] + source['sub_dir_name'],
        log_level='main.page_loader.localization')
    tags = [('img', 'src'), ('link', 'href'), ('script', 'src')]
    for tag, sub_tug in tags:
        links = soup.find_all(tag)
        if links is not None:
            page_key = tag + 's'
            source[page_key] = replace_urls(links, source, sub_tug)
            LOGGER.info(f'Sources -{tag}- was localized')
        else:
            LOGGER.info(f'Sources -{tag}- not found')
    with open(html_filename, 'w', encoding='utf-8') as content:
        content.write(soup.prettify(formatter='html5'))


def replace_urls(sub_links, source, sub_tag):
    """
    replace_url(list_internal_lincs, page_metadata, source_as_subtug):
    Replace internal links with local pathes,
    form pairs (link, name of the local file)
    for subsequent download.
    """
    pares_for_load = []
    for link in sub_links:
        sub_tag_value = link.get(sub_tag)
        sub_url = make.current_url(source['url'], sub_tag_value)
        if sub_url is not None:
            sub_name = make.current_name(sub_url)
            if len(sub_name.split('.')) == 1:
                sub_name += '.html'
            link[sub_tag] = source['sub_dir_name'] + os.sep + sub_name
            pares_for_load.append((sub_url, source['sub_dir_path'] + sub_name))
    return pares_for_load
