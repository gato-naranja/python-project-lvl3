import logging

import requests
from progress.bar import Bar


def fill(main_path, paths_and_links):
    bar_limit = len(paths_and_links)
    mark = ''
    bar = Bar(f'Loading {mark}', suffix='%(percent)d%%', max=bar_limit)
    for path, link in paths_and_links:
        mark = path.split('/')[-1]
        path_for_save = main_path + path
        source = requests.get(link)
        if source.ok:
            logging.info(f'Source {link} was load')
            with open(path_for_save, 'wb') as file:
                file.write(source.content)
            logging.info(f'It was save to {path_for_save}')
        else:
            logging.warning(
                f'Source {link} not load. Code: {source.status_code}',
            )
        bar.next()
