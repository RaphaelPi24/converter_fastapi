import pytest

from convert_code.interface import TextInterface

conversion_format = TextInterface.conversion_format
from path import INPUT_DIR, OUTPUT_DIR


@pytest.mark.parametrize("src_fmt,tgt_fmt", [
    (src, tgt) for src, targets in conversion_format.items() for tgt in targets.keys()
])
def test_text_conversion(src_fmt, tgt_fmt):
    input_file = INPUT_DIR / f"example.{src_fmt}"
    output_file = OUTPUT_DIR / f"{src_fmt}_{tgt_fmt}.{tgt_fmt}"

    interface = TextInterface(
        source_format=src_fmt,
        target_format=tgt_fmt,
        input_data=input_file,
        output_path=output_file
    )

    result = interface.run()
    assert result is True
    assert output_file.exists()
