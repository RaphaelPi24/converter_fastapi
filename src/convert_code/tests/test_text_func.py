from pathlib import Path
import pytest

from convert_code.text import (
    txt_to_csv, txt_to_json, txt_to_pdf, txt_to_docx,
    csv_to_txt, json_to_txt, pdf_to_txt, docx_to_txt
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FILES_DIR = PROJECT_ROOT / "src" / "convert_code"
INPUT_DIR = FILES_DIR / "files before conversion"
OUTPUT_DIR = FILES_DIR / "files after conversion"


@pytest.fixture
def cleanup_file():
    def _clean(path: Path):
        if path.exists():
            path.unlink()
    return _clean


def skip_if_missing(path: Path):
    if not path.exists():
        pytest.skip(f"Пропущен: отсутствует входной файл {path.name}")


def test_txt_to_csv(cleanup_file):
    input_file = INPUT_DIR / "example.txt"
    output_file = OUTPUT_DIR / "test_txt_to_csv.csv"
    skip_if_missing(input_file)
    cleanup_file(output_file)

    txt_to_csv(input_file, output_file)
    assert output_file.exists()


def test_txt_to_json(cleanup_file):
    input_file = INPUT_DIR / "example.txt"
    output_file = OUTPUT_DIR / "test_txt_to_json.json"
    skip_if_missing(input_file)
    cleanup_file(output_file)

    txt_to_json(input_file, output_file)
    assert output_file.exists()


def test_csv_to_txt(cleanup_file):
    input_file = INPUT_DIR / "example.csv"
    output_file = OUTPUT_DIR / "test_csv_to_txt.txt"
    skip_if_missing(input_file)
    cleanup_file(output_file)

    csv_to_txt(input_file, output_file)
    assert output_file.exists()


def test_json_to_txt(cleanup_file):
    input_file = INPUT_DIR / "example.json"
    output_file = OUTPUT_DIR / "test_json_to_txt.txt"
    skip_if_missing(input_file)
    cleanup_file(output_file)

    json_to_txt(input_file, output_file)
    assert output_file.exists()


def test_txt_to_pdf(cleanup_file):
    input_file = INPUT_DIR / "example.txt"
    output_file = OUTPUT_DIR / "test_txt_to_pdf.pdf"
    skip_if_missing(input_file)
    cleanup_file(output_file)

    txt_to_pdf(input_file, output_file)
    assert output_file.exists()


def test_pdf_to_txt(cleanup_file):
    input_file = INPUT_DIR / "example.pdf"
    output_file = OUTPUT_DIR / "test_pdf_to_txt.txt"
    skip_if_missing(input_file)
    cleanup_file(output_file)

    pdf_to_txt(input_file, output_file)
    assert output_file.exists()


def test_docx_to_txt(cleanup_file):
    input_file = INPUT_DIR / "example.docx"
    output_file = OUTPUT_DIR / "test_docx_to_txt.txt"
    skip_if_missing(input_file)
    cleanup_file(output_file)

    docx_to_txt(input_file, output_file)
    assert output_file.exists()


def test_txt_to_docx(cleanup_file):
    input_file = INPUT_DIR / "example.txt"
    output_file = OUTPUT_DIR / "test_txt_to_docx.docx"
    skip_if_missing(input_file)
    cleanup_file(output_file)

    txt_to_docx(input_file, output_file)
    assert output_file.exists()
