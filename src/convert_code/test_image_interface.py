import pytest
from pathlib import Path
from convert_code.interface import ImageInterface

TEST_FILES_DIR = Path(__file__).resolve().parents[2] / "src" / "convert_code" / "files before conversion"
OUTPUT_DIR = Path(__file__).resolve().parents[2] / "src" / "convert_code" / "files after conversion"

input_format_to_outputs = ImageInterface.conversion_format

@pytest.mark.parametrize("src_fmt,tgt_fmt", [
    (src, tgt) for src, targets in input_format_to_outputs.items() for tgt in targets.keys()
])
def test_image_conversion(src_fmt, tgt_fmt):
    input_file = TEST_FILES_DIR / f"example.{src_fmt}"
    output_file = OUTPUT_DIR / f"{src_fmt}_{tgt_fmt}.{tgt_fmt}"

    interface = ImageInterface(
        source_format=src_fmt,
        target_format=tgt_fmt,
        input_data=input_file,
        output_path=output_file
    )

    result = interface.run()
    assert result is True
    assert output_file.exists()
