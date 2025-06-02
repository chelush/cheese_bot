import functools
import random
from typing import Callable

import aiohttp

def pass_exception(coro: Callable, *exceptions):
    @functools.wraps(coro)
    async def wrapper():
        try:
            return await coro
        except exceptions:
            pass

    return wrapper()