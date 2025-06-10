from pathlib import Path

import pytest

from converters.convertor import Selector
from tests_convertors.path import INPUT_DIR, OUTPUT_DIR, skip_if_missing, cleanup_output


def test_universal_interface_unsupported_format():
    with pytest.raises(ValueError, match=f"Формат 'rar' → 'folder' не поддерживается ни одним конвертором."):
        Selector(
            source_format="rar",
            target_format="folder",
            input_path=Path("/tmp/dummy.txt"),
            output_path=Path("/tmp/dummy.txt")
        )


def test_universal_interface_supported_format(cleanup_output):
    input_file = INPUT_DIR / f"example.txt"
    output_file = OUTPUT_DIR / f"txt_to_pdf.pdf"

    skip_if_missing(input_file)
    cleanup_output(output_file)

    convertor = Selector(
        source_format='txt',
        target_format='pdf',
        input_path=input_file,
        output_path=output_file
    )
    convertor.run()

    assert output_file.exists()
