from concurrent.futures import ProcessPoolExecutor
import asyncio


def async_wrapper(func):
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        with ProcessPoolExecutor(max_workers=1) as executor:
            result = await loop.run_in_executor(executor, func, *args, **kwargs)
        return result
    return wrapper
