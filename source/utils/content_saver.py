from pathlib import Path
from random import randint
from urllib.parse import urlparse


class ContentSaver:
    @classmethod
    def get_absolute_path(cls, content_path: Path, url: str) -> Path:
        parsed_url = urlparse(url)

        path = parsed_url.path
        if not path:
            path = '/'
        if path[-1] == '/':
            path += f'index_{randint(1, 999999999999)}.html'

        if parsed_url.query:
            path += '?' + parsed_url.query

        return content_path / path.lstrip('/')

    @classmethod
    def save_page(cls, content_path: Path, url: str, content: str) -> Path:
        filepath = cls.get_absolute_path(content_path, url)
        filepath.write_text(content)

        return filepath
