import pytest

from converters.convertor import Image
from path import INPUT_DIR, OUTPUT_DIR, skip_if_missing, cleanup_output

conversion_formats = Image.conversion_formats


@pytest.mark.parametrize("source_format,target_format", [
    (src, tgt) for src, targets in conversion_formats.items() for tgt in targets
])
def test_image_conversion(source_format, target_format, cleanup_output):
    input_file = INPUT_DIR / f"example.{source_format}"
    output_file = OUTPUT_DIR / f"{source_format}_to_{target_format}.{target_format}"

    skip_if_missing(input_file)
    cleanup_output(output_file)

    interface = Image()
    interface.convert(
        source_format=source_format,
        target_format=target_format,
        input_path=input_file,
        output_path=output_file
    )

    assert output_file.exists()
