
from typing import Optional, List, Dict

from page_cacher.page_cacher_abstract import PageCacherAbstract
from page_cacher.page_cache_item import PageCacheItemStatus, PageCacheItem
from utils.url_normaliser import URLNormaliser


class PageCacher(PageCacherAbstract):
    def __init__(self):
        self.data: Dict[str, PageCacheItem] = {}

    async def set_item(self, url: str, content: Optional[str] = None,
                       status: PageCacheItemStatus = PageCacheItemStatus.PENDING) \
            -> None:
        url_normalised = self.normalise_url(url)
        item = self.data.get(url_normalised)
        if not item:
            item = PageCacheItem(url_normalised=url_normalised, status=status)
            self.data[url_normalised] = item
            item.url_synonyms.add(url_normalised)
        item.url_synonyms.add(url)
        item.content = content
        item.status = status

    async def get_item(self, url: str) -> Optional[PageCacheItem]:
        url_normalised = self.normalise_url(url)
        found_value = self.data.get(url_normalised)
        if found_value:
            found_value.url_synonyms.add(url)
        return found_value

    def normalise_url(self, url: str) -> str:
        return URLNormaliser.normalise_url(url)

    async def clean(self) -> None:
        self.data = {}

    async def get_keys(self) -> List[str]:
        return list(self.data.keys())

    async def finished(self) -> bool:
        return all([item.status != PageCacheItemStatus.PENDING for item in self.data.values()])
