#!/usr/bin/env python3
from typing import Iterable, Optional
from anyio import run, create_task_group
from aiohttp import ClientSession
from itertools import repeat


class HttpClient:
    def __init__(self, session: ClientSession) -> None:
        self._session = session

    async def get_any(self, urls: Iterable[str]) -> Optional[bytes]:
        result = None
        async with create_task_group() as tg:

            async def task(url: str) -> None:
                try:
                    async with self._session.get(url) as response:
                        if response.status == 200:
                            nonlocal result
                            result = await response.content.read()
                            tg.cancel_scope.cancel()
                except Exception:
                    pass

            for url in urls:
                tg.start_soon(task, url)
        return result


async def main() -> None:
    async with ClientSession() as session:
        http_client = HttpClient(session)
        print(await http_client.get_any(repeat('http://worldclockapi.com/api/json/utc/now', 2)))


if __name__ == '__main__':
    run(main)
