from typing import Dict
from unittest import mock

import pytest

from request_maker.request_maker import RequestMaker
from request_maker.request_maker_abstract import NotHTML


class FakeResponse:
    def __init__(self, text: str, headers: Dict, status_exception_type=None):
        self.text = text
        self.headers = headers
        self.status_exception_type = status_exception_type

    def raise_for_status(self):
        if self.status_exception_type:
            raise self.status_exception_type()


@pytest.mark.parametrize('response, expected_text, expected_exception_class', [
    (
            FakeResponse(text='OK', headers={'Content-type': 'text/html some'}),
            'OK',
            None
    ),
    (
            FakeResponse(text='BINARY, NOT OK', headers={'Content-type': 'image/jpeg'}),
            None,
            NotHTML),
    (
            FakeResponse(text='', headers={'Content-type': 'text/html some'}, status_exception_type=ConnectionError),
            None,
            ConnectionError
    ),
])
@pytest.mark.asyncio
async def test_request_maker(response, expected_text, expected_exception_class):
    def __fake_request(*args, **kwargs):
        return response

    with mock.patch('requests.head', side_effect=__fake_request), mock.patch(
            'requests.get', side_effect=__fake_request):
        request_maker = RequestMaker(timeout=3, allowed_content_types=['text/html'])
        if expected_exception_class:
            with pytest.raises(expected_exception_class):
                await request_maker.make_get_request(url='some')
        else:
            result_text = await request_maker.make_get_request(url='some')
            assert result_text == expected_text
