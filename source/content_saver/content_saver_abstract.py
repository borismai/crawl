import abc
from pathlib import Path


class ContentSaverAbstract:
    @abc.abstractmethod
    def save_page(self, content_path: Path, url: str, content: str) -> Path:
        pass
