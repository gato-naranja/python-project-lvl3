import os
import logging
from bs4 import BeautifulSoup
from page_loader import make


TAGS = [('img', 'src'), ('link', 'href'), ('script', 'src')]


def localize(url, source_content, source_name, source_dir):
    """
    localize(url, downloaded_page, page_name, path_to_load):
    Search on the downloaded page for internal links (images, css, js-scripts),
    form lists of internal links for loading.
    """
    logger = logging.getLogger('main.page_loader.localization')
    logger.info('Start page localization')
    soup = BeautifulSoup(source_content, 'html.parser')
    sub_dir_name = source_name + '_files'
    sub_dir_path = make.directory(
        source_dir + os.sep + sub_dir_name,
        log_level='main.page_loader.localization')
    sub_meta = (sub_dir_name, sub_dir_path)
    sources_for_load = {}
    for tag, sub_tug in TAGS:
        links = soup.find_all(tag)
        if links is not None:
            page_key = tag + 's'
            sources_for_load[page_key] = replace_urls(
                url,
                links,
                sub_tug,
                sub_meta,
                )
            logger.info(f'Sources -{tag}- was localized')
        else:
            logger.info(f'Sources -{tag}- not found')
    logger.info('Finish page localization')
    return soup.prettify(formatter='html5'), sources_for_load


def replace_urls(url, sub_links, sub_tag, sub_meta):
    """
    replace_url(original_url, list_of_links, tag_in_link, name_&_path):
    Replace internal links with local pathes,
    form pairs (link, name of the local file)
    for subsequent download.
    """
    name, path = sub_meta
    pares_for_load = []
    for link in sub_links:
        sub_tag_value = link.get(sub_tag)
        sub_url = make.current_url(url, sub_tag_value)
        if sub_url is not None:
            sub_name = make.current_name(sub_url)
            if len(sub_name.split('.')) == 1:
                sub_name += '.html'
            link[sub_tag] = name + os.sep + sub_name
            pares_for_load.append((sub_url, path + sub_name))
    return pares_for_load
