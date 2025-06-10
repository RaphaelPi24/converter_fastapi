from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FILES_DIR = PROJECT_ROOT / "tests_convertors"
INPUT_DIR = FILES_DIR / "files before conversion"
OUTPUT_DIR = FILES_DIR / "files after conversion"


@pytest.fixture(autouse=True)
def cleanup_output():
    def _clean(path: Path):
        if path.exists():
            path.unlink()

    return _clean


def skip_if_missing(path: Path):
    if not path.exists():
        pytest.skip(f"Пропущен: отсутствует входной файл {path.name}")
