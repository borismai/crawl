from asyncio import sleep


class Doer:
    @classmethod
    def do(cls) -> int:
        print('doing!')
        return 3

    @classmethod
    async def do_async(cls) -> int:
        await sleep(0.1)
        return 3
