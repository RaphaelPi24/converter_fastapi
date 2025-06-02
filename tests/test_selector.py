import pytest
from converters.convertor import Selector
from pathlib import Path

def test_universal_interface_unsupported_format():
    with pytest.raises(ValueError, match=f"Формат 'rar' → 'folder' не поддерживается ни одним конвертором."):
        Selector(
            source_format="rar",
            target_format="folder",
            input_path=Path("/tmp/dummy.txt"),
            output_path=Path("/tmp/dummy.txt")
        )