import os
import requests
import requests_mock
import tempfile
from page_loader import download


def fixture_connect_mock(function):

    def context_wrapper():
        with requests_mock.Mocker() as mock_source:
            mock_source.get('mock://test.com', text='test')
            return function

    return context_wrapper


def fixture_tempdir(function):

    def wrapper():
        with tempfile.mkstemp(dir=os.getcwd()):
            return function

    return wrapper


@fixture_connect_mock
@fixture_tempdir
def test_page_download():
    loaded_file = download('mock://test.com', tempfile.gettempdir())
    with open(loaded_file, 'r') as test_file:
        assert test_file.read() == requests.get('mock://test.com').content
