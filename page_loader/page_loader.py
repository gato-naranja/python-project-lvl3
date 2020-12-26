import requests
from page_loader.io import construct


def download(url, user_dir):
    session = requests.session()
    response = session.get(url)
    path_to_file = construct(user_dir, url)
    with open(path_to_file, 'wb') as user_file:
        user_file.write(response.content)
    return path_to_file
