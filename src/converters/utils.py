from pathlib import Path

from config import CONVERTED_DIR
from converters.convertor import Selector


def get_converted_filename(original_filename: str, target_format: str) -> str:
    source, target = target_format.split("_to_")
    stem = Path(original_filename).stem
    return f"{stem}_converted.{target}"


def convert_file(input_path: str, filename: str, conversion_type: str) -> None:
    source, target = conversion_type.split("_to_")
    input_path = Path(input_path)
    new_name = get_converted_filename(filename, conversion_type)
    output_path = CONVERTED_DIR / new_name
    convertor = Selector(source_format=source, target_format=target, input_path=input_path,
                         output_path=output_path)
    convertor.run()
