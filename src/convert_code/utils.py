from pathlib import Path

from convert_code.interface import UniversalInterface


def get_converted_filename(original_filename: str, target_format: str) -> str:
    """
    Возвращает имя нового файла после конвертации.
    Пример: ("report.txt", "pdf") → "report_converted.pdf"
    """
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
    source, target = conversion_type.split("_to_")
    input_path = Path(input_path)
    output_dir = Path(__file__).resolve().parent.parent / "converted_files"
    output_dir.mkdir(exist_ok=True)
    output_filename = f"{input_path.stem}_converted.{target}"
    output_path = output_dir / output_filename

    interface = UniversalInterface(source_format=source, target_format=target, input_data=input_path,
                                   output_path=output_path)
    interface.run()

#
# from convert_code.text import txt_to_csv, txt_to_json, csv_to_txt, json_to_txt
#
#
# CONVERTED_FOLDER = Path("converted_files")
# CONVERTED_FOLDER.mkdir(exist_ok=True)
#
#
# def get_converted_filename(original_name: str, conversion_type: str) -> str:
#     stem = Path(original_name).stem
#     ext_map = {
#         "txt_to_csv": ".csv",
#         "txt_to_json": ".json",
#         "csv_to_txt": ".txt",
#         "json_to_txt": ".txt",
#     }
#     new_ext = ext_map.get(conversion_type, ".txt")
#     return f"{stem}{new_ext}"
#
#
# def convert_file(input_path: str, output_filename: str, conversion_type: str):
#     input_path = Path(input_path)
#     output_path = CONVERTED_FOLDER / get_converted_filename(output_filename, conversion_type)
#
#     print(f"📂 Конвертация: {conversion_type}")
#     print(f"📥 Исходный файл: {input_path}")
#     print(f"📤 Будет сохранён в: {output_path}")
#
#     with input_path.open("r", encoding="utf-8") as infile:
#         content = infile.read()
#
#     match conversion_type:
#         case "txt_to_csv":
#             txt_to_csv(content, output_path)
#         case "txt_to_json":
#             txt_to_json(content, output_path)
#         case "csv_to_txt":
#             csv_to_txt(input_path, output_path)
#         case "json_to_txt":
#             json_to_txt(content, output_path)
#         case _:
#             raise ValueError(f"Unsupported conversion type: {conversion_type}")
#
#     print(f"✅ Файл сконвертирован: {output_path.name}")
#
#
# ext_map = {
#     "txt_to_csv": {
#         "format": ".csv",
#         "converter": txt_to_csv,
#     },
#     "txt_to_json": ".json",
#     "csv_to_txt": ".txt",
#     "json_to_txt": ".txt",
# }
#
