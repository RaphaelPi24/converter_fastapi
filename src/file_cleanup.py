from pathlib import Path


def cleanup_files(filepath: Path) -> None:
    print(type(filepath))
    try:
        filepath.unlink()
    except Exception as e:
        print(e)
