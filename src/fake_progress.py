import asyncio


# Коэффициенты "скорости" обработки в секундах на мегабайт (или килобайт)
BYTES_IN_MB = 1024 * 1024

# Настраиваемая «скорость» (в секундах) на мегабайт
DEFAULT_SECONDS_PER_MB = 2.0  # легко подстраивается под реальную обработку

def from_number_to_sec(file_size_bytes: int, speed_per_mb: float = DEFAULT_SECONDS_PER_MB) -> float:
    """
    Преобразует размер файла в байтах в длительность прогресса.
    Чем больше файл — тем дольше идёт прогресс.
    :param file_size_bytes: размер файла в байтах
    :param speed_per_mb: количество секунд, которые "тратятся" на мегабайт
    :return: длительность в секундах
    """
    size_in_mb = file_size_bytes / BYTES_IN_MB
    return max(1.0, size_in_mb * speed_per_mb)


async def async_progress_bar(duration: float, steps: int = 100):
    """
    Генератор прогресса. Делит длительность на шаги и постепенно продвигает процент.
    :param duration: общее время (сек)
    :param steps: количество шагов прогресса (по умолчанию 100)
    """
    delay = duration / steps
    for i in range(steps + 1):
        yield i
        await asyncio.sleep(delay)
