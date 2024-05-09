import dataclasses
from enum import Enum
from typing import Optional, Set


class PageCacheItemStatus(Enum):
    PENDING = 'pending'
    OK = 'ok'
    ERROR = 'error'


@dataclasses.dataclass
class PageCacheItem:
    url_normalised: str
    status: PageCacheItemStatus
    content: Optional[str] = dataclasses.field(default_factory=str)
    url_synonyms: Set[str] = dataclasses.field(default_factory=set)
