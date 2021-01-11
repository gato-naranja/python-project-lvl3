import os
import requests
from page_loader.io import make_dir, make_source_name, have_not_netloc
from bs4 import BeautifulSoup


def download(url, user_path):
    page = make_page_meta(url, user_path)
    path_to_file = page['workdir'] + page['file']
    load([(page['url'], path_to_file)])
    localize(page)
    return path_to_file


def make_page_meta(url, user_path):
    name = make_source_name(url)
    return {
        'name': name,
        'url': url,
        'workdir': make_dir(user_path),
        'file': name + '.html',
    }


def load(data_loading):
    with requests.session() as session:
        for url, filename in data_loading:
            response = session.get(url)
            with open(filename, 'wb') as source_file:
                source_file.write(response.content)


def localize(source):
    work_file = source['workdir'] + source['file']
    with open(work_file, 'rb') as content:
        soup = BeautifulSoup(content, 'lxml')
    replace_urls(soup, source)
    with open(work_file, 'w', encoding='utf-8') as content:
        content.write(soup.prettify(formatter='html5'))
    load(source['sub_links'])


def replace_urls(loaded_html, source):
    links = loaded_html.find_all('img')
    if links is not None:
        sub_dir = source['name'] + '_files'
        sub_workdir = make_dir(source['workdir'] + sub_dir)
        source['sub_links'] = []
        for link in links:
            current_name = link.get('src')
            if have_not_netloc(current_name):
                sub_url = source['url'] + current_name
                link_name = make_source_name(sub_url)
                link['src'] = sub_dir + os.sep + link_name
                source['sub_links'].append((sub_url, sub_workdir + link_name))
