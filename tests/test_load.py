import os
import requests
import requests_mock
import tempfile
import pytest
from bs4 import BeautifulSoup
from page_loader import download


@pytest.fixture(scope='module')
def fixture_tempdir(function):
    tempfile.TemporaryDirectory(dir=os.getcwd())


@requests_mock.Mocker(kw='m')
def test_page_download(**kwargs):
    path = tempfile.gettempdir()
    mock_source = kwargs['m']
    mock_source.get('mock://test.com', text='test_text')
    loaded_file = download('mock://test.com', path)
    expected = BeautifulSoup(requests.get('mock://test.com').content, 'lxml')
    with open(loaded_file, 'r', encoding='utf-8') as file:
        resulting = file.read()
    assert resulting == expected.prettify(formatter='html5')


@requests_mock.Mocker(kw='mock')
def test_localization(**kwargs):
    mock_source = kwargs['mock']
    with open('tests/fixtures/test.html', 'r', encoding='utf-8') as test_file:
        test_text = test_file.read()
    mock_source.get('mock://test.com', text=test_text)
    with open('tests/fixtures/haha.png', 'rb') as img_file:
        img_img = img_file.read()
    mock_source.get('mock://test.com/haha.png', content=img_img)
    with open('tests/fixtures/test1.css', 'r', encoding='utf-8') as css_file:
        css_text = css_file.read()
    mock_source.get('mock://test.com/test1.css', text=css_text)
    with open('tests/fixtures/test2.js', 'r', encoding='utf-8') as js_file:
        js_text = js_file.read()
    mock_source.get('mock://test.com/test2.js', text=js_text)
    mock_source.get('mock://test.com/courses', text='')
    path_to_html = download('mock://test.com', tempfile.gettempdir())
    assert path_to_html == tempfile.gettempdir() + os.sep + 'test-com.html'
