from pathlib import Path
import pytest

from converters.convertor import Video
from path import INPUT_DIR, OUTPUT_DIR

conversion_formats = Video.conversion_formats


@pytest.fixture(autouse=True)
def cleanup_output():
    """Удаляет выходной файл перед тестом (если он существует)."""
    def _clean(path: Path):
        if path.exists():
            path.unlink()
    return _clean


def skip_if_missing(path: Path):
    if not path.exists():
        pytest.skip(f"Пропущен: отсутствует входной файл {path.name}")


@pytest.mark.parametrize("source_format,target_format", [
    (src, tgt) for src, targets in conversion_formats.items() for tgt in targets
])
def test_video_conversion(source_format, target_format, cleanup_output):
    input_file = INPUT_DIR / f"sample.{source_format}"
    output_file = OUTPUT_DIR / f"{source_format}_to_{target_format}.{target_format}"

    skip_if_missing(input_file)
    cleanup_output(output_file)

    interface = Video()
    interface.convert(
        source_format=source_format,
        target_format=target_format,
        input_path=input_file,
        output_path=output_file
    )

    assert output_file.exists()
