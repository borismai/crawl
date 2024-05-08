import pytest

from module.doer import Doer


pytest_plugins = ('pytest_asyncio',)


@pytest.mark.parametrize('arg', [1, 2])
def test_doer(arg):
    print(arg)
    assert Doer.do() == 3


@pytest.mark.asyncio
async def test_do_async():
    assert await Doer().do_async() == 3
