import pytest

from page_cacher.page_cache_item import PageCacheItemStatus
from page_cacher.page_cacher import PageCacher


pytest_plugins = ('pytest_asyncio',)


@pytest.mark.parametrize('urls, cache_dump_expected', [
    (
        (
            'http://ya.ru/some',
            'http://ya.ru/',
        ),
        {
            'http://ya.ru:80/some': {
                'url_normalised': 'http://ya.ru:80/some',
                'url_synonyms': {'http://ya.ru/some', 'http://ya.ru:80/some'},
                'content': '',
                'status': PageCacheItemStatus.PENDING,
            },
            'http://ya.ru:80/': {
                'url_normalised': 'http://ya.ru:80/',
                'url_synonyms': {'http://ya.ru/', 'http://ya.ru:80/'},
                'content': '',
                'status': PageCacheItemStatus.PENDING,
            },
        }
    ),
    (
        (
            'https://ya.ru/some',
            'https://YA.ru/some#anchor',
            'https://ya.ru/',
            'https://ya.RU/',
            'HTTPs://ya.RU/',
        ),
        {
            'https://ya.ru:443/some': {
                'url_normalised': 'https://ya.ru:443/some',
                'url_synonyms': {'https://ya.ru/some', 'https://YA.ru/some#anchor', 'https://ya.ru:443/some'},
                'content': '',
                'status': PageCacheItemStatus.PENDING,
            },
            'https://ya.ru:443/': {
                'url_normalised': 'https://ya.ru:443/',
                'url_synonyms': {'https://ya.ru/', 'https://ya.RU/', 'HTTPs://ya.RU/', 'https://ya.ru:443/'},
                'content': '',
                'status': PageCacheItemStatus.PENDING,
            },
        }
    ),
])
@pytest.mark.asyncio
async def test_synonyms(urls, cache_dump_expected):

    async def get_dump(_cacher):
        cache_dump = {}
        for key in await _cacher.get_keys():
            item = await _cacher.get_item(key)
            cache_dump[key] = {
                'url_normalised': item.url_normalised,
                'url_synonyms': item.url_synonyms,
                'content': item.content,
                'status': item.status,
            }
        return cache_dump

    cacher = PageCacher()

    content = ''
    for url in urls:
        await cacher.set_item(url, content=content)
    assert cache_dump_expected == await get_dump(cacher)


@pytest.mark.asyncio
async def test_finished():
    cacher = PageCacher()

    some_url = 'http://path/'
    await cacher.set_item(url=some_url)
    assert not await cacher.finished()

    await cacher.set_item(url=some_url, status=PageCacheItemStatus.ERROR)
    assert await cacher.finished()

    other_url = 'http://path/other'
    await cacher.set_item(url=other_url)
    assert not await cacher.finished()

    await cacher.set_item(url=other_url, status=PageCacheItemStatus.OK)
    assert await cacher.finished()
