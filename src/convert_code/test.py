import os
from pathlib import Path
import pytest

from src.convert_code.image import (
    jpg_to_webp, png_to_webp,
    webp_to_png, webp_to_jpg,
    svg_to_png, jpg_to_svg,
    png_to_svg
)

# Пути к директориям
BASE_DIR = Path(__file__).resolve().parent
FILES_DIR = BASE_DIR / "convert_code"
INPUT_DIR = FILES_DIR / "files before conversion"
OUTPUT_DIR = FILES_DIR / "files after conversion"

# Фикстура очистки выходного файла
@pytest.fixture
def cleanup_file():
    def _clean(path: Path):
        if path.exists():
            path.unlink()
    return _clean

def test_jpg_to_webp(cleanup_file):
    input_file = INPUT_DIR / "1722632278781.jpg"
    output_file = OUTPUT_DIR / "test_converted.webp"
    cleanup_file(output_file)

    jpg_to_webp(input_file, output_file)
    assert output_file.exists()

def test_webp_to_jpg(cleanup_file):
    input_file = INPUT_DIR / "1720436187320.webp"
    output_file = OUTPUT_DIR / "test_converted.jpg"
    cleanup_file(output_file)

    webp_to_jpg(input_file, output_file)
    assert output_file.exists()

def test_webp_to_png(cleanup_file):
    input_file = INPUT_DIR / "1720436187320.webp"
    output_file = OUTPUT_DIR / "test_converted.png"
    cleanup_file(output_file)

    webp_to_png(input_file, output_file)
    assert output_file.exists()

# def test_svg_to_png(cleanup_file):
#     input_file = INPUT_DIR / "1727482.svg"
#     output_file = OUTPUT_DIR / "test_converted.png"
#     cleanup_file(output_file)
#
#     svg_to_png(input_file, output_file)
#     assert output_file.exists()
#
# def test_png_to_svg(cleanup_file):
#     input_file = INPUT_DIR / "Без названия.png"
#     output_file = OUTPUT_DIR / "test_converted.svg"
#     cleanup_file(output_file)
#
#     png_to_svg(input_file, output_file)
#     assert output_file.exists()
