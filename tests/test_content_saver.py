from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

import pytest

from utils.content_saver import ContentSaver


@pytest.mark.parametrize('url, path_expected', [
    ('http://ya.ru/',                           '/tmp/dump/index_333.html'),
    ('http://ya.ru/index.html',                 '/tmp/dump/index.html'),
    ('http://ya.ru/d1',                         '/tmp/dump/d1'),
    ('http://ya.ru/d1/',                        '/tmp/dump/d1/index_333.html'),
    ('http://ya.ru/d1/index.html',              '/tmp/dump/d1/index.html'),
    ('http://ya.ru/d1/index.html?q=v',          '/tmp/dump/d1/index.html?q=v'),
    ('http://ya.ru/d1/index.html?q=v&qq=vv',    '/tmp/dump/d1/index.html?q=v&qq=vv'),
])
def test_get_absolute_path(url, path_expected):
    with mock.patch('utils.content_saver.randint', return_value=333):
        assert path_expected == str(ContentSaver.get_absolute_path(Path('/tmp/dump/'), url))


@pytest.mark.parametrize('url, filepath', [
    ('http://ya.ru/',                           'index_333.html'),
    ('http://ya.ru/index.html',                 'index.html'),
    ('http://ya.ru/d1',                         'd1'),
    ('http://ya.ru/d1/',                        'd1/index_333.html'),
    ('http://ya.ru/d1/index.html',              'd1/index.html'),
    ('http://ya.ru/d1/index.html?q=v',          'd1/index.html?q=v'),
    ('http://ya.ru/d1/index.html?q=v&qq=vv',    'd1/index.html?q=v&qq=vv'),
])
def test_save(url, filepath):
    with TemporaryDirectory() as tmpdir:
        with mock.patch('utils.content_saver.randint', return_value=333):

            content_dir = Path(tmpdir)
            content = '1'
            saved_path = ContentSaver.save_page(content_dir, url, content)
            saved_path_expected = content_dir / filepath
            assert saved_path.is_file()
            assert saved_path_expected == saved_path