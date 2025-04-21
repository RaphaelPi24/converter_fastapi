import asyncio

async def async_progress_bar(duration: float, steps: int = 100):
    delay = duration / steps
    for i in range(steps + 1):
        yield i
        await asyncio.sleep(delay)


def from_number_to_sec(number):
    return number / 100 + 1
