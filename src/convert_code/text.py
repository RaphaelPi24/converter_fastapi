import csv
import json
from pathlib import Path

import fitz  # PyMuPDF
from docx import Document
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas




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


def txt_to_pdf(input_path: Path, output_path: Path) -> None:
    with open(input_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    c = canvas.Canvas(str(output_path), pagesize=A4)
    width, height = A4
    y = height - 40

    for line in lines:
        if y < 40:  # Новая страница
            c.showPage()
            y = height - 40
        c.drawString(40, y, line.strip())
        y -= 15

    c.save()


def pdf_to_txt(input_path: Path, output_path: Path):
    text = ""
    with fitz.open(input_path) as pdf:
        for page in pdf:
            text += page.get_text()
    output_path.write_text(text, encoding="utf-8")


def docx_to_txt(input_path: Path, output_path: Path):
    document = Document(input_path)
    with output_path.open("w", encoding="utf-8") as file:
        for para in document.paragraphs:
            file.write(para.text + "\n")


def txt_to_docx(input_path: Path, output_path: Path):
    document = Document()
    with input_path.open("r", encoding="utf-8") as file:
        for line in file:
            document.add_paragraph(line.strip())
    document.save(output_path)


# conversion_format = {
#     'txt': {
#         'csv': txt_to_csv,
#         'json': txt_to_json,
#         'pdf': txt_to_pdf,
#         'docx': txt_to_docx,
#     },
#     'csv': {
#         'txt': csv_to_txt,
#     },
#     'json': {
#         'txt': json_to_txt,
#     },
#     'pdf': {
#         'txt': pdf_to_txt,
#     },
#     'docx': {
#         'txt': docx_to_txt,
#     }
# }

#
# def handle_conversion(source_format: str, target_format: str, input_data, output_path: Path):
#     """
#     Универсальный обработчик конвертации.
#
#     :param source_format: Исходный формат (например, 'txt')
#     :param target_format: Целевой формат (например, 'csv')
#     :param input_data: Либо Path (если файл), либо content:str (если текст)
#     :param output_path: Куда сохранить результат
#     """
#     source_format = source_format.lower()
#     target_format = target_format.lower()
#
#     # Проверка наличия конверсии
#     if source_format not in conversion_format:
#         raise ValueError(f"Конвертация из формата {source_format} не поддерживается.")
#     if target_format not in conversion_format[source_format]:
#         raise ValueError(f"Конвертация из {source_format} в {target_format} не поддерживается.")
#
#     # Получение нужной функции
#     converter_func = conversion_format[source_format][target_format]
#
#     # Проверка по сигнатуре функции
#     if isinstance(input_data, Path):
#         # Функция принимает путь к файлу
#         converter_func(input_data, output_path)
#     elif isinstance(input_data, str):
#         # Функция принимает текстовое содержимое
#         converter_func(input_data, output_path)
#     else:
#         raise TypeError("input_data должен быть либо Path, либо строкой (str)")
#
#
# #handle_conversion('pdf', 'txt', Path('example.pdf'), Path('output.txt')) пример
