from pathlib import Path


def cleanup_files(filepath: Path) -> None:
    try:
        if filepath.is_file():
            filepath.unlink()
            print(f"Файл {filepath} успешно удалён")
        else:
            print(f"Файл {filepath} не существует или это не файл")
    except Exception as e:
        print(f"Ошибка при удалении {filepath}: {e}")
