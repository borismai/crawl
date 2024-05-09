import pytest

from page_parser.page_parser import PageParser


TEST_HTML = '''
<html><head><title>Test</title></head>
<body><h1>Parse me!</h1>

<A href="http://ya.ru/some/path/file.html">abs</a>
<a href="http://ya.ru/some/path/other.html">abs other</A>
<A href="http://ya.ru/some/path/file.html#anc">abs same w anchor</a>
<a href="http://ya.ru/some/path/other.html#anc">abs other w anchor</A>
<a href="other.html">rel nearest file</a>
<a href="/at_root.html">rel file at root</a>
<a href="http://ya.ru:80/my/path/index.html">self abs</a>
<a href="index.html">self local</a>
<a href="http://mail.ru/some_non_local.html">not local</a>
<a href="https://ya.ru/some_secret">other domain</a>

</body></html>
'''


def test_get_hrefs():
    assert {
               '/at_root.html',
               'http://mail.ru/some_non_local.html',
               'http://ya.ru/some/path/file.html',
               'http://ya.ru/some/path/file.html#anc',
               'http://ya.ru/some/path/other.html',
               'http://ya.ru/some/path/other.html#anc',
               'http://ya.ru:80/my/path/index.html',
               'https://ya.ru/some_secret',
               'index.html',
               'other.html'
           } == set(PageParser(url='http://a1.tu').get_hrefs(TEST_HTML))


def test_abs_urls():
    page_url = 'http://ya.ru:80/my/path/index.html'

    result_expected = [
        'http://ya.ru:80/some/path/file.html',
        'http://ya.ru:80/some/path/other.html',
        'http://ya.ru:80/some/path/file.html',
        'http://ya.ru:80/some/path/other.html',
        'http://ya.ru:80/my/path/other.html',
        'http://ya.ru:80/at_root.html',
        'http://ya.ru:80/my/path/index.html',
        'http://ya.ru:80/my/path/index.html',
    ]
    assert result_expected == PageParser(url=page_url).get_absolute_local_urls(page_url=page_url, page=TEST_HTML)
