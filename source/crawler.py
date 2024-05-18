import asyncio
import datetime
from asyncio import sleep
from pathlib import Path
from urllib.parse import urlparse

from content_saver.content_saver_abstract import ContentSaverAbstract
from page_cacher.page_cache_item import PageCacheItemStatus
from page_cacher.page_cacher_abstract import PageCacherAbstract
from page_parser.page_parser_abstract import PageParserAbstract
from request_maker.request_maker_abstract import RequestMakerAbstract
from utils.url_normaliser import URLNormaliser


class Crawler:
    def __init__(self, site_url: str, page_cacher: PageCacherAbstract,
                 request_maker: RequestMakerAbstract, page_parser: PageParserAbstract,
                 content_saver: ContentSaverAbstract, timeout: int, threads_cont: int, sleep_seconds: int,
                 empty_loop_sleep_seconds: float = 0.1):
        self.page_cacher = page_cacher
        self.request_maker = request_maker
        self.page_parser = page_parser
        self.content_saver = content_saver
        self.timeout = timeout
        self.threads_cont = threads_cont
        self.sleep_seconds = sleep_seconds
        self.empty_loop_sleep_seconds = empty_loop_sleep_seconds

        site_url_norm = URLNormaliser.normalise_url(site_url)
        url_parsed = urlparse(site_url_norm)

        self.netloc = url_parsed.netloc
        self.site_url = site_url_norm

        self.urls_to_process = []

    async def crawl(self):
        await self.add_url_to_process(self.site_url)

        current_tasks = set()
        current_tasks.add(asyncio.create_task(self.process_url(self.site_url)))
        while self.urls_to_process or not await self.page_cacher.finished() or current_tasks:
            self.log(f'current_tasks len: {len(current_tasks)}')
            finished, current_tasks = await asyncio.wait(current_tasks, return_when=asyncio.FIRST_COMPLETED)

            if not self.urls_to_process:
                self.log('no new urls to process')
                await sleep(self.empty_loop_sleep_seconds)

            while self.urls_to_process and len(current_tasks) < self.threads_cont:
                url = self.urls_to_process.pop(0)
                if not await self.page_cacher.get_item(url=url):
                    await self.page_cacher.set_item(url=url, status=PageCacheItemStatus.PENDING)
                    current_tasks.add(asyncio.create_task(self.process_url(url)))

    async def process_url(self, url: str) -> None:
        try:
            content = await self.request_maker.make_get_request(url)
        except Exception as exception:
            await self.page_cacher.set_item(url=url, status=PageCacheItemStatus.ERROR, content=str(exception))
            return None

        await self.page_cacher.set_item(url=url, status=PageCacheItemStatus.OK, content=content)

        new_urls = self.page_parser.get_absolute_local_urls(page_url=url, page=content)

        for url in new_urls:
            await self.add_url_to_process(url)

        await sleep(self.sleep_seconds)

    async def add_url_to_process(self, url: str) -> None:
        if not await self.page_cacher.get_item(url):
            self.urls_to_process.append(url)

    async def dump(self, content_path: Path):
        keys = await self.page_cacher.get_keys()
        for key in keys:
            item = await self.page_cacher.get_item(key)
            filepath = self.content_saver.save_page(content_path=content_path, url=item.url_normalised,
                                                    content=item.content)
            self.log(f'Saved {item.url_normalised} to {filepath}')

    def log(self, message: str) -> None:
        print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {message}")

