import os
from bs4 import BeautifulSoup
from page_loader.io import make_dir, make_source_name, make_url


def localize(source):
    html_filename = source['dir'] + source['file']
    with open(html_filename, 'rb') as content:
        soup = BeautifulSoup(content, 'lxml')
    source['sub_dir_name'] = source['name'] + '_files'
    source['sub_dir_path'] = make_dir(source['dir'] + source['sub_dir_name'])
    tags = [('img', 'src'), ('link', 'href'), ('script', 'src')]
    for tag, sub_tug in tags:
        links = soup.find_all(tag)
        if links is not None:
            page_key = tag + '_links'
            source[page_key] = replace_urls(links, source, sub_tug)
    with open(html_filename, 'w', encoding='utf-8') as content:
        content.write(soup.prettify(formatter='html5'))


def replace_urls(sub_links, source, sub_tag):
    pares_for_load = []
    for link in sub_links:
        sub_tag_value = link.get(sub_tag)
        sub_url = make_url(source['url'], sub_tag_value)
        if sub_url is not None:
            sub_name = make_source_name(sub_url)
            link[sub_tag] = source['sub_dir_name'] + os.sep + sub_name
            pares_for_load.append((sub_url, source['sub_dir_path'] + sub_name))
    return pares_for_load
