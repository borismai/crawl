from typing import List
from urllib.parse import urljoin, urlparse

from page_parser.page_parser_abstract import PageParserAbstract
from page_parser.simple_html_parser import SimpleHTMLParser
from utils.url_normaliser import URLNormaliser


class PageParser(PageParserAbstract):
    def __init__(self, url: str):
        url_parsed = urlparse(URLNormaliser.normalise_url(url=url))
        self.netloc = url_parsed.netloc
        self.html_parser = SimpleHTMLParser()

    def get_absolute_local_urls(self, page_url: str, page: str) -> List[str]:
        result = []
        for href in self.get_hrefs(page):
            url = urljoin(page_url, href)
            url_norm = URLNormaliser.normalise_url(url=url)
            if self.is_local(url_norm):
                result.append(url_norm)
        return result

    def is_local(self, url: str) -> bool:
        url_parsed = urlparse(url)
        if not url_parsed.netloc:
            return True
        if url_parsed.netloc == self.netloc:
            return True
        return False

    def get_hrefs(self, page: str) -> List[str]:
        self.html_parser.hrefs = []
        self.html_parser.feed(page)
        self.html_parser.reset()
        return self.html_parser.hrefs

    def get_absolute_urls(self, page_url: str, page: str) -> List[str]:
        return [urljoin(page_url, href) for href in self.get_hrefs(page)]
