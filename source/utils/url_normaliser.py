from urllib.parse import urlparse, ParseResult


class URLNormaliser:
    @classmethod
    def normalise_url(cls, url: str, default_netloc: str = '', add_port=True) -> str:
        url_parsed = urlparse(url)
        scheme = url_parsed.scheme.lower()

        if not scheme:
            scheme = 'http'

        netloc = url_parsed.netloc.lower() if url_parsed.netloc else default_netloc
        if not netloc:
            raise ValueError(f'Could not determine netloc for url: {url}')

        if add_port and ':' not in netloc:
            if scheme == 'http':
                netloc = f'{netloc}:80'
            elif scheme == 'https':
                netloc = f'{netloc}:443'

        parsed_result_args = {
            'scheme': scheme,
            'netloc': netloc,
            'fragment': '',
            'path': url_parsed.path,
            'params': url_parsed.params,
            'query': url_parsed.query,
        }
        return ParseResult(**parsed_result_args).geturl()

    @classmethod
    def denormalise_url(cls, url: str) -> str:
        url_parsed = urlparse(url)
        scheme = url_parsed.scheme.lower()
        netloc = url_parsed.netloc.lower()
        if ':' not in url:
            return url
        host, port = netloc.split(':')
        if (scheme == 'http' and port == '80') or \
                (scheme == 'https' and port == '443'):
            netloc = host

        parsed_result_args = {
            'scheme': scheme,
            'netloc': netloc,
            'fragment': url_parsed.fragment,
            'path': url_parsed.path,
            'params': url_parsed.params,
            'query': url_parsed.query,
        }
        return ParseResult(**parsed_result_args).geturl()
