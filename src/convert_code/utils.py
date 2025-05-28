from pathlib import Path

from config import CONVERTED_DIR
from convert_code.interface import UniversalInterface


def get_converted_filename(original_filename: str, target_format: str) -> str:
    """
    Возвращает имя нового файла после конвертации.
    Пример: ("report.txt", "pdf") → "report_converted.pdf"
    """
    print(target_format)
    source, target = target_format.split("_to_")
    stem = Path(original_filename).stem
    return f"{stem}_converted.{target}"


def convert_file(input_path: str, filename: str, conversion_type: str) -> None:
    """
    Универсальная точка входа для RQ worker. Вызывает нужный интерфейс.
    :param input_path: путь до входного файла
    :param filename: имя входного файла
    :param conversion_type: строка вида 'txt_to_pdf'
    """
    print('начало конвертации')
    source, target = conversion_type.split("_to_")
    input_path = Path(input_path)
    new_name = get_converted_filename(filename, conversion_type)
    output_path = CONVERTED_DIR / new_name
    print('---------------------', output_path)
    interface = UniversalInterface(source_format=source, target_format=target, input_path=input_path,
                                   output_path=output_path)
    interface.run()
    print('ее конец')
