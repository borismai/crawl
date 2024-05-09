import abc


class NotHTML(Exception):
    pass


class RequestMakerAbstract:
    @abc.abstractmethod
    async def make_get_request(self, url: str) -> str:
        pass
