import abc
from typing import List


class PageParserAbstract:
    @abc.abstractmethod
    def get_absolute_local_urls(self, page_url: str, page: str) -> List[str]:
        pass
