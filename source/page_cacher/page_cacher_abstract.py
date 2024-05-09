import abc
from typing import Optional, List

from page_cacher.page_cache_item import PageCacheItemStatus, PageCacheItem


class PageCacherAbstract:
    @abc.abstractmethod
    async def set_item(self, url: str, content: Optional[str] = None,
                       status: PageCacheItemStatus = PageCacheItemStatus.PENDING) \
            -> None:
        pass

    @abc.abstractmethod
    async def get_item(self, url: str) -> Optional[PageCacheItem]:
        pass

    @abc.abstractmethod
    async def clean(self) -> None:
        pass

    @abc.abstractmethod
    async def get_keys(self) -> List[str]:
        pass

    @abc.abstractmethod
    async def finished(self) -> bool:
        pass
