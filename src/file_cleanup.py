import time
from pathlib import Path

MAX_AGE_SECONDS = 300  # 1 час, теперь 5 минут
MAX_TOTAL_SIZE_MB = 1024  # 1 ГБ


def cleanup_files(dir_paths: list[Path], max_age: int = MAX_AGE_SECONDS, max_size_mb: int = MAX_TOTAL_SIZE_MB):
    if isinstance(dir_paths, Path):
        raise TypeError("Ожидается список путей, а не одиночный Path")
    print('------------------', dir_paths)
    now = time.time()
    size_limit = max_size_mb * 1024 * 1024

    for dir_path in dir_paths:
        if not dir_path.exists() or not dir_path.is_dir():
            continue

        files = [f for f in dir_path.iterdir() if f.is_file()]
        files.sort(key=lambda f: f.stat().st_mtime)  # старые первыми

        total_size = sum(f.stat().st_size for f in files)

        for f in files:
            try:
                file_age = now - f.stat().st_mtime

                # Удаляем по времени
                if file_age > max_age:
                    f.unlink()
                    total_size -= f.stat().st_size
                    continue

                # Удаляем по размеру (если лимит уже превышен)
                if total_size > size_limit:
                    total_size -= f.stat().st_size
                    f.unlink()

            except Exception as e:
                print(f"Ошибка при удалении {f}: {e}")
