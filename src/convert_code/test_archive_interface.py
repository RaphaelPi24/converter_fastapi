from pathlib import Path

import pytest

from convert_code.interface import ArchiveInterface

FILES_DIR = Path(__file__).resolve().parents[2] / "src" / "convert_code"
INPUT_DIR = FILES_DIR / "files before conversion"
OUTPUT_DIR = FILES_DIR / "files after conversion"
TMP_WORK_DIR = OUTPUT_DIR / "archive_temp"


@pytest.fixture
def prepare_folder(tmp_path):
    # Копирует одну папку с файлами для архивации
    folder = tmp_path / "to_archive"
    folder.mkdir()
    test_file = folder / "test.txt"
    test_file.write_text("Hello Archive Test!", encoding="utf-8")
    return folder


def test_zip_archive_and_extract(prepare_folder):
    archive_path = TMP_WORK_DIR / "test.zip"
    extract_path = TMP_WORK_DIR / "unpacked_zip"
    archive_path.parent.mkdir(parents=True, exist_ok=True)

    # Архивация
    archiver = ArchiveInterface(
        source_format="folder",  # => это архивирование
        target_format=".zip",
        input_data=prepare_folder,
        output_path=archive_path
    )
    archiver.run()
    assert archive_path.exists()

    # Распаковка
    extractor = ArchiveInterface(
        source_format=".zip",
        target_format="folder",
        input_data=archive_path,
        output_path=extract_path
    )
    extractor.run()
    extracted_file = extract_path / "test.txt"
    assert extracted_file.exists()
    assert extracted_file.read_text() == "Hello Archive Test!"


def test_tar_gz_archive_and_extract(prepare_folder):
    archive_path = TMP_WORK_DIR / "test.tar.gz"
    extract_path = TMP_WORK_DIR / "unpacked_tgz"
    archive_path.parent.mkdir(parents=True, exist_ok=True)

    # Архивация
    archiver = ArchiveInterface(
        source_format="folder",
        target_format=".tar.gz",
        input_data=prepare_folder,
        output_path=archive_path
    )
    archiver.run()
    assert archive_path.exists()

    # Распаковка
    extractor = ArchiveInterface(
        source_format=".tar.gz",
        target_format="folder",
        input_data=archive_path,
        output_path=extract_path
    )
    extractor.run()
    extracted_file = extract_path / "test.txt"
    assert extracted_file.exists()
    assert extracted_file.read_text() == "Hello Archive Test!"


def test_invalid_format_raises_error():
    dummy_path = Path("dummy")  # допустим, несуществующий путь
    with pytest.raises(ValueError, match=r"Неподдерживаемый формат"):
        ArchiveInterface(
            source_format=".rar",  # <- заведомо неподдерживаемый формат
            target_format="folder",
            input_data=dummy_path,
            output_path=dummy_path
        )
