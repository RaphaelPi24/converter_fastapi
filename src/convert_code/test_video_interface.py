from pathlib import Path

import pytest

from src.convert_code.interface import VideoInterface

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


def run_video_test(source_filename, target_ext, cleanup_file):
    input_file = INPUT_DIR / source_filename
    output_file = OUTPUT_DIR / f"test_{input_file.stem}_to_{target_ext}.{target_ext}"
    skip_if_missing(input_file)
    cleanup_file(output_file)

    interface = VideoInterface(
        source_format=input_file.suffix[1:],  # без точки
        target_format=target_ext,
        input_data=input_file,
        output_path=output_file
    )
    interface.run()
    assert output_file.exists()


def test_mp4_to_avi(cleanup_file):
    run_video_test("sample.mp4", "avi", cleanup_file)


def test_mp4_to_webm(cleanup_file):
    run_video_test("sample.mp4", "webm", cleanup_file)


def test_avi_to_mp4(cleanup_file):
    run_video_test("sample.avi", "mp4", cleanup_file)


def test_webm_to_mp4(cleanup_file):
    run_video_test("sample.webm", "mp4", cleanup_file)
