import asyncio
from pathlib import Path
from sys import argv

from crawler import Crawler
from page_cacher.page_cacher import PageCacher
from page_parser.page_parser import PageParser
from request_maker.request_maker import RequestMaker


async def main():
    site_url = argv[1]
    content_dir = Path(argv[2])
    allowed_content = ['text/html']
    crawler = Crawler(site_url=site_url, page_cacher=PageCacher(),
                      request_maker=RequestMaker(allowed_content_types=allowed_content, timeout=10),
                      page_parser=PageParser(url=site_url), timeout=0, threads_cont=2, sleep_seconds=0)

    await crawler.crawl()
    await crawler.dump(content_path=content_dir)


if __name__ == '__main__':
    asyncio.run(main())