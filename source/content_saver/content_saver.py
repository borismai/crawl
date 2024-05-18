from pathlib import Path
from random import randint
from urllib.parse import urlparse

from content_saver.content_saver_abstract import ContentSaverAbstract


class ContentSaver(ContentSaverAbstract):
    @classmethod
    def save_page(cls, content_path: Path, url: str, content: str) -> Path:
        filepath = cls.get_absolute_path(content_path, url)
        if not filepath.parent.exists():
            filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content)

        return filepath

    @classmethod
    def get_absolute_path(cls, content_path: Path, url: str) -> Path:
        parsed_url = urlparse(url)

        path = parsed_url.path
        if not path:
            path = '/'
        if path[-1] == '/':
            path += f'index_{cls.get_uniq_name()}.html'

        if parsed_url.query:
            path += '?' + parsed_url.query

        return content_path / path.lstrip('/')

    @classmethod
    def get_uniq_name(cls):
        return randint(1, 999999999999)

