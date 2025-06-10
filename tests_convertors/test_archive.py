import shutil

import pytest

from converters.convertor import Archive
from tests_convertors.path import OUTPUT_DIR

TMP_WORK_DIR = OUTPUT_DIR / "archive_temp"


@pytest.fixture(autouse=True)
def clean_tmp_dir():
    if TMP_WORK_DIR.exists():
        shutil.rmtree(TMP_WORK_DIR)
    TMP_WORK_DIR.mkdir(parents=True, exist_ok=True)


@pytest.fixture
def prepare_folder(tmp_path):
    folder = tmp_path / "to_archive"
    folder.mkdir()
    test_file = folder / "test.txt"
    test_file.write_text("Hello Archive Test!", encoding="utf-8")
    return folder


def test_zip_archive_and_extract(prepare_folder):
    archive_path = TMP_WORK_DIR / "test.zip"
    extract_path = TMP_WORK_DIR / "unpacked_zip"

    archiver = Archive()
    archiver.convert(
        source_format="folder",
        target_format="zip",
        input_path=prepare_folder,
        output_path=archive_path
    )
    assert archive_path.exists()

    extractor = Archive()
    extractor.convert(
        source_format="zip",
        target_format="folder",
        input_path=archive_path,
        output_path=extract_path
    )
    extracted_file = extract_path / "test.txt"
    assert extracted_file.exists()
    assert extracted_file.read_text(encoding="utf-8") == "Hello Archive Test!"


def test_tar_gz_archive_and_extract(prepare_folder):
    archive_path = TMP_WORK_DIR / "test.tar.gz"
    extract_path = TMP_WORK_DIR / "unpacked_tgz"

    archiver = Archive()
    archiver.convert(
        source_format="folder",
        target_format="tar_gz",
        input_path=prepare_folder,
        output_path=archive_path
    )
    assert archive_path.exists()

    extractor = Archive()
    extractor.convert(
        source_format="tar_gz",
        target_format="folder",
        input_path=archive_path,
        output_path=extract_path
    )
    extracted_file = extract_path / "test.txt"
    assert extracted_file.exists()
    assert extracted_file.read_text(encoding="utf-8") == "Hello Archive Test!"
