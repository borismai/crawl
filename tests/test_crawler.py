from asyncio import sleep
from urllib.parse import urlparse

import pytest
from pathlib import Path


from content_saver.content_saver_abstract import ContentSaverAbstract
from crawler import Crawler
from page_cacher.page_cacher import PageCacher
from page_cacher.page_cache_item import PageCacheItemStatus
from page_parser.page_parser import PageParser
from request_maker.request_maker import RequestMaker


EXPECTED_URL_RESULTS = {
    'http://d1:80': {'status': PageCacheItemStatus.OK, 'query_mark': None, 'path_mark': '/index.html', },
    'http://d1:80/index.html': {'status': PageCacheItemStatus.OK, 'query_mark': None, 'path_mark': '/index.html', },
    'http://d1:80/file1.html': {'status': PageCacheItemStatus.OK, 'query_mark': None, 'path_mark': '/file1.html', },
    'http://d1:80/file2.html': {'status': PageCacheItemStatus.ERROR, 'query_mark': None, 'path_mark': None, },

    'http://d1:80/dir1/': {'status': PageCacheItemStatus.OK, 'query_mark': None, 'path_mark': '/dir1/index.html', },
    'http://d1:80/dir1/index.html': {'status': PageCacheItemStatus.OK, 'query_mark': None, 'path_mark': '/dir1/index.html', },
    'http://d1:80/dir1/dir1_f1.html': {'status': PageCacheItemStatus.OK, 'query_mark': None, 'path_mark': '/dir1/dir1_f1.html', },
    'http://d1:80/dir1/dir1_f2.html': {'status': PageCacheItemStatus.OK, 'query_mark': None, 'path_mark': '/dir1/dir1_f2.html', },

    'http://d1:80/dir1/dir2/': {'status': PageCacheItemStatus.ERROR, 'query_mark': None, 'path_mark': None, },
    'http://d1:80/dir1/dir2/dir1_dir2_file1.html': {'status': PageCacheItemStatus.OK, 'query_mark': None, 'path_mark': '/dir1/dir2/dir1_dir2_file1.html', },
    'http://d1:80/dir1/dir2/dir1_dir2_file2.html': {'status': PageCacheItemStatus.OK, 'query_mark': None, 'path_mark': '/dir1/dir2/dir1_dir2_file2.html', },
    'http://d1:80/dir1/dir2/dir1_dir2_file2.html?k=v': {'status': PageCacheItemStatus.OK, 'query_mark': 'k=v', 'path_mark': '/dir1/dir2/dir1_dir2_file2.html', },
}

EXPECTED_SAVING_MESSAGES = {
    'Saved http://d1:80 to /tmp/some/index_333.html',
    'Saved http://d1:80/index.html to /tmp/some/index.html',
    'Saved http://d1:80/file1.html to /tmp/some/file1.html',
    'Saved http://d1:80/file2.html to /tmp/some/file2.html',
    'Saved http://d1:80/dir1/ to /tmp/some/dir1/index_333.html',
    'Saved http://d1:80/dir1/index.html to /tmp/some/dir1/index.html',
    'Saved http://d1:80/dir1/dir1_f1.html to /tmp/some/dir1/dir1_f1.html',
    'Saved http://d1:80/dir1/dir1_f2.html to /tmp/some/dir1/dir1_f2.html',
    'Saved http://d1:80/dir1/dir2/ to /tmp/some/dir1/dir2/index_333.html',
    'Saved http://d1:80/dir1/dir2/dir1_dir2_file1.html to /tmp/some/dir1/dir2/dir1_dir2_file1.html',
    'Saved http://d1:80/dir1/dir2/dir1_dir2_file2.html to /tmp/some/dir1/dir2/dir1_dir2_file2.html',
    'Saved http://d1:80/dir1/dir2/dir1_dir2_file2.html?k=v to /tmp/some/dir1/dir2/dir1_dir2_file2.html?k=v'
}


class FakeRequestMaker(RequestMaker):
    def __init__(self):
        super(FakeRequestMaker, self).__init__(timeout=1, allowed_content_types=[])
        self.urls_requested = set()

    async def make_get_request(self, url: str) -> str:
        await sleep(0.1)
        assert url not in self.urls_requested
        self.urls_requested.add(url)
        return await super(FakeRequestMaker, self).make_get_request(url)

    def get_request_sync(self, url: str) -> str:
        data_dir = Path(__file__).parent / 'data' / 'crawler'
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.split(':')[0] if ':' in parsed_url.netloc else parsed_url.netloc

        path = parsed_url.path.lstrip('/')

        path = data_dir / domain / path
        result = None
        if path.is_file():
            result = path.read_text()
        elif path.is_dir():
            path = path / 'index.html'
            if path.is_file():
                result = path.read_text()
        if result is None:
            raise ValueError('not found')

        if parsed_url.query:
            result += f'\n#query: {parsed_url.query}\n'

        return result


class ContentSaverStub(ContentSaverAbstract):
    def __init__(self):
        self.saved_pages = {}

    def save_page(self, content_path: Path, url: str, content: str) -> Path:
        self.saved_pages[url] = content
        return Path('/tmp')


def __get_path_mark(response_text):
    for line in response_text.split('\n'):
        if line.startswith('#path'):
            path = line.split(' ')[1]
            return path
    return None


def __get_query_mark(response_text):
    for line in response_text.split('\n'):
        if line.startswith('#query'):
            query = line.split(' ')[1]
            return query
    return None


@pytest.mark.asyncio
@pytest.mark.parametrize('url, path_mark, query_mark, expected_exception', [
    ('http://d1/', '/index.html', None, None),
    ('http://d1/index.html', '/index.html', None, None),
    ('http://d1/dir1/', '/dir1/index.html', None, None),
    ('http://d1/dir1/index.html', '/dir1/index.html', None, None),
    ('http://d1/dir1/index.html?key=value', '/dir1/index.html', 'key=value', None),
    ('http://d1/dir1/dir2/dir1_dir2_file1.html', '/dir1/dir2/dir1_dir2_file1.html', None, None),
    ('http://d1/dir1/dir2/', None, None, True),
    ('http://d1/no.html', None, None, True),
])
async def test_fake_request_maker(url, path_mark, query_mark, expected_exception):

    if expected_exception:
        with pytest.raises(Exception):
            await FakeRequestMaker().make_get_request(url)
    else:
        response_text = await FakeRequestMaker().make_get_request(url)
        assert __get_path_mark(response_text) == path_mark
        assert __get_query_mark(response_text) == query_mark


@pytest.mark.asyncio
async def test_crawler():
    site_url = 'http://d1'
    page_cacher = PageCacher()
    content_saver = ContentSaverStub()
    crawler = Crawler(site_url=site_url, page_cacher=page_cacher, request_maker=FakeRequestMaker(),
                      page_parser=PageParser(url=site_url), content_saver=content_saver, timeout=0, threads_cont=2,
                      sleep_seconds=0, empty_loop_sleep_seconds=0.1)
    await crawler.crawl()

    keys = await page_cacher.get_keys()
    url_results = {}
    for key in keys:
        item = await page_cacher.get_item(key)
        url_results[key] = item

    url_results = {
        item.url_normalised: {
            'status': item.status,
            'path_mark': __get_path_mark(item.content),
            'query_mark': __get_query_mark(item.content),
        } for item in url_results.values()}

    assert EXPECTED_URL_RESULTS == url_results

    await crawler.dump(Path('/tmp'))

    assert set(EXPECTED_URL_RESULTS.keys()) == set(content_saver.saved_pages.keys())
