from pathlib import Path

import pytest

from src.convert_code.image import (
    jpg_to_webp, webp_to_png, webp_to_jpg,
    svg_to_png, png_to_svg
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FILES_DIR = PROJECT_ROOT / "src" / "convert_code"
INPUT_DIR = FILES_DIR / "files before conversion"
OUTPUT_DIR = FILES_DIR / "files after conversion"


# Фикстура очистки выходного файла
@pytest.fixture
def cleanup_file():
    def _clean(path: Path):
        if path.exists():
            path.unlink()

    return _clean


def skip_if_missing(path: Path):
    if not path.exists():
        pytest.skip(f"Пропущен: отсутствует входной файл {path.name}")


def test_jpg_to_webp(cleanup_file):
    input_file = INPUT_DIR / "example.jpg"
    output_file = OUTPUT_DIR / "test_jpg_to_webp.webp"
    skip_if_missing(input_file)
    cleanup_file(output_file)

    jpg_to_webp(input_file, output_file)
    assert output_file.exists()


def test_webp_to_jpg(cleanup_file):
    input_file = INPUT_DIR / "example.webp"
    output_file = OUTPUT_DIR / "test_webp_to_jpg.jpg"
    skip_if_missing(input_file)
    cleanup_file(output_file)

    webp_to_jpg(input_file, output_file)
    assert output_file.exists()


def test_webp_to_png(cleanup_file):
    input_file = INPUT_DIR / "example.webp"
    output_file = OUTPUT_DIR / "test_webp_to_png.png"
    skip_if_missing(input_file)
    cleanup_file(output_file)

    webp_to_png(input_file, output_file)
    assert output_file.exists()


def test_svg_to_png(cleanup_file):
    input_file = INPUT_DIR / "example.svg"
    output_file = OUTPUT_DIR / "test_svg_to_png.png"
    skip_if_missing(input_file)
    cleanup_file(output_file)

    svg_to_png(input_file, output_file)
    assert output_file.exists()


def test_png_to_svg(cleanup_file):
    input_file = INPUT_DIR / "example.png"
    output_file = OUTPUT_DIR / "test_png_to_svg.svg"
    skip_if_missing(input_file)
    cleanup_file(output_file)

    png_to_svg(input_file, output_file)
    assert output_file.exists()
