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


@pytest.fixture(scope='module')
@requests_mock.Mocker(kw='mock')
def fixture_source_mock(**kwargs):
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
    return path_to_html


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


def test_localization(fixture_source_mock):
    path_to_html = fixture_source_mock
    assert path_to_html == tempfile.gettempdir() + os.sep + 'test-com.html'


@pytest.mark.parametrize(
    'expect, result',
    [
        (('tests/fixtures/haha.png', 'rb'), ('img', 'src', 'rb')),
        (('tests/fixtures/test1.css', 'r'), ('link', 'href', 'r')),
        (('tests/fixtures/test2.js', 'r'), ('script', 'src', 'r')),
    ]
)
def test_loaded_sources(fixture_source_mock, expect, result):
    ex_path, ex_mode = expect
    with open(ex_path, ex_mode) as img_file:
        expected = img_file.read()
    html_path = fixture_source_mock
    with open(html_path, 'rb') as page:
        soup = BeautifulSoup(page, 'lxml')
    tag, sub_tag, mode = result
    path = tempfile.gettempdir() + os.sep + soup.find(tag)[sub_tag]
    with open(path, mode) as source_file:
        resulting = source_file.read()
    assert resulting == expected
