from pathlib import Path

CONVERTED_FOLDER = Path("converted")
CONVERTED_FOLDER.mkdir(exist_ok=True)


import json
import csv
from pathlib import Path

CONVERTED_FOLDER = Path("converted")
CONVERTED_FOLDER.mkdir(exist_ok=True)


def get_converted_filename(original_name: str, conversion_type: str) -> str:
    stem = Path(original_name).stem
    ext_map = {
        "txt_to_csv": ".csv",
        "txt_to_json": ".json",
        "csv_to_txt": ".txt",
        "json_to_txt": ".txt",
    }
    new_ext = ext_map.get(conversion_type, ".txt")
    return f"{stem}{new_ext}"


def txt_to_csv(content: str, output_path: Path):
    lines = content.strip().splitlines()
    rows = [line.split() for line in lines]
    with output_path.open("w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)


def txt_to_json(content: str, output_path: Path):
    lines = content.strip().splitlines()
    data = {"lines": lines}
    with output_path.open("w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=2)


def csv_to_txt(input_path: Path, output_path: Path):
    with input_path.open("r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        with output_path.open("w", encoding="utf-8") as txtfile:
            for row in reader:
                txtfile.write(" ".join(row) + "\n")


def json_to_txt(content: str, output_path: Path):
    data = json.loads(content)
    with output_path.open("w", encoding="utf-8") as txtfile:
        if isinstance(data, dict):
            for key, value in data.items():
                txtfile.write(f"{key}: {value}\n")
        elif isinstance(data, list):
            for item in data:
                txtfile.write(f"{item}\n")


def convert_file(input_path: str, output_filename: str, conversion_type: str):
    input_path = Path(input_path)
    output_path = CONVERTED_FOLDER / get_converted_filename(output_filename, conversion_type)

    print(f"📂 Конвертация: {conversion_type}")
    print(f"📥 Исходный файл: {input_path}")
    print(f"📤 Будет сохранён в: {output_path}")

    with input_path.open("r", encoding="utf-8") as infile:
        content = infile.read()

    match conversion_type:
        case "txt_to_csv":
            txt_to_csv(content, output_path)
        case "txt_to_json":
            txt_to_json(content, output_path)
        case "csv_to_txt":
            csv_to_txt(input_path, output_path)
        case "json_to_txt":
            json_to_txt(content, output_path)
        case _:
            raise ValueError(f"Unsupported conversion type: {conversion_type}")

    print(f"✅ Файл сконвертирован: {output_path.name}")


# def convert_file_to_lowercase(input_path: str, output_filename):
#     input_path = Path(input_path)
#     output_path = CONVERTED_FOLDER / output_filename
#
#     with input_path.open("r", encoding="utf-8") as infile:
#         content = infile.read()
#
#     lower_content = content.lower()
#     print(f'а сейчас запишем файл uploads/{output_path} с контентом {lower_content}')
#
#     with output_path.open("w", encoding="utf-8") as outfile:
#         outfile.write(lower_content)
#     print('записано')


def count_characters_in_file(file_path='t1.txt') -> int:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return len(content)


def from_number_to_sec(number):
    print(number)
    return number / 100
